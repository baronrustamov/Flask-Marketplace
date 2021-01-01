'''
Shop related models, currently we have:
  1. Currency
  2. Order
  3. OrderLine
  4. Product
  5. Store
'''
from datetime import datetime

from factory import db


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), nullable=False)
    country = db.Column(db.String(50), nullable=False)


class Order(db.Model):
    ''' Table of orders: status can be one of `open` | `done` '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(20, 2), default=0)
    status = db.Column(db.String(5), default='open', nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    last_modified_at = db.Column(db.DateTime(), default=datetime.utcnow())

    @classmethod
    def cart(cls):
        # only products from active stores are made public
        return(Order.query.filter(Order.status == 'open'))


class OrderLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('product.id'),
                           nullable=False)
    price = db.Column(db.Numeric(20, 2), nullable=False)
    qty = db.Column(db.Integer, default=1, nullable=False)


class Product(db.Model):
    ''' Table of all Products from all stores '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Numeric(20, 2))
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
    ''' 
    Table of stores information. Key features are:
      - A User is permitted to register more than one store
      - A Store is given assigned a dispatch ride
    '''
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
