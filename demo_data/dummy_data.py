import os

roles = {
    'Admin': 'Add and deactivate users, dispatchers and products',
    'User': 'All external user (customer and Store Owners',
}

users = {
    'Jumga Admin': [
        'admin@jumga.com',
        'password',
        'Admin'
    ],
    'Store1 Owner1': [
        'owner1@gmail.com',
        'password',
        'User',
    ],
    'Store2 Owner2': [
        'owner2@gmail.com',
        'password',
        'User',
    ],
    'Random Customer': [
        'customer@gmail.com',
        'password',
        'User',
    ]
}

currencies = {
    'Kenya': 'KES',
    'Nigeria': 'NGN',
    'United Kingdom': 'GBP',
    'United State': 'USD',
}

dispatchers = {
    'Errandi': ['Errandi PLC', 30989012345, 'Union', ],  # account
    'Motorize': ['Motorize LTD', 1098765432, 'Access', ],
}

stores = {
    'Phone360': [
        os.urandom(10),
        'Phone is a basic neccesity',
        3, # currency_id
        1,  # dispatcher_id
        2,  # user_id
        
        ['Phone360 PLC', 3021345678, 'Polaris', ],  # account
    ],
    'Farmingo': [
        os.urandom(500),
        'We sell farm harvest at cheapest prices',
        2,
        3,
        2,
        ['Farmingo INC', 1012345678, 'GT Bank', ],
    ],
}

products = {
    'Product 1': [
        2500.50,  # price
        'Decsription 1',
        os.urandom(500),
        2,  # store_id
        True,
    ],
    'Product 2': [
        2200.00,
        'Decsription 2',
        os.urandom(500),
        2,
        True,
    ],
    'Product 3': [
        1500.90,
        'Decsription 1',
        os.urandom(500),
        2,
        True,
    ],
    'Product 4': [
        2500.10,  # price
        'Decsription 1',
        os.urandom(500),
        3,  # store_id
        True,
    ],
    'Product 5': [
        2200,
        'Decsription 2',
        os.urandom(500),
        3,
        True,
    ],
    'Product 6': [
        1500,
        'Decsription 1',
        os.urandom(500),
        3,
        True,
    ],
}
