''' Defination of all shop views in `shop` blueprint '''
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from factory import db
from .models import Currency, Order, OrderLine, Product, Store

# ---------- Declaring the blueprint ----------
shop = Blueprint('shop', __name__, template_folder="templates")


@shop.route('/')
def index():
    return render_template('index.html')


@shop.route('/cart', methods=['GET'])
@login_required
def cart():
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
            cart = Order(user_id=current_user.id)
            db.session.add(cart)
            # I am yet to figure out a sensible way of defferring this commit
            db.session.commit()
            db.session.add(OrderLine(order_id=cart.id,
                                     product_id=cart_line.id,
                                     price=cart_line.price,))
        db.session.commit()
    
    if cart:
        cart = OrderLine.query.filter_by(order_id=cart.id).all()
    print(cart)
    return render_template('cart.html', cart=cart)
