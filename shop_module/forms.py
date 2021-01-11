from wtforms import FileField, IntegerField, SelectField, StringField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import required, ValidationError, optional
from .models import Store, Currency


def unique_entry(form, field):
    pass


class StoreRegisterForm(FlaskForm):
    name = StringField('Store name', [required(), unique_entry])
    about = StringField('Short description', [required()])
    iso_code = SelectField(
        'Currency', choices=Currency.query.with_entities(
            Currency.code, Currency.code).all())
    logo = FileField()
    save = SubmitField()


class AccountDetailForm(FlaskForm):
    account_name = StringField('Account Name', [required()])
    account_num = IntegerField('Account Number', [required()])
    bank_name = StringField('Bank', [required()])
    save = SubmitField()
