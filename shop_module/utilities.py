from requests import get

from flask import make_response, redirect, request, render_template
from .models import Currency

def convert_currency(price, from_currency, to_currency):
    ''' Converts price of products to visitor's currency based on scale'''
    if to_currency:
        scale = (Currency.query.filter_by(code=to_currency).first().rate /
                  Currency.query.filter_by(code=from_currency).first().rate)
        return price * scale
    return price


def payment_split_ratio(amount_list):
    ''' Converts amount_list to ratios usable for checkout split payments '''
    return [round(x/sum(price_list)*10000) for x in price_list]

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
      #'ratios': payment_split_ratio(store_total+shipping),
    }