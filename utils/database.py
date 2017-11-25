#get stuff from database and update database
import sqlite3
import random

#TODO: put this in every function
'''db = sqlite3.connect(db_name)
c = db.cursor()
### Inbetween stuff
db.commit()
db.close()
'''

#functions

#initial creation
def create_table(table_name, cols, db_name):
    db = sqlite3.connect(db_name)
    c = db.cursor()

    cmd = 'CREATE TABLE ' + table_name + '(' + cols + ')'
    c.execute(cmd)
    
    db.commit()
    db.close()

#for login
def authorize(username, password, db_name):
    db = sqlite3.connect(db_name)
    c = db.cursor()

    cmd = 'SELECT password FROM user_info WHERE username="' + username + '"'
    c.execute(cmd)

    passes = c.fetchall()
    print(passes)
    if len(list(passes)) == 0:
        db.commit()
        db.close()
        return False
    for pw in passes:
        if pw[0] == password:
            db.commit()
            db.close()
            return True
    db.commit()
    db.close()
    return False

#for register
def check_account_not_exists(username, db_name):
    db = sqlite3.connect(db_name)
    c = db.cursor()

    cmd = 'SELECT username FROM user_info WHERE username="' + username + '"'
    c.execute(cmd)

    users = c.fetchall()
    if len(list(users)) > 0:
        db.commit()
        db.close()
        return False

    db.commit()
    db.close()
    return True

def add_account(username, password, db_name):
    db = sqlite3.connect(db_name)
    c = db.cursor()

    cmd = 'INSERT INTO user_info VALUES("' + username + '","' + password + '")'
    c.execute(cmd)

    #create a user history table for this username
    cmd = 'CREATE TABLE ' + username + '_history(city CHAR, video CHAR)'
    c.execute(cmd)
    
    db.commit()
    db.close()

#for search_result
def update_user_history(username, city, new_video, db_name):
    db = sqlite3.connect(db_name)
    c = db.cursor()

    cmd = 'INSERT INTO ' + username + '_history VALUES("' + city + '","' + new_video + '")'
    c.execute(cmd)
    
    db.commit()
    db.close()

def get_user_history(username, db_name):
    db = sqlite3.connect(db_name)
    c = db.cursor()

    cmd = 'SELECT city, video FROM ' + username + '_history'
    c.execute(cmd)

    history = c.fetchall()
    if len(history) > 0:
        rand_index = random.randrange(len(history))

        city = history[rand_index][0]
        video = history[rand_index][1]
        
        db.commit()
        db.close()

        return city, video

    db.commit()
    db.close()

    return None, None


if __name__ == '__main__':
    db_name = 'music_under_the_weather.db'
    #create_table('user_info', 'username CHAR PRIMARY KEY, password CHAR', db_name)

    print (check_account_not_exists('me', db_name))
    #add_account('me', 'pass', db_name)
    print (check_account_not_exists('me', db_name))
    print (authorize('me', 'pass', db_name))
    print (get_user_history('me', db_name))
    update_user_history('me', 'New York City', 'test_video_5', db_name)
    print (get_user_history('me', db_name))
