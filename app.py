from flask import render_template
from flask import Flask
from flask import request
from flask import redirect
from utils.get_dynamic_data import get_dynamic_data
from utils.get_dynamic_data import build_authorization_url

app = Flask(__name__)

@app.route("/")
def home():
    return "hello, you're home!"

@app.route("/default")
def default():
    return render_template("default.html")

@app.route("/dynamic")
def dynamic(name=None, accounts_count=None):
    if name and accounts_count is not None:
        return render_template("dynamic.html", name=name, accounts_count=accounts_count)
    else:
        return render_template("default.html")
    
@app.route("/auth")
def auth():
    print("In auth endpoint")
    # get the authorization URL
    authorization_url = build_authorization_url()

    # redirect the user to the authorization URL
    print("Redirecting to authorization URL:", authorization_url)
    return redirect(authorization_url)


@app.route("/auth/callback")
def auth_callback():
    print("In auth callback endpoint")
    authorization_code = request.args.get('code')
    print("Authorization Code received in callback:", authorization_code)

    name, accounts_count = get_dynamic_data(authorization_code)
    print("Name:", name)
    print("Accounts Count:", accounts_count)
    if name is None or accounts_count is None:
        return render_template("default.html")
    return render_template("dynamic.html", name=name, accounts_count=accounts_count)    

