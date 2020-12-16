import json
import requests
from flask_babel import _
from app import app

def getISBNInfo(isbn):
    reqstring = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'+ isbn
    r = requests.get(reqstring)
    if r.status_code != 200:
        return _('Error: the ISBN service failed.')
    
    count = int(r.json()['totalItems'])
    if count > 0:   
        book = r.json()['items'][0]
        return book
    else:
        return _('Error: No Data Found for this ISBN.')