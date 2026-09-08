import streamlit as st
import requests
import re

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

def get_ai_response(question: str, profile: dict, chat_history: list) -> str:
    """
    Returns personalized study advice from qwen/qwen3.6-27b.
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
10. Write the predicted score with exactly 2 decimal places in responses (e.g., 87.45).
11. Only mention the Predicted Score when the question is directly about performance, 
    progress, exam readiness, or study strategy. For unrelated questions (food, sleep, 
    motivation, daily routine), do NOT restate the score — just answer the actual question.
12. Never repeat the same boilerplate structure (e.g. "Current Status Overview") in every 
    single reply. Vary your opening based on what's actually being asked — sometimes a 
    direct answer needs no status recap at all.
13. If the student ask for a specific goal (e.g. a competitive exam, an admission target)
    acknowledge the goal explicitly and tailor advice toward sustained long term consistency
    and stamina-building habits appropriate for that kind of goal - without giving 
    subject-specific content, exam solutions, or naming the exam's syllabus

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
    messages = [{"role": "system", "content": prompt}]
 
    # Include recent conversation turns so the model has memory (last 6 messages = ~3 exchanges)
    if chat_history:
        for msg in chat_history[-6:]:
            if msg["role"] in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})
 
    messages.append({"role": "user", "content": question})

    payload = {
    "model": "qwen/qwen3.6-27b",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 600,
    "temperature": 0.7,
    "reasoning_effort": "none"
    }

    try:
        response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload, timeout=120)
        result = response.json()

        if isinstance(result, dict) and "error" in result:
            return f"Error from API: {result['error']}"
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"].strip()
            content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
            return content
        
        return "No valid response returned from the API."
    except Exception as e:
        return f"API Error: {e}"

