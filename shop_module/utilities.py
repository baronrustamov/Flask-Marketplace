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
