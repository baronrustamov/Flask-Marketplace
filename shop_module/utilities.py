from requests import get

from flask import make_response, redirect, request, render_template, \
    current_app

from .models import Currency


def convert_currency(price, from_currency, to_currency):
    ''' Converts price of products to visitor's currency based on scale'''
    if to_currency:
        scale = (
            Currency.query.filter_by(code=to_currency).first().rate /
            Currency.query.filter_by(code=from_currency).first().rate)
        return price * scale
    return price


def payment_split_ratio(amount_list):
    ''' Converts amount_list to ratios usable for checkout split payments'''
    return [round(x/sum(amount_list)*10000) for x in amount_list]


def amounts_sep(iso_code, pay_data):
    shipping = []
    store_total = 0
    for i in range(len(pay_data)):
        shipping_charge = convert_currency(
            pay_data[i][0].dispatcher.charge,
            pay_data[i][0].iso_code, iso_code) * pay_data[i][2]
        shipping.append(shipping_charge)
        store_total += pay_data[i][1]
    return {
        'iso_code': iso_code,
        'store_total': store_total,
        'shipping_costs': shipping,
        # 'ratios': payment_split_ratio(store_total+shipping),
    }


def confirm_payment(tx_id, currency, value, flw_sec_key):
    '''
    Note: Flutterwave only checks if the given payment exists.
    It does not tell me if it has been formerly used previously
    used on this platform.
    Thus, calling functions have to check its usability.
    '''
    flw_resp = get(
        'https://api.flutterwave.com/v3/transactions/'+tx_id+'/verify',
        headers={"Content-Type": "application/json",
                 'Authorization': 'Bearer ' + flw_sec_key}
    )
    if flw_resp['data']['status'] == 'successful':
      # confirm currency and amount
        if flw_resp['data']['currency'] == currency:
            if flw_resp['data']['amount'] >= float(value):
                return True
    return False


def confirm_store_reg(trans_id, currency, value, store_reg_amt, flw_sec_key):
    value, currency = store_reg_amt.split(' ')
    if confirm_payment(trans_id, currency, value, flw_sec_key):
        # Check if the txref is still usable
        # Recall, txref = store/userid/number_of_stores.
        # Confirm that the current user matches the ref. id
        _, tx_id, tx_store = txref.split('/')
        if tx_id == current_user.id:
            # confirm is number of stores is valid
            if tx_store == len(current_user.stores.all())+1:
                # Now, it's too good not to be true
                # proceed with dummy store creation
                # We want to randomly fix a store to a dispatcher
                dispatcher = db.session.query(
                    Dispatcher).order_by(db.func.random()).first().id
                store = Store(
                    name=trans_id,
                    about='Give your store a short Description',
                    iso_code='USD',
                    dispatcher_id=dispatcher,
                    user_id=current_user.id,
                )
                db.session.add(store)
                db.session.commit()
                # Note: trans_id has been used to create a store
                return trans_id
    return False
