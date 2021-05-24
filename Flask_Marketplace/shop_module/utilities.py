from decimal import Decimal
from requests import get

from flask import make_response, redirect, request, render_template
from flask_security import current_user

from .models import AccountDetail, Currency, Dispatcher, Order, Store
from .forms import AccountForm
from factory import db


def account_detail(partner):
    account_form = AccountForm()
    if not partner.account:
        account = AccountDetail(
            account_name=account_form.name.data,
            account_num=account_form.account_num.data,
            bank=account_form.bank.data,)
        partner.account=account
    else:
        # The store owner is trying to change the attached account
        partner.account.account_name=account_form.name.data
        partner.account.account_num=account_form.account_num.data
        partner.account.bank=account_form.bank.data
    db.session.commit()
    return('Your account has been edited', 'success')


def convert_currency(price, from_currency, to_currency):
    '''Converts price of products to visitor's currency based on scale'''
    if to_currency:
        scale=(
            Currency.query.filter_by(code=to_currency).first().rate /
            Currency.query.filter_by(code=from_currency).first().rate)
        return round(Decimal(price) * scale, 2)
    return price


def payment_split_ratio(amount_list):
    '''Converts amount_list to ratios usable for checkout split payments'''
    return [round(x/sum(amount_list)*10000) for x in amount_list]


def amounts_sep(iso_code, pay_data, dispatch_currency):
    shipping=[]
    store_total=0
    for i in range(len(pay_data)):
        shipping_charge=convert_currency(
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


def currency_options():
    return Currency.query.with_entities(Currency.code, Currency.code).all()


def latest_stores():
    return Store.query.with_entities(Store.name).order_by(
        'created_at').limit(3).all()
