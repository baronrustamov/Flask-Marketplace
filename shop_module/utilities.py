from requests import get

from flask import make_response, redirect, request

def currency(destination):
    if not(request.cookies.get('iso_code')):
        response = make_response(redirect('destination'))
        iso_code = get('https://ipapi.co/currency/').text
        # print(iso_code)
        response.set_cookie('iso_code', iso_code)
        return response
    return True
