import json
#from urllib import response
import requests
from flask import request
from flask import redirect
import urllib
import jwt
from utils.pkce import create_code_challenge, create_code_verifier
from utils.state import generate_random_string

# create a dictionary to hold parameter values
# This is NOT recommended for production use
params = {
    "client_id": None,
    "client_secret": None,
    "redirect_uri": None,
    "state": None,
    "code_verifier": None,
    "code_challenge": None,
    "code_challenge_method": None,
    "response_type": None,
    "scope": None,
    "claims": None
}

# base URL for the authorization server
# global variable
baseURL = None

def return_none():
    return None, None

def request_user_data(access_token, id_token):
    name = None
    accounts_count = None

    user_id = id_token.get("sub")
    print("User ID from ID Token:", user_id)

    user_info_url = f'{baseURL}/a/consumer/api/v0/users/{user_id}/accounts'
    print("User Info URL:", user_info_url)
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(user_info_url, headers=headers)
    if response.status_code != 200:
        print("Failed to get user info. Status code:", response.status_code)
        print("Response:", response.text)
        return name, accounts_count
    
    accounts_data = response.json()
    accounts_count = len(accounts_data.get("accounts", []))
    print("Accounts Data:", accounts_data)
    print("Number of Accounts:", accounts_count)

    name = id_token.get("given_name")
   
    return name, accounts_count

