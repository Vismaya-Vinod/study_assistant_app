import streamlit as st

def dashboard_ui():
    st.title("📊 Dashboard")

    current_user = st.session_state.get("current_user", "User")
    user_data = st.session_state.get("user_data", {})
    
    pdf_count = user_data.get("pdf_uploaded", 0)
    topics_count = user_data.get("topics_covered", 0)

    # ---- Welcome ----
    st.write(f"Welcome back, **{current_user}** 👋")

    # ---- Main Stats Box ----
    st.markdown(
        f"""
        <div style="
            padding:20px; 
            background-color:#2c2c3a; 
            border-radius:10px; 
            border: 1px solid #c78fff;
            color:#f5f5f5;
            width: 100%;
        ">
            <h3 style="margin-bottom: 20px;">Your Study Status</h3>
            <div style="display: flex; justify-content: space-around;">
                <div style="text-align:center;">
                    <div style="font-size: 32px; font-weight:bold;">{pdf_count}</div>
                    <div>📚 PDFs Uploaded</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size: 32px; font-weight:bold;">{topics_count}</div>
                    <div>📅 Topics Covered</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    