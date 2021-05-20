'''
This file may by called:
  - Directly during developement or
  - The WSGI during production
'''
import os
import sys


if __name__ == '__main__':
    from flask import Flask
    from . import marketplace
    app = Flask(__name__)
    marketplace(app).run(port=6060, host='0.0.0.0', debug=True)
