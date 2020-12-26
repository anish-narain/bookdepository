Welcome to my NEA project: Book Depository.
===========================================

The design document is available here [link](https://www.google.com)


**How to setup (Mac)**

A. Pre-requisites

1) Python should be there on machine. Check by typing:

```
~ $ python3
Python 3.7.5 (default, Nov 1 2019, 02:16:32)
[Clang 11.0.0 (clang-1100.0.33.8)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

B. Copy the code from here to local machine

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

F. Set up the environment variables after setting right values
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


To do
-----
A. Index Page

    a) Nearest centre?

B. General Improvements

    a) Session timeout is not there.

C. User Profile

    a) Show only last 3 transactions -- done
    b) Edit profile?

D. Search for Reservation

E. Reserve

F. Search for Donation

G. Donate

H. Manage

References:

The work is inspired by https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world