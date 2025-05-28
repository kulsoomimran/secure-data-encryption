# auth.py
from utils import hash_passkey

def register_user(username: str, password: str):
    users = get_user_store()
    if username in users:
        return False, "Username already exists."
    
    users[username] = hash_passkey(password)
    return True, "Registration successful."

def login_user(username: str, password: str) -> bool:
    users = get_user_store()
    hashed_input = hash_passkey(password)
    return users.get(username) == hashed_input

def get_user_store():
    import streamlit as st
    if "user_store" not in st.session_state:
        st.session_state.user_store = {
            "admin": hash_passkey("admin12345")  # Default admin user
        }
    return st.session_state.user_store
