'''
The Factory Function:  
The aim of this file is to return a fully decorated app object through the
`create_app` function
  - The database is initialised here, thus to add table(s) db must be inherited from here
  - All blueprint are stitched within the app_context
'''
from flask import Flask, render_template, request, flash
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
        # ----- Setup users_module
        import users_module.models
        from users_module import user_datastore, User, Role, UserAdmin, RoleAdmin
        from users_module.forms import ExtendedRegisterForm
        security = Security(app, user_datastore,
                            register_form=ExtendedRegisterForm)

        @security.send_mail_task  # disable emails
        def no_emails(payload):
            flash('You were successfully registered', 'success')

        # ----- Setup shop_module
        import shop_module.models
        from shop_module.views import shop
        app.register_blueprint(shop, url_prefix='/')

        # ----- Setup flw_moodule
        import flw_module.models
        from flw_module.views import flw
        app.register_blueprint(flw, url_prefix='/flw')

        # ----- Setup admin
        admin = Admin(app)
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(RoleAdmin(Role, db.session))

        db.create_all()
    return app
