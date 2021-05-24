'''
Human related models are located here, currently we have:
  - Role: Which may be one of Admin | Vendor | Customer
  - User: Table of everyone capable of logging in to the system
'''
from factory import db
from Flask_Marketplace.shop_module.models import AccountDetail

class FlwDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_number = db.Column(db.Integer)
    sub_id = db.Column(db.Integer,)
    account_id = db.Column(db.ForeignKey(AccountDetail.id))
    account_detail = db.relationship(AccountDetail, backref='flw', uselist=False)
    # relationships --------------------------------------\
