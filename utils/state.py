# generate a random string of 60 bytes
import os   

def generate_random_string():
    return os.urandom(60).hex()

print(generate_random_string())