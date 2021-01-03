

from flask import render_template, flash, redirect, url_for, request, jsonify, session, send_from_directory
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, SearchBookForm, DonateBookForm, SearchISBNForm, ReserveBookForm, WishBookForm, ManageBookForm, ManageDetailsForm, ManageUserForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Books, Branch, BookItem, Transactions, BookCondition
from werkzeug.urls import url_parse
from app.email import send_password_reset_email, send_reservation_email, send_donation_email, send_registration_email, send_transaction_email
from app.getBookByISBN import getISBNInfo
from sqlalchemy import func
import os


# Default Home Page. It shows all the branch information.
@app.route('/')
@app.route('/index')
def index():
    outputData = []
    outputData = Branch.query.all()
    wishlistData = []
    # outputData = Books.query.filter_by(isbn = isbn).all()
    wishlistData = Books.query.join(BookItem, BookItem.book_id == Books.book_id).add_columns(Books.isbn, Books.title, Books.author).filter(BookItem.status == 'WISHED').all()
    
    return render_template('index.html', title='Home', outputData=outputData, wishlistData=wishlistData)

# Login Page. Validates the login credentials.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        session.permanent = True
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

# Logout Page.
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# User Home Page. Shown to user once they login.
# Displays the recent 3 transactions and user profile information
@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    outputData = []
    outputData = User.query.get(current_user.id)
    transactions =[]
    # Table joins are requires to get the details and replace the ids
    transactions = Transactions.query.join(BookItem, BookItem.book_item_id == Transactions.book_item_id).join(Books, Books.book_id == BookItem.book_id).add_columns(Transactions.transaction_id, Books.title, Transactions.transaction_type, Transactions.transaction_date, Transactions.award_points).filter(Transactions.transaction_account == current_user.id).order_by(Transactions.transaction_date.desc()).limit(3)

    sumpoints = Transactions.query.with_entities(func.sum(Transactions.award_points).label('total')).filter(Transactions.transaction_account == current_user.id).first().total

    form = ManageUserForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Your account details have been updated')
        return redirect(url_for('login'))
    return render_template('results.html', transactions=transactions, outputData=outputData, totalpoints = sumpoints, form=form)

# User Registration. Shown to user for registration.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Save user data
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_registration_email(user)
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
        publisher = form.publisher.data
        
        grade = request.form['grade']
        subject = request.form['subject']
        examboard = request.form['examboard']
        branch = request.form['location']
        condition = request.form['condition']

        # When dropdown isnt selected, it sends None. Need to blank it 
        if str(grade) == '__None':
            grade = ''
        if str(subject) == '__None':
            subject = ''
        if str(examboard) == '__None':
            examboard = ''
        if str(condition) == '__None':
            condition = ''

        retvalue = isbn + '::' + title + '::' + author + '::' + str(grade) + '::' + str(subject) + '::' + str(examboard) + '::' + publisher + '::' + str(branch) + '::' + str(condition)

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
    inputbranch = inputdata.split("::")[7]
    inputcondition = inputdata.split("::")[8]

    outputData = []
    # outputData = Books.query.filter_by(isbn = isbn).all()
    query = Books.query.join(BookItem, BookItem.book_id == Books.book_id).join(Branch, Branch.branch_id == BookItem.branch_id).join(BookCondition, BookCondition.id == BookItem.condition).add_columns(Books.isbn, Books.title, Books.author, BookCondition.condition, Branch.branch_name, Branch.city, BookItem.book_item_id).filter(BookItem.status == 'AVAILABLE')

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
        query = query.filter(Books.grade == inputgrade)
    if inputsubject:
        query = query.filter(Books.subject == inputsubject)
    if inputexamboard:  
        query = query.filter(Books.examboard == inputexamboard)
    if inputcondition:
        query = query.filter(BookItem.condition == inputcondition)
    if inputbranch:  
        query = query.filter(BookItem.branch_id == inputbranch)
    if inputpublisher:
        search = "%{}%".format(inputpublisher)    
        query = query.filter(Books.publisher.like(search))

    outputData = query.limit(25)

    if not outputData:
        flash('Sorry, No books found for you search conditions. Please search again')
        return redirect('/search')
        # use response to populate reservation page
    
    form = ReserveBookForm()

    if form.validate_on_submit():
        selected_book_item_id = request.form['chosenoption']
        bookitem = BookItem.query.filter_by(book_item_id = selected_book_item_id).first()
        bookitem.status = 'RESERVED'
        db.session.commit()

        transaction = Transactions(book_item_id=selected_book_item_id, transaction_account=current_user.id, transaction_type = 'RESERVE', award_points = 0)
        db.session.add(transaction)
        db.session.commit()

        # send_reservation_email
        user = User.query.filter_by(id=current_user.id).first()
        reservation_details = BookItem.query.join(Branch, Branch.branch_id == BookItem.branch_id).join(Books, Books.book_id == BookItem.book_id).add_columns(Books.title,Branch.branch_name, Branch.city).filter(BookItem.book_item_id == selected_book_item_id).first()

        send_reservation_email(user, transaction, reservation_details)
        flash('Congratulations, you have reserved the book! ')
        return redirect(url_for('results'))
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

    if form.validate_on_submit():
        # check if book already exists in Books
        outputData = Books.query.filter_by(isbn=form.isbn.data).all()
        if not outputData:
            # if not, save into Books
            grade = request.form['grade']
            subject = request.form['subject']
            examboard = request.form['examboard']

            # When dropdown isnt selected, it sends None. Need to blank it 
            if str(grade) == '__None':
                grade = ''
            if str(subject) == '__None':
                subject = ''
            if str(examboard) == '__None':
                examboard = ''

            book = Books(title=form.title.data, author=form.author.data, isbn=form.isbn.data, grade=grade, subject=subject, publisher=form.publisher.data, examboard=examboard)
            db.session.add(book)
            db.session.commit()
            bi_book_id = book.book_id
            send_book_title = form.title.data
        else:
            # otherwise get the book id, to be used while saving bookitem
            bi_book_id = outputData[0].book_id
            send_book_title = outputData[0].title

        promise_date = form.planned_date.data
        selected_location = request.form['location']
        # Save into BookItem
        book_item = BookItem(book_id=bi_book_id, status='DONATED', branch_id=selected_location, promise_date= promise_date)
        db.session.add(book_item)
        db.session.commit()
        bi_book_item_id = book_item.book_item_id
        
        # Save into Transactions
        transaction = Transactions(book_item_id=bi_book_item_id, transaction_account=current_user.id, transaction_type = 'DONATION', award_points = 0)
        db.session.add(transaction)
        db.session.commit()

        # send_donation_email
        user = User.query.filter_by(id=current_user.id).first()
        branch = Branch.query.filter_by(branch_id=selected_location).first()
        send_donation_email(user, send_book_title, transaction, branch)
        flash('Congratulations, you have donated the book!')
        return redirect(url_for('results'))
    return render_template('donate.html', title='Donate',form=form)

@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    form = ManageBookForm()
    if form.validate_on_submit():
        transactionid=form.transactionid.data
        return redirect(url_for('managedetails', inputdata = transactionid)) 
    return render_template('manage.html', title='Home',form=form)

@app.route('/managedetails/<inputdata>', methods=['GET','POST'])
@login_required
def managedetails(inputdata):
    outputData = []
    outputData = Transactions.query.join(BookItem, BookItem.book_item_id == Transactions.book_item_id).join(Branch, Branch.branch_id == BookItem.branch_id).join(User, User.id == Transactions.transaction_account).join(Books, Books.book_id == BookItem.book_id).add_columns(Books.isbn, Books.title, Books.author, Branch.branch_name, Branch.city, BookItem.book_item_id, Transactions.transaction_type, User.id).filter(Transactions.transaction_id == inputdata).first()
    if not outputData:
        flash('No results found for this transaction id!')
        return redirect('/manage')
    else:
        form = ManageDetailsForm()
        if outputData.transaction_type == 'DONATION':
            new_status = 'AVAILABLE'
            new_transaction_type = 'DEPOSIT'

        if outputData.transaction_type == 'RESERVE':
            new_status = 'ISSUED'
            new_transaction_type = 'ISSUE'

        print(form.errors)

        if form.is_submitted():
            print('submitted')

        if form.validate():
            print ('valid')

        print(form.errors)

        if form.validate_on_submit():
            selected_book_item_id = request.form['chosenoption']
            bookitem = BookItem.query.filter_by(book_item_id = selected_book_item_id).first()
            if outputData.transaction_type == 'DONATION':
                bookitem.condition = request.form['condition']
            bookitem.status = new_status
            db.session.commit()

            transaction = Transactions.query.filter_by(transaction_id = inputdata).first()
            transaction.transaction_type = new_transaction_type
            transaction.award_points = 10
            db.session.commit()

            # send_transaction_email
            user = User.query.filter_by(id=outputData.id).first()
            transid = inputdata
            send_transaction_email(user, transid)
            return redirect(url_for('results'))
    return render_template('managedetails.html', outputData=outputData,form=form)

@app.route('/getISBNDetails', methods=['POST'])
def isbn_details():
    return jsonify({'text': getISBNInfo(request.form['isbn'])})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/wish', methods=['GET', 'POST'])
@login_required
def wish():
    form = SearchISBNForm()
    if form.validate_on_submit():
        outputData = []
        outputData = getISBNInfo(request.form['isbn'])
        if not outputData:
            flash('No results found!')
            return redirect('/wish')
        else:
        # use response to populate donation page
            return redirect(url_for('wishdetails', indata = outputData))
    return render_template('wishbook.html', title='SearchBook',form=form)

@app.route('/wishdetails', methods=['GET', 'POST'])
@login_required
def wishdetails():
    form = WishBookForm()
    # use response to populate donation page
    inputdata = request.args.get("indata")
    form.title.data = inputdata.split("::")[0]
    form.author.data = inputdata.split("::")[1]
    form.isbn.data = inputdata.split("::")[2]

    if form.validate_on_submit():
        # check if book already exists in Books
        outputData = Books.query.filter_by(isbn=form.isbn.data).all()
        if not outputData:
            book = Books(title=form.title.data, author=form.author.data, isbn=form.isbn.data)
            db.session.add(book)
            db.session.commit()
            bi_book_id = book.book_id
        else:
            # otherwise get the book id, to be used while saving bookitem
            bi_book_id = outputData[0].book_id
        
        # Save into BookItem
        book_item = BookItem(book_id=bi_book_id, status='WISHED')
        db.session.add(book_item)
        db.session.commit()
        bi_book_item_id = book_item.book_item_id
        
        # Save into Transactions
        transaction = Transactions(book_item_id=bi_book_item_id, transaction_account=current_user.id, transaction_type = 'WISH', award_points = 0)
        db.session.add(transaction)
        db.session.commit()

        # TO-DO: send_donation_email 
        flash('Congratulations, you have added the book to your wishlist!')
        return redirect(url_for('results'))
    return render_template('wish.html', title='Donate',form=form)

