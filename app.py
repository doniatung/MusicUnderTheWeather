from flask import Flask, render_template, redirect, url_for
import urllib2, json

app = Flask(__name__)

#main routes

@app.route('/')
def root():
    return render_template('POTENTIALLOGIN.html')

#TODO: add session stuff and authorization
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('PotentialRegister.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/search_result')
def search():
    return render_template('search_result.html')

#in between routes (logout, authorize, etc.)

@app.route('/logout')
def logout():
    return redirect(url_for('root'))

if __name__ == "__main__":
    app.debug = True
    app.run()
