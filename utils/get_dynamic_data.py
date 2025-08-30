import json
import requests

from pkce import create_code_challenge, create_code_verifier
from state import generate_random_string

def return_none():
    return None

def request_authorization():
    # build the authorization URL and direct the user to it
    success = True

    # get parameter values from config.json
    # and place into parameters
    with open('../config.json') as f:
        config = json.load(f)
    client_id = config.get("client_id")
    client_id_param = f'client_id={client_id}'
    client_secret = config.get("client_secret")
    client_secret_param = f'client_secret={client_secret}'  
    redirect_uri = config.get("redirect_uri")
    redirect_uri_param = f'redirect_uri={redirect_uri}'

    environment = config.get("environment")

    # close file
    f.close()

    response_type = "code"
    response_type_param = f'response_type={response_type}'

    scope = "openid%20profile%20https://api.banno.com/consumer/auth/accounts.readonly"
    scope_param = f'scope={scope}'

    state = generate_random_string()
    state_param = f'state={state}'

    code_challenge_method = "S256"
    code_challenge_method_param = f'code_challenge_method={code_challenge_method}'

    code_verifier = create_code_verifier()
    code_challenge = create_code_challenge(code_verifier)
    code_challenge_param = f'code_challenge={code_challenge}'

    auth_baseURL = f'{environment}/a/consumer/api/v0/oidc/auth'

    authorization_url = f'{auth_baseURL}?{client_id_param}&{redirect_uri_param}&{scope_param}&{response_type_param}&{state_param}&{code_challenge_param}&{code_challenge_method_param}'

    print("Visit this URL to authorize the application:")
    print(authorization_url)

    # redirect the user to the authorization URL    
    # response_type.redirect(authorization_url)
    # simulate user authorization by making a GET request to the authorization URL
    # and following redirects to capture the full redirect URI
    #redirect_uri_full = redirect(authorization_url).location  

    #redirect_uri_full = redirect(authorization_url).location     

    redirect_uri_full = requests.get(authorization_url).url 

    response = redirect(redirect_uri_full)
    print("Redirect URI full:", redirect_uri_full)
    print("Response object:", response.location)

    query = urllib.parse.urlparse(redirect_uri_full).query
    params = urllib.parse.parse_qs(query)
    print("params", params)

    print("code", request.args.get('code'))  # simulate getting the authorization code from the redirect URI

    #authorization_response = requests.get(authorization_url)

    #if authorization_response.status_code != 200:
    #    return redirect_uri_full
    
    #redirect_uri_full = authorization_response.url
    #print(authorization_response.status_code)
    #print(authorization_response.url)

    #return redirect_uri_full

def get_dynamic_data():

    redirect_uri_full = request_authorization()
    
    if redirect_uri_full is None:
        return None
    
    if exchange_tokens(redirect_uri_full) is False:
        return None

    # Simulate fetching dynamic data, e.g., from a database or an API
    return {
        "name": "Dynamic User",
        "accounts_count": 5
    }




# get_dynamic_data()    # Simulate fetching dynamic data, e.g., from a database or an API
if __name__ == "__main__":
    data = get_dynamic_data()
    print(data)