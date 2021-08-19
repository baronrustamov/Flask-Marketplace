"""Minimal implentation of Flask-Markeplace
"""

from Flask_Marketplace import marketplace

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Long hard to guess key'
    marketplace(app).run(port=5001, host='0.0.0.0', debug=False)
