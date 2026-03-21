import streamlit as st
from datetime import datetime, timedelta
import math

def study_scheduler_ui(save_user_data=None, current_user=None):

    st.title("📅 Study Scheduler")

    # ---- Initialize exams ----
    if "exams" not in st.session_state:
        st.session_state.exams = {}

    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

    # 🔥 Clear form button
    if st.button("➕ Add New (Clear Form)"):
        st.session_state.exam_name = ""
        st.session_state.topics_input = ""
        if "exam_date" in st.session_state:
            del st.session_state["exam_date"]
        st.rerun()

    # ---- Inputs ----
    exam_name = st.text_input("Exam Name", key="exam_name")
    exam_date = st.date_input("Exam Date", key="exam_date")
    topics_input = st.text_area("Enter topics (one per line)", key="topics_input")

    topics = [t.strip() for t in topics_input.split("\n") if t.strip()]

    # ---- Add Exam ----
    if st.button("Add Exam Schedule"):
        today = datetime.today().date()
        days_left = (exam_date - today).days

        if not exam_name:
            st.warning("Please enter exam name.")
            return

        if days_left <= 0:
            st.error("Exam date must be in the future.")
            return

        if not topics:
            st.warning("Please enter at least one topic.")
            return

        topics_per_day = math.ceil(len(topics) / days_left)
        schedule = {}

        for i in range(days_left):
            start = i * topics_per_day
            end = start + topics_per_day
            day = today + timedelta(days=i)
            schedule[str(day)] = topics[start:end]   # 🔥 string for JSON safety

        st.session_state.exams[exam_name] = {
            "exam_date": str(exam_date),  # 🔥 string for JSON
            "schedule": schedule,
            "completed_topics": []
        }

        st.success(f"{exam_name} schedule added successfully!")

    # ---- Display Exams ----
    if st.session_state.exams:
        st.divider()
        st.subheader("📚 Your Exams")

        for exam_name in list(st.session_state.exams.keys()):
            exam_data = st.session_state.exams[exam_name]

            col1, col2 = st.columns([8, 1])

            with col1:
                st.markdown(f"## 📝 {exam_name} (Exam: {exam_data['exam_date']})")

            with col2:
                if st.button("🗑", key=f"delete_{exam_name}"):
                    del st.session_state.exams[exam_name]
                    st.success(f"{exam_name} deleted successfully!")
                    st.rerun()

            total_topics = 0
            completed_count = 0

            # ---- Loop days ----
            for day, day_topics in exam_data["schedule"].items():
                if not day_topics:
                    continue

                st.markdown(f"### 📌 {day}")

                # ---- Loop topics ----
                for topic in day_topics:
                    total_topics += 1
                    key = f"{exam_name}_{day}_{topic}"
                    checked = topic in exam_data["completed_topics"]

                    if st.checkbox(topic, value=checked, key=key):
                        if topic not in exam_data["completed_topics"]:
                            exam_data["completed_topics"].append(topic)
                        completed_count += 1
                    else:
                        if topic in exam_data["completed_topics"]:
                            exam_data["completed_topics"].remove(topic)

            # ---- Progress ----
            progress = int((completed_count / total_topics) * 100) if total_topics > 0 else 0

            st.progress(progress / 100)
            st.write(f"Progress: {progress}%")
            st.divider()

    # ---- Calculate TOTAL topics covered (ALL exams) ----
    st.session_state.user_data["topics_covered"] = sum(
        len(exam["completed_topics"])
        for exam in st.session_state.exams.values()
    )

    # ---- SAVE TO DATABASE ----
    if save_user_data and current_user:
        st.session_state.user_data["exams"] = st.session_state.exams
        save_user_data(current_user, st.session_state.user_data)


# ---- Standalone Run ----
if __name__ == "__main__":
    study_scheduler_ui()