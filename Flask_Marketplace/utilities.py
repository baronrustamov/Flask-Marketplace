from decimal import Decimal
from requests import get

from flask import make_response, redirect, request, render_template
from flask_security import current_user

from Flask_Marketplace.models.shop_models import (
    AccountDetail, Currency, Dispatcher, Order, Store)
from Flask_Marketplace.factory import db
from Flask_Marketplace.models.shop_models import AccountDetail, Dispatcher, Order, OrderLine, Store


def convert_currency(price, from_currency, to_currency):
    '''Converts price of products to visitor's currency based on scale'''
    if to_currency:
        scale = (
            Currency.query.filter_by(code=to_currency).first().rate /
            Currency.query.filter_by(code=from_currency).first().rate)
        return round(Decimal(price) * scale, 2)
    return price


def payment_split_ratio(amount_list):
    '''Converts amount_list to ratios usable for checkout split payments'''
    return [round(x/sum(amount_list)*10000) for x in amount_list]


def amounts_sep(iso_code, pay_data, dispatch_currency):
    shipping = []
    store_total = 0
    for i in range(len(pay_data)):
        shipping_charge = convert_currency(
            pay_data[i][0].dispatcher.charge,
            dispatch_currency, iso_code) * pay_data[i][2]
        shipping.append(shipping_charge)
        store_total += pay_data[i][1]
    return {
        'iso_code': iso_code,
        'store_total': store_total,
        'shipping_costs': shipping,
        # 'ratios': payment_split_ratio(store_total+shipping),
    }


def can_edit_product(current_user, product_store):
    '''
    Checks if a product is editable, returns True if either the
    accessing user is a platform admin or the owner of the product.
    It is also made a global jinja function as it is also used to
    determine if an Edit button should be visible to the web user.
    :param current_user: Flask-Security extended Flask-Login current
                         user object
    :type current_user: object
    param product_store: The store of the given product
    :type product_store: str
    '''
    if current_user.is_authenticated:
        if current_user.has_role('Admin'):
            return True
        if product_store in current_user.stores:
            return True
    return False


def update_cart_status(status='order'):
    """Update cart status

    Args:
        user_id (int): DB id of the user
        status (str, optional): stage of the cart. Defaults to 'order'.
    """
    # get the order data for comparism and verification
    cart = Order.cart().filter_by(user_id=current_user.id).first()
    cart_tot = db.session.query(
        db.func.sum(OrderLine.qty * OrderLine.price)).filter(
        OrderLine.order_id == cart.id).group_by(OrderLine.order_id).first()
    # We can now certify the order
    cart.status = status
    cart.amount = str(cart_tot[0])
    db.session.commit()
    return "Transaction updated to {}".format(status)


def create_new_store(name=None):
    name = len(Store)
    dispatcher = db.session.query(
        Dispatcher).order_by(db.func.random()).first().id
    store = Store(
        name=name,
        about='Give your store a short Description',
        iso_code='USD',
        dispatcher_id=dispatcher,
        user_id=current_user.id,
        phone='e.g. 08123456789',
        email='e.g. abc@gmail.com'
    )
    db.session.add(store)
    db.session.commit()
    return name


def currency_options():
    return Currency.query.with_entities(Currency.code, Currency.code).all()


def latest_stores():
    return Store.query.with_entities(Store.name).order_by(
        Store.created_at.desc()).limit(3).all()


def _get_all_subclasses(cls):
    # Recursively get all subclasses
    all_subclasses = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(_get_all_subclasses(subclass))
    return all_subclasses


def create_new(cls):
    """[summary]

    Returns:
        [type]: [description]
    """
    mod_views = [cls]
    all_subclasses = _get_all_subclasses(cls)
    if all_subclasses:
        mod_views.extend(all_subclasses)
        _def_view, *args = mod_views

        class NewClass(*args):
            pass
    else:
        NewClass = cls
    return NewClass
