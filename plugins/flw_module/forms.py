from flask_wtf import FlaskForm
from wtforms import (IntegerField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import required

from .utilities import bank_options
from Flask_Marketplace.shop_module.forms import AccountForm


class AccountForm(AccountForm):
    account_num = IntegerField('Account Number', [required()])
    bank = SelectField('Select a bank', [required()],
                       choices=bank_options,
                       render_kw={'title': 'Search',
                                  'data-live-search': 'true'}
                       )
    save = SubmitField()

from Flask_Marketplace import MarketViews as ujik
from flask import render_template
class MarketViews(ujik):
    def index(self):
        print("asdfghjklpuy What")
        latest = self.Product.query.limit(3).all()
        return render_template('marketplace/h8ome.html', products=latest)

