from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
from datetime import datetime
import pytz  #pip install pytz

# company model
class CompanyModel(db.Model):
    __tablename__='company'

    id = db.Column(db.Integer, primary_key=True)
    company_name=db.Column(db.String(),nullable=False)
    cash_balance=db.Column(db.Float,default=1000.00)

# item model
class ItemModel(db.Model):
    __tablename__ ='item'

    item_id=db.Column(db.Integer,primary_key=True)
    item_name=db.Column(db.String(),nullable=False)
    qty=db.Column(db.Integer,default=0,nullable=False)  # Bonus column for item quantity

# for current timestamp in purchase/sale
local_tz = pytz.timezone('Asia/Kolkata')
def local_time():
    now = datetime.now(local_tz)
    return now.replace(second=0, microsecond=0)

# purchase model
class PurchaseModel(db.Model):
    __tablename__ ='purchase'

    purchase_id=db.Column(db.Integer,primary_key=True)
    timestamp=db.Column(db.DateTime, default=local_time, nullable=False)
    item_id=db.Column(db.Integer,db.ForeignKey('item.item_id'),nullable=False)
    item_name=db.Column(db.String(),nullable=False)
    qty=db.Column(db.Integer,nullable=False)
    rate=db.Column(db.Float,nullable=False)
    amount=db.Column(db.Float,nullable=False)

# sales model
class SalesModel(db.Model):
    __tablename__ ='sales'

    sales_id=db.Column(db.Integer,primary_key=True)
    timestamp=db.Column(db.DateTime, default=local_time, nullable=False)
    item_id=db.Column(db.Integer,db.ForeignKey('item.item_id'),nullable=False)
    item_name=db.Column(db.String(),nullable=False)
    qty=db.Column(db.Integer,nullable=False)
    rate=db.Column(db.Float,nullable=False)
    amount=db.Column(db.Float,nullable=False)