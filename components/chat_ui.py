import streamlit as st
from core.explainer import explain_concept
from core.summarizer import summarize_text
from core.quizzer import (
    generate_questions,
    solve_questions,
    evaluate_answers
)
from utils.logger import log_usage

def get_previous_messages_summary(messages, limit=3):
    context_messages = messages[-2*limit:]
    return "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in context_messages)

def chat_ui(selected_mode, selected_sub_mode=None):
    """Main chat interface with mode and optional sub-mode for Quizzer."""
    
    # Build subheader dynamically
    if selected_sub_mode:
        st.subheader(f"💬 {selected_mode} | {selected_sub_mode}")
    else:
        st.subheader(f"💬 {selected_mode}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input(f"Type your message…")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        previous_context = get_previous_messages_summary(st.session_state.messages[:-1], limit=3)
        assistant_response = ""
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            try:
                with st.spinner("💡 Study Buddy is thinking…"):
                    if selected_mode == "💡 Explainer":
                        assistant_response = explain_concept(prompt, previous_context)

                    elif selected_mode == "📰 Summarizer":
                        pdf = st.session_state.get("pdf_content")
                        user_focus = st.session_state.get("user_focus", "")

                        p = prompt.strip()
                        first_word = p.split()[0].lower() if p else ""
                        is_short = len(p.split()) <= 12
                        is_question = p.endswith("?") or first_word in ("what","why","how","when","which","who","where","explain","describe")
                        is_followup = bool(p) and (is_short or is_question)

                        if pdf:
                            if is_followup:
                                extra = f"Follow-up question: {p}. Use the previous assistant response and the PDF content to answer concisely."
                            else:
                                extra = p or user_focus

                            assistant_response = summarize_text(
                                text=pdf,
                                previous_context=previous_context,
                                user_focus=user_focus,
                                extra_instruction=extra
                            )
                        else:
                            assistant_response = summarize_text(p, previous_context)

                    elif selected_mode == "🧩 Quizzer":
                        pdf_text = st.session_state.get("pdf_content")
                        user_focus = st.session_state.get("user_focus", "")
                        text_to_use = pdf_text if pdf_text else prompt

                        if selected_sub_mode == "📝 Generate Questions":
                            st.info("Generating questions from PDF or input text...")
                            assistant_response = generate_questions(text_to_use, previous_context)
                        elif selected_sub_mode == "📖 Solve Questions":
                            st.info("Solving questions from PDF or input text...")
                            assistant_response = solve_questions(text_to_use, previous_context)
                        elif selected_sub_mode == "✅ Evaluate Answers":
                            qs_ans = prompt.split("---")
                            assistant_response = evaluate_answers(qs_ans[0].strip(), qs_ans[1].strip(), previous_context)
                        else:
                            assistant_response = "⚠️ Unknown Quizzer sub-mode."
                    else:
                        assistant_response = "⚠️ Unknown mode selected."
            except Exception as e:
                assistant_response = (
                    "❌ Sorry, there was an error processing your request. "
                    "Please try again in a few seconds.\n\n"
                    f"Error: {str(e)}"
                )
            response_placeholder.markdown(assistant_response)
            st.code(assistant_response, language="markdown")

            # Log usage with visual tracking
            log_usage(
                mode=selected_mode,
                sub_mode=selected_sub_mode,
                had_pdf=("pdf" in (previous_context or "").lower()),
                prompt_text=prompt,
                response_text=assistant_response,
                visuals_enabled=st.session_state.get("include_visuals", False),
            )
            
            # Feedback buttons            
            st.markdown("**Was this response helpful?**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Helpful", key=f"fb_yes_{len(st.session_state.messages)}"):
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎 Not Helpful", key=f"fb_no_{len(st.session_state.messages)}"):
                    st.info("We appreciate your input! Please let us know how we can improve.")

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})