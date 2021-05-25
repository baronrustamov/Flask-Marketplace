''' Module for handling interactions '''
from flask_security import SQLAlchemyUserDatastore
from Flask_Marketplace.users_module.models import db, User, Role, UserAdmin, RoleAdmin

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
