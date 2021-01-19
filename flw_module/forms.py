from flask_wtf import FlaskForm
from wtforms import (IntegerField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import required

from .utilities import bank_options


class AccountDetailForm(FlaskForm):
    account_num = IntegerField('Account Number', [required()])
    bank = SelectField('Select a bank', [required()],
                       choices=bank_options,
                       render_kw={'title': 'Search',
                                  'data-live-search': 'true'}
                       )
    save = SubmitField()
