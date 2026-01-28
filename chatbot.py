import streamlit as st
import numpy as np
import joblib

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Mental Health Chatbot", page_icon="💙")

# ================= LOAD MODELS =================
stress_model = joblib.load("stress_model.pkl")
depression_model = joblib.load("depression_model.pkl")

# ================= QUESTIONS =================
stress_questions = [
    "How often do you feel overwhelmed by daily responsibilities?",
    "How often do you feel nervous or anxious?",
    "How difficult is it for you to relax?",
    "How often do you feel irritated or angry?",
    "Do you feel mentally exhausted at the end of the day?",
    "Are you having difficulty sleeping due to stress?",
    "How often do you feel pressure related to work or studies?",
    "How often do you worry about things beyond your control?",
    "Do you experience physical symptoms like headaches or fatigue?",
    "How difficult is it to concentrate because of stress?"
]

depression_questions = [
    "How often do you feel sad or hopeless?",
    "How often do you lose interest in activities you enjoy?",
    "How often do you feel tired or low in energy?",
    "How often do you have difficulty concentrating?",
    "How often do you feel worthless or guilty?",
    "How often do you have sleep problems?",
    "How often do you notice appetite or weight changes?",
    "How often do you feel restless or slowed down?",
    "How often do you avoid social interactions?",
    "How often do you feel life is meaningless?"
]

# ================= FUNCTIONS =================
def ask_questions(questions, key_prefix):
    answers = []
    for i, q in enumerate(questions):
        ans = st.slider(
            q,
            0, 4, 2,
            format="%d",
            help="0 = Never | 4 = Always",
            key=f"{key_prefix}_{i}"
        )
        answers.append(ans)
    return np.array(answers).reshape(1, -1)

# ================= UI =================
st.title("🤖 Mental Health Assessment Chatbot")
st.markdown(
    """
    💙 This tool is **not a medical diagnosis**.  
    Please answer honestly for a general self-assessment.
    """
)

assessment = st.radio(
    "What would you like to assess?",
    ("Stress", "Depression")
)

# ================= STRESS =================
if assessment == "Stress":
    st.subheader("🧠 Stress Assessment")
    X = ask_questions(stress_questions, "stress")

    if st.button("🔍 Predict Stress Level"):
        result = stress_model.predict(X)[0]
        st.success(f"📊 Your Stress Level: **{result}**")

        if result in ["High", "Severe"]:
            st.warning("⚠️ You may be experiencing high stress.")
            st.info("💬 Consider relaxation techniques or professional support.")
        else:
            st.success("✅ Your stress seems manageable. Keep taking care 🌱")

        st.markdown("### 📝 Summary")
        st.write(f"Your stress level assessment is **{result}**.")
        st.write("Remember to take breaks, stay hydrated, and practice mindfulness 💙")

# ================= DEPRESSION =================
if assessment == "Depression":
    st.subheader("💙 Depression Assessment")
    X = ask_questions(depression_questions, "depression")

    if st.button("🔍 Predict Depression Level"):
        result = depression_model.predict(X)[0]
        st.success(f"📊 Your Depression Level: **{result}**")

        if result in ["Moderate", "Severe"]:
            st.warning("⚠️ You may be experiencing emotional distress.")
            st.info("💬 Please consider speaking with a mental health professional.")
        else:
            st.success("✅ Your responses suggest things are okay 🌈")

        st.markdown("### 📝 Summary")
        st.write(f"Your depression level assessment is **{result}**.")
        st.write("Stay connected, take care of yourself, and reach out when needed 💙")
