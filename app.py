import streamlit as st
import pandas as pd
import plotly.express as px
import random
import pdfplumber

st.set_page_config(layout="wide", page_title="InterviewBuddy")

# --------------------------
# GLOBAL STYLE
# --------------------------

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp {
    background: linear-gradient(180deg,#020617,#020617);
}

.hero-title {
    font-size:70px;
    font-weight:700;
    text-align:center;
}

.hero-sub {
    font-size:22px;
    color:#94a3b8;
    text-align:center;
}

.card {
    padding:30px;
    border-radius:14px;
    background:#0f172a;
    border:1px solid #1e293b;
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# HERO SECTION
# --------------------------

st.image("logo.png", width=200)

st.markdown('<div class="hero-title">InterviewBuddy</div>', unsafe_allow_html=True)

st.markdown(
'<div class="hero-sub">AI Interview Preparation Platform</div>',
unsafe_allow_html=True
)

st.write(" ")

# --------------------------
# FEATURE SECTION
# --------------------------

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
    Upload resume and generate interview questions automatically.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
    <h3>AI Chat Coach</h3>
    Ask AI how to improve your interview answers.
    </div>
    """, unsafe_allow_html=True)

st.write(" ")
st.divider()

# --------------------------
# NAVIGATION
# --------------------------

page = st.sidebar.radio(
"Menu",
["Dashboard","Interview Practice","Resume Questions","AI Chat Coach"]
)

# --------------------------
# SESSION DATA
# --------------------------

if "scores" not in st.session_state:
    st.session_state.scores = []

if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------
# DASHBOARD
# --------------------------

if page=="Dashboard":

    st.header("Dashboard")

    m1,m2,m3 = st.columns(3)

    m1.metric("Interviews Taken", len(st.session_state.scores))

    avg = 0
    if st.session_state.scores:
        avg = sum(st.session_state.scores)/len(st.session_state.scores)

    m2.metric("Average Score", round(avg,2))

    m3.metric("Sessions", len(st.session_state.history))

    if st.session_state.scores:

        df = pd.DataFrame({
            "Attempt": list(range(1,len(st.session_state.scores)+1)),
            "Score": st.session_state.scores
        })

        fig = px.line(df,x="Attempt",y="Score",markers=True)

        st.plotly_chart(fig,use_container_width=True)

    if st.session_state.history:

        st.subheader("Interview History")

        st.dataframe(pd.DataFrame(st.session_state.history))

# --------------------------
# INTERVIEW PRACTICE
# --------------------------

elif page=="Interview Practice":

    st.header("Practice Interview")

    questions=[
        "Explain Linear Regression",
        "What is Overfitting",
        "Explain Gradient Descent",
        "What is Machine Learning"
    ]

    q=random.choice(questions)

    st.subheader(q)

    ans=st.text_area("Your Answer")

    if st.button("Evaluate"):

        score=random.randint(6,9)

        st.success(f"Score: {score}/10")

        st.session_state.scores.append(score)

        st.session_state.history.append({
            "Question":q,
            "Score":score
        })

# --------------------------
# RESUME QUESTIONS
# --------------------------

elif page=="Resume Questions":

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

# --------------------------
# AI CHAT
# --------------------------

elif page=="AI Chat Coach":

    st.header("AI Chat Coach")

    q=st.text_input("Ask a question")

    if q:

        st.success("A strong answer should include definition, explanation and example.")
