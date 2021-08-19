'''
The Factory Function:  
The aim of this file is to return a fully decorated app object through the
`marketplace` function
'''
from importlib import import_module
import jinja2
import logging
import os
import sys

from flask import render_template, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, login_required, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_wtf import CSRFProtect

try:
    import db
except ImportError:
    db = SQLAlchemy()
from Flask_Marketplace import utilities as util

logging.basicConfig(
    filename='marketplace.log',
    level=logging.DEBUG,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)


def marketplace(app, url_prefix=''):
    # Configs
    default_config = {
        'SECURITY_PASSWORD_HASH': 'sha512_crypt',
        'SECURITY_PASSWORD_SALT': 'vcxdse4r6yu8ijjnb$cde456y7fc',
        'SECURITY_REGISTERABLE': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'sqlite.db'), #os.path.dirname(__file__)), 'platform.sqlite3'),

        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        # ----- Flask Markeplace Specifics
        'APP_NAME': 'FlaskMarkt',  # Ecommerce Name
        'DISPATCHER_CURRENCY': 'USD',  # Delivery rates currency
        'DEFAULT_STORE_NAME': 'Name your store',  # Name of newly created stores
        'PLUGINS_FOLDER': 'plugins',  # Plugins folder relative to the app root
        # None(multicurrency) or ISO code(fixed currency)
        'PRODUCT_PRICING': None,
        'SPLIT_RATIO_DISPATCHER': 0.85,  # Payout fraction from delivery cost
        'SPLIT_RATIO_STORE': 0.9,  # Payout fraction from item price
        # None(stores specify currency) or ISO code(fixed)
        'STORE_CURRENCY': None,
    }
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
        # Enabling protection against CSRF
        csrf = CSRFProtect(app)
        
        # Make sure the default tables exists before been used by forms and plugins
        from Flask_Marketplace.models import user_models
        from Flask_Marketplace.models import shop_models
        db.create_all()
        
        # Setting up Security and Admins
        from Flask_Marketplace.forms.user_forms import ExtendedRegisterForm
        user_datastore = SQLAlchemyUserDatastore(
            db, user_models.User, user_models.Role)
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
            # Get a list of all available plugins
            # Neglect folders that starts with point(.) and double underscore(__)
            plugins = [p for p in os.listdir(plugins_path) if not(
                p.startswith('.') or p.startswith('__'))]
            for plugin in plugins:
                # Import the setup.py file, which must be present at the root
                setup = None
                try:
                    setup = import_module(plugins_path+'.'+plugin+'.setup')
                    if hasattr(setup, 'config'):
                        # apply the module's configuration
                        for config in setup.config:
                            if not config in app.config:
                                app.config[config] = setup.config[config]
                    app.logger.info('Installing '+setup.name)
                except (ModuleNotFoundError, AttributeError) as e:
                    app.logger.info(f'Skipping a plugin - {e}')
                    continue
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
                    app.logger.info(
                        f'No views registered for {setup.name} - {e}')
        else:
            app.logger.info('No plugins folder found')
        # Create other plugins models
        db.create_all()
        
        # === Time to set the default view, noting that they might have  been subclassed
        from Flask_Marketplace.forms.shop_forms import AccountForm, ProductForm, StoreRegisterForm
        from Flask_Marketplace.forms.user_forms import ProfileForm
        from Flask_Marketplace import MarketViews
        marketends = util.inherit_classes(MarketViews)(
            util.inherit_classes(
                AccountForm), util.inherit_classes(ProductForm),
            util.inherit_classes(ProfileForm), util.inherit_classes(StoreRegisterForm))
        app.logger.info(
            f'Views inheritance hierarchy:\n{marketends.__class__.__mro__}')
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
