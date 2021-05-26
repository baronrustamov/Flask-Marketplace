'''
The Factory Function:  
The aim of this file is to return a fully decorated app object through the
`marketplace` function
  - The database is initialised here, thus to add table(s) db must be inherited from here
  - All blueprint are stitched within the app_context
'''
import jinja2
import os
from flask import render_template, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, login_required
from flask_admin import Admin

from config import config

try:
    import db
except ImportError:
    db = SQLAlchemy()
import os
import sys
sys.path.append(os.path.dirname(__file__))


def marketplace(
        app,
        config_name=os.getenv('CONFIG_NAME', default='default'),
        url_prefix=''):
    app.config.from_object(config[config_name])
    if not 'SQLALCHEMY_DATABASE_URI' in app.config:
        test_db = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'platform.sqlite3')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + test_db

    # This section won't have been needed if I don't want to customize 
    # security views by default.
    # I found it difficult to overide security blueprint template for login and registration
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
        from models import user_datastore, User, Role, UserAdmin, RoleAdmin
        from Flask_Marketplace.models.shop_models import AccountDetail, Currency, Dispatcher, Order, OrderLine, Product, Store
        from Flask_Marketplace.forms.shop_forms import AccountForm, ProductForm, StoreRegisterForm
        from Flask_Marketplace.forms.user_forms import ExtendedRegisterForm, ProfileForm
        from Flask_Marketplace import MarketViews

        # Setting up Security and Admins
        security = Security(app, user_datastore, register_form=ExtendedRegisterForm)
        admin = Admin(app)
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(RoleAdmin(Role, db.session))

        @security.send_mail_task  # disable emails
        def no_emails(payload):
            flash('You were successfully registered', 'success')


        # ----- Setup Plugins
        import importlib
        plugins = [{'path': 'flw_module', 'bp_name': 'flw'}]
        for plugin in plugins:
            my_module = importlib.import_module('plugins.'+plugin['path'], '*')
            module_dict = my_module.__dict__
            imports = {name: module_dict[name] for name in module_dict if not name.startswith('_')}
            
            module = importlib.import_module('plugins.'+plugin['path']+'.views')
            app.register_blueprint(
                getattr(module, plugin['bp_name']), url_prefix=url_prefix+'/'+plugin['bp_name'])
        
        # Make sure all models exists
        db.create_all()

        """Overiding default market views from plugins
        """
        mod_views = [MarketViews]
        sub_views = MarketViews.get_all_subclasses()
        if sub_views:
            mod_views.extend(sub_views)
            _def_view, *args = mod_views
            class NewMarketViews(*args): pass
        else:
            NewMarketViews = MarketViews
        
        marketends = NewMarketViews(
            AccountDetail, Currency, Dispatcher, Order, OrderLine, Product, Store,
            AccountForm, ProductForm, ProfileForm, StoreRegisterForm)

        # Registering Marketplace rules
        shop = Blueprint('marketplace', __name__, template_folder='templates', static_folder='static',
                         static_url_path='/static/marketplace')
        shop.before_request(marketends.before_request)
        shop.add_url_rule('/', view_func=marketends.index)
        shop.add_url_rule('/cart', view_func=marketends.cart)
        shop.add_url_rule('/checkout', view_func=marketends.checkout)
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
        from Flask_Marketplace.utilities import can_edit_product, currency_options, latest_stores
        shop.add_app_template_global(can_edit_product)
        shop.add_app_template_global(currency_options)
        shop.add_app_template_global(latest_stores)

        app.register_blueprint(shop, url_prefix=url_prefix+'/')

    return app
