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
    name = db.Column(db.String(100))
    price = db.Column(db.Numeric(10,2))
    description = db.Column(db.String(200))
    # Yes, images are stored on the database
    # from experience, it is preferrable a scenario like this
    image = db.Column(db.Binary)
    store_id = db.Column(db.Integer,
                         db.ForeignKey('store.id'),
                         nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    last_modified_at = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def public(cls):
        # only active products are made public
        return(Product.query.filter(Product.is_active == 1))


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # Yes, images are stored on the database
    # from experience, it is preferrable a scenario like this
    logo = db.Column(db.Binary)
    about = db.Column(db.String(150), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'),
                            nullable=False)
    dispatcher_id = db.Column(db.Integer, db.ForeignKey('dispatcher.id'),
                            nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    is_active = db.Column(db.Boolean(), default=True)

    @classmethod
    def public(cls):
        # only products from active stores are made public
        return(Store.query.filter(Store.is_active == 1))


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), nullable=False)
    country = db.Column(db.String(50), nullable=False)
