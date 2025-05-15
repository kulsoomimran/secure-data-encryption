import streamlit as st
from cryptography.fernet import Fernet
import hashlib

if "fernet_key" not in st.session_state:
    st.session_state.fernet_key = Fernet.generate_key()
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = {}
if "authorized" not in st.session_state:
    st.session_state.authorized = True
if "page" not in st.session_state:
    st.session_state.page = "Home"

fernet = Fernet(st.session_state.fernet_key)

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def insert_data(user_id, text, passkey):
    encrypted_text = fernet.encrypt(text.encode()).decode()
    hashed_passkey = hash_passkey(passkey)
    st.session_state.stored_data[user_id] = {
        "encrypted_text": encrypted_text,
        "passkey": hashed_passkey
    }
    st.success(f"Data stored securely for user: {user_id}")

def retrieve_data(user_id, passkey):
    data_store = st.session_state.stored_data
    attempts = st.session_state.failed_attempts

    if user_id not in data_store:
        st.error("No data found for this user.")
        return

    if attempts.get(user_id, 0) >= 3:
        st.session_state.authorized = False
        st.session_state.page = "Login"
        st.warning("Too many failed attempts. Please reauthorize.")
        st.rerun()
        return

    hashed_input = hash_passkey(passkey)
    if hashed_input == data_store[user_id]["passkey"]:
        decrypted = fernet.decrypt(data_store[user_id]["encrypted_text"].encode()).decode()
        st.success(f"Decrypted Data: {decrypted}")
        attempts[user_id] = 0
    else:
        attempts[user_id] = attempts.get(user_id, 0) + 1
        attempts_left = 3 - attempts[user_id]
        st.error(f"Incorrect passkey. Attempts left: {attempts_left}")

def login_page():
    st.title("🔐 Reauthorization Required")
    username = st.text_input("Enter Admin Username")
    password = st.text_input("Enter Admin Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin12345":
            st.session_state.authorized = True
            st.session_state.failed_attempts = {}
            st.success("Login successful!")
            st.session_state.page = "Home"
            st.rerun()
        else:
            st.error("Invalid credentials.")

def main():
    if not st.session_state.authorized:
        login_page()
        return

    st.sidebar.title("🔐 Secure Data Storage")
    st.session_state.page = st.sidebar.radio("Navigate", ["Home", "Insert Data", "Retrieve Data", "Login"], index=["Home", "Insert Data", "Retrieve Data", "Login"].index(st.session_state.page))

    if st.session_state.page == "Home":
        st.title("Welcome to Secure Data Encryption System")
        st.write("Use the sidebar to insert or retrieve encrypted data.")

    elif st.session_state.page == "Insert Data":
        st.title("📥 Store Your Secure Data")
        user_id = st.text_input("Enter User ID")
        data = st.text_area("Enter Data to Encrypt")
        passkey = st.text_input("Set a Passkey", type="password")
        if st.button("Store Data"):
            if user_id and data and passkey:
                insert_data(user_id, data, passkey)
            else:
                st.warning("All fields are required.")

    elif st.session_state.page == "Retrieve Data":
        st.title("🔓 Retrieve Your Encrypted Data")
        user_id = st.text_input("Enter Your User ID")
        passkey = st.text_input("Enter Your Passkey", type="password")
        if st.button("Decrypt Data"):
            if user_id and passkey:
                retrieve_data(user_id, passkey)
            else:
                st.warning("Both User ID and Passkey are required.")

    elif st.session_state.page == "Login":
        login_page()

if __name__ == "__main__":
    main()
