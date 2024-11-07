from flask import Flask,redirect,request,render_template,flash
from models import db,CompanyModel,PurchaseModel,ItemModel,SalesModel
from datetime import datetime


app=Flask(__name__)
app.config['SECRET_KEY'] = 'shop'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

#Database Connection Timeout
# engine = create_engine('sqlite:///shop.db', connect_args={'timeout': 30})

with app.app_context():
    # db.drop_all()
    db.create_all()
    print("Database dropped and recreated successfully.")

#home
@app.route('/')
def home():
    company=CompanyModel.query.first()
    items=ItemModel.query.all()
    year=datetime.now().year   
    if company is None:
        default=1000
        return render_template('index.html',cash_balance=default,items=items,year=year)

    return render_template('index.html',cash_balance=company.cash_balance,items=items,year=year)

#add items
@app.route('/additems',methods=['GET','POST'])
def additems():
    if request.method=='POST':
        item_name = request.form.get('item_name')
      
        existing= ItemModel.query.filter_by(item_name=item_name).first()
        print(f"Item Name: {item_name}") 
        if existing is None:
            item = ItemModel(
                item_name=item_name
            )
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        else:
            flash("Already exits please check", "warning")
    return render_template('additems.html')


# #view items
# @app.route('/itemtable',methods=['GET','POST'])
# def itemtable():
#     if request.method=='POST':
#         return redirect('/')
#     items=ItemModel.query.all()
#     return render_template('itemtable.html',items=items)

#update items
@app.route('/updateitems/<int:id>',methods=['GET','POST'])
def updateitems(id):
    item=ItemModel.query.get(id)
    print(id)
    print(item)
    if not item:
        abort(404)
        items=ItemModel.query.all()
    if request.method =='POST':
        item_name=request.form['item_name']  # This retrieves the value entered by the user in the input field with the name attribute set to first_name
        existing= ItemModel.query.filter_by(item_name=item_name).first()
        if existing is None:
            try:
                item.item_name = item_name
                db.session.commit()
                return redirect('/')
            except Exception as e:
                db.session.rollback()  # Roll back the session on error
                print(f"Error updating item: {e}")
                return "An error occurred while updating the item", 500
            
        
        else:
            flash("Already exits please check", "warning")
    return render_template('updateitems.html', item=item)

#purchase
@app.route('/addpurchase',methods=['GET','POST'])
def purchase():
    if request.method == 'POST':
        # return "rfvdrbgd"
        item_id = request.form.get('item_id')
        qty = int(request.form.get('qty', 0))
        rate = float(request.form.get('rate', 0))
        amount = abs(rate * qty)
        item = ItemModel.query.get(item_id)
        print(item.item_name)
        if item: 
           
            company = CompanyModel.query.first()
            if not company:  # Check if the company exists
                print("No company found. Creating default company...")
                company = CompanyModel(company_name="Namma Kadai", cash_balance=1000.0)
                db.session.add(company)
                db.session.commit()
        
            company.cash_balance -= amount
            db.session.flush()
            
            purchase = PurchaseModel(
                item_id=item_id, 
                item_name=item.item_name,
                qty=qty, 
                rate=rate, 
                amount=amount
            )
            db.session.add(purchase)
            item.qty += qty  # Increase the item quantity
            db.session.commit()
            return redirect('/')
        else:
            print(f"Item with id {item_id} not found.")
            return "Item not found.", 404 
    items = ItemModel.query.all()
    return render_template('addpurchase.html', items=items)


#view purchasetable
@app.route('/purchasetable',methods=['GET','POST'])
def purchasetable():
    if request.method=='POST':
        return redirect('/')
    purchasetab=PurchaseModel.query.all()
    return render_template('purchasetable.html',purchasetab=purchasetab)
    
#sale
@app.route('/addsale',methods=['GET','POST'])
def sale():
    if request.method == 'POST':
        # return "rfvdrbgd"
        item_id = request.form.get('item_id')
        item_name=request.form.get('item_name')
        qty = int(request.form.get('qty', 0))
        rate = float(request.form.get('rate', 0))
        amount = rate * qty
        item = ItemModel.query.get(item_id)
        print(item)
        if item and item.qty >= qty: 
           
            company = CompanyModel.query.first()
            print(company)
            if not company:  # Check if the company exists
                print("No company found. Creating default company...")
                company = CompanyModel(
                    company_name="Namma Kadai", 
                    cash_balance=1000.0
                )
                db.session.add(company)
                db.session.commit()
        
            company.cash_balance += amount
            db.session.flush()
            
            sale = SalesModel(
                item_id=item_id, 
                item_name=item.item_name,
                qty=qty, 
                rate=rate, 
                amount=amount
            )
            db.session.add(sale)
            item.qty -= qty  # decrease the item quantity
            db.session.commit()
            return redirect('/')
        else:
            flash("Out of stock. Please reduce the quantity or check back later.", "warning")
    items = ItemModel.query.all()
    return render_template('addsale.html', items=items)

#view salestable
@app.route('/salestable',methods=['GET','POST'])
def salestable():
    if request.method=='POST':
        return redirect('/')
    salestab=SalesModel.query.all()
    return render_template('salestable.html',salestab=salestab)

if __name__=='__main__':
    app.run(debug=True)