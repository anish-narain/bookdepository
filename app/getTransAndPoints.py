import json
import requests
from flask_babel import _
from app import app

def getTransAndPoints(account_id):

    q = Session.query(
         Books, Transactions, Awards,
    ).filter(
        Awards.account_id == account_id,
    ).filter(
        Awards.transaction_id == Transactions.transaction_id,
    ).filter(
        Transactions.book_id == Book.book_id
    ).all()


    reqstring = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'+ isbn_input
    r = requests.get(reqstring)
    if r.status_code != 200:
        return _('Error: the ISBN service failed.')
    
    count = int(r.json()['totalItems'])
    if count > 0:   
        title = r.json()['items'][0]['volumeInfo']['title']
        author = r.json()['items'][0]['volumeInfo']['authors'][0]
        isbn = isbn_input
        return title + '::' + author + '::' + isbn
    else:
        return _('Error: No Data Found for this ISBN.')