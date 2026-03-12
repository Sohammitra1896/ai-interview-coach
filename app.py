import streamlit as st
import pandas as pd
import plotly.express as px
import random
import pdfplumber
import json
import os
#import speech_recognition as sr

st.set_page_config(page_title="InterviewBuddy", layout="wide", page_icon="🤖")

# -----------------------------
# STYLING
# -----------------------------

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.stApp {
    background: linear-gradient(180deg,#020617,#0f172a);
    color:white;
}

.hero-title {
    font-size:60px;
    font-weight:700;
}

.hero-sub {
    font-size:22px;
    color:#94a3b8;
}

.card {
    background:#0f172a;
    padding:25px;
    border-radius:12px;
    border:1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGO
# -----------------------------

if os.path.exists("logo.png"):
    st.image("logo.png", width=180)

st.markdown('<div class="hero-title">InterviewBuddy</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">AI Interview Preparation Platform</div>', unsafe_allow_html=True)

st.write(" ")

# -----------------------------
# FEATURES
# -----------------------------

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
    <h3>Interview Practice</h3>
    Practice technical and behavioral interview questions.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
    <h3>Resume Based Questions</h3>
    Upload resume and generate interview questions.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
    <h3>AI Chat Coach</h3>
    Ask AI how to improve your answers.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------
# HISTORY STORAGE
# -----------------------------

DATA_FILE = "history.json"

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    return []

def save_history(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)

history = load_history()

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

page = st.sidebar.radio(
"Navigation",
["Dashboard","Interview Practice","Resume Questions","AI Chat Coach","Voice Assistant"]
)

# -----------------------------
# SESSION STORAGE
# -----------------------------

if "scores" not in st.session_state:
    st.session_state.scores = []

# -----------------------------
# DASHBOARD
# -----------------------------

if page == "Dashboard":

    st.header("Dashboard")

    m1,m2,m3 = st.columns(3)

    m1.metric("Interviews Taken",len(st.session_state.scores))

    avg = 0
    if st.session_state.scores:
        avg = sum(st.session_state.scores)/len(st.session_state.scores)

    m2.metric("Average Score",round(avg,2))
    m3.metric("Sessions",len(history))

    if st.session_state.scores:

        df = pd.DataFrame({
            "Attempt": list(range(1,len(st.session_state.scores)+1)),
            "Score": st.session_state.scores
        })

        fig = px.line(df,x="Attempt",y="Score",markers=True)

        st.plotly_chart(fig,use_container_width=True)

    if history:
        st.subheader("Interview History")
        st.dataframe(pd.DataFrame(history))

# -----------------------------
# INTERVIEW PRACTICE
# -----------------------------

elif page == "Interview Practice":

    st.header("Practice Interview")

    questions = [

    # Data science
    "Explain linear regression",
    "Explain logistic regression",
    "What is overfitting",
    "What is underfitting",
    "Explain gradient descent",
    "What is bias vs variance",
    "Explain decision trees",
    "What is random forest",
    "Explain cross validation",

    # Programming
    "Explain recursion",
    "What is time complexity",
    "Explain O(n log n)",
    "What is dynamic programming",

    # Data analyst
    "Explain data cleaning",
    "What is exploratory data analysis",
    "Explain correlation vs causation",
    "What is linear regression used for",

    ]

    q = random.choice(questions)

    st.subheader(q)

    ans = st.text_area("Your Answer")

    if st.button("Evaluate"):

        score = random.randint(6,9)

        st.success(f"Score: {score}/10")

        st.session_state.scores.append(score)

        history.append({
            "Question": q,
            "Score": score
        })

        save_history(history)

# -----------------------------
# RESUME QUESTIONS
# -----------------------------

elif page == "Resume Questions":

    st.header("Upload Resume")

    file = st.file_uploader("Upload PDF", type="pdf")

    if file:

        with pdfplumber.open(file) as pdf:

            text=""

            for p in pdf.pages:
                txt = p.extract_text()
                if txt:
                    text+=txt

        st.subheader("Generated Questions")

        skills = {
            "python": "Explain a Python project you built",
            "machine learning": "Explain a machine learning model you trained",
            "data analysis": "How did you clean your dataset",
            "sql": "Explain how you optimized a SQL query",
            "deep learning": "Explain a neural network project",
            "statistics": "Explain hypothesis testing",
            "tableau": "Explain a dashboard you created",
        }

        for skill,q in skills.items():
            if skill in text.lower():
                st.write(q)

# -----------------------------
# AI CHAT COACH
# -----------------------------

elif page == "AI Chat Coach":

    st.header("AI Chat Coach")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.chat_input("Ask an interview question")

    if user_input:

        response = "A strong answer should include definition, explanation and a real example."

        st.session_state.chat.append(("user",user_input))
        st.session_state.chat.append(("assistant",response))

    for role,msg in st.session_state.chat:

        if role=="user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

