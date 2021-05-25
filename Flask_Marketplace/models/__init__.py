''' Module for handling interactions '''
from flask_security import SQLAlchemyUserDatastore
from Flask_Marketplace.models.user_models import db, User, Role, UserAdmin, RoleAdmin

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
