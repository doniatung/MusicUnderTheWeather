#get stuff from database and update database
import sqlite3


#TODO: put this in every function
db = sqlite3.connect(<db name>)
c = db.cursor()
### Inbetween stuff
db.commit()
db.close()


#functions

#for login
def authorize():
    pass

#for register
def check_account_exists():
    pass

def add_account():
    pass

#for search_result
def update_user_history():
    pass
