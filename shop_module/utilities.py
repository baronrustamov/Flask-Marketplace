from requests import get

from flask import make_response, redirect, request, render_template

def currency(destination):
    iso_code = request.cookies.get('iso_code')
    if not(iso_code):
        response = make_response(render_template('index.html'))
        iso_code = get('https://ipapi.co/currency/').text
        print('Just got code')
        response.set_cookie('iso_code', iso_code)
        return response
    return iso_code
