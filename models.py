from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
from datetime import datetime
import pytz #pip install pytz

local_tz = pytz.timezone('Asia/Kolkata')

def local_time():
    now = datetime.now(local_tz)
    return now.replace(second=0, microsecond=0)

class CompanyModel(db.Model):
    __tablename__='company'

    id = db.Column(db.Integer, primary_key=True)
    company_name=db.Column(db.String(),nullable=False)
    cash_balance=db.Column(db.Float,default=1000.0)

    def __init__(self,company_name,cash_balance): #to set default values
        self.company_name=company_name
        self.cash_balance=cash_balance



class ItemModel(db.Model):
    __tablename__ ='item'

    item_id=db.Column(db.Integer,primary_key=True)
    item_name=db.Column(db.String(),nullable=False)
    qty=db.Column(db.Integer,default=0,nullable=False)  # Bonus column for item quantity

    

    def __init__(self,item_name):
        self.item_name=item_name
    def __repr__(self):
        return f'<Item {self.item_name}>'

class PurchaseModel(db.Model):
    __tablename__ ='purchase'

    purchase_id=db.Column(db.Integer,primary_key=True)
    timestamp=db.Column(db.DateTime, default=local_time, nullable=False)
    item_id=db.Column(db.Integer,db.ForeignKey('item.item_id'),nullable=False)
    item_name=db.Column(db.String(),nullable=False)
    qty=db.Column(db.Integer,nullable=False)
    rate=db.Column(db.Float,nullable=False)
    amount=db.Column(db.Float,nullable=False)

    

class SalesModel(db.Model):
    __tablename__ ='sales'

    sales_id=db.Column(db.Integer,primary_key=True)
    timestamp=db.Column(db.DateTime, default=local_time, nullable=False)
    item_id=db.Column(db.Integer,db.ForeignKey('item.item_id'),nullable=False)
    item_name=db.Column(db.String(),nullable=False)
    qty=db.Column(db.Integer,nullable=False)
    rate=db.Column(db.Float,nullable=False)
    amount=db.Column(db.Float,nullable=False)




#its defined in item model
    #Define a relationship to easily access the related item object directly from a purchase object.
    # purchase=db.relationship('PurchaseModel',backref='related_items') 
    # sale=db.relationship('SalesModel',backref='related_items') 