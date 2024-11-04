from flask import Flask,redirect,request,render_template
from models import db,CompanyModel,PurchaseModel,ItemModel,SalesModel
# from sqlalchemy import create_engine

app=Flask(__name__)
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
    if company is None:
        default=1000
        return render_template('index.html',cash_balance=default,items=items)

    return render_template('index.html',cash_balance=company.cash_balance,items=items)

#add
@app.route('/additems',methods=['GET','POST'])
def additems():
    if request.method=='POST':
        # item_name=request.form['item_name']
        
        item_name = request.form.get('item_name')
        qty = request.form.get('qty', 0)
        print(f"Item Name: {item_name}, Quantity: {qty}") 
        if item_name:
            item = ItemModel(
                item_name=item_name, 
                qty=int(qty)
            )
            db.session.add(item)
            db.session.commit()
            return redirect('/')
    return render_template('additems.html')


#update
@app.route('/updateitems/<int:id>',methods=['GET','POST'])
def updateitems(id):
    item=ItemModel.query.get(id)
    # print(f"Updating item with ID: {id}")
    # print(item)
    if not item:
        abort(404)
    if request.method =='POST':
        item_name=request.form['item_name']  # This retrieves the value entered by the user in the input field with the name attribute set to first_name
        qty=request.form['qty']
        print(f"Item Name: {item_name}, Quantity: {qty}") 
        if item_name and qty is not None:
            item.item_name=item_name
            item.qty=int(qty)
            db.session.commit()
            return redirect('/')
        else:
            return "Invalid form data", 400
    return render_template('updateitems.html', item=item)

#purchase
@app.route('/purchase',methods=['GET','POST'])
def purchase():
    if request.method == 'POST':
        # return "rfvdrbgd"
        item_id = request.form.get('item_id')
        qty = int(request.form.get('qty', 0))
        rate = float(request.form.get('rate', 0))
        amount = abs(rate * qty)
        item = ItemModel.query.get(item_id)
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
    return render_template('purchase.html', items=items)


#purchasetable
@app.route('/purchasetable',methods=['GET','POST'])
def purchasetable():
    if request.method=='POST':
        return redirect('/')
    purchasetab=PurchaseModel.query.all()
    return render_template('purchasetable.html',purchasetab=purchasetab)
    
#sale
@app.route('/sale',methods=['GET','POST'])
def sale():
    if request.method == 'POST':
        # return "rfvdrbgd"
        item_id = request.form.get('item_id')
        qty = int(request.form.get('qty', 0))
        rate = float(request.form.get('rate', 0))
        amount = rate * qty
        item = ItemModel.query.get(item_id)
        if item: 
           
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
                qty=qty, 
                rate=rate, 
                amount=amount
            )
            db.session.add(sale)
            item.qty -= qty  # decrease the item quantity
            db.session.commit()
            return redirect('/')
        else:
            print(f"Item with id {item_id} not found.")
            return "Item not found.", 404 
    items = ItemModel.query.all()
    return render_template('sale.html', items=items)

#salestable
@app.route('/salestable',methods=['GET','POST'])
def salestable():
    if request.method=='POST':
        return redirect('/')
    salestab=SalesModel.query.all()
    return render_template('salestable.html',salestab=salestab)

if __name__=='__main__':
    app.run(debug=True)