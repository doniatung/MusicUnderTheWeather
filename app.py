from flask import Flask, render_template, redirect, url_for, request, session, flash
#import urllib.request as urllib2
import os, json, urllib2
from utils import database
import random


app = Flask(__name__)
app.secret_key = os.urandom(32)

key = 'user'
db_name = 'music_under_the_weather.db'


less30 = ["o2uvtl-1V70", "6bbuBubZ1yE", "yXQViqx6GMY","b9XNyeeJZ2k", "mjwV5w0IrcA"]
bw3050 = ["WibQR0tQ0P8", "L4sbDxR22z4", "iuS1nGPbtq4", "BBAtAM7vtgc", "J_ub7Etch2U"]
bw5070 = ["GCdwKhTtNNw", "kTHNpusq654", "LHQqqM5sr7g", "50zL8TnMBN8", "zKXhwOSsCJ0"]
bw7090 = ["DVkkYlQNmbc","weeI1G46q0o","HL1UzIK-flA", "by3yRdlQvzs", "LiILUT_Px84"]
over90 = ["HCjNJDNzw8Y", "bncb3dm8K7g","yd8jh9QYfEs","CTFtOOh47oo", "HMqgVXSvwGo"]

def cityFinder(zipcode):
    url = "http://api.wunderground.com/api/31c0e27929b4d46c/geolookup/q/" + zipcode + ".json"
    u = urllib2.urlopen(url)
    data = u.read()#.decode('utf-8')
    dic = json.loads(data)
    locationdic = dic["location"]
    city = locationdic["city"]
    return city

def weatherGetter(zipcode):
    url1 = "http://api.wunderground.com/api/31c0e27929b4d46c/geolookup/q/" + zipcode + ".json"
    u = urllib2.urlopen(url1)
    data = u.read()#.decode('utf-8')
    dic = json.loads(data)
    locationdic = dic["location"]
    addon = locationdic["requesturl"]
    url2 = "http://api.wunderground.com/api/31c0e27929b4d46c/conditions/q/" + addon + ".json"
    u2 = urllib2.urlopen(url2)
    data2 = u2.read()#.decode('utf-8')
    dic2 = json.loads(data2)
    currentObsDic = dic2["current_observation"]
    temp = currentObsDic["temp_f"]
    return temp


def songGetter(temp):
    temperature = int(temp)
    index = random.randint(0,4)
    if temperature < 30:
        return less30[index]
    elif temperature < 50:
        return bw3050[index]
    elif temperature < 70:
        return bw5070[index]
    elif temperature < 90:
        return bw7090[index]
    else:
        return over90[index]

def titleGetter(id):
    url = "https://www.googleapis.com/youtube/v3/videos?id=" + id + "&key=AIzaSyDXJKY4vKmS5WhwX4D3TWVA61NUSTE4Ihk&part=snippet,contentDetails,statistics,status"
    print (url)
    u = urllib2.urlopen(url)
    data = u.read()#.decode('utf-8')
    dic = json.loads(data)
    dictionarylist = dic["items"]
    dic2 =  dictionarylist[0]
    return dic2['snippet']['title']

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
    if not(key in session):
        flash('You are not logged in.')
        return redirect(url_for('login'))
    try:
        zipp = request.form["zipcode"]
        city = cityFinder(zipp)
        temp = weatherGetter(zipp)
        songID = songGetter(temp)
        iD = ["https://www.youtube.com/embed/" + songID]
        name = titleGetter(songID)
        database.update_user_history(session[key], city, str(temp), iD[0], db_name)
        return render_template("search_result.html", cT = city, temperature = temp, playlist = iD, title = name)
    except:
        flash('That is not a valid US zipcode. Please enter a valid zipcode')
        return redirect(url_for('home'))

@app.route('/user_history', methods= ['GET'])
def user_history():
    if not(key in session):
        flash('You are not logged in.')
        return redirect(url_for('login'))
    #print(session[key])
    city, temp, iD = database.get_user_history(session[key], db_name)
    if city == None:
        flash('Sorry, you have not listened to any music yet. You do not have anything in your history')
        return redirect(url_for('home'))
    return render_template("user_history.html", ct = city, temperature = temp, songID = [iD])

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
