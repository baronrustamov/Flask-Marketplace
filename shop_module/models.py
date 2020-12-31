'''
Models here product related ones, currently we have:
  - Product: Table of all Products from all stores
  - Transactions (Comming Soon): For handling transaction histories
'''
from datetime import datetime

from factory import db


class Product(db.Model):
    ''' Table of all Products from all stores '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    price = db.Column(db.String(100), unique=True)
    # Yes, images are stored on the database
    # from experience, it is preferrable a scenario like this
    image = db.Column(db.Binary)
    vendor_id = db.Column(db.Integer,
                          db.ForeignKey('user.id'),
                          nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    last_modified_at = db.Column(db.DateTime, default=datetime.now())

    @classmethod
    def public(cls):
        # only active products are made public
        return(Product.query.filter(Product.is_active == 1))
