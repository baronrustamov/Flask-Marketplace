'''
The Factory Function:  
The aim of this file is to return a fully decorated app object through the
`marketplace` function
'''
import jinja2
import os
import sys

from flask import render_template, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, login_required, SQLAlchemyUserDatastore
from flask_admin import Admin

try:
    import db
except ImportError:
    db = SQLAlchemy()
from Flask_Marketplace import utilities as util


default_config = {
    'APP_NAME': 'Flask',
    'DEBUG': True,
    'SECRET_KEY': 'Ir$6789BoknbgRt678/;oAp[@.kjhgHfdsaw34I&?lP56789M',
    'SECURITY_PASSWORD_HASH': 'sha512_crypt',
    'SECURITY_PASSWORD_SALT': 'vcxdse4r6yu8ijjnb$cde456y7fc',
    'SECURITY_REGISTERABLE': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    # ----- Plugins
    'PLUGINS_FOLDER': 'plugins',  # plugins folder relative to the app root
    # ----- Payment Info
    'CURRENCY_DISPATCHER': 'USD',
    'STORE_MULTICURRENCY': True, # Allow stores to specify currency
    'PRODUCT_PRICING': 'localize',
    'DEFAULT_STORE_NAME': 'Name your store',
    'SPLIT_RATIO_STORE': 0.9,
    'SPLIT_RATIO_DISPATCHER': 0.85,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'platform.sqlite3')
}


def marketplace(app, url_prefix=''):
    # Configs
    for config in default_config:
        if not config in app.config:
            app.config[config] = default_config[config]

    # This section won't have been needed if I don't want to customize
    # security views by default.
    # It's difficult to overide security blueprint template for login and registration
    # Thus, a quick fix will be to manually direct Jinja Loader.
    # I can think of some possible issues now, but untill then...

    shop_module_temps = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'templates')
    enhanced_jinja_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(shop_module_temps),
    ])
    app.jinja_loader = enhanced_jinja_loader

    db.init_app(app)
    with app.app_context():

        from Flask_Marketplace.models import user_models
        from Flask_Marketplace.models import shop_models
        from Flask_Marketplace.forms.shop_forms import AccountForm, ProductForm, StoreRegisterForm
        from Flask_Marketplace.forms.user_forms import ExtendedRegisterForm, ProfileForm
        from Flask_Marketplace import MarketViews

        user_datastore = SQLAlchemyUserDatastore(
            db, user_models.User, user_models.Role)
        # Setting up Security and Admins
        security = Security(app, user_datastore,
                            register_form=ExtendedRegisterForm)
        admin = Admin(app)
        admin.add_view(user_models.UserAdmin(user_models.User, db.session))
        admin.add_view(user_models.RoleAdmin(user_models.Role, db.session))

        @security.send_mail_task  # disable emails
        def no_emails(payload):
            flash('You were successfully registered', 'success')

        # ----- Setup Plugins
        plugins_path = app.config['PLUGINS_FOLDER']
        if os.path.isdir(plugins_path):
            from importlib import import_module
            plugins = os.listdir(plugins_path)  # List of plugins
            for plugin in plugins:
                # import everything exposed through the __init__ of each plugins
                my_module = import_module(plugins_path+'.'+plugin, '*')
                module_dict = my_module.__dict__
                plugin_imports = {name: module_dict[name]
                                  for name in module_dict if not name.startswith('_')}
                # If present, register a blueprint found in views.py file
                # Note that the blueprint name must be the same as the plugin.
                try:
                    view_mod = import_module(plugins_path+'.'+plugin+'.views')
                    app.register_blueprint(
                        getattr(view_mod, plugin), url_prefix=url_prefix+'/'+plugin)
                except (ModuleNotFoundError, AttributeError) as e:
                    print('Info:', e)
        else:
            print('Info: No plugins folder found')
        # Make sure all models exists
        db.create_all()

        """Overiding default market views from plugins"""
        # views can be subclassed to overide some default routes
        marketends = util.inherit_classes(MarketViews)(
            util.inherit_classes(
                AccountForm), util.inherit_classes(ProductForm),
            util.inherit_classes(ProfileForm), util.inherit_classes(StoreRegisterForm))
        print('Info: Views inheritance is as stated below \n',
              marketends.__class__.__mro__)
        # Registering Marketplace rules
        shop = Blueprint('marketplace', __name__, template_folder='templates',
                         static_folder='static', static_url_path='/static/marketplace')
        shop.before_request(marketends.before_request)
        shop.add_url_rule('/', view_func=marketends.index)
        shop.add_url_rule('/cart', view_func=marketends.cart)
        shop.add_url_rule('/checkout', view_func=marketends.checkout)
        shop.add_url_rule('/checked-out', view_func=marketends.checked_out)
        shop.add_url_rule('/dashboard', view_func=marketends.dashboard)
        shop.add_url_rule('/img/<string:model>/<int:id>',
                          view_func=marketends.image)
        shop.add_url_rule('/market', view_func=marketends.market)
        shop.add_url_rule('/save-cart', view_func=marketends.save_cart,
                          methods=['POST'])
        shop.add_url_rule('/store/<string:store_name>/admin',
                          view_func=marketends.store_admin, methods=['GET', 'POST'])
        shop.add_url_rule('/store/new', view_func=marketends.store_new,
                          methods=['GET', 'POST'])
        shop.add_url_rule('/store/<string:store_name>/products',
                          view_func=marketends.store_product, methods=['GET', 'POST'])
        shop.add_url_rule('/store/<string:store_name>/admin/product',
                          view_func=marketends.store_product_admin, methods=['GET', 'POST'])
        shop.add_url_rule('/store/<string:store_name>/admin/product',
                          view_func=marketends.store_product_admin, methods=['GET', 'POST'])

        # Template-wide accessible variables
        shop.add_app_template_global(util.can_edit_product)
        shop.add_app_template_global(util.currency_options)
        shop.add_app_template_global(util.latest_stores)

        app.register_blueprint(shop, url_prefix=url_prefix+'/')

    return app
