from flask_mail import Message
from app import mail, app
from flask import render_template
from threading import Thread

def send_registration_email(user):
    send_email('[Book Depository] Welcome to Berkshire Depository',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/welcome_email.txt',
                                         user=user),
               html_body=render_template('email/welcome_email.html',
                                         user=user))

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Book Depository] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_reservation_email(user, transaction, reservation_details):
    send_email('[Book Depository] Your reservation details are enclosed',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reservation.txt',
                                         user=user, transaction = transaction, reservation_details = reservation_details),
               html_body=render_template('email/reservation.html',
                                         user=user, transaction = transaction, reservation_details = reservation_details))

def send_donation_email(user, send_book_title, transaction, branch):
    send_email('[Book Depository] Thanks for your donation',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/donation.txt',
                                         user=user, send_book_title = send_book_title, transaction = transaction, branch = branch),
               html_body=render_template('email/donation.html',
                                         user=user, send_book_title = send_book_title, transaction = transaction, branch = branch))


def send_transaction_email(user, transid):
    send_email('[Book Depository] Thanks for completing the transaction',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/transaction.txt', 
                                        user=user, transid = transid),
               html_body=render_template('email/transaction.html',
                                        user=user, transid = transid))

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
