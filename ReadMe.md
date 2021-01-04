------ Delivery -----
Rate: Dispatchers are registered with a fixed rate in the currency of assigned store. For example, in the demo data, the two dispather charges 5USD/item and 750NGN/item respectively, since the former was assigned to a store denominated in USD while the latter was assigned to a store deniminated in NGN.

Payment Calculation: Say, a customer ordered for 30 items from _Phone360_ store which is denoted in USD, _Errandi_, its attached vendor with 5USD/item delivery rate.
* Customer pays 5 * 30 (150USD)  
* Errantin gets 5 * 30 * 0.8 (120USD), that is 80% of delivery fee  
* Platform charges 5 * 30 * 0.2 (30USD), that is 80% of delivery fee.

Disbursement of payments: Hust like the stores, dispatchers subaccounts are created for dispatchers, once registered on the database  and stored in, accounting table and used to split payments during checkout when the `INSTANT_PAYMENT_SPLIT` is set in the configuration, otherwise, the store accpunt detail, will be used to effect payment after the order has been marked as delivered by the store owner.


----- Store ----
Store Creation: Store users are elligble to create a store after the payment of 2000NGN or its equivalent in store base currency.


A vistor visit the website, the platform guesses the currency of the visitor from the its IP Address and sets it as a cookie.
based on the visitors currency, values of all products are converted to the visitors' currency value.