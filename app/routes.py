

from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, SearchBookForm, DonateBookForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Books, Branch, BookItem, Transactions, AwardPoints
from werkzeug.urls import url_parse
from app.email import send_password_reset_email
from flask import jsonify
from app.getBookByISBN import getISBNInfo

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/results')
def results():
    outputData = []
    outputData = User.query.all()
    if not outputData:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', outputData=outputData)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchBookForm()
    if form.validate_on_submit():
        # return jsonify({'text': getISBNInfo(request.form['isbn'])})
        outputData = []
        outputData = getISBNInfo(request.form['isbn'])
        # print(outputData)
        if not outputData:
            flash('No results found!')
            return redirect('/')
        else:
        # display results
            # print('in else, going to render')
            # return render_template('booksearchresults.html', outputData=outputData)
            return redirect(url_for('donate', indata = outputData))
    return render_template('searchbook.html', title='SearchBook',form=form)

@app.route('/donate/<indata>', methods=['GET', 'POST'])
def donate(indata):
    form = DonateBookForm()
    form.title.data = indata.volumeInfo.title
    if form.validate_on_submit():
        book = Books(title=form.title.data, author=form.author.data, isbn=form.isbn.data
        ,grade=form.grade.data, subject=form.subject.data, publisher=form.publisher.data, examboard=form.examboard.data)
        db.session.add(book)
        db.session.commit()
        flash('Congratulations, you have donated the book!')
        return redirect(url_for('index'))
    return render_template('donate.html', title='Donate',form=form)


@app.route('/manage', methods=['GET', 'POST'])
def manage():
    form = DonateBookForm()
    if form.validate_on_submit():
        book = Books(title=form.title.data, author=form.author.data, isbn=form.isbn.data)
        db.session.add(book)
        db.session.commit()
        flash('Congratulations, you have donated the book!')
        return redirect(url_for('index'))
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/getISBNDetails', methods=['POST'])
def isbn_details():
    return jsonify({'text': getISBNInfo(request.form['isbn'])})