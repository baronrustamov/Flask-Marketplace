from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, DecimalField, FileField, FloatField, IntegerField,
    SelectField, StringField, SubmitField, ValidationError)
from wtforms.validators import length, required

from Flask_Marketplace.models.shop_models import AccountDetail, Currency, Dispatcher, Order, OrderLine, Store


def unique_entry(form, field):
    pass


class AccountForm(FlaskForm):
    account_name = StringField('Bank Name', [required()])
    account_num = IntegerField('Account Number', [required()])
    bank = StringField('Bank Name', [required()])
    save = SubmitField()


class StoreRegisterForm(FlaskForm):
    name = StringField('Store name', [required(), unique_entry])
    about = StringField('Short description', [required()])
    iso_code = SelectField(
        'Currency', choices=Currency.query.with_entities(
            Currency.code, Currency.code).all())
    phone = StringField('Business Phone Number',
                        [required(), length(min=10, max=15)])
    email = StringField('Valid Email',
                        [required(), length(min=10, max=15)])
    logo = FileField()
    save = SubmitField()


class ProductForm(FlaskForm):
    name = StringField('Product name', [required()])
    description = StringField('Short description', [required()])
    price = DecimalField('Sale price', [required()])
    image = FileField('Product image')
    is_active = BooleanField('Publish')
    save = SubmitField()
