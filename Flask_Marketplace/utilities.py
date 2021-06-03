from datetime import datetime
from decimal import Decimal
from requests import get

from flask import current_app, make_response, redirect, request, render_template
from flask_security import current_user

from Flask_Marketplace.models.shop_models import (
    Currency, Dispatcher, Order, OrderLine, Product, Store)
from Flask_Marketplace.factory import db


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


def inherit_classes(cls):
    """Creates a new class that Inherits all subclasses

    Returns:
        class: new common child class
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


def compute_checkout(cart_id, iso_code):
    """Summarize the cart items by Store>>store_amt_sum>>store_qty_sum
    Why sum of quantities per store? Recall, dispatchers rates are per qty

    Args:
        cart_id ([type]): [description]
        iso_code (bool): [description]

    Returns:
        [type]: [description]
    """
    # Subquery of store values
    store_value_sq = db.session.query(
        Product.store_id.label('store_id'),
        db.func.sum(OrderLine.qty * OrderLine.price).label('store_amt_sum'),
        db.func.sum(OrderLine.qty).label(
            'store_qty_sum').label('store_qty_sum'),
    ).join(Product).filter(OrderLine.order_id == cart_id).group_by(
        Product.store_id).subquery()
    # All other payment data are related to the store
    pay_data = db.session.query(
        Store, store_value_sq.c.store_amt_sum,
        store_value_sq.c.store_qty_sum).join(
        store_value_sq, Store.id == store_value_sq.c.store_id).all()
    # Compute amounts
    store_value = amounts_sep(
        iso_code, pay_data, current_app.config['DISPATCHER_CURRENCY'])
    for i in range(len(pay_data)):
        store_charge = float(pay_data[i][1]) * (
            current_app.config['SPLIT_RATIO_STORE'])
        dispatch_charge = float(store_value['shipping_costs'][i]
                                ) * current_app.config['SPLIT_RATIO_DISPATCHER']
    return (pay_data, store_value)


def record_sales(cart_id, address=None, phone=None, store_payout=None,
                 dispatcher_id=None, dispatcher_payout=None):
    # Mark this order
    order = db.session.query(Order).filter_by(id=cart_id).first()
    order.address = address
    order.phone = phone
    order.status = 'order'
    order.last_modified_at = datetime.utcnow()
    # Write other columns of Orderlines Model
    for line in db.session.query(OrderLine).filter_by(order_id=cart_id).all():
        line.position = "store"
        line.store_payout = store_payout or (
            current_app.config['SPLIT_RATIO_STORE'] * float(line.price) * line.qty)
        line.store_payout_status = 'open'
        line.dispatcher_id = dispatcher_id or line.product.store.dispatcher_id
        line.dispatcher_payout = dispatcher_payout or (
            line.product.store.dispatcher.charge * line.qty *
            current_app.config['SPLIT_RATIO_DISPATCHER'])
        line.dispatcher_payout_status = 'open'
    db.session.commit()
    return True
