# JUMGA MARKETPLACE
![Bootstrap-4.4.1](https://img.shields.io/badge/Bootstrap-4.4.1-blue "Bootstrap-4.4.1")
![Flask==1.2.2](https://img.shields.io/badge/Flask-1.1.2-black "Flask==1.2.2")
![Flask-SQLAlchemy==2.4.4](https://img.shields.io/badge/FlaskSQLAlchemy-2.4.4-black "Flask-SQLAlchemy==2.4.4")
![Flutterwave API V3](https://img.shields.io/badge/FlutterwaveApi-V3-orange "Flask-SQLAlchemy==2.4.4")
![JQuery-3.5.1](https://img.shields.io/badge/JQuery-3.5.1-yellow "JQuery-3.5.1")

> A multi-vendor modular marketplace web applicatiion with full online payment solution  
> Developed during Flutterwave's Developer Challenge 2021
<hr>
<div align='center'>
  <img src="./static/shop/img/site-banner.jpg" title="Github Logo" width='100%'>
</div>
<hr>

# Table of Contents
* [Introduction](#Introduction)
* [Setup](#Setup)
* [Testing Data](#Testing)
* [How it works](#How-it-works)
  * Delivery
  * Store
* [Configuration Parameters](#Configuration-parameters)
<hr>

## Introduction
This web application provides a Jumia-Like online market features where different vendors register their stores and publish products for sale. This app also provide some features, notable of which are:
  * Multicurrency: By default the platform allows customers to switch currency. This could be fixed to a desired currency in the configuration file by setting the `PRODUCT_PRICING` value[See configurations section](#Configuration-parameters). 
  * Vendor Registration Token: For registration, a fee whose value and currency could be set by setting the `STORE_REG_AMT (defaults to 10 USD) value in the config [Read more in the config section]().
  * Dispatcher Assignment: Upon successful registration, a JUMGA dispatcher is randomly assigned to each store.
  * Revenue sharing: For every checked-out order, the total revenue is shared based on the value of the `STORE_PAY_RATIO` and `SPLIT_RATIO_DISPATCHER` configuration values. But by default:
    * Vendor:Jumga = 0.97:0.03 of the product prices
    * Dispatcher:Jumga = 0.80:0.2 of delivery fee.  
  Note: The point at which the splitting occurs is defined by the `PAYMENT_SPLIT_POINT` (defaults to `'instant'`) [see the Configuration section]().

## Setup
1. _[required]_ Install the requirements file by doing ```python -m pip install -r requirements.txt```
2. _[optional]_ During production, it is advisable to set configuration variables as explained in the [configuration section](Configuration Variables) but can be skipped during testing
3. _[optional]_ For testing purpose, if desired some dummy data (products, users, stores, and  dispatchers) can be automatically bootstraped to the database by running ```python create_dummy.py``` [see more](testing)
3. _[required]_ launch the app by doing ```python run.py```

## How it Works
### Shopping and checking out

### Store


### Delivery
Dispatchers are registered with a fixed rate in the currency of assigned store. For example, in the demo data, the two dispather charges 5USD/item and 750NGN/item respectively, since the former was assigned to a store denominated in USD while the latter was assigned to a store deniminated in NGN.

### Payment Calculation:
Say, a customer ordered for 30 items from _Phone360_ store which is denoted in USD, _Errandi_, its attached vendor with 5USD/item delivery rate.
* Customer pays 5 * 30 (150USD)  
* Errantin gets 5 * 30 * 0.8 (120USD), that is 80% of delivery fee  
* Platform charges 5 * 30 * 0.2 (30USD), that is 20% of delivery fee.

### Disbursement of payments:
Just like the stores, dispatchers subaccounts are created for dispatchers, once registered on the database  and stored in, accounting table and used to split payments during checkout when the `INSTANT_PAYMENT_SPLIT` is set in the configuration, otherwise, the store accpunt detail, will be used to effect payment after the order has been marked as delivered by the store owner.


### Store
Store Creation: Store users are elligble to create a store after the payment of 2000NGN or its equivalent in store base currency.


A vistor visit the website, the platform guesses the currency of the visitor from the its IP Address and sets it as a cookie.
based on the visitors currency, values of all products are converted to the visitors' currency value.

## Configuration Parameters
Variable  | Type / Default | Description
---------- | - | -------
SPLIT_RATIO_STORE | String of float (defaults to  '0.8') | The fraction of the products price to disburse to the store owners, the other fraction goes to the platform
SPLIT_RATIO_DISPATCHER | String of float (defaults to  '0.975') | The fraction of the delivery cost to disburse to the dispatcher, the other fraction goes to the platform
FLW_PUB_KEY | String (defaults to a flutterwave test api value of 'FLWPUBK_TEST-4b5acac8e21aceb3fc87f634a846c001-X'). | Flutterwave's public key for integrating frontend payments, you have to [get yours](https://developer.flutterwave.com/docs/api-keys) to be able to handle payments succesfully.
FLW_SEC_KEY | String (defaults to a flutterwave test api value of 'FLWSECK_TEST-604a7225885949af8eded44c605deb0c-X' | Flutterwave's secret key for backend communications with your flutterwave's account, you have to [get yours](https://developer.flutterwave.com/docs/api-keys) to be able to perform backend activities like confirmation of payments succesfully
PAYMENT_SPLIT_POINT | String (defaults to 'instant') | When to disburse payment to the parties (store and dispatchers) involved. Can be one of `'instant'` (pay each vendors and dispatchers during checkout using subaccount flat split payment), `'fullfil'` (_not_yet_implemented_ pay parties after when an order has been marked as done)
PAYMENT_PLATFORM | String (defaults to 'flutterwave') | The payment platform to use, note that this app is built on modular architecture, thus one can always write modules for other payment system but must really understand what needs to be tweaked, thus the scope of this app is currently for flutterwave payment system which is known for its reliability
PRODUCT_PRICING | String (defaults to 'localize') | The currencu to display the product in. Can be one of: `localize` (converts the products from their store currency to the clients currency based on the conversion rates specified provided the client currency is one stated next, else product prices will be converted to USD); `'GBP'`; `'KES'`; `'NGN'`; `'USD'` (The product prices will be fixed at the specified ISO CODE)
STORE_REG_AMT | String of value+space+code (defaults to '10 USD') | The registration fee to charge Vendors