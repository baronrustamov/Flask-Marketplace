'''
Human related models are located here, currently we have:
  - Role: Which may be one of Admin | Vendor | Customer
  - User: Table of everyone capable of logging in to the system
'''
from factory import db


class AccountDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(50), nullable=False)
    account_num = db.Column(db.Integer, nullable=False)
    bank = db.Column(db.String(100), nullable=False)
    sub_number = db.Column(db.Integer)
    sub_id = db.Column(db.Integer,)
    # relationships --------------------------------------
    stores = db.relationship('Store', backref='account')
    dispatchers = db.relationship('Dispatcher', backref='dispatcher')
