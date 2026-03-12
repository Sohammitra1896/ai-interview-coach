import streamlit as st
import pandas as pd
import plotly.express as px
import random
import pdfplumber
import json

st.set_page_config(
    page_title="InterviewBuddy",
    layout="wide",
    page_icon="🚀"
)

# -------------------------------
# GLOBAL STYLE
# -------------------------------

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.stApp {
background: linear-gradient(180deg,#020617,#020617);
color:white;
}

.hero-title {
font-size:60px;
font-weight:700;
}

.hero-sub {
font-size:20px;
color:#94a3b8;
}

.card {
background:#0f172a;
padding:25px;
border-radius:14px;
border:1px solid #1e293b;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOGO
# -------------------------------

try:
    st.image("logo.png", width=200)
except:
    st.title("InterviewBuddy")

# -------------------------------
# HERO
# -------------------------------

st.markdown('<div class="hero-title">InterviewBuddy</div>', unsafe_allow_html=True)

st.markdown(
'<div class="hero-sub">AI Interview Preparation Platform</div>',
unsafe_allow_html=True
)

st.write(" ")

# -------------------------------
# FEATURES
# -------------------------------

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
    <h3>Interview Practice</h3>
    Practice technical and behavioural interview questions.
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

# -------------------------------
# DATA STORAGE
# -------------------------------

DATA_FILE = "history.json"

def load_history():
    try:
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    except:
        return []

def save_history(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)

history = load_history()

# -------------------------------
# NAVIGATION
# -------------------------------

page = st.sidebar.radio(
"Navigation",
["Dashboard","Interview Practice","Resume Questions","AI Chat Coach"]
)

# -------------------------------
# SESSION DATA
# -------------------------------

if "scores" not in st.session_state:
    st.session_state.scores = []

# -------------------------------
# DASHBOARD
# -------------------------------

if page == "Dashboard":

    st.header("Dashboard")

    m1,m2,m3 = st.columns(3)

    m1.metric("Interviews Taken",len(st.session_state.scores))

    avg=0
    if st.session_state.scores:
        avg=sum(st.session_state.scores)/len(st.session_state.scores)

    m2.metric("Average Score",round(avg,2))

    m3.metric("Sessions",len(history))

    if st.session_state.scores:

        df=pd.DataFrame({
            "Attempt": list(range(1,len(st.session_state.scores)+1)),
            "Score": st.session_state.scores
        })

        fig=px.line(df,x="Attempt",y="Score",markers=True)

        st.plotly_chart(fig,use_container_width=True)

    if history:

        st.subheader("Interview History")

        st.dataframe(pd.DataFrame(history))

# -------------------------------
# INTERVIEW PRACTICE
# -------------------------------

elif page == "Interview Practice":

    st.header("Practice Interview")

    questions=[
        "Explain Linear Regression",
        "What is Overfitting",
        "Explain Gradient Descent",
        "What is Machine Learning",
        "Explain Decision Trees"
    ]

    q=random.choice(questions)

    st.subheader(q)

    ans=st.text_area("Your Answer")

    if st.button("Evaluate"):

        score=random.randint(6,9)

        st.success(f"Score: {score}/10")

        st.session_state.scores.append(score)

        history.append({
            "Question":q,
            "Score":score
        })

        save_history(history)

# -------------------------------
# RESUME QUESTIONS
# -------------------------------

elif page == "Resume Questions":

    st.header("Upload Resume")

    file=st.file_uploader("Upload PDF",type="pdf")

    if file:

        with pdfplumber.open(file) as pdf:

            text=""

            for p in pdf.pages:
                text+=p.extract_text()

        st.subheader("Generated Questions")

        if "python" in text.lower():
            st.write("Explain a Python project you built")

        if "machine learning" in text.lower():
            st.write("Explain a machine learning model you trained")

        if "data analysis" in text.lower():
            st.write("How did you clean your dataset")

# -------------------------------
# AI CHAT COACH
# -------------------------------

elif page == "AI Chat Coach":

    st.header("AI Chat Coach")

    q=st.text_input("Ask a question")

    if q:

        st.success(
        "A strong answer should include definition, explanation and real-world example."
        )
