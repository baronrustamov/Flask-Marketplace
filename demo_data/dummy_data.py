import os

roles = {
    'Admin': 'Add and deactivate users, dispatchers and products',
    'User': 'All external user (customer and Store Owners',
}

users = {
    'Admin': [
        'admin@market.com',
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
    'Kenya': ['KES', 109.74],
    'Nigeria': ['NGN', 396.70],
    'United Kingdom': ['GBP', 0.73],
    'United State': ['USD', 1],
}

dispatchers = {
    'Errandi': [5, '08123456789', 'errandi@gmail.com',
                'Errandi PLC', 30989012345, 'Union', ],
    'Motorize': [1500, '08123456789', 'motorize@gmail.com',
                 'Motorize LTD', 1098765432, 'Access', ],
}

stores = {
    'Phone360': [
        os.urandom(10),
        'Phone is a basic neccesity',
        'USD',  # currency_code
        1,  # dispatcher_id
        2,  # user_id
        '08012345678',  # phone
        'phone360@gmail.com',
        ['Phone360 PLC', 3021345678, 'Polaris', ],  # account
    ],
    'Farmingo': [
        os.urandom(500),
        'We sell farm harvest at cheapest prices',
        'NGN',
        2,
        3,
        '08012345679',
        'farmingo@gmail.com',
        ['Farmingo INC', 1012345678, 'GT Bank', ],
    ],
}

products = {
    'Product 1': [
        2500.50,  # price
        'Decsription 1',
        os.urandom(500),
        1,  # store_id
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
        1,
        True,
    ],
    'Product 4': [
        2500.10,  # price
        'Decsription 1',
        os.urandom(500),
        2,  # store_id
        True,
    ],
    'Product 5': [
        2200,
        'Decsription 2',
        os.urandom(500),
        1,
        True,
    ],
    'Product 6': [
        1500,
        'Decsription 1',
        os.urandom(500),
        2,
        True,
    ],
}
