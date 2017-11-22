from flask import Flask, render_template, redirect, url_for
import urllib2, json

app = Flask(__name__)
app.secret_key = os.urandom(32)

key = 'user'

#main routes

#TODO: add session and authorizaion stuff
@app.route('/')
def root():
    if key in session:
        return redirect(url_for('home'))
    return render_template('POTENTIALLOGIN.html')

@app.route('/register')
def register():
    return render_template('PotentialRegister.html')

@app.route('/home')
def home():
    #if the key is already in the session
    if key in session:
        return render_template('home.html')

    #if just logged in
    '''elif database.authorize(request.form('username'), request.form('password')):
        session[key] = request.form('username')
        return render_template('home.html')''' #not yet usable

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
    return redirect(url_for('root'))

if __name__ == "__main__":
    app.debug = True
    app.run()
