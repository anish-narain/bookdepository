from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login, app
from flask_login import UserMixin
from time import time
import jwt
from sqlalchemy import Integer


class Transactions(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    book_item_id = db.Column(db.Integer, db.ForeignKey('bookitem.book_item_id'))
    transaction_account = db.Column(db.Integer, db.ForeignKey('user.id'))
    transaction_type = db.Column(db.String(30))
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    award_points = db.Column(db.Integer)

    def __repr__(self):
        return '<Transactions {}>'.format(self.transaction_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_user = db.Column(db.Boolean, nullable=True, default=True)
    transactions = db.relationship('Transactions',
                                   foreign_keys=[Transactions.transaction_account],
                                   backref=db.backref('userb', lazy='joined'),
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Branch(db.Model):
    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(120))
    city = db.Column(db.String(60))
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(60))
    contact_person = db.Column(db.String(60))
    items = db.relationship('BookItem', backref='item', lazy='dynamic')

    def __repr__(self):
        return '<Branch {}>'.format(self.branch_id)

    def __str__(self):
        return self.branch_name + ', ' + self.city
    


class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(30), index=True, unique=True)
    title = db.Column(db.String(120), index=True)
    author = db.Column(db.String(120), index=True)
    grade = db.Column(db.String(30))
    examboard = db.Column(db.String(30))
    publisher = db.Column(db.String(120))
    subject = db.Column(db.String(30))
    items = db.relationship('BookItem', backref='book', lazy='dynamic')

    def __repr__(self):
        return '<Books {}>'.format(self.book_id)


class BookItem(db.Model):
    __tablename__ = "bookitem"
    book_item_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    status = db.Column(db.String(30))
    acquisition_date = db.Column(db.Date)
    promise_date = db.Column(db.Date)
    condition = db.Column(db.String(30))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'))
    transactions = db.relationship('Transactions',
                                   foreign_keys=[Transactions.book_item_id],
                                   backref=db.backref(
                                       'bookite', lazy='joined'),
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')

    def __repr__(self):
        return '<BookItem {}>'.format(self.book_item_id)


class NotificationTemplate(db.Model):
    template_id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(60))
    template_text = db.Column(db.String(3000))

    def __repr__(self):
        return '<NotificationTemplate {}>'.format(self.template_name)

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(255))

class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255))

class Boards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board = db.Column(db.String(255))

class BookCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(255))