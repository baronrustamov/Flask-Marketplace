''' Defination of all shop views in `shop` blueprint '''
from flask import render_template, Blueprint

# ---------- Declaring the blueprint ----------
shop = Blueprint('shop', __name__, template_folder="templates")


# -------- Endpoints -------------------------------------------------
@shop.route('/')
def index():
    return render_template('index.html')
