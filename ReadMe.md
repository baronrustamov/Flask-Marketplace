# [Flask-Marketplace](http://ewetoye.pythonanywhere.com/)
![Bootstrap-4.4.1](https://img.shields.io/badge/Bootstrap-4.4.1-blue "Bootstrap-4.4.1")
![Flask==1.2.2](https://img.shields.io/badge/Flask-1.1.2-black "Flask==1.2.2")
![Flask-SQLAlchemy==2.4.4](https://img.shields.io/badge/FlaskSQLAlchemy-2.4.4-black "Flask-SQLAlchemy==2.4.4")
![Flutterwave API V3](https://img.shields.io/badge/FlutterwaveApi-V3-orange "Flask-SQLAlchemy==2.4.4")
![JQuery-3.5.1](https://img.shields.io/badge/JQuery-3.5.1-yellow "JQuery-3.5.1")


> A modular multi-store marketplace extension with a full online payment solution. Can be deployed as a standalone application or installed to provide marketplace features to an existing application.
> [Try out a working version here.](http://ewetoye.pythonanywhere.com/)
<hr>

<div align='center'>
  <img src="https://raw.githubusercontent.com/EwetoyeIbrahim/Flask-Marketplace/master/Flask_Marketplace/static/marketplace/img/site_logo.png" title="Flask-Marketplace Banner" width='100%'>
</div>
<hr>


## Table of Contents
* [Introduction](#Introduction)
* [Setup](#Setup)
  * [Setup Steps](#Steps)
  * [Minimal Example](#Minimal-Example)
* [Testing Data](#Testing)
* [How it works](#How-it-works)
  * [Registration](#Registration)
  * [Store](#Store-and-Product-Registration)
  * [Dispatcher](#Dispatcher)
  * [Shopping and Checkout](#Shopping-and-checking-out)
  * [Payment and Calculations](#Payments-and-calculations)
  * [Configuration Parameters](#Configuration-parameters)
* [Upcoming improvements](#Upcoming-improvements)
<hr>

## Introduction
Flask-Marketplace provides a Jumia-Like online market features where different vendors register their stores and publish products for sale and also posses some additional features, notable of which are:
  * **Extensible:**  The core can easily be extended by using existing or new plugins to introduce features.
  * **Multicurrency:** By default the platform allows customers to switch currency. This could be fixed to the desired currency in the configuration file by setting the `PRODUCT_PRICING` value. [More in the configurations section](#Configuration-parameters).
  * **Revenue sharing:** For every checked-out order, the total revenue is shared based on the value of the `STORE_PAY_RATIO` and `SPLIT_RATIO_DISPATCHER` configuration values. But by default:
    * Vendor:Platform = 0.97:0.03 of the product prices
    * Dispatcher:Platform = 0.80:0.2 of delivery fee.

## Setup
See a [working version here](http://ewetoye.pythonanywhere.com/)
### Steps
1. Install the package, preferably in a virtual environment, with `pip install Flask-Marketplace`
2. Call the Marketplace function with an app object, as shown [below](#Minimal-Example).  
Optional: During production, it is advisable to set configuration variables as explained in the [configuration section](#Configuration-parameters) but can be skipped during testing

### Minimal Example
```
from Flask_Marketplace import marketplace

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Long hard to guess key'
    marketplace(app).run(port=6060, host='0.0.0.0', debug=True)

```

## How it Works
### Registration
[Try the steps below from a this working version](http://ewetoye.pythonanywhere.com/)
<div align='center'>
  <img src="https://raw.githubusercontent.com/EwetoyeIbrahim/static_assets/master/Flask-Marketplace/readme_files/registration.gif"
    title="Registration process" width='100%'>
</div>


* An anonymous user visits or get redirected to the login page
* Clicks on the signup link
* Fills the registration form with a unique email address, and instantly got registered and logged in.

### Store and Product Registration
[Try registering a store](http://ewetoye.pythonanywhere.com/)
<div align='center'>
  <img src="https://raw.githubusercontent.com/EwetoyeIbrahim/static_assets/master/Flask-Marketplace/readme_files/store_product_reg.gif"
    title="Registration process" width='100%'>
</div>

Any registered user can create a store.
For every store sales, the share of the store owner is picked up from the `SPLIT_RATIO_STORE` (default is 0.975) configuration variable. Check [payments and calculations](#Payments-and-calculations) for more.

### Dispatcher
Dispatchers are created on the platform, each dispatcher can charge different delivery rates which is specified during creation.
For every product sales, the dispatcher receives `SPLIT_RATIO_DISPATCHER` (default to 0.8) fraction of it's sum of delivery charge. Check [payments and calculations](#Payments-and-calculations) for more.

### Shopping and checking-out
[Try shopping and checking out](http://ewetoye.pythonanywhere.com/)
<div align='center'>
  <img src="https://raw.githubusercontent.com/EwetoyeIbrahim/static_assets/master/Flask-Marketplace/readme_files/shopping_checkout.gif"
    title="shopping and checkout" width='100%'>
</div>

* A visitor visits the website, the platform guesses the currency of the visitor from its IP Address and sets it as a cookie. based on the visitor's currency, values of all products are converted to the visitor's currency value.
* A user selects all the desired products which could be from different stores
* Clicks on checkout when ready and for redirected to the checkout page, where contact information is collected and summary of the impending order is displayed.
* Clicks on pay now will trigger, if available, an installed payment acquirer plugin and save the checkout data.

### Payments and Calculations:
Say, a customer whose currency iso_code is NGN ordered for two products, Fanta 30cl and Nokia 2.4


**| Fanta 30cl | Nokia 2.4
---------| ------------- | ------------
Store Name | Cocacola | Nokia
Attached Dispatcher | Kwik | Max
Store Unit price | 10 USD | 59,000 NGN
Quantity | 5 | 2
Cart Unit Price | 470 NGN (1USD = 470NGN) | 59,000 NGN
Total Cart amount | 470* 10 *5 = 23500 NGN | 118,000 NGN
Dispatcher Rate | 1.20 USD | 2 USD
Total cart delivery | 5* 1.2 * 470 = 2820NGN | 2 * 2 * 470 = 1880NGN
Checkout Amount | 23500+2820= 26,320NGN |  118000 + 1880 = 119,880 NGN  

In this scenario:
* The customer pays 26320+119880 = 146,200 NGN
* Cocacola gets 23500 * 0.975 = 22,912.50 NGN
* Kwik(Dispatcher attched to Cocacola) gets 2820 * 0.8 = 2,256 NGN
* Nokia gets 118000 * 0.975 = 115,050 NGN
* Max(Dispatcher attched to Cocacola) gets 1880 * 0.8 = 1,504 NGN
* The platform receives the balance less the fluttewaves tranction charges


## Configuration Parameters
Variable  | Type / Default | Description
---------- | - | -------
APP_NAME | String (defaults to `'Flask'`) | Ecommerce  name
DEFAULT_STORE_NAME | String (defaults to `'Name your store'`) | Name of a newly created store. Stores with this name will not be active on the platform
DISPATCHER_CURRENCY | String (defaults to `'USD'`) | The currency at which the store dispatcher charges are saved
PLUGINS_FOLDER | String of path (defaults to `'plugins'`) | path to the location of plugins folder relative to the app root
PRODUCT_PRICING | String of ISO code or None (defaults to `None`) | Specify if products should be converted to different currencies. Values can be one of: String of ISO code, e.g `'NGN'`, to fixed product sales prices  at the specified ISO CODE; or None to allow users converts the product prices from their store currencies to the clients currency based on the conversion rates
SPLIT_RATIO_STORE | String of float (defaults to  `'0.8'`) | The fraction of the products price to disburse to the store owners, the other fraction goes to the platform
SPLIT_RATIO_DISPATCHER | String of float (defaults to  `'0.975'`) | The fraction of the delivery cost to disburse to the dispatcher, the other fraction goes to the platform
STORE_CURRENCY | String of ISO code (defaults to `None`)| Allow stores to specify trading currency

## Upcoming Improvements
* Automated tests
* Plugins
