import json
import requests
from flask_babel import _
from app import app

def getISBNInfo(isbn_input):
    reqstring = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'+ isbn_input
    r = requests.get(reqstring)
    if r.status_code != 200:
        return 'Error: the ISBN service failed.'
    
    count = int(r.json()['totalItems'])
    if count > 0:   
        title = r.json()['items'][0]['volumeInfo']['title']
        author = r.json()['items'][0]['volumeInfo']['authors'][0]
        isbn = isbn_input
        return title + '::' + author + '::' + isbn
    else:
        return 'Error: No Data Found for this ISBN.'