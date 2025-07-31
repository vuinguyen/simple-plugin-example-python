from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "hello, you're home!"

@app.route("/default")
def default():
    return render_template("default.html")