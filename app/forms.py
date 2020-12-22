from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

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
    grade = SelectField('Year', choices=[('', ''), ('Eight', 'Eight'), ('Nine', 'Nine'),
    ('Ten', 'Ten'), ('Eleven', 'Eleven'), ('Twelve', 'Twelve'),
    ('Thirteen', 'Thirteen'), ('Primary', 'Primary'), ('College', 'College')])
    subject = SelectField('Subject', choices=[('', ''), 
    ('History', 'History'), ('Maths', 'Maths'), ('Physics', 'Physics'), 
    ('English', 'English'), ('Biology', 'Biology'), ('Chemistry', 'Chemistry')])
    examboard = SelectField('Board', choices=[('', ''),('OCR', 'OCR'), ('AQA', 'AQA')])
    publisher = StringField('Publisher')
    submit = SubmitField('Donate Book')

class ManageBookForm(FlaskForm):
    transactionid = StringField('TransactionId')
    submit = SubmitField('Get Details')

class SearchBookForm(FlaskForm):
    title = StringField('Title')
    isbn = StringField('ISBN')
    author = StringField('Author')
    grade = SelectField('Year', choices=[('', ''), ('Eight', 'Eight'), ('Nine', 'Nine'),
    ('Ten', 'Ten'), ('Eleven', 'Eleven'), ('Twelve', 'Twelve'),
    ('Thirteen', 'Thirteen'), ('Primary', 'Primary'), ('College', 'College')])
    subject = SelectField('Subject', choices=[('', ''), 
    ('History', 'History'), ('Maths', 'Maths'), ('Physics', 'Physics'), 
    ('English', 'English'), ('Biology', 'Biology'), ('Chemistry', 'Chemistry')])
    examboard = SelectField('Board', choices=[('', ''),('OCR', 'OCR'), ('AQA', 'AQA')])
    publisher = StringField('Publisher')
    submit = SubmitField('Search Book')

class ReserveBookForm(FlaskForm):
    title = StringField('Title')
    isbn = StringField('ISBN')
    author = StringField('Author')
    submit = SubmitField('Reserve Book')



