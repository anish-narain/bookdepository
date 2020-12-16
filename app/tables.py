from flask_table import Table, Col

class Results(Table):
    id = Col('Id', show=False)
    username = Col('User Name')
    email = Col('Email')