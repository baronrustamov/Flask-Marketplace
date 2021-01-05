''' Defination of all shop views in `shop` blueprint '''
from requests import get

from flask import Blueprint, make_response, redirect, render_template, request
from flask_login import current_user, login_required

from factory import db
from .models import Currency, Order, OrderLine, Product, Store
from . import utilities
# ---------- Declaring the blueprint ----------
shop = Blueprint('shop', __name__,)


@shop.route('/')
def index():
    if not(request.cookies.get('iso_code')):
        return redirect('/currency_token')
    return render_template('index.html')


@shop.route('/cart', methods=['GET'])
@login_required
def cart():
    iso_code = request.cookies.get('iso_code')
    if not(iso_code):
        return redirect('/currency_token')
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

    if cart:
        cart = OrderLine.query.filter_by(order_id=cart.id).all()
    return render_template('cart.html', cart=cart)


@shop.route('/checkout', methods=['GET'])
@login_required
def checkout():
    iso_code = request.cookies.get('iso_code')
    if not(iso_code):
        return redirect('/currency_token?next=checkout')
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
    # Calculate delivery fee
    shipping = []
    store_total = 0
    for i in range(len(pay_data)):
        shipping_charge = utilities.convert_currency(
            pay_data[i][0].dispatcher.charge,
            pay_data[i][0].iso_code, iso_code) * pay_data[i][2]
        shipping.append(shipping_charge)
        store_total += pay_data[i][1]
    print(pay_data)
    return render_template('checkout.html', cart=cart_lines,
                           store_value=[iso_code, store_total, shipping],
                           pay_data=pay_data)


@shop.route('/currency_token', methods=['GET'])
def currency():
    '''This view duty is simply add iso_code cookie'''
    destination = request.args.get('next') or '/'
    response = make_response(redirect(destination))
    code = request.cookies.get('iso_code')
    if not(code):
        iso_code = get('https://ipapi.co/currency/').text
        response.set_cookie('iso_code', iso_code)
    return response


@shop.route('/market', methods=['GET'])
@login_required
def market():

    return render_template('market.html')
