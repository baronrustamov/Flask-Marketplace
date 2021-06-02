'''
Shop related models, currently we have:
  2. Currency
  3. Dispatcher
  4. Order
  5. OrderLine
  6. Product
  7. Store
'''
from datetime import datetime

from flask import current_app
from Flask_Marketplace.factory import db


class AccountDetail(db.Model):
    """Account numbers
    - One account can be used multiple entities
    """
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(50), nullable=False)
    account_num = db.Column(db.Integer, nullable=False)
    bank = db.Column(db.String(100), nullable=False)
    # relationships --------------------------------------
    dispatchers = db.relationship('Dispatcher', backref='account')
    stores = db.relationship('Store', backref='account')


class Currency(db.Model):
    """Conversion rates relative to base currency
    - The default base currency is USD
    """
    code = db.Column(db.String(3), primary_key=True)
    country = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Numeric(12, 6), nullable=False)
    # relationships --------------------------------------
    orders = db.relationship('Order', backref='currency')
    stores = db.relationship('Store', backref='currency')


class Dispatcher(db.Model):
    """Delivery agents
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account_detail.id'))
    charge = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    phone = db.Column(db.String(15), nullable=False)
    # relationships --------------------------------------
    orderlines = db.relationship('OrderLine', backref='orderlines')
    stores = db.relationship('Store', backref='dispatcher')


class Order(db.Model):
    """ Record of carts
    - Status can be one of
        * `open`: The order have not been checked-out
        * `order`: It has been checkout, but not yet paid for
        * `paid`: It has been fully paid for
    """
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(20))
    iso_code = db.Column(db.Integer, db.ForeignKey('currency.code'),
                         nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(5), default='open', nullable=False)
    # Checkout variables ----
    address = db.Column(db.String(100)) # May be different from the user
    phone = db.Column(db.Integer) # May be different from the user
    # time stamps ----------------
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    last_modified_at = db.Column(db.DateTime(), default=datetime.utcnow())
    # relationship ---------------
    orderlines = db.relationship('OrderLine', backref='order')

    @classmethod
    def cart(cls):
        # only products from active stores are made public
        return(Order.query.filter(Order.status == 'open'))


class OrderLine(db.Model):
    """Individual items cart history
    """
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'),
                         nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           nullable=False)
    price = db.Column(db.Numeric(20, 2), nullable=False)
    qty = db.Column(db.Integer, default=1, nullable=False)
    # ----- Filled after checking out -----
    position = db.Column(db.String(10)) # ["store", "dispatcher", "fulfilled"]
    store_payout = db.Column(db.Numeric(20, 2))
    store_payout_status = db.Column(db.String(10))
    # Dispatcher can be changed from the store-attached one
    dispatcher_id = db.Column(db.Integer, db.ForeignKey('dispatcher.id'))
    dispatcher_payout = db.Column(db.Numeric(20, 2))
    dispatcher_payout_status = db.Column(db.String(10))


class Product(db.Model):
    """Table of all Products from all stores.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Numeric(20, 2))
    description = db.Column(db.String(200))
    # Yes, images are stored on the database
    # from experience, it is preferrable in a scenario like this
    image = db.Column(db.BLOB)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'),
                         nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    last_modified_at = db.Column(db.DateTime, default=datetime.utcnow())
    # relationships ---------------------------------------------
    orderlines = db.relationship('OrderLine', backref='product')

    @classmethod
    def public(cls):
        # only active products are made public
        return(Product.query.filter(Product.is_active == 1))

    def sale_price(self, to_currency):
        """Converts price of products to a specified currency
        
        Args:
            product_pricing (str): how to compute sales price (localize or fixed)

        Returns:
            float: converted sales price
        """
        if (current_app.config['PRODUCT_PRICING'] == 'localize' or
                current_app.config['STORE_MULTICURRENCY']):
            scale = (
                Currency.query.filter_by(code=to_currency).first().rate /
                self.store.currency.rate)
            return round(self.price * scale, 2)
        return self.price


class Store(db.Model):
    """Table of stores information. Key features are:
      - A User is permitted to register more than one store
      - A Store is assigned a dispatch rider
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # Yes, images are stored on the database
    # from experience, it is preferrable a scenario like this
    logo = db.Column(db.BLOB)
    about = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    email = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    phone = db.Column(db.String(15), nullable=False)
    # Foreign Keys -----
    account_id = db.Column(db.Integer, db.ForeignKey('account_detail.id'))
    dispatcher_id = db.Column(db.Integer, db.ForeignKey('dispatcher.id'),
                              nullable=False)
    iso_code = db.Column(db.Integer, db.ForeignKey('currency.code'),
                         nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    # Relationships -----
    products = db.relationship('Product', backref='store')

    @ classmethod
    def public(cls):
        # only products from active stores are made public
        return(Store.query.filter(Store.is_active == 1))
