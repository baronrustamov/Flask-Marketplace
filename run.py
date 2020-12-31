'''
This file may by called:
  - Directly during developement or
  - The WSGI during production
'''
import os
from factory import create_app

app = create_app(os.getenv('CONFIG_NAME', default='default'))

if __name__ == '__main__':
    app.run(port=6060, host='0.0.0.0', debug=True)
