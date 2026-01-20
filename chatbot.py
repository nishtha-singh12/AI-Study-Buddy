import streamlit as st
import requests

HF_API_KEY = st.secrets["HF_API_KEY"]
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}

def get_ai_response(question: str, profile: dict) -> str:
    """
    Returns personalized study advice from Qwen2.5-7B-Instruct.
    profile keys: study_hours, sleep_hours, mental_health, attendance, diet, social_media, prediction_score
    """

    # ---------------- Set defaults ----------------
    profile_defaults = {
        "study_hours": 3,
        "sleep_hours": 7,
        "mental_health": 7,
        "attendance": 80,
        "diet": "Average",
        "social_media": 2,
        "prediction_score": 50
    }
    profile_complete = {**profile_defaults, **profile}

    prompt = f"""
You are a friendly AI Study Buddy. Your goal is to provide short, practical, and encouraging study advice based on the student's data.

Student Profile:
Study Hours: {profile_complete['study_hours']}
Sleep Hours: {profile_complete['sleep_hours']}
Mental Health: {profile_complete['mental_health']}
Attendance: {profile_complete['attendance']}
Diet: {profile_complete['diet']}
Social Media: {profile_complete['social_media']}

Predicted Exam Score: {profile_complete['prediction_score']}

Rules:
DO NOT REFERENCE SUBJECTS (maths, science, english etc) INDIVIUALLY AND DO NOT INCLUDE THEM IN OUTPUT
FOCUS ON OVERALL STUDY HABITS, PREDICTED SCORE AND LIFESTYLE FACTORS

1.Keep responses within 6-7 lines for general advice. 
  Allow detailed and structured responses for study plans, timetables, or when the user explicitly asks for detail.
2. DO NOT provide exam solutions or answers.
3. If predicted score is missing, give general habit-based advice.
4. Be gentle, motivating, and professional.
5. Suggest 7-8 hours of sleep if sleep hours are low.
6. Suggest a personalized study plan when the student asks for it (according to their profile).
7. Avoid generic statements like "lifestyle is balanced" if any factors are low or high.
8. You should support students academically and emotionally.
9. Answer consistently in the same style and format every time.

Format the output clearly with headings, subheadings, and bullet points for readability.

Numeric Interpretation:
- Study Hours: higher is better.
- Sleep Hours: 7-8 is ideal; lower needs improvement.
- Mental Health: higher is better; do not give warnings if high.
- Attendance: > 75 is good , if less suggest improvement.
- Social Media: higher values are negative; lower is better.
- Predicted Score: higher is better.

User Question:
{question}

Answer:
"""
    
    payload = {
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "max_new_tokens": 200,
    "temperature": 0.7
    }

    try:
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=120)
        result = response.json()

        if isinstance(result, dict) and "error" in result:
            return f"Error from API: {result['error']}"
        
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()
        
        return "No valid response returned from the API."
    except Exception as e:
        return f"API Error: {e}"