# encryption.py
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def get_fernet(key):
    return Fernet(key)

def encrypt_text(text: str, fernet: Fernet) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text: str, fernet: Fernet) -> str:
    return fernet.decrypt(encrypted_text.encode()).decode()
