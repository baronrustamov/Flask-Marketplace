from flask_wtf import FlaskForm
from wtforms import (
    DecimalField, FileField, FloatField, IntegerField, SelectField, StringField,
    SubmitField, ValidationError)
from wtforms.validators import length, required

from .models import Currency, Store


def unique_entry(form, field):
    if Store.query.filter_by(name=field.data) is not None:
        raise ValidationError(f'{field.data} already exists')


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


class ProductForm(FlaskForm):
    name = StringField('Store name', [required(), unique_entry])
    description = StringField('Short description', [required()])
    price = DecimalField('Sale price', [required()], 0.01)
    image = FileField('Product image')
    save = SubmitField()
