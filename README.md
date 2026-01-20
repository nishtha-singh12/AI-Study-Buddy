# 🎓 AI STUDY BUDDY

AI Study Buddy is a **professional, data-driven academic support system** designed to assist students in improving their academic performance through **predictive analytics and personalized AI guidance**. The system integrates machine learning–based exam score prediction with a large language model (LLM) accessed via the Hugging Face API to deliver study recommendations, lifestyle insights, and motivational support.

## 📌 Project Overview

**AI Study Buddy** is an interactive, data-driven platform that predicts student performance and provides personalized study guidance through its AI chatbot - **AI Study Companion**. It includes a **“Today’s Task”** section where students can write, plan, and track their daily goals.

The platform uses student data—including gender, study hours, attendance, mental health, sleep, diet, part-time work, parental education, extracurricular activity, and social media usage—to generate **predicted exam scores, personalized study plans, daily timetables, motivational guidance** and **lifestyle insights**.

## 🎯 Key Features

- **Predict Academic Performance:** Use machine learning models to predict student scores based on study habits, attendance, and lifestyle factors.
- **Analyze Lifestyle Impact:** Evaluate how study hours, sleep hours, diet, mental health, attendance, and social media usage affect academic performance.
- **Provide Personalized Study Plans:** Generate personalized study plan and daily time table according to student's predicted score.
- **Offer Motivational Guidance:** Give tips and encouragement to help students improve their study habits and stay motivated.
- **Enable Daily Task Management:** Allow students to plan, write, and track their daily tasks effectively.
- **AI Student Companion:** A personalized AI chatbot powered by Qwen/Qwen2.5-7B-Instruct via Hugging Face API, providing academic and lifestyle guidance based on the student’s profile.


## 🛠️ Tools & Technologies Used

| Component                  | Technology / Library                                                               |
|--------------------------  |------------------------------------------------------------------------------------|
| Programming Language       | Python                                                                             |
| Data Processing            | Pandas, NumPy                                                                      |
| Development Environment    | Jupyter Notebook (EDA, preprocessing & model training)                             |
| Visualization              | Matplotlib, Seaborn                                                                |
| Machine Learning Models    | Linear Regression, Decision Tree Regressor, Random Forest Regressor (Scikit-learn) |
| Model Persistence          | Joblib, Pickle (for saving/loading models)                                         |
| AI Assistant (Chatbot)     | Qwen/Qwen2.5-7B-Instruct via Hugging Face API                                      |
| API Requests               | `requests` library for Hugging Face API calls                                      |
| Web Framework              | Streamlit                                                                          |


## ⚙️ How It Works

1. Students enter academic and lifestyle details (sidebar).
2. The system processes the data and predicts exam performance using a trained ML model.
3. Motivational feedback and a lifestyle impact summary highlight factors affecting performance.
4. A personalized study plan and daily timetable are generated based on the predicted score.
5. AI Study Companion chatbot (Tab2) provides guidance using the student’s profile and prediction, powered by a large language model (Qwen/Qwen2.5-7B-Instruct) accessed via the Hugging Face API.


## 📂 Project Structure

```
AI-Study-Buddy/
│
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
├── app.py                            # Main Streamlit application
├── chatbot.py                        # AI Study Companion chatbot logic
├── model_pipeline.ipynb              # EDA, preprocessing, ML training & evaluation
├── Student_performance_analysis.pkl  # Saved trained ML model (Joblib)
├── student_habits_performance.csv    # Student study & lifestyle dataset
```

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nishtha-singh12/AI-Study-Buddy.git
   cd AI-Study-Buddy
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app locally:**
   ```bash
   streamlit run app.py
   ```
## 🌐 Deployment
- **Platform** : Streamlit
- **URL** : https://ai-study-buddy-01.streamlit.app/
