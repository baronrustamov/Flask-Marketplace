''' Defination of all marketplace views in `marketplace` blueprint '''
import os
from requests import get

from flask import (abort, current_app, flash, make_response, redirect,
                   render_template, request, Response, url_for)
from flask_login import current_user, login_required
from sqlalchemy import text

from . import utilities
from Flask_Marketplace.factory import db
from Flask_Marketplace.models.shop_models import (
    AccountDetail, Currency, Dispatcher, Order, OrderLine, Product, Store)


class MarketViews:
    def __init__(self, AccountForm, ProductForm, ProfileForm, StoreRegisterForm):
        # Models
        self.AccountDetail = AccountDetail
        self.Currency = Currency
        self.Dispatcher = Dispatcher
        self.Order = Order
        self.OrderLine = OrderLine
        self.Product = Product
        self.Store = Store
        # Forms
        self.AccountForm = AccountForm
        self.ProductForm = ProductForm
        self.ProfileForm = ProfileForm
        self.StoreRegisterForm = StoreRegisterForm

    def before_request(self):
        ''' Make sure that the currency is always known '''
        if not(request.cookies.get('iso_code')):
            response = make_response(redirect(request.path))
            if (current_app.config['PRODUCT_PRICING'].split('-')[0] not
                    in ['localize', 'localize_market']):
                code = current_app.config['PRODUCT_PRICING']
            else:
                try:
                    code = get('https://ipapi.co/currency/').text
                except Exception:
                    code = 'USD'
                if not((code,) in self.Currency.query.with_entities(
                        self.Currency.code).all()):
                    code = 'USD'
            response.set_cookie('iso_code', code)
            return response

    def index(self):
        """Homepage of marketplace

        Returns:
            template: marketplace/home.html
        """
        try:
            # Use the user defined ones, if present
            ban_dir = 'static/marketplace_assets/img/banners/'
            banners = [ban_dir + img for img in os.listdir(ban_dir)]
        except FileNotFoundError:
            # Use the default place holders
            ban_dir = 'marketplace/img/banners/'
            banners = os.listdir(os.path.join(os.path.abspath(
                os.path.dirname(__file__)), 'static/'+ban_dir))
            banners = ['/static/marketplace/' +
                       ban_dir + img for img in banners]
        latest = self.Product.query.order_by(
            self.Product.created_at.desc()).limit(6).all()
        return render_template('marketplace/home.html', products=latest, banners=banners)

    @login_required
    def cart(self):
        """Add or view items in cart

        Returns:
            template: marketplace/cart.html
        """
        iso_code = request.cookies.get('iso_code')
        prod_str = request.args.get('id')
        # Check if the current user has an hanging cart
        cart = self.Order.cart().filter_by(user_id=current_user.id).first()
        if prod_str:
            # ---- The user is adding a product to cart ------
            prod_id = int(prod_str)
            # Get the selected product detail
            cart_line = self.Product.public().filter_by(id=prod_id).first()
            if cart:
                # Check if this product already exist in the cart
                prev_prod_line = db.session.query(self.OrderLine).filter_by(
                    order_id=cart.id, product_id=prod_id).first()
                if prev_prod_line:
                    # Add one to the quantity of this product
                    prev_prod_line.qty += 1
                else:
                    # Include this product in the previous cart
                    db.session.add(self.OrderLine(order_id=cart.id,
                                                  product_id=cart_line.id,
                                                  price=cart_line.price,))
            else:
                # Take the product with price tag and add it to an new cart
                cart_line = self.OrderLine(product_id=cart_line.id,
                                           price=cart_line.price,)
                cart = self.Order(user_id=current_user.id, iso_code=iso_code,
                                  orderlines=[cart_line])
                db.session.add(cart_line)
                db.session.add(cart)
            db.session.commit()
            flash("Item has been added to cart", 'success')
            return redirect(url_for('marketplace.cart', cart=cart))
        if cart:
            cart = self.OrderLine.query.filter_by(order_id=cart.id).all()
        return render_template('marketplace/cart.html', cart=cart)

    @login_required
    def checkout(self):
        iso_code = request.cookies.get('iso_code')
        # Get the last hanging cart
        cart_lines = None
        cart = self.Order.cart().filter_by(user_id=current_user.id).first()
        if cart:
            # For security reason, let's update all the order line prices
            for line in db.session.query(self.OrderLine).filter_by(order_id=cart.id).all():
                line.price = line.product.sale_price(iso_code)
            db.session.commit()  # To ensure the updated figures are picked up
            cart_lines = self.OrderLine.query.filter_by(order_id=cart.id).all()
        # Summarize the cart items by Store>>store_amt_sum>>store_qty_sum
        # Why sum of quantities per store? Recall, dispatchers rates are per qty
        pay_data, store_value = utilities.compute_checkout(cart.id, iso_code)
        return render_template('marketplace/checkout.html', cart=cart_lines,
                               store_value=store_value, pay_data=pay_data)

    @login_required
    def checked_out(self):
        address = request.args.get('address')
        print(address)
        phone = text = request.args.get('phone')
        print(phone)
        cart = Order.cart().filter_by(user_id=current_user.id).first()
        try:
            utilities.record_sales(cart.id, address=address, phone=phone)
            flash('Thank you, your order is being processed', 'success')
        except Exception:
            raise Exception
            flash('Unable to checkout \n Kindly contact us', 'danger')
        return redirect(url_for('marketplace.index', cart=cart))

    @login_required
    def dashboard(self):
        profile_form = self.ProfileForm()
        if profile_form.validate_on_submit():
            # Changing the store detail
            current_user.name = profile_form.name.data
            current_user.about = profile_form.email.data
            db.session.commit()
            flash('Profile details: succesfully edited', 'success')
            return redirect(url_for('marketplace.dashboard'))
        # Pre-populating the form
        profile_form.name.data = current_user.name
        profile_form.email.data = current_user.email
        return render_template('marketplace/dashboard.html',
                               profile_form=profile_form)

    def image(self, model, id):
        if model == 'product':
            product = self.Product.query.get_or_404(id)
            if product:
                return Response(product.image, mimetype='image/jpg')
        elif model == 'store':
            store = self.Store.query.get_or_404(id)
            if store:
                return Response(store.logo, mimetype='image/jpg')
        return False

    def market(self):
        iso_code = request.cookies.get('iso_code')
        products = self.Product.public()
        return render_template('marketplace/market.html',
                               products=products,
                               iso_code=iso_code)

    @login_required
    def save_cart(self):
        # Still being worked on
        cart_data = request.json
        cart = OrderLine.query.filter_by(order_id=cart_data['cart_id']).all()
        if (cart[0].order.user_id == current_user.id):
            iso_code = request.cookies.get('iso_code')
            # clear this cart OrderLines
            db.session.query(OrderLine).filter(
                OrderLine.order_id == cart_data['cart_id']).delete()
            # Recreate the orderlines
            for cart_line in cart_data['prod_data']:
                db.session.add(OrderLine(
                    order_id=cart_data['cart_id'],
                    product_id=cart_line['id'],
                    qty=cart_line['qty'],
                    price=Product.query.get(
                        cart_line['id']).sale_price(iso_code)
                ))
            db.session.commit()
            # load the newly populated cart
            flash("Cart was successfully saved", 'success')
            cart = Order.cart().filter_by(user_id=current_user.id).first()
            return "Success"
        flash("Unable to save your cart", 'info')
        return "Failed"

    @login_required
    def store_admin(self, store_name):
        # get the current store object
        store = Store.query.filter_by(name=store_name).first()
        if (not store) or (store.user.id != current_user.id):
            # Will be handled appropriately later. Just control access for now
            abort(Response('''It seems either you don't possess access or
                        you've input a wrong address'''))
        store_form = self.StoreRegisterForm()
        account_form = self.AccountForm()
        if store_form.validate_on_submit():
            # Changing the store detail
            store.name = store_form.name.data
            store.about = store_form.about.data
            store.iso_code = store_form.iso_code.data
            store.phone = store_form.phone.data
            store.email = store_form.email.data
            if store_form.logo.data:
                store.logo = store_form.logo.data.read()
            store.user_id = current_user.id
            db.session.commit()
            flash('Store details: succesfully edited', 'success')
            return redirect(url_for('marketplace.store_admin', store_name=store.name))

        if account_form.validate_on_submit():
            # Create or edit a account detail
            if not store.account:
                account = AccountDetail(
                    account_name=account_form.account_name.data,
                    account_num=account_form.account_num.data,
                    bank=account_form.bank.data,)
                store.account = account
            else:
                # The store owner is trying to change the attached account
                store.account.account_name = account_form.account_name.data
                store.account.account_num = account_form.account_num.data
                store.account.bank = account_form.bank.data
            db.session.commit()
            flash('Your account has been edited', 'success')
            return redirect(url_for('marketplace.store_admin', store_name=store.name))

        # Pre-populating the form
        store_form.name.data = store.name
        store_form.about.data = store.about
        store_form.iso_code.data = store.iso_code
        store_form.logo.data = store.logo
        store_form.phone.data = store.phone
        store_form.email.data = store.email
        print(store.account)
        # New stores don't posses account details
        # if store.account:
        account_form.account_name.data = store.account.account_name
        account_form.account_num.data = store.account.account_num
        account_form.bank.data = store.account.bank

        return render_template('marketplace/store_admin.html',
                               store_form=store_form,
                               account_form=account_form)

    def store_new(self, name=None):
        if request.method == 'POST':
            if not name:
                name = current_app.config['DEFAULT_STORE_NAME']
            dispatcher = db.session.query(
                Dispatcher).order_by(db.func.random()).first().id
            store = Store(name=name, about='Give your store a short Description',
                          iso_code='USD', dispatcher_id=dispatcher, user_id=current_user.id,
                          phone='e.g. 08123456789', email='e.g. abc@gmail.com')
            db.session.add(store)
            db.session.commit()
            return {'redirect': url_for('marketplace.store_admin', store_name=name)}
        return render_template('marketplace/store_new.html')

    def store_product(self, store_name):
        # List the products
        store = Store.query.filter_by(name=store_name).first()
        print(store.account)
        prod_list = Product.query.filter_by(store_id=store.id).all()
        return render_template('marketplace/market.html',
                               products=prod_list,
                               iso_code=request.cookies.get('iso_code'))

    def store_product_admin(self, store_name):
        # get the current store object
        store = Store.query.filter_by(name=store_name).first()
        if store and (store.user.id == current_user.id):
            prod = Product.query.get(request.args.get('id'))
            prod_form = self.ProductForm()
            if prod:
                if prod.store_id == store.id:
                    # Permitted to edit this product
                    if prod_form.validate_on_submit():
                        # Changing the store detail
                        prod.name = prod_form.name.data
                        prod.description = prod_form.description.data
                        prod.price = prod_form.price.data
                        prod.image = prod_form.image.data.read()
                        prod.is_active = prod_form.is_active.data
                        prod.store_id = store.id
                        db.session.commit()
                        flash('Product edited succesfully', 'success')
                    else:
                        prod_form.name.data = prod.name
                        prod_form.description.data = prod.description
                        prod_form.price.data = prod.price
                        prod_form.is_active.data = prod.is_active
                        return render_template('marketplace/product.html',
                                               product_form=prod_form)
                else:
                    flash("Unable to edit product", 'danger')
                return redirect(url_for('marketplace.store_product', store_name=store_name))
            if prod_form.validate_on_submit():
                db.session.add(Product(
                    name=prod_form.name.data,
                    description=prod_form.description.data,
                    price=prod_form.price.data,
                    image=prod_form.image.data.read(),
                    is_active=prod_form.is_active.data,
                    store_id=store.id)
                )
                db.session.commit()
                flash('Product created successfully', 'success')
                # List the products
                return redirect(url_for('marketplace.store_product', store_name=store_name))
            return render_template('marketplace/product.html', product_form=prod_form, currency=store.iso_code)
        else:
            flash('Access Error', 'danger')
            return redirect(url_for('marketplace.market'))

