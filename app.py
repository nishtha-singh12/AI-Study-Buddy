import streamlit as st
import random
import numpy as np
import joblib
from chatbot import get_ai_response

import warnings
warnings.filterwarnings("ignore")

# ---------------------------- Page config -------------------------------------------
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------- Load ML model -----------------------------------------
ml_model = joblib.load("Student_performance_analysis.pkl")

# ------------------------------- Header -------------------------------------------------
st.markdown("<h1 style='text-align:center;'>🎓 AI Study Buddy</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:gray;'>Smart Student Performance Analytics & Assistant</p>",
    unsafe_allow_html=True
)
st.divider()

# ---------------------- SIDEBAR -----------------------------------------------------------
st.sidebar.header("📌 Student Details")

gender = st.sidebar.selectbox("Gender", ["Select", "Male", "Female"])
study_hours = st.sidebar.slider("Study Hours Per Day", 0.0, 12.0)
attendance = st.sidebar.slider("Attendance (%)", 0, 100)
mental_health = st.sidebar.slider("Mental Health Rating (1-10)", 1, 10)
sleep_hours = st.sidebar.slider("Sleep Hours", 0.0, 12.0)
diet = st.sidebar.selectbox("Diet Quality", ["Select", "Poor", "Average", "Good"])
part_time_job = st.sidebar.selectbox("Part-Time Job", ["Select", "No", "Yes"])
parent_edu = st.sidebar.selectbox("Parental Education Level", ["Select", "High School", "Bachelor", "Master"])
extra = st.sidebar.selectbox("Extracurricular Participation", ["Select", "No", "Yes"])
social_media = st.sidebar.slider("Social Media Hours", 0.0, 8.0)


if "profile" not in st.session_state:
    st.session_state.profile = {}

if "predicted_score" not in st.session_state:
    st.session_state.predicted_score = None

# ----------------------- TABS ---------------------------------------
tab1, tab2 = st.tabs(["📊 Prediction Score", u"\U0001F916 Chatbot"])

