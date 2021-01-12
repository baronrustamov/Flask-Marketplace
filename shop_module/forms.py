from flask_wtf import FlaskForm
from wtforms import (FileField, IntegerField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import ValidationError, length, required

from .models import Currency, Store


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

