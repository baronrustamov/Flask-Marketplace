'''
The Factory Function:  
The aim of this file is to return a fully decorated app object through the
`create_app` function
  - The database is initialised here, thus to add table(s) db must be inherited from here
  - All blueprint are stitched within the app_context
'''
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_admin import Admin

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    with app.app_context():
        # setup users_module
        import users_module.models
        from users_module import user_datastore, User, Role, UserAdmin, RoleAdmin

        # Setup shop_moodule
        import shop_module.models
        from shop_module.views import shop
        app.register_blueprint(shop, url_prefix='/')

        # Setup security and admin
        Security(app, user_datastore)
        admin = Admin(app)
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(RoleAdmin(Role, db.session))
        
        db.create_all()
    return app
