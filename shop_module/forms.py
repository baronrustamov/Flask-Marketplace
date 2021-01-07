from wtforms import FileField, IntegerField, SelectField, StringField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import required, ValidationError
from .models import Store, AccountDetail


def unique_store_name(form, field):
    if Store.query.filter(name=field.data) is not None:
        msg = 'A store already exists with this name'
        raise ValidationError(msg)


class StoreRegisterForm(FlaskForm):
    name = StringField('Store name',
                       validators=[required(), unique_store_name])
    about = StringField('Short description', validators=[required()])
    iso_code = SelectField()
    logo = FileField('Logo',)
    # ----- Account detail
    account_name = StringField('Account Name',
                               validators=[required()])
    account_num = IntegerField('Account Number',
                               validators=[required()])
    bank_name = StringField('Bank Name', validators=[required()])

    
