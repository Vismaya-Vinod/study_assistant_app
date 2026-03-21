import streamlit as st
from PyPDF2 import PdfReader

def handle_pdf_upload():
    """
    Handles PDF upload with editable extraction.
    Returns: final_text
    """

    uploaded_file = st.file_uploader("📚 Upload your study material (PDF)", type=["pdf"])

    # Initialize counter if missing
    if "pdf_uploaded" not in st.session_state:
        st.session_state["pdf_uploaded"] = 0

    pdf_text = ""

    if uploaded_file:

        file_name = uploaded_file.name

        # Check if this is a NEW upload
        is_new_upload = st.session_state.get("last_upload_name") != file_name

        if is_new_upload:
            try:
                with st.spinner("Extracting text from PDF..."):
                    reader = PdfReader(uploaded_file)
                    for page in reader.pages:
                        pdf_text += page.extract_text() or ""

                st.success("✅ PDF processed successfully!")

                # Store raw + preview
                st.session_state["pdf_raw"] = pdf_text
                st.session_state["pdf_edited"] = pdf_text[:3000]
                st.session_state["last_upload_name"] = file_name

                # 🔥 Increment upload counter ONLY once per new file
                st.session_state["pdf_uploaded"] += 1

            except Exception as e:
                st.error(f"❌ Error reading PDF: {str(e)}")
                return None

        # Editable preview area
        st.markdown("### 📝 Review & Edit Extracted Text")
        st.text_area(
            "Edit extracted text below:",
            value=st.session_state.get("pdf_edited", ""),
            height=300,
            key="pdf_edited"
        )

        return st.session_state.get("pdf_edited", "")

    return None