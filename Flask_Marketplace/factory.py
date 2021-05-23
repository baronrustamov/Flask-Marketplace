'''
The Factory Function:  
The aim of this file is to return a fully decorated app object through the
`marketplace` function
  - The database is initialised here, thus to add table(s) db must be inherited from here
  - All blueprint are stitched within the app_context
'''
import jinja2
import os
from flask import render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
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

    #--- This section won't have been needed if don't want to customize security views by default
    # I found it difficult to overide security blueprint template for login and registration
    # Thus, a quick fix will be to manually direct Jinja Loader.
    # I can think of some possible issues now, but untill then...
    shop_module_temps = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'shop_module', 'templates')
    main_temps = (os.path.join(os.path.abspath(
        os.path.dirname(sys.modules['__main__'].__name__)), 'templates'))
    print(shop_module_temps)
    enhanced_jinja_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(main_temps),
        jinja2.FileSystemLoader(shop_module_temps),
    ])
    app.jinja_loader = enhanced_jinja_loader

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

        # ----- Setup flw_moodule
        import importlib
        plugins = [{'path': 'flw_module', 'bp_name': 'flw'}]
        for plugin in plugins:
            importlib.import_module('plugins.'+plugin['path']+'.models') 
            #importlib.import_module('models', package='plugins.'+plugin['path'])
            module = importlib.import_module('plugins.'+plugin['path']+'.views') 
            app.register_blueprint(getattr(module, plugin['bp_name']), url_prefix=url_prefix+'/'+plugin['bp_name'])
        '''
        import flw_module.models
        from flw_module.views import flw
        app.register_blueprint(flw, url_prefix=url_prefix+'/flw')
        '''
        # ----- Setup shop_module
        import shop_module.models
        # After the last models,
        # we have to make sure the tables or present
        db.create_all()
        from shop_module.views import marketplace as shop
        app.register_blueprint(shop, url_prefix=url_prefix+'/')

        # ----- Setup admin
        admin = Admin(app)
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(RoleAdmin(Role, db.session))

    return app
