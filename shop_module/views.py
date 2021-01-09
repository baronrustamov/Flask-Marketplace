''' Defination of all shop views in `shop` blueprint '''
from requests import get
from flask import Blueprint, flash, make_response, redirect, \
    render_template, request, url_for
from flask_login import current_user, login_required
from flask import Response, stream_with_context

from factory import db
from .models import AccountDetail, Currency, Dispatcher, \
    Order, OrderLine, Product, Store
from . import utilities
from users_module.forms import ExtendedRegisterForm
from.forms import StoreRegisterForm
# ---------- Declaring the blueprint ----------
shop = Blueprint('shop', __name__, template_folder='templates')


@shop.before_request
def before_request():
    ''' Make sure that the currency is always known '''
    if not(request.cookies.get('iso_code')):
        response = make_response(redirect(request.path))
        code = get('https://ipapi.co/currency/').text
        if not((code,) in Currency.query.with_entities(Currency.code).all()):
            code = 'USD'
        response.set_cookie('iso_code', code, samesite='None')
        return response


@shop.route('/')
def index():
    return render_template('home.html')


@shop.route('/cart', methods=['GET'])
@login_required
def cart():
    iso_code = request.cookies.get('iso_code')
    prod_str = request.args.get('prod_id')
    # Check if the current user has an hanging cart
    cart = Order.cart().filter_by(user_id=current_user.id).first()
    if prod_str:
        # ---- The user is adding a product to cart ------
        prod_id = int(prod_str)
        # Get the selected product detail
        cart_line = Product.public().filter_by(id=prod_id).first()
        if cart:
            # Check if this product already exist in the cart
            prev_prod_line = db.session.query(OrderLine).filter_by(
                order_id=cart.id, product_id=prod_id).first()
            if prev_prod_line:
                # Add one to the quantity of this product
                prev_prod_line.qty += 1
            else:
                # Include this product in the previous cart
                db.session.add(OrderLine(order_id=cart.id,
                                         product_id=cart_line.id,
                                         price=cart_line.price,))
        else:
            # Create a new cart and add this product
            cart = Order(user_id=current_user.id,
                         iso_code=iso_code)
            db.session.add(cart)
            # I am yet to figure out a sensible way of defferring this commit
            db.session.commit()
            db.session.add(OrderLine(order_id=cart.id,
                                     product_id=cart_line.id,
                                     price=cart_line.price,))
        db.session.commit()
        return redirect('/cart')
    if cart:
        cart = OrderLine.query.filter_by(order_id=cart.id).all()
    return render_template('cart.html', cart=cart)


@shop.route('/checkout', methods=['GET'])
@login_required
def checkout():
    iso_code = request.cookies.get('iso_code')
    # Get the last hanging cart
    cart_lines = None
    cart = Order.cart().filter_by(user_id=current_user.id).first()
    if cart:
        cart_lines = OrderLine.query.filter_by(order_id=cart.id).all()
        # For security reason, let's update all the order line prices again
        for line in db.session.query(OrderLine).filter_by(order_id=1).all():
            line.price = line.product.sale_price(iso_code)
        db.session.commit()  # To ensure the update figures are picked up
    # Get the publisher of the cart products, sum total, and qty total
    store_value = db.session.query(
        Product.store_id.label('store_id'),
        db.func.sum(OrderLine.qty * OrderLine.price).label('store_sum'),
        db.func.sum(OrderLine.qty).label('qty_sum').label('qty_sum'),
    ).join(Product).filter(OrderLine.order_id == cart.id).group_by(
        Product.store_id).subquery()
    # All other payment data are related to the store
    pay_data = db.session.query(
        Store, store_value.c.store_sum,
        store_value.c.qty_sum).join(
        store_value, Store.id == store_value.c.store_id).all()
    # Compute amounts
    store_value = utilities.amounts_sep(iso_code, pay_data)
    return render_template('checkout.html', cart=cart_lines,
                           store_value=store_value,
                           pay_data=pay_data)


@shop.route('/market', methods=['GET'])
def market():
    iso_code = request.cookies.get('iso_code')
    products = Product.public()
    return render_template('market.html', products=products,
                           iso_code=iso_code)


@shop.route('/img/product/<int:id>', methods=['GET'])
def product_img(id):
    product = Product.query.get_or_404(id)
    return Response(product.image, mimetype='image/jpg')


@shop.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@shop.route('/store/new', methods=['GET', 'POST'])
@login_required
def store_new():
    form = StoreRegisterForm(request.form)
    print(request.method)
    print(form.validate())
    print(form.logo.data)
    if form.validate_on_submit():
        # We want to randomly fix a store to a dispatcher
        print('form validated')
        dispatcher = db.session.query(
            Dispatcher).order_by(db.func.random()).first().id
        print(dispatcher)
        print(form.account_name.data)
        account = AccountDetail(account_name=form.account_name.data,
                                account_num=form.account_num.data,
                                bank_name=form.bank_name.data)
        store = Store(name=form.name.data,
                      about=form.about.data,
                      iso_code=form.iso_code.data,
                      logo=form.logo.data,
                      dispatcher_id=dispatcher,
                      user_id=current_user.id,
                      account=account)
        db.session.add(account)
        db.session.add(store)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('.index'))
    return render_template('store_new.html', form=form)


@shop.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
