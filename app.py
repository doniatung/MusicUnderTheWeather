from flask import Flask, render_template, redirect, url_for, request, session, flash
import os, urllib2, json
#from utils import database


app = Flask(__name__)
app.secret_key = os.urandom(32)

key = 'user'
db_name = 'music_under_the_weather.db'

def cityFinder(zipcode):
    url = "http://api.wunderground.com/api/31c0e27929b4d46c/geolookup/q/" + zipcode + ".json"
    u = urllib2.urlopen(url)
    data = u.read()
    dic = json.loads(data)
    locationdic = dic["location"]
    city = locationdic["city"]
    return city

def weatherGetter(zipcode):
    url1 = "http://api.wunderground.com/api/31c0e27929b4d46c/geolookup/q/" + zipcode + ".json"
    u = urllib2.urlopen(url1)
    data = u.read()
    dic = json.loads(data)
    locationdic = dic["location"]
    addon = locationdic["requesturl"]
    url2 = "http://api.wunderground.com/api/31c0e27929b4d46c/conditions/q/" + addon + ".json"
    u2 = urllib2.urlopen(url2)
    data2 = u2.read()
    dic2 = json.loads(data2)
    currentObsDic = dic2["current_observation"]
    temp = currentObsDic["temp_f"]
    return temp

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
        flash("Login Successful")
        return render_template('home.html') 

    #if not logged in
    else:
        #TODO: add flash message
        flash("Login Unsuccessful. Try again.")
        return redirect(url_for('root'))

@app.route('/search_result', methods = ["GET", "POST"])
def result():
    zipp = request.form["zipcode"]
    city = cityFinder(zipp)
    temp = weatherGetter(zipp)
    return render_template("search_result.html", cT = city, temperature = temp)


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
