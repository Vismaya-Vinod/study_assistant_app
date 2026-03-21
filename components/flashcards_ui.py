import streamlit as st
from core.flashcards import generate_flashcards

def flashcards_ui():

    st.subheader("📚 AI Flashcards")

    if not st.session_state.get("pdf_content"):
        st.warning("Upload and summarize a PDF first.")
        return

    if st.button("✨ Generate Flashcards"):

        with st.spinner("Generating flashcards..."):
            response = generate_flashcards(
                st.session_state.pdf_content
            )

        cards = response.split("Q:")
        flashcards = []

        for card in cards:
            if "A:" in card:
                q, a = card.split("A:", 1)
                flashcards.append({
                    "question": q.strip(),
                    "answer": a.strip()
                })

        st.session_state.flashcards = flashcards

    if "flashcards" in st.session_state:
        st.divider()
        for i, card in enumerate(st.session_state.flashcards):
            with st.expander(f"Card {i+1}: {card['question']}"):
                st.write(card["answer"])