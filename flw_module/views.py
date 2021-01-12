''' Defination of all shop views in `shop` blueprint '''
from flask import Blueprint, current_app, flash, request, url_for
import json
from . import utilities
from factory import db


# ---------- Declaring the blueprint ----------
flw = Blueprint('flw', __name__, template_folder='templates')


@flw.route('/callback/store_payment', methods=['POST'])
def callback_store_payment():
    flw_data = request.json
    print(flw_data)
    store_name = utilities.confirm_store_reg(
        flw_data['transaction_id'],
        current_app.config['STORE_REG_AMT'],
        current_app.config['FLW_SEC_KEY'])
    if store_name:
        flash("Payment confirmed, thank you", 'success')
        return {'redirect': url_for('shop.store_admin', store_name=store_name)}
    flash("Unable to confirm payment, contact us", 'danger')
    return {'redirect': url_for('shop.dashboard')}


@flw.route('/callback/sales_payment', methods=['POST'])
def callback_sales_payment():
    flw_data = request.json
    print(flw_data)
    if utilities.confirm_sales_payment(
            flw_data['transaction_id'], flw_data['tx_ref'],
            flw_data['currency'], flw_data['amount'],
            current_app.config['FLW_SEC_KEY']):
        flash("Payment confirmed, thank you", 'success')
    else:
        flash("Unable to confirm payment, contact us", 'danger')
    return {'redirect': url_for('shop.market')}
