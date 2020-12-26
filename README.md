Welcome to my NEA project: Book Depository
===========================================

The design document is available here [link](https://www.google.com)


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

C. Create python virtual environment and then activate it
 ```   
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $
```
Now you can notice the venv on your command prompt

D. Install flask
```
    (venv) $ pip install flask
```

E. Install all flask dependencies
```
     (venv) $ pip install -r requirements.txt
```

F. Set up the environment variables after editing the file with right values
```
    (venv) $ . ./.setenv.sh
```

G. Set up the database by running these 3 commands
```
    (venv) $ flask db init
    (venv) $ flask db migrate
    (venv) $ flask db upgrade
```

H. Populate the initial dataset
```
    (venv) $ cat metadata.sql | sqlite3 bookrepo.db
```
I. Quick sanity check before we start running the application

    a) Your folder structure now should look something like
    ```
    (venv) ~/Anish/nea/bookdepository $ 
            LICENSE
            README.md
            __pycache__
            app
                __init__.py		
                email.py		
                getBookByISBN.py	
                models.py		
                tables.py
                __pycache__		
                forms.py		
                getTransAndPoints.py	
                routes.py		
                templates
            bookdepository.py
            bookrepo.db
            config.py
            metadata.sql
            migrations
            requirements.txt
            setenv.sh
            venv
            (venv) ~/Anish/nea/bookdepository $ 
    ```

J. Start the application
```
    (venv) $ flask run
```

K. Access the application on local [browser](http://127.0.0.1:5000)

**To do**

A. General Improvements

    a) Session timeout is not there.
    b) Documentation
    c) Remove prints, debug settings

B. Index Page

    a) Nearest centre?

C. User Profile

    <del>a) Show only last 3 transactions</del>
    b) Edit profile?

D. Search for Reservation

    a) Validations?

E. Reserve

    a) Currently the option list is hardcoded. Generalize it
    b) Send reservation email
    c) Future dated reservations
    d) Send email once reserved book is available

F. Search for Donation

    a) Validation for ISBN
    b) Handle when service is down or no information is available

G. Donate

    a) Send donation email

H. Manage

    a) Accept Book, send acceptance thanks email
    b) Give Book, send confirmation email
    c) Make manage availabe only to admin users

**Cheat Sheet**

1. How to drop the entire database and start afresh?

2. How to view actual table schema?

3. How to view table data?

4. How to enable SQL logging?

5. How to add branches or any other master data?


**References**

1. The work is inspired by https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

2. Stackoverflow

