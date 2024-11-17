from flask import Flask,redirect,request,render_template,flash,url_for,session
from models import db,CompanyModel,PurchaseModel,ItemModel,SalesModel
from datetime import datetime #to display current year
from sqlalchemy import func # to use sql functions

app=Flask(__name__)
app.secret_key = 'shop'  #for flashing 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()
    # print("Database dropped and recreated successfully.")

#current path details
@app.context_processor
def inject_path():
    return {'current_path': request.path}

#home
@app.route('/')
def home():
    company=CompanyModel.query.first()
    year=datetime.now().year   
    if company is None:
        new_company=CompanyModel(
            company_name="Namma Kadai"
        )
        db.session.add(new_company)
        db.session.commit()
    company.cash_balance = f'{company.cash_balance:.2f}'
    # print(company.cash_balance)
    return render_template('home.html',company=company,year=year)

#add items
@app.route('/additems',methods=['GET','POST'])
def additems():
    company=CompanyModel.query.first()
    items=ItemModel.query.all()
    no_items = len(items) == 0
    if request.method=='POST':
        item_name = request.form.get('item_name').strip().upper()
        existing= ItemModel.query.filter_by(item_name=item_name).first()
        # print(f"Item Name: {item_name}") 
        if existing is None:
            item = ItemModel(
                item_name=item_name
            )
            db.session.add(item)
            db.session.commit()
            flash('Item Added Successfully!', 'success')
            print(session)
            return redirect('/additems')
        else:
            flash("Already exits please check", "error")
    company.cash_balance = f'{company.cash_balance:.2f}'
    return render_template('add_items.html',company=company,items=items, no_items= no_items)


#update item
@app.route('/updateitems/<int:id>',methods=['GET','POST'])
def updateitems(id):
    item=ItemModel.query.get(id)
    if request.method =='POST':
        item_name=request.form.get('item_name').strip().upper() # This retrieves the value entered by the user in the input field with the name attribute set to first_name
        existing= ItemModel.query.filter_by(item_name=item_name).first()
        if existing is None:
            try:
                item.item_name = item_name
                db.session.commit()
                flash('Item Updated Successfully!!','success')
                return redirect('/additems')
            except Exception as e:
                db.session.rollback()  # Roll back the session 
                flash('An error occurred while updating the item',"error")
                return redirect('/additems')
        else:
            flash('Item Already Exist!!','error')
    company=CompanyModel.query.first()
    company.cash_balance=f'{company.cash_balance:.2f}'
    return render_template('update_items.html', item=item,company=company)

#delete item
@app.route('/deleteitems/<int:id>',methods=['POST','GET'])
def deleteitems(id):
    item=ItemModel.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    else:
        flash('Item not found!', "error")
    return redirect(url_for('additems')) 

#purchase
@app.route('/addpurchase',methods=['GET','POST'])
def purchase():
    company=CompanyModel.query.first()
    if request.method=='POST':
        selected_items=request.form.getlist('selected_items[]')
        quantities=request.form.getlist('qty[]')
        rates=request.form.getlist('rate[]')
        total_cost=0
        for item_id, qty, rate in zip(selected_items, quantities, rates):
            qty = int(qty)
            rate = float(rate)
            amount = float(qty * rate)
            total_cost+=amount
            item = ItemModel.query.get(item_id)

            purchase=PurchaseModel(
                item_id=item_id,
                item_name=item.item_name,
                qty=qty,
                rate=rate,
                amount=amount
            )
            db.session.add(purchase)
            item.qty += qty
        if total_cost==0:
            flash("Items need to be Selected...","error")
            return redirect('/addpurchase')
        if company.cash_balance < total_cost:
            flash("Insufficient Balance to Purchase","error")
            return redirect('/addpurchase')
        company.cash_balance-=total_cost
        db.session.commit()
        flash("Purchase is Done..Check Down for History..","success")
        return redirect(url_for('purchase'))
    items = ItemModel.query.all()
    purchasedtable=PurchaseModel.query.all()
    no_items =len(items)==0
    no_purchase=len(purchasedtable)==0
    company.cash_balance = f'{company.cash_balance:.2f}'
    return render_template('add_purchase.html', items=items, purchasedtable=purchasedtable,no_purchase=no_purchase, no_items=no_items,company=company)

#sale
@app.route('/addsale',methods=['GET','POST'])
def sale():
    company=CompanyModel.query.first()
    if request.method=='POST':
        selected_items=request.form.getlist('selected_items[]')
        quantities=request.form.getlist('qty[]')
        rates=request.form.getlist('rate[]')
        total_cost=0
        for item_id, qty, rate in zip(selected_items, quantities, rates):
            qty = int(qty)
            rate = float(rate)
            amount = float(qty * rate)
            total_cost+=amount
            item = ItemModel.query.get(item_id)
            if(item.qty < qty):
                flash("Insufficient Quantity to Sale","error")
                return redirect('/addsale')
            
            sale=SalesModel(
                item_id=item_id,
                item_name=item.item_name,
                qty=qty,
                rate=rate,
                amount=amount
            )
            db.session.add(sale)
            item.qty -= qty
        if total_cost==0:
            flash("Items need to be Selected...","error")
            return redirect('/addsale')
        company.cash_balance+=total_cost
        db.session.commit()
        flash("Sale is Done..Check Down for History..","success")
        return redirect(url_for('sale'))
    items = ItemModel.query.all()
    soldtable = SalesModel.query.all()
    no_items =len(items)==0
    no_sale=len(soldtable)==0
    company.cash_balance = f'{company.cash_balance:.2f}'
    return render_template('add_sale.html', items=items, soldtable=soldtable,no_sale=no_sale, no_items=no_items,company=company)


#view reports of both
@app.route('/reports',methods=['GET','POST'])
def reports():
    items = ItemModel.query.all()
    reports= []  # A list to store 
    for item in items:
        # purchase amount for the item from PurchaseModel
        total_purchased_qty = db.session.query(func.sum(PurchaseModel.qty)).filter_by(item_id=item.item_id).scalar() or 0
        total_purchased_amount = db.session.query(func.sum(PurchaseModel.amount)).filter_by(item_id=item.item_id).scalar() or 0
        #sold amount for the item from SaleModel
        total_sold_qty = db.session.query(func.sum(SalesModel.qty)).filter_by(item_id=item.item_id).scalar() or 0
        total_sold_amount = db.session.query(func.sum(SalesModel.amount)).filter_by(item_id=item.item_id).scalar() or 0
        profit_or_loss=0
        if total_sold_amount !=0 and total_purchased_amount!=0:
            profit_or_loss = total_sold_amount - total_purchased_amount
        # adding dictionary to reports list
        reports.append({
            'item_name': item.item_name,
            'total_purchased_qty': total_purchased_qty,
            'total_sold_qty': total_sold_qty,
            'total_purchased_amount': total_purchased_amount,
            'total_sold_amount': total_sold_amount,
            'profit_or_loss':profit_or_loss,
            'available_qty':item.qty
        })
    company=CompanyModel.query.first()
    no_items =len(items)==0
    company.cash_balance=f'{company.cash_balance:.2f}'
    return render_template('reports.html',reports=reports,company=company,no_items=no_items)
    

if __name__=='__main__':
    app.run(debug=True)