def get_JWT_tokens(code):
    tokens = None, None

    print("Building token URL...")
    token_baseURL = f'{baseURL}/a/consumer/api/v0/oidc/token'

    data = {
        "client_id": params["client_id"],
        "client_secret": params["client_secret"],
        "grant_type": "authorization_code",
        "code": code,
        "state": params["state"],
        "redirect_uri": params["redirect_uri"],
        "code_verifier": params["code_verifier"]
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    print("Making POST request to token URL...")
    print("URL:", token_baseURL)
    print("Data:", data)
    print("Headers:", headers)

    # make a POST request to the token endpoint
    response = requests.post(token_baseURL, data=data, headers=headers, allow_redirects=False)

    #if response.status_code == 200:
    #    tokens = response.json()
    #    print("Token URL response:", tokens)
    #else:
   #     print("Failed to get token URL. Status code:", response.status_code)
   #     print("Response:", response.text)

    if response.status_code != 200:
        print("Failed to get token URL. Status code:", response.status_code)
        print("Response:", response.text)  
        return tokens

    print("Token URL response:", response.json())
    tokens = response.json()
    access_token = tokens.get("access_token")
    print("Access Token:", access_token)
    id_token = tokens.get("id_token")
    id_token_decoded = jwt.decode(id_token, options={"verify_signature": False})
    print("ID Token (decoded):", id_token_decoded)

    return access_token, id_token_decoded

def exchange_tokens(token_url):

    return True  # placeholder


def build_user_info_url(code):
    # use the authorization code to get an access token
    # request an access token from the token endpoint
    # then use the access token to get user info from the user info endpoint
    print("Building user info URL...")

    return True  # placeholder

def build_authorization_url():
    # get parameter values from config.json
    # and populate the params dictionary
    print("Building authorization URL...")

    # update baseURL to be used in other functions
    global baseURL

    with open('config.json') as f:
        config = json.load(f)

    #client_id = config.get("client_id")
    #params["client_id"] = f'client_id={config.get("client_id")}'  # alternative one-liner
    #params["client_id"] = f'client_id={client_id}'
    params["client_id"] = f'{config.get("client_id")}'  # alternative one-liner

    #client_secret = config.get("client_secret")
    #params["client_secret"] = f'client_secret={client_secret}'  
    params["client_secret"] = f'{config.get("client_secret")}'  # alternative one-liner

    #redirect_uri = config.get("redirect_uri")
    #params["redirect_uri"] = f'redirect_uri={redirect_uri}'
    params["redirect_uri"] = f'{config.get("redirect_uri")}'  # alternative one-liner

    #environment = config.get("environment")
    baseURL = f'{config.get("environment")}'  # alternative one-liner

    # close file
    f.close()

    #response_type = "code"
    #params["response_type"] = f'response_type={response_type}'
    params["response_type"] = 'code'

    params["scope"] = "openid%20profile%20https://api.banno.com/consumer/auth/accounts.readonly"
    #params["scope"] = f'scope={scope}'

    params["state"] = generate_random_string()
    #params["state"] = f'state={state}'

    params["code_challenge_method"] = "S256"
    #params["code_challenge_method"] = f'code_challenge_method={code_challenge_method}'

    # params["code_verifier"] = create_code_verifier()
    code_verifier = create_code_verifier()
    code_challenge = create_code_challenge(code_verifier)

    params["code_verifier"] = f'{code_verifier}'
    params["code_challenge"] = f'{code_challenge}'
    #params["code_verifier"] = f'code_verifier={code_verifier}'

    # store the code verifier somewhere safe to use later when exchanging the authorization code for tokens
    # create the code challenge from the code verifier
    #code_challenge = create_code_challenge(code_verifier)
    #params["code_challenge"] = f'code_challenge={code_challenge}'
    # params["code_challenge"] = create_code_challenge(params["code_verifier"])

    # Note, claims parameter is optional
    claims = {
        'https://api.banno.com/consumer/claim/institution_id': '',
    }

    claimsToRequest = {
        'id_token': claims,
        'userinfo': claims
    }

    claims_json = json.dumps(claimsToRequest)
    claims_encoded = urllib.parse.quote(claims_json)
    params["claims"] = f'claims={claims_encoded}'

    auth_baseURL = f'{baseURL}/a/consumer/api/v0/oidc/auth'

    auth_params = f'client_id={params["client_id"]}&redirect_uri={params["redirect_uri"]}&scope={params["scope"]}&response_type={params["response_type"]}&state={params["state"]}&code_challenge={params["code_challenge"]}&code_challenge_method={params["code_challenge_method"]}&{params["claims"]}'
    #auth_params = '&'.join(params.values())
    #auth_params = urllib.parse.quote(params.values, safe='=&')  # encode the parameters

    authorization_url = f'{auth_baseURL}?{auth_params}'
    print("Visit this URL to authorize the application:")
    print(authorization_url)
    return authorization_url

# build the authorization URL and direct the user to it
def request_authorization():
    redirect_uri_full = None
    authorization_url = build_authorization_url()
    

    # redirect the user to the authorization URL    
    # response_type.redirect(authorization_url)
    # simulate user authorization by making a GET request to the authorization URL
    # and following redirects to capture the full redirect URI
    #redirect_uri_full = redirect(authorization_url).location  

    #redirect_uri_full = redirect(authorization_url).location     

    response = requests.get(authorization_url) 
    cookies = response.headers.get('Set-Cookie')
    print("cookies", cookies)
    # response = redirect(redirect_uri_full)

    redirect = response.headers.get('Location')
    print("Redirect full:", redirect)

    #print("Redirect URI full:", redirect_uri_full)
    #print("Response object:", response.location)

    query = urllib.parse.urlparse(redirect).query
    params = urllib.parse.parse_qs(query)
    print("params", params)

    params.get('code')
    print("code", params.get('code'))  # simulate getting the authorization code from the
   # print("code", request.args.get('code'))  # simulate getting the authorization code from the redirect URI

    #authorization_response = requests.get(authorization_url)

    #if authorization_response.status_code != 200:
    #    return redirect_uri_full
    
    #redirect_uri_full = authorization_response.url
    #print(authorization_response.status_code)
    #print(authorization_response.url)

    return redirect_uri_full

def get_dynamic_data(code=None):
    name = None
    accounts_count = None

    if code == None:
        print("No authorization code provided.")
        return return_none()

    access_token, id_token_decoded = get_JWT_tokens(code)
    if access_token is None or id_token_decoded is None:
        print("Failed to build token URL.")
        return return_none()
    
    name, accounts_count = request_user_data(access_token, id_token_decoded)

    print("Returning dynamic data...")
    return name, accounts_count 
    




# get_dynamic_data()    # Simulate fetching dynamic data, e.g., from a database or an API
if __name__ == "__main__":
    data = get_dynamic_data()
    print(data)