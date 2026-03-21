import streamlit as st
import time

def sidebar_ui():
    """Sidebar with mode and Quizzer sub-mode selectors, and core controls."""

    # 🔥 Top section: Logo + Logout side by side
    col1, col2 = st.sidebar.columns([3, 1])

    with col1:
        st.image("assets/sgpa_logo.png", width=60)

    with col2:
        if st.button("🚪", help="Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()

    # Mode selection
    st.sidebar.markdown("### 🧩 Choose Mode")
    mode = st.sidebar.selectbox(
        "Select a core function:",
        ["💡 Explainer", "📰 Summarizer", "🧩 Quizzer", "📚 Flashcards", "🗓️ Study Scheduler", "📊 Dashboard"],
        index=0
    )

    # Nested selector for Quizzer
    sub_mode = None
    # if mode == "🧩 Quizzer":
    #     st.sidebar.markdown("### ✨ Quizzer Action")
    #     sub_mode = st.sidebar.selectbox(
    #         "Choose Quizzer action:",
    #         ["📝 Generate Questions"],
    #         index=0
    #     )

    st.sidebar.caption("AI-POWERED STUDY COMPANION")

    return mode, sub_mode