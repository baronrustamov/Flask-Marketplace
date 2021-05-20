''' Module for handling interactions '''
from flask_security import SQLAlchemyUserDatastore
from .models import db, User, Role, UserAdmin, RoleAdmin

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
