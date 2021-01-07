'''
Human related models are located here, currently we have:
  - Role: Which may be one of Admin | Vendor | Customer
  - User: Table of everyone capable of logging in to the system
'''
from datetime import datetime

from flask_security import utils, current_user, UserMixin, RoleMixin
from flask_admin.contrib import sqla
from wtforms.fields import PasswordField

from factory import db


roles_users = db.Table(
    'roles_users', db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    ''' Table of everyone capable of logging in to the system '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, default=True)
    # relationships --------------------------------------
    orders = db.relationship('Order', backref='user')
    roles = db.relationship(
        'Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))
    stores = db.relationship('Store', backref='user')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        if self.active:
            return True
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.name)


# Customized User model for SQL-Admin
class UserAdmin(sqla.ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when
    # creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and
    # available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in
    # user has the 'Admin' role
    def is_accessible(self):
        return current_user.has_role('Admin')

    # On the form for creating or editing a User, don't display a field
    # corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password
    # before storing in the database. Second, we want to use a password field
    # (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already
        # told Flask-Admin to exclude the password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, name it 'password2' and labeling it 'New Password'.
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or
    # edited User -- before the changes are committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # Encrypt the new password prior to storing it in the database.
            # If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)


class RoleAdmin(sqla.ModelView):
    def is_accessible(self):
        return current_user.has_role('Admin')
