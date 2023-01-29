"""Encryption Module"""
import json
from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("security/secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    return open("security/secret.key", "rb").read()

def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(encoded_message)

    print(encrypted_message)
    return encrypted_message


def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message)

    print(decrypted_message.decode())
    return decrypted_message.decode()


def encrypted_response(data):
    """Encrypted_Response"""

    if type(data) != dict and type(data)!=list:
        result=data.json()

    if  isinstance(data, dict):
        result = json.dumps(data)

    response = json.dumps(result)

    if response is not None:
        generate_key()
        encrypt_response=encrypt_message(response)
        encrypted_response = json.dumps({'encrypted_data': encrypt_response.decode('utf-8')})
        encrpyted_data = json.loads(encrypted_response)

    return encrpyted_data

# Return Encrypted Response
     