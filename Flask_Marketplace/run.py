'''
This file may by called:
  - Directly during developement or
  - The WSGI during production
'''
import os
import sys


if __name__ == '__main__':
    from flask import Flask
    from Flask_Marketplace import marketplace
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Insane L0ng mIxuture 0f Ch@rac7er5"
    marketplace(app).run(port=5001, host='0.0.0.0', debug=False)
