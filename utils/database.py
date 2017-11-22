#get stuff from database and update database
import sqlite3


#TODO: put this in every function
db = sqlite3.connect(<db name>)
c = db.cursor()
### Inbetween stuff
db.commit()
db.close()


#functions

#initial creation
def create_table(table_name):
    db = sqlite3.connect(<db name>)
    c = db.cursor()

    cmd = 'CREATE TABLE ' + table_name '(' + cols + ')'
    c.execute(cmd)
    
    db.commit()
    db.close()

#for login
def authorize(username, password):
    db = sqlite3.connect(<db name>)
    c = db.cursor()

    cmd = ''
    c.execute(cmd)
    
    db.commit()
    db.close()

#for register
def check_account_exists():
    pass

def add_account():
    pass

#for search_result
def update_user_history():
    pass
