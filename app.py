from urllib import response
from flask import json, render_template
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
import requests
from utils.get_dynamic_data import request_authorization
from utils.get_dynamic_data import build_authorization_url
from utils.pkce import create_code_challenge, create_code_verifier
from utils.state import generate_random_string

app = Flask(__name__)

@app.route("/")
def home():
    return "hello, you're home!"

@app.route("/default")
def default():
    return render_template("default.html")

@app.route("/dynamic")
def dynamic(name=None, accounts_count=None):
    # if name and accounts count are not None, return a dynamic html page
    # hardcoded for now, until we connect to the backend for real data
    # name = "Dynamic User"
    # accounts_count = 3
    if name and accounts_count is not None:
        return render_template("dynamic.html", name=name, accounts_count=accounts_count)
    else:
        return render_template("default.html")
    
@app.route("/auth")
def auth():
    # return "This is the auth endpoint."
    print("In auth endpoint")
    # get the authorization URL
    authorization_url = build_authorization_url()

    # redirect the user to the authorization URL
    print("Redirecting to authorization URL:", authorization_url)
    # make a GET request to the authorization URL   
    #response = requests.get(authorization_url)
   
    response = requests.get(authorization_url, allow_redirects=False)

    # get the full redirect URL from the response
    redirect_uri_full = response.url
    print("Full Redirect URL:", redirect_uri_full)
    print("Authorization Code received in auth endpoint:", request.args.get('code'))
    print("State received in auth endpoint:", request.args.get('state'))
    print("Response object:", response)
    print("Response headers:", response.headers)
    print("Response status code:", response.status_code)
    print("Response cookies:", response.cookies)

    #response = requests.get(authorization_url)
    #redirect_url = response.url
    #print("redirect: ", redirect_url)
    #request.args.get('code')
    #print("Authorization Code received in auth endpoint:", request.args.get('code'))
    #cookies = response.headers.get('Set-Cookie')
    #print("cookies", cookies)
    # response = redirect(redirect_uri_full)
    #redirect_uri_full = response.headers.get('Location')
    #print("Redirect full:", redirect_uri_full)

    # how to pass the request to the auth_callback endpoint?

    #return redirect(url_for("auth_callback"))
    #return "This was the auth endpoint."
    return redirect(authorization_url)


@app.route("/auth/callback")
def auth_callback():
    print("In auth callback endpoint")
    code = request.args.get('code')
    print("Authorization Code received in callback:", code)
    return redirect(url_for("dynamic"))    

