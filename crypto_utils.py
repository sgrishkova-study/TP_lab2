from cryptography.fernet import Fernet

with open("signature.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data):
    return cipher.decrypt(data.encode()).decode()