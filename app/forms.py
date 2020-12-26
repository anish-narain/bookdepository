from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User, Grades, Subjects, Boards, Branch
from wtforms.fields.html5 import DateField

def get_grades():
    return Grades.query.all()

def get_subjects():
    return Subjects.query.all() 

def get_boards():
    return Boards.query.all() 

def get_locations():
    return Branch.query.all()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class SearchISBNForm(FlaskForm):
    isbn = StringField('ISBN')
    submit = SubmitField('Get ISBN Details')

class DonateBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    isbn = StringField('ISBN')
    author = StringField('Author')
    grade = QuerySelectField('Year', query_factory=get_grades, get_label='grade', allow_blank=True)
    subject = QuerySelectField('Subject', query_factory=get_subjects, get_label='subject', allow_blank=True)
    examboard = QuerySelectField('Board', query_factory=get_boards, get_label='board', allow_blank=True)
    publisher = StringField('Publisher')
    location = QuerySelectField('Branch', query_factory=get_locations)
    planned_date = DateField('Planned Date', format='%Y-%m-%d')
    submit = SubmitField('Donate Book')

class ManageBookForm(FlaskForm):
    transactionid = StringField('TransactionId')
    submit = SubmitField('Get Details')

class SearchBookForm(FlaskForm):
    title = StringField('Title')
    isbn = StringField('ISBN')
    author = StringField('Author')
    grade = QuerySelectField('Year', query_factory=get_grades, get_label='grade', allow_blank=True)
    subject = QuerySelectField('Subject', query_factory=get_subjects, get_label='subject', allow_blank=True)
    examboard = QuerySelectField('Board', query_factory=get_boards, get_label='board', allow_blank=True)
    publisher = StringField('Publisher')
    submit = SubmitField('Search Book')

class ReserveBookForm(FlaskForm):
    chosenoption = RadioField('Options', choices=[('1', '1'), ('2', '2')], default=1, coerce=int)
    submit = SubmitField('Reserve Book')



