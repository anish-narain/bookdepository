

from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, SearchBookForm, DonateBookForm, SearchISBNForm, ReserveBookForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Books, Branch, BookItem, Transactions
from werkzeug.urls import url_parse
from app.email import send_password_reset_email, send_reservation_email, send_donation_email
from flask import jsonify
from app.getBookByISBN import getISBNInfo
from sqlalchemy.exc import IntegrityError

@app.route('/')
@app.route('/index')
def index():
    outputData = []
    outputData = Branch.query.all()
    return render_template('index.html', title='Home', outputData=outputData)
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
            next_page = url_for('results')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/results')
def results():
    outputData = []
    outputData = User.query.get(current_user.id)
    transactions =[]
    # transactions = outputData.transactions.filter_by(transaction_account = current_user.id).all()
    transactions = Transactions.query.join(BookItem, BookItem.book_item_id == Transactions.book_item_id).join(Books, Books.book_id == BookItem.book_id).add_columns(Transactions.transaction_id, Books.title, Transactions.transaction_type, Transactions.transaction_date, Transactions.award_points).filter(Transactions.transaction_account == current_user.id).order_by(Transactions.transaction_date.desc()).limit(3)

    if not outputData:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', transactions=transactions, outputData=outputData)

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
@login_required
def search():
    form = SearchBookForm()
    if form.validate_on_submit():
        isbn = form.isbn.data
        title = form.title.data 
        author = form.author.data
        grade = form.grade.data 
        subject = form.subject.data 
        examboard = form.examboard.data
        publisher = form.publisher.data
        
        if str(grade) == 'None':
            grade = ''

        if str(subject) == 'None':
            subject = ''

        if str(examboard) == 'None':
            examboard = ''

        retvalue = isbn + '::' + title + '::' + author + '::' + str(grade) + '::' + str(subject) + '::' + str(examboard) + '::' + publisher

        return redirect(url_for('searchdetails', inputdata = retvalue))   
    return render_template('search.html', title='SearchBook',form=form)

@app.route('/searchdetails/<inputdata>', methods=['GET','POST'])
@login_required
def searchdetails(inputdata):
    inputisbn = inputdata.split("::")[0]
    inputtitle = inputdata.split("::")[1]
    inputauthor = inputdata.split("::")[2]
    inputgrade = inputdata.split("::")[3]
    inputsubject = inputdata.split("::")[4]
    inputexamboard = inputdata.split("::")[5]
    inputpublisher = inputdata.split("::")[6]

    outputData = []
    # outputData = Books.query.filter_by(isbn = isbn).all()
    query = Books.query.join(BookItem, BookItem.book_id == Books.book_id).join(Branch, Branch.branch_id == BookItem.branch_id).add_columns(Books.isbn, Books.title, Books.author, BookItem.status, Branch.branch_name, Branch.city, BookItem.book_item_id)


    if inputisbn:
        search = "%{}%".format(inputisbn)
        query = query.filter(Books.isbn.like(search))
    if inputtitle:
        search = "%{}%".format(inputtitle)
        query = query.filter(Books.title.like(search))
    if inputauthor:
        search = "%{}%".format(inputauthor)    
        query = query.filter(Books.author.like(search))
    if inputgrade:
        search = "%{}%".format(inputgrade)
        query = query.filter(Books.grade.like(search))
    if inputsubject:
        search = "%{}%".format(inputsubject)
        query = query.filter(Books.subject.like(search))
    if inputexamboard:
        search = "%{}%".format(inputexamboard)    
        query = query.filter(Books.examboard.like(search))
    if inputpublisher:
        search = "%{}%".format(inputpublisher)    
        query = query.filter(Books.publisher.like(search))

    outputData = query.all()

    form = ReserveBookForm()
    if not outputData:
        flash('Sorry, No books found for you search conditions. Please search again')
        return redirect('/search')
        # use response to populate reservation page
    print('lets get the itemid:')
    print(form.errors)

    if form.is_submitted():
        print('submitted')

    if form.validate():
        print ('valid')

    print(form.errors)

    if form.validate_on_submit():
        selected_book_item_id = 1
        print('itemid:' + str(selected_book_item_id))
        bookitem = BookItem.query.filter_by(book_item_id = selected_book_item_id).first()
        bookitem.status = 'RESERVED'

        transaction = Transactions(book_item_id=selected_book_item_id, transaction_account=current_user.id, transaction_type = 'RESERVE', award_points = 0)
        db.session.add(transaction)
        db.session.commit()
        # TO-DO: send_reservation_email 
        flash('Congratulations, you have reserved the book! ' + str(transaction.transaction_id))
        return redirect(url_for('index'))
    return render_template('reserve.html', outputData=outputData,form=form)

@app.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    form = SearchISBNForm()
    if form.validate_on_submit():
        outputData = []
        outputData = getISBNInfo(request.form['isbn'])
        if not outputData:
            flash('No results found!')
            return redirect('/')
        else:
        # use response to populate donation page
            return redirect(url_for('donatedetails', indata = outputData))
    return render_template('searchbook.html', title='SearchBook',form=form)

@app.route('/donatedetails', methods=['GET', 'POST'])
@login_required
def donatedetails():
    form = DonateBookForm()
    # use response to populate donation page
    inputdata = request.args.get("indata")
    form.title.data = inputdata.split("::")[0]
    form.author.data = inputdata.split("::")[1]
    form.isbn.data = inputdata.split("::")[2]

    # save the actual provided values
    grade = form.grade.data
    subject = form.subject.data
    examboard = form.examboard.data

    if str(grade) == 'None':
        grade = ''

    if str(subject) == 'None':
        subject = ''

    if str(examboard) == 'None':
        examboard = ''

    if form.validate_on_submit():
        outputData = Books.query.filter_by(isbn=form.isbn.data).all()
        print('check outputdata')
        if not outputData:
            print('not outputdata')
            book = Books(title=form.title.data, author=form.author.data, isbn=form.isbn.data, grade=grade, subject=subject, publisher=form.publisher.data, examboard=examboard)
            db.session.add(book)
            db.session.commit()
            bi_book_id = book.book_id
        else:
            # TO-DO: remove hardcoding
            bi_book_id = outputData[0].book_id
        
        # TO-DO: remove hardcoding
        print('location' + str(form.location.data))
        book_item = BookItem(book_id=bi_book_id, status='PROMISED', branch_id=1 )
        db.session.add(book_item)
        db.session.commit()
        # TO-DO: send_donation_email 
        flash('Congratulations, you have donated the book!')
        return redirect(url_for('index'))
    return render_template('donate.html', title='Donate',form=form)


@app.route('/manage', methods=['GET', 'POST'])
@login_required
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