# app.py

import streamlit as st
from encryption import generate_key, get_fernet, encrypt_text, decrypt_text
from utils import hash_passkey
from auth import login_user, register_user

# --- Session Initialization ---
if "fernet_key" not in st.session_state:
    st.session_state.fernet_key = generate_key()
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = {}
if "authorized_user" not in st.session_state:
    st.session_state.authorized_user = None
if "page" not in st.session_state:
    st.session_state.page = "Login"

fernet = get_fernet(st.session_state.fernet_key)


# --- UI Pages ---
def show_login():
    st.markdown("### 🔐 Login to Secure Data System")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if login_user(username, password):
                st.session_state.authorized_user = username
                st.success("Login successful!")
                st.session_state.page = "Home"
                st.rerun()
            else:
                st.error("Invalid username or password.")

    st.markdown("---")
    st.info("Don't have an account?")
    if st.button("Create New Account"):
        st.session_state.page = "Register"
        st.rerun()


def show_register():
    st.markdown("### 📝 Create New Account")
    with st.form("register_form"):
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            success, msg = register_user(username, password)
            if success:
                st.success(msg)
                st.session_state.page = "Login"
                st.rerun()
            else:
                st.error(msg)

    if st.button("⬅ Back to Login"):
        st.session_state.page = "Login"
        st.rerun()


def insert_data_ui():
    st.subheader("📥 Store Secure Data")

    user_id = st.text_input("Enter Data Identifier")
    data = st.text_area("Enter Data to Encrypt")
    passkey = st.text_input("Set a Passkey", type="password")

    if st.button("Encrypt & Store"):
        if user_id and data and passkey:
            encrypted = encrypt_text(data, fernet)
            st.session_state.stored_data[user_id] = {
                "encrypted_text": encrypted,
                "passkey": hash_passkey(passkey)
            }
            st.success(f"Data stored successfully for: {user_id}")
        else:
            st.warning("All fields are required.")


def retrieve_data_ui():
    st.subheader("🔓 Retrieve Encrypted Data")

    user_id = st.text_input("Enter Your Data Identifier")
    passkey = st.text_input("Enter Your Passkey", type="password")

    if st.button("Decrypt"):
        data_store = st.session_state.stored_data
        attempts = st.session_state.failed_attempts

        if user_id not in data_store:
            st.error("No data found for this ID.")
            return

        if attempts.get(user_id, 0) >= 3:
            st.warning("Too many failed attempts. Please re-login.")
            st.session_state.page = "Login"
            st.session_state.authorized_user = None
            st.rerun()
            return

        if hash_passkey(passkey) == data_store[user_id]["passkey"]:
            decrypted = decrypt_text(data_store[user_id]["encrypted_text"], fernet)
            st.success(f"Decrypted Data: {decrypted}")
            attempts[user_id] = 0
        else:
            attempts[user_id] = attempts.get(user_id, 0) + 1
            st.error(f"Incorrect passkey. Attempts left: {3 - attempts[user_id]}")


def home():
    st.title("🔒 Welcome to Secure Data Encryption")
    st.write(f"👋 Logged in as: `{st.session_state.authorized_user}`")
    st.success("Use the sidebar to navigate.")


# --- Main Function ---
def main():
    if not st.session_state.authorized_user and st.session_state.page != "Register":
        show_login()
        return
    elif st.session_state.page == "Register":
        show_register()
        return

    st.sidebar.title("📂 Menu")
    st.session_state.page = st.sidebar.radio(
        "Navigation",
        ["Home", "Insert Data", "Retrieve Data", "Logout"],
        index=["Home", "Insert Data", "Retrieve Data", "Logout"].index(st.session_state.page)
    )

    if st.session_state.page == "Home":
        home()
    elif st.session_state.page == "Insert Data":
        insert_data_ui()
    elif st.session_state.page == "Retrieve Data":
        retrieve_data_ui()
    elif st.session_state.page == "Logout":
        st.session_state.authorized_user = None
        st.session_state.page = "Login"
        st.success("Logged out successfully!")
        st.rerun()


if __name__ == "__main__":
    main()

