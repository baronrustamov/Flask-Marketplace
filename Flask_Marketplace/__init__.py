"""
Flask-Market is an modular ecommerce flask app.
It can either be used as standalone or as extension to provide marketplace
feature to existing flask applications.

Author: Ewetoye Ibrahim
"""

__author__ = 'Ewetoye Ibrahim'
__version__ = '0.0.7-alpha'

import os, sys
sys.path.append(os.path.dirname(__file__))
from .factory import marketplace
