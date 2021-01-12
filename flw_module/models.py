'''
Human related models are located here, currently we have:
  - Role: Which may be one of Admin | Vendor | Customer
  - User: Table of everyone capable of logging in to the system
'''
from factory import db


class FlwSubAccount(db.Model):
    # Note that a subaccount can be used by multiple store,
    # for example, if a user registered multiple stores
    sub_id = db.Column(db.Integer, primary_key=True)
    sub_account_number = db.Column(db.Integer)
    account = db.relationship('AccountDetail', uselist=False,
                              backref='flw')

