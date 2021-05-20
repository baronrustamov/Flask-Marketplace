from flask_security.forms import RegisterForm, Required
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, ValidationError
from wtforms.validators import required

from .models import User


def unique_entry(form, field):
    pass


class ExtendedRegisterForm(RegisterForm):
    name = StringField('Full Name', [Required()])


class ProfileForm(FlaskForm):
    name = StringField('Full Name', [required(), unique_entry])
    email = StringField('Login Email', [required()])
    save = SubmitField()
