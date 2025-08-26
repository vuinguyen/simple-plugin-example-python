from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "hello, you're home!"

@app.route("/default")
def default():
    return render_template("default.html")

@app.route("/dynamic")
def dynamic():
    # if name and accounts count are not None, return a dynamic html page
    # hardcoded for now, until we connect to the backend for real data
    name = "Dynamic User"
    accounts_count = 3
    if name and accounts_count is not None:
        return render_template("dynamic.html", name=name, accounts_count=accounts_count)
    else:
        return render_template("default.html")