from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import (FileField, IntegerField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import ValidationError, length, required

from .models import Currency, Store
from flw_module.utilities import bank_options


def unique_entry(form, field):
    pass


class StoreRegisterForm(FlaskForm):
    name = StringField('Store name', [required(), unique_entry])
    about = StringField('Short description', [required()])
    iso_code = SelectField(
        'Currency', choices=Currency.query.with_entities(
            Currency.code, Currency.code).all())
    phone = StringField('Business Phone Number',
                        [required(), length(min=10, max=15)])
    logo = FileField()
    save = SubmitField()


class AccountDetailForm(FlaskForm):
    account_name = StringField('Account Name', [required()])
    account_num = IntegerField('Account Number', [required()])
    bank_name = SelectField('Select a bank', [required()],
                            choices=bank_options,)
    save = SubmitField()
