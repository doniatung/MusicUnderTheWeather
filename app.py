from flask import Flask, render_template
import urllib2, json

my_app = Flask(__name__)

@my_app.route('/')
def root():
    return render_template("base.html")


if __name__ == "__main__":
    my_app.debug = True
    my_app.run()
