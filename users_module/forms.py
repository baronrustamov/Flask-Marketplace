from flask_security.forms import RegisterForm, Required
from wtforms import StringField
from wtforms.validators import required

class ExtendedRegisterForm(RegisterForm):
    name = StringField('Full Name', [Required()])

class classname(object):
  """
  docstring
  """
  pass