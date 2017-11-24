from flask import Flask, render_template, redirect, url_for, request, session, flash
import os
from utils import database
#import urllib2, json

app = Flask(__name__)
app.secret_key = os.urandom(32)

key = 'user'
db_name = 'music_under_the_weather.db'

#main routes

#TODO: add session and authorizaion stuff
@app.route('/')
def root():
    if key in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    #if the key is already in the session
    if key in session:
        return render_template('home.html')

    #if just logged in
    username = request.form['username']
    password = request.form['password']
    if database.authorize(username, password, db_name):
        session[key] = username
        return render_template('home.html') 

    #if not logged in
    else:
        #TODO: add flash message
        return redirect(url_for('root'))

@app.route('/search_result')
def search():
    return render_template('search_result.html')

#in between routes (logout, authorize, etc.)

@app.route('/logout')
def logout():
    if key in session:
        session.pop(key)
        flash('You logged out!')
    return redirect(url_for('root'))

@app.route('/check_new_account', methods=['POST'])
def check_new_account():
    username = request.form['newUsername']
    password = request.form['newPassword']
    confirmed_pass = request.form['repeatPassword']

    if not (password == confirmed_pass):
        flash('Passwords do not match, try again.')
        return redirect(url_for('register'))
    
    if not database.check_account_not_exists(username, db_name):
        flash('Account already exists')
        return redirect(url_for('register'))
    
    database.add_account(username, password, db_name)
    flash('You have registed, ' + username + '!')
    return redirect(url_for('root'))

if __name__ == "__main__":
    app.debug = True
    app.run()