# ------------ TAB 1 — PREDICTION SCORE ------------------------------
with tab1:

    col1, col2 = st.columns([3, 2], gap="large")

    # ------------------ Today's Task ------------------
    with col1:
        st.subheader("📝 Today's Task")

        if "daily_task" not in st.session_state:
            st.session_state.daily_task = ""

        st.session_state.daily_task = st.text_area(
            "Write your daily plan",
            value=st.session_state.daily_task,
            height=160,
            placeholder="Write your plan for today..."
        )

    # ------------------ Student Profile -------------------
    with col2:
        st.subheader("👤 Student Profile")

        st.session_state.profile = {
            "Gender": gender,
            "Study Hours": study_hours,
            "Attendance": attendance,
            "Mental Health": mental_health,
            "Sleep Hours": sleep_hours,
            "Diet": diet,
            "Part-Time Job": part_time_job,
            "Parent Education": parent_edu,
            "Extracurricular": extra,
            "Social Media": social_media
        }

        # Compact display using HTML
        profile_html = ""
        for k, v in st.session_state.profile.items():
            profile_html += f"<p style='margin:2px 0'><b>{k}:</b> {v}</p>"

        st.markdown(profile_html, unsafe_allow_html=True)

    # ------------------ Prediction ---------------------
    if st.button("🔍 Predict Exam Score"):

        # Encoding
        gender_enc = 1 if gender == "Male" else 0
        diet_enc = ["Select", "Poor", "Average", "Good"].index(diet)
        part_time_job_enc = 1 if part_time_job == "Yes" else 0
        parent_edu_enc = ["Select", "High School", "Bachelor", "Master"].index(parent_edu)
        extra_enc = 1 if extra == "Yes" else 0

        input_data = np.array([[
            gender_enc,
            study_hours,
            attendance,
            mental_health,
            sleep_hours,
            diet_enc,
            part_time_job_enc,
            parent_edu_enc,
            extra_enc,
            social_media
        ]])

        prediction = ml_model.predict(input_data)[0]
        prediction = max(0, min(100, prediction))
        st.session_state.predicted_score = prediction

        st.success(f"🎯 **Predicted Exam Score:** {prediction:.2f}")

        # ------------------ Motivation ------------------
        quotes = [
            "Small improvements every day lead to big results.",
            "Consistency matters more than perfection.",
            "Your effort today shapes your success tomorrow.",
            "Focus on progress, not comparison.",
            "One good habit can change everything.",
            "Believe in the process, not just the outcome.",
            "Hard work beats talent when talent doesn't work hard.",
            "Learning is a journey, not a race.",
            "Discipline is choosing what you want most.",
            "Success starts with showing up."
        ]

        if prediction < 95:
            st.info(f"💡 **Motivation:** {random.choice(quotes)}")

        st.divider()

        # ------------------ Lifestyle Impact ------------------
        st.markdown("### ✨ Lifestyle Impact Summary")
        
        insights = []
        lifestyle_issues=[]

        if study_hours < 3: 
            insights.append("📚 Low study hours may reduce concept clarity.")
            lifestyle_issues.append("Low study hours")

        if attendance < 75:
            insights.append("🏫 Low attendance affects learning consistency.")
            lifestyle_issues.append("Low attendance")

        if mental_health < 4:
            insights.append("💙 Mental stress lowers academic performance.")
            lifestyle_issues.append("Mental well-being")

        if sleep_hours < 5:
            insights.append("😴 Insufficient sleep may reduce focus and memory retention.")
            lifestyle_issues.append("Insufficient sleep")

        if social_media > 1.5:
            insights.append("📱 Excessive social media distracts from studies.")
            lifestyle_issues.append("High social media usage")

        if diet == "Poor" :
            insights.append("🥗 Poor diet may reduce energy.")
            lifestyle_issues.append("Poor diet reduces energy")


        if insights:
            for i in insights:
                st.write(i)

        if prediction >= 85 and lifestyle_issues:
            issue_text = ", ".join(lifestyle_issues)
            st.write(f"⚠️ Your study effort is strong, but issues such as **{issue_text}** may impact long-term performance and well-being.")

        if not insights:
            st.success("✅ Your lifestyle habits appear balanced and supportive for academic success.")

        st.divider()

        # ------------------ Study Plan & Daily Time Table ------------------
        st.subheader("📝 Personalized Study Plan & Daily Timetable")

        with st.expander("📌 Personalized Study Plan"):
            if prediction < 60:
                st.markdown("""
                - Study 2-3 hours daily using short, focused sessions to strengthen foundational understanding.
                - Revise fundamentals and previously covered material.
                - Use active learning methods like self-testing and summaries.
                - Improve sleep to 7-8 hours to support focus and memory.
                - Reduce social media gradually and replace with revision time.
                - Maintain regular attendance to avoid learning gaps.
                """)

            elif prediction > 90:
                st.markdown("""
                - Study 4-5 hours daily with emphasis on refinement.
                - Practice advanced questions and timed mock sessions.
                - Maintain strong routines for sleep, diet, and mental health.
                - Avoid overstudying; include breaks to sustain performance.
                - Focus on confidence, accuracy, and consistency.
                """)
            else:
                st.markdown("""
                - Study 3-4 hours daily with a mix of revision and practice.
                - Focus on consistency rather than increasing pressure.
                - Identify weak areas from past assessments and revise them.
                - Keep sleep and mental health stable to avoid burnout.
                - Balance academics with extracurricular activities.
                """)

        with st.expander("📌 Daily Timetable"):
            if prediction < 60:
                st.markdown("""
                - **Recommended Study:** 2-3 hours/day
                            
                - **Morning:** 
                    Wake up and begin the day with personal hygiene and breakfast. 
                    Engage in a focused study session of approximately **1 hour**, emphasizing foundational concepts and revision.
                            
                - **Afternoon:** 
                    Attend classes or learning sessions. Take time for lunch, rest, and a short hobby or activity. 
                    If possible, do a **quick 30-minute review** of what you studied in the morning.
                            
                - **Evening:** 
                    Second study session or practice questions (about 1 hour). Take a short break if needed to refresh your mind.
                            
                - **Night:** 
                    Relax and unwind, prepare for the next day. Aim for **7-8 hours of sleep** to optimize mental clarity and overall well-being.
                """)

            elif prediction > 90:
                st.markdown("""
                - **Recommended Study:** 4-5 hours/day
                            
                - **Morning:** 
                    Wake up, freshen up, and have breakfast. 
                    Begin a **deep study or practice session (1.5-2 hours)**, focusing on refinement and problem-solving.
                            
                - **Afternoon:** 
                    Attend classes or learning sessions. Take lunch and allocate time for hobbies, light review, or physical activity. 
                    Include a brief review session to reinforce morning learning.
                                        
                - **Evening:** 
                    Study, recap, or practice for **1.5-2 hours**, emphasizing weak areas or timed exercises to enhance performance.
                            
                - **Night:** 
                    Relax and prepare for the next day. Ensure **7-8 hours of sleep** to maintain cognitive performance and well-being.   
                """)                     
                
            else :
                st.markdown("""
                - **Recommended Study:** 3-4 hours/day
                            
                - **Morning:** 
                    Wake up, engage in light stretching or exercise, and have breakfast. 
                    Begin a **focused study session of 1-2 hours**, covering review topics or problem-solving exercises.
                            
                - **Afternoon:** 
                    Attend classes or learning sessions. Follow with lunch and free time for hobbies or relaxation. 
                    Include a **short review session (30-45 minutes)** to consolidate learning.   
                                     
                - **Evening:** 
                    Conduct a study/practice/recap session lasting **1-1.5 hours**. 
                    Utilize active learning methods such as note summarization or self-testing.
                            
                - **Night:** 
                    Relax, engage in hobbies or light recreational activities, and prepare for the next day. Maintain **7-8 hours of sleep.**   
                """)


# ------------------- TAB 2 — CHATBOT --------------------------
with tab2:
    st.subheader(u"\U0001F916 AI Study Companion")

    # Container for chat messages
    chat_container = st.container()

    # Input box
    user_input = st.chat_input("Ask about studies, focus, planning, or performance")

    # Initialize chat history if needed
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Process user input
    if user_input:
        profile_for_ai = {
            "study_hours": study_hours,
            "sleep_hours": sleep_hours,
            "mental_health": mental_health,
            "attendance": attendance,
            "diet": diet,
            "social_media": social_media,
            "prediction_score": st.session_state.predicted_score
        }

        # Append user message
        st.session_state.chat_history.append(("user", user_input))

        # Get AI response
        try:
            with st.spinner("Study Buddy is thinking..."):
                ai_reply = get_ai_response(user_input, profile_for_ai)
        except Exception as e:
            ai_reply = f"Error: {e}"

        st.session_state.chat_history.append(("assistant", ai_reply))

    # Display chat messages
    for role, msg in st.session_state.chat_history:
        with chat_container:
            with st.chat_message(role):
                st.write(msg)
