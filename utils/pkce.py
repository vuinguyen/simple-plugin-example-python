import secrets
import string
import hashlib
import base64

def create_code_verifier():
    # generate a random string of characters, 60 bytes long
    # must be composed of characters A-Z, a-z, 0-9, and the punctuation characters "-", ".", "_", and "~"
    allowed_chars = string.ascii_letters + string.digits + '-._~'
    verifier = ''.join(secrets.choice(allowed_chars) for _ in range(60))
    return verifier

def create_code_challenge(verifier):
    # create a SHA256 hash of the verifier
    sha256_hash = hashlib.sha256(verifier.encode('utf-8')).digest()
    # base64-url encode the hash (replace + with -, / with _, and remove padding =)
    challenge = base64.urlsafe_b64encode(sha256_hash).decode('utf-8').replace('=', '')
    return challenge

if __name__ == "__main__":
    verifier = create_code_verifier()
    challenge = create_code_challenge(verifier)
    print("Code Verifier:", verifier)
    print("Code Challenge:", challenge)