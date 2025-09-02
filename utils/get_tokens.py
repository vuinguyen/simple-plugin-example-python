import jwt
import json
import sys

# This is a utility script to decode and print JWT tokens
if len(sys.argv) != 3:
    print("Usage: python get_tokens.py <access_token> <id_token>")
    sys.exit(1)

access_token = sys.argv[1]
id_token = sys.argv[2]

try:
    # Decode the access token
    decoded_access_jwt = jwt.decode(access_token, options={"verify_signature": False})
    print("Decoded Access Token:", json.dumps(decoded_access_jwt, indent=2))

    # Decode the id token
    decoded_id_jwt = jwt.decode(id_token, options={"verify_signature": False})
    print("Decoded ID Token:", json.dumps(decoded_id_jwt, indent=2))
except jwt.ExpiredSignatureError:
    print("The token has expired.")
except jwt.InvalidTokenError:
    print("Invalid token. Please check your secret key and token.") 
except Exception as e:
    print(f"An error occurred: {e}")    

