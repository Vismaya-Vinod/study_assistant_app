import streamlit as st
import json

USERS_FILE = "users.json"

VALID_USERS = {
    "test@example.com": "1234",
    "user@example.com": "password"
}

def login_ui():
    st.title("🔐 Login to SGPA")

    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    col1, col2 = st.columns([3,1])

    # LOGIN
    with col1:
        if st.button("Login"):
            try:
                with open(USERS_FILE, "r") as f:
                    users = json.load(f)
            except:
                users = {}

            if email in users:
                if isinstance(users[email], dict):
                    real_password = users[email].get("password", "")
                else:
                    real_password = users[email]

                if real_password == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = email
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Wrong password")
            else:
                st.error("❌ User not found")

    # RESET FIELDS BUTTON
    with col2:
        if st.button("Reset"):
            st.session_state.clear()
            st.info("Fields cleared.")

    # 🔥 THIS PART MUST BE AT SAME INDENT LEVEL AS col1/col2
    st.markdown("---")
    st.subheader("🔁 Forgot Password?")

    reset_email = st.text_input("Enter your registered email", key="reset_email")
    new_password = st.text_input("Enter new password", type="password", key="reset_pass")

    if st.button("Update Password"):
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
        except:
            users = {}

        if reset_email in users:
            if isinstance(users[reset_email], dict):
                users[reset_email]["password"] = new_password
            else:
                users[reset_email] = new_password

            with open(USERS_FILE, "w") as f:
                json.dump(users, f, indent=2)

            st.success("✅ Password updated! You can now login.")
        else:
            st.error("❌ Email not found")