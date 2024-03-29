Welcome to my NEA project: Book Bank
===========================================

**How to setup on local machine (Mac)**

A. Pre-requisites

    a) Python should be there on machine. Check by typing:

```
~ $ python3
Python 3.7.5 (default, Nov 1 2019, 02:16:32)
[Clang 11.0.0 (clang-1100.0.33.8)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

B. Copy the code from here to local machine and ensure that you change directory to bookrepository. 

C. Create python virtual environment
 ```   
    $ python3 -m venv venv
```

D. Activate the virtual environment
 ```   
    $ source venv/bin/activate
    (venv) $
```
Now you can notice the venv on your command prompt

E. Install flask
```
    (venv) $ pip install flask
```

F. Install all flask dependencies
```
     (venv) $ pip install -r requirements.txt
```

G. Set up the environment variables after editing the setenv.sh file with right values
```
    (venv) $ . ./setenv.sh
```
Everytime you close the terminal window and start afresh, you will have to run steps D and G.

H. Set up the database by running these 3 commands
```
    (venv) $ flask db init
    (venv) $ flask db migrate
    (venv) $ flask db upgrade
```

I. Populate the initial dataset
```
    (venv) $ cat metadata.sql | sqlite3 bookrepo.db
```
J. Quick sanity check before we start running the application

    Your folder structure now should look something like

        (venv) ~/Anish/nea/bookdepository $ ls *
        LICENSE			bookrepo.db		requirements.txt
        README.md		config.py		setenv.sh
        bookdepository.py	metadata.sql		

        __pycache__:
        bookdepository.cpython-37.pyc	config.cpython-37.pyc

        app:
        __init__.py		forms.py		routes.py
        __pycache__		getBookByISBN.py	tables.py
        email.py		models.py		templates

        migrations:
        README		alembic.ini	script.py.mako
        __pycache__	env.py		versions

        venv:
        bin		include		lib		pyvenv.cfg
        (venv) ~/Anish/nea/bookdepository $ 

K. Start the application
```
    (venv) $ flask run
```

L. Access the application on local [browser](http://127.0.0.1:5000)

**To do**

A. General Improvements

    a) Session timeout is not there. ** Done **
    b) Documentation
    c) Remove prints, debug settings ** Done **
    d) Find correct syntax to insert date values **Done**

B. Index Page

    a) Nearest centre?

C. User Profile

    a) Show only last 3 transactions ** Done **
    b) Add total award points ** Done **

D. Search for Reservation

    a) Validations?

E. Reserve

    a) Currently the option list is hardcoded. Generalize it ** Done **
    b) Send reservation email ** Done **
    c) Future dated reservations ** Cant do, change design **
    d) Send email once reserved book is available ** Done**
    e) Limit result to 25 rows ** Done **

F. Search for Donation

    a) Validation for ISBN **Partially done. Need to check for integers too**
    b) Handle when service is down or no information is available

G. Donate

    a) Send donation email ** Done **

H. Manage

    a) Accept Book, send acceptance thanks email
    b) Issue Book, send confirmation email
    c) Make manage availabe only to admin users

**Cheat Sheet**

1. How to drop the entire database and start afresh?

    If you want to start afresh, remove the db file and the migrations folder.
    (venv) $ rm bookrepo.db
    (venv) $ rm -rf migrations

    Then execute setup step H and I again.
    
2. How to view actual table schema?

    Connect to the sqlite prompt and run the following command
    (venv) $ sqlite3 bookrepo.db
    sqlite> .output schema-dump.sql
    sqlite> .dump
    sqlite> .exit

3. How to view table data?

    Connect to the sqlite prompt and run the following command
    (venv) $ sqlite3 bookrepo.db
    sqlite> select * from books;   

4. How to enable SQL logging?

    Edit the config.py file.
    Change the value of variable SQLALCHEMY_ECHO = True

5. How to add more master data?

    (venv) $ sqlite3 bookrepo.db
    sqlite> Enter normal SQL commands here. 


**References**

0. Dummies guide for [Flask](https://codeburst.io/flask-for-dummies-a-beginners-guide-to-flask-part-uno-53aec6afc5b1)

1. The work is inspired by [Miguel's blog](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

2. Used Stackoverflow extensively

3. SQLite [tutorial](https://www.sqlitetutorial.net/)

