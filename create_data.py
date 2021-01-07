'''
Posses two functions:
create_role, which adds roles three roles if not found
create_dummy_db, which adds dummy users to the db
Note: this file should never be called on a production database
as calling this file directly invokes the create_dummy_db() function
which adds four Users with varying priviledges as stated in the
create_dummy_db() docstring
'''
from datetime import datetime, timedelta
import os

from flask_security import utils, SQLAlchemyUserDatastore

from demo_data import dummy_data
from factory import db
from run import app
import shop_module.models
import users_module.models


def create_roles(user_datastore):
    # Create the tables, if they don't exist
    db.create_all()

    # Create the Roles if they don't exist
    for key in dummy_data.roles:
        user_datastore.find_or_create_role(name=key,
                                           description=dummy_data.roles[key])


def create_users(user_datastore):
    # Create four Users for testing and debugging purposes: unless they already
    # exists.
    for username, detail in dummy_data.users.items():
        if not user_datastore.get_user(detail[0]):
            user_datastore.create_user(
                name=username,
                email=detail[0],
                password=utils.encrypt_password(detail[1]),
            )
        # Assign roles to this user
        for i in detail[2:]:
            user_datastore.add_role_to_user(detail[0], i)


def create_currencies():
    for country in dummy_data.currencies:
        currency = shop_module.models.Currency(
            country=country,
            code=dummy_data.currencies[country][0],
            rate=dummy_data.currencies[country][1],
        )
        db.session.add(currency)


def create_dispatchers():
    i = 1
    for name, details in dummy_data.dispatchers.items():
        dispatcher = shop_module.models.Dispatcher(
            name=name, charge=details[3])
        account = shop_module.models.AccountDetail(
            account_name=details[0],
            account_num=details[1],
            bank_name=details[2],
            dispatcher_id=i,
        )
        db.session.add(dispatcher)
        db.session.add(account)
        i += 1


def create_stores():
    i = 1
    for name, details in dummy_data.stores.items():
        store = shop_module.models.Store(
            name=name,
            logo=details[0],
            about=details[1],
            iso_code=details[2],
            dispatcher_id=details[3],
            user_id=details[4],
        )
        account = shop_module.models.AccountDetail(
            account_name=details[5][0],
            account_num=details[5][1],
            bank_name=details[5][2],
            store_id=i,
        )
        db.session.add(store)
        db.session.add(account)
        i += 1


def create_products():
    i = 1
    for name, details in dummy_data.products.items():
        product = shop_module.models.Product(
            name=name,
            price=details[0],
            description=details[1],
            image=details[2],
            store_id=details[3],
            is_active=details[4],
            # stagger creation time to reflect the new products feature
            created_at=datetime.utcnow() - timedelta(minutes=2*i),
        )
        db.session.add(product)
        i += 1


def create_dummy_db():
    '''
    Some dummy users will be created and assigned roles: The names and roles
    of the dummy users are as stated above, i.e,
    Authour is assigned username='Authour', email='author@example.com', and
    password='password'
    '''
    with app.app_context():
        from users_module import user_datastore, User, Role
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        # Create the Roles
        create_roles(user_datastore)
        # Create four Users for testing and debugging purposes
        create_users(user_datastore)
        create_currencies()
        create_dispatchers()
        create_stores()
        create_products()
        # Committing seems to be the beat optuion here,
        # as nothing will be committed is any constraint is breached
        db.session.commit()


if __name__ == "__main__":
    create_dummy_db()
