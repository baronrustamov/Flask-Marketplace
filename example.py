'''
Minimal implentation
'''
from Flask_Marketplace import marketplace

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    marketplace(app).run(port=6060, host='0.0.0.0', debug=True)