import streamlit as st
from core.quizzer import generate_questions, solve_questions, evaluate_answers

def quizzer_ui(sub_mode="📝 Generate Questions"):
    st.header("🧩 Quizzer")

    pdf_text = st.session_state.get("pdf_content", "")

    if not pdf_text:
        st.info("Upload a PDF first to use the Quizzer!")
        return

    # For now, just show the PDF text preview and action
    st.write("PDF is loaded. Ready to generate questions.")

    # You can add UI for sub_mode actions here
    if sub_mode == "📝 Generate Questions":
        if st.button("Generate Questions"):
            questions = generate_questions(pdf_text)
            st.text_area("Generated Questions", questions, height=300)