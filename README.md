# 🔐 Secure Data Encryption System

A Streamlit web application that allows users to securely **register**, **log in**, and **store/retrieve encrypted data** using a passkey-based protection mechanism. It also features a lockout mechanism after multiple failed decryption attempts.

---

## 🚀 Live Demo

[Click here to open the app](https://secure-data-encryption-bykulsoomimran.streamlit.app/)

---

## 📦 Built With

- [Streamlit](https://streamlit.io/) – for building the UI
- [Cryptography](https://cryptography.io/en/latest/) – for Fernet encryption
- [uv](https://github.com/astral-sh/uv) – for fast and modern Python dependency management

---

## ✨ Features

- 🔐 **User Authentication System**
  - Register a new account
  - Secure login system
- 🧾 **Encrypt and securely store** user data
- 🔓 **Decrypt data** using the correct passkey
- 🚫 **Lockout** after 3 failed decryption attempts
- 🔁 **Re-login required** after lockout
- 🧠 **Session-based storage** (data resets on refresh)
- 🎯 **Clean UI with guided forms**
- 🧭 **Sidebar navigation** between Home, Insert, Retrieve, and Logout pages

---

## 🧪 How It Works

1. User registers an account.
2. Logs in with the correct credentials.
3. Encrypts data using a custom passkey.
4. Data can only be retrieved by entering the same user ID and passkey.
5. After 3 wrong attempts, user is logged out and must re-login.

---