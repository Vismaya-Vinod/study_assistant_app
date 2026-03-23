import streamlit as st
import json
import os
from PIL import Image

# Components
from components.sidebar import sidebar_ui
from components.chat_ui import chat_ui
from components.flashcards_ui import flashcards_ui
from components.dashboard_ui import dashboard_ui
from components.study_scheduler_ui import study_scheduler_ui
from components.pdf_handler import handle_pdf_upload

# Core Quizzer
from core.quizzer import generate_questions

# --- Page Setup ---
img = Image.open("assets/sgpa_logo.png")
st.set_page_config(page_title="SGPA", page_icon=img, layout="wide")

# --- Users file ---
USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f, indent=2)

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "pdf_content" not in st.session_state:
    st.session_state.pdf_content = None
if "exams" not in st.session_state:
    st.session_state.exams = {}

# --- Helper Functions ---
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_user_data(email):
    users = load_users()
    data = users.get(email, {})

    # 🔥 Handle old format (email: password)
    if isinstance(data, str):
        data = {
            "password": data,
            "pdf_uploaded": 0,
            "topics_covered": 0,
            "exams": {},
            "pdf_content": None
        }
        users[email] = data
        save_users(users)

    # Defaults
    data.setdefault("password", "")
    data.setdefault("pdf_uploaded", 0)
    data.setdefault("topics_covered", 0)
    data.setdefault("exams", {})
    data.setdefault("pdf_content", None)

    return data

def save_user_data(email, data):
    users = load_users()
    users[email] = data

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# --- Login UI ---
def login_ui():
    st.title("🔐 Login to SGPA")

    email = st.text_input("Email")  
    password = st.text_input("Password", type="password")  

    col1, col2 = st.columns(2)  

    # --- LOGIN ---
    with col1:
     if st.button("Login"):
        users = load_users()

        if email in users:
            user_data = load_user_data(email)

            if user_data["password"] == password:

                # 🔥 CLEAR SESSION (correct place)
                for key in list(st.session_state.keys()):
                    del st.session_state[key]

                # ✅ Now set fresh session
                st.session_state.logged_in = True
                st.session_state.current_user = email

                st.session_state.pdf_content = None
                st.session_state.questions = ""

                st.session_state.user_data = user_data
                st.session_state.exams = user_data.get("exams", {})

                st.success("✅ Logged in!")
                st.rerun()

            else:
                st.error("❌ Wrong password")
        else:
            st.error("❌ User not found")

    # 🔥 ADD THIS ONLY (nothing else touched)
    st.markdown("---")
    st.subheader("🔁 Forgot Password?")

    reset_email = st.text_input("Enter your registered email", key="reset_email")
    new_password = st.text_input("Enter new password", type="password", key="reset_pass")

    if st.button("Update Password"):
        users = load_users()

        if reset_email in users:
            # handle both formats (dict or string)
            if isinstance(users[reset_email], dict):
                users[reset_email]["password"] = new_password
            else:
                users[reset_email] = new_password

            save_users(users)
            st.success("✅ Password updated! You can now login.")
        else:
            st.error("❌ Email not found")

    # REGISTER
    with col2:
        if st.button("Register"):
            users = load_users()

            if email in users:
                st.error("❌ User already exists")
            else:
                users[email] = {
                    "password": password,
                    "pdf_uploaded": 0,
                    "topics_covered": 0,
                    "exams": {},
                    "pdf_content": None
                }
                save_users(users)
                st.success("✅ Registered! Now login.")

# --- Main App ---
def app_ui():
    selected_mode, _ = sidebar_ui()
    st.title("Study Guide & Personal Assistant")

    # ---- Load exams into session ----
    if not st.session_state.exams:
        st.session_state.exams = st.session_state.user_data.get("exams", {})

    # ---- PDF Handling ----
    pdf_text = st.session_state.user_data.get("pdf_content", None)

    uploaded_text = handle_pdf_upload()

    if uploaded_text:
        pdf_text = uploaded_text
        st.session_state.pdf_content = pdf_text
        st.session_state.user_data["pdf_content"] = pdf_text

        # ✅ Only count NEW file
        current_file = st.session_state.get("last_upload_name")

        if st.session_state.get("counted_file") != current_file:
            st.session_state.user_data["pdf_uploaded"] += 1
            st.session_state["counted_file"] = current_file

        # ✅ Save ONLY when new upload happens
        save_user_data(st.session_state.current_user, st.session_state.user_data)

    st.divider()

    # ---- Routing ----
    if selected_mode in ["💡 Explainer", "📰 Summarizer"]:
        chat_ui(selected_mode, None)

    elif selected_mode == "🧩 Quizzer":
        st.header("🧩 Quizzer")

        if not pdf_text:
            st.info("📌 Upload a PDF first!")
        else:
            if st.button("📝 Generate Questions"):
                with st.spinner("Generating questions..."):
                    st.session_state.questions = generate_questions(pdf_text)
                st.text_area("Generated Questions", st.session_state.questions, height=300)

    elif selected_mode == "📚 Flashcards":
        flashcards_ui()

    elif selected_mode == "🗓️ Study Scheduler":
        study_scheduler_ui(save_user_data, st.session_state.current_user)

        # Save scheduler data
        st.session_state.user_data["exams"] = st.session_state.exams
        save_user_data(st.session_state.current_user, st.session_state.user_data)

    elif selected_mode == "📊 Dashboard":
        dashboard_ui()

# --- Run ---
if st.session_state.logged_in:
    app_ui()
else:
    login_ui()