import streamlit as st
import pandas as pd
import plotly.express as px
import random
import pdfplumber

# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------

st.set_page_config(
    page_title="InterviewBuddy",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------------------------
# MODERN CSS STYLE
# -------------------------------------------------

st.markdown("""
<style>

.main {
    background-color:#0E1117;
}

h1 {
    font-size:48px !important;
}

.hero {
    text-align:center;
    padding:40px;
}

.feature-card {
    background-color:#1c1f26;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 5px 20px rgba(0,0,0,0.4);
}

.metric-card {
    background-color:#1c1f26;
    padding:20px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOGO
# -------------------------------------------------

st.image("logo.png", width=220)

# -------------------------------------------------
# HERO SECTION
# -------------------------------------------------

st.markdown("""
<div class="hero">

<h1>InterviewBuddy</h1>

<h3>AI Interview Preparation Platform</h3>

<p>Practice interviews, analyze answers and get AI feedback instantly.</p>

</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FEATURE CARDS
# -------------------------------------------------

col1,col2,col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    <h3>AI Interview Practice</h3>
    <p>Practice technical and behavioral interview questions.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <h3>Resume Based Questions</h3>
    <p>Upload your resume and generate tailored interview questions.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h3>AI Chat Coach</h3>
    <p>Ask the AI coach how to improve your answers.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard","Interview Practice","Resume Questions","AI Chat Coach"]
)

# -------------------------------------------------
# SESSION STORAGE
# -------------------------------------------------

if "scores" not in st.session_state:
    st.session_state.scores = []

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

if page == "Dashboard":

    st.header("Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric("Interviews Taken", len(st.session_state.scores))

    avg = 0
    if st.session_state.scores:
        avg = sum(st.session_state.scores)/len(st.session_state.scores)

    col2.metric("Average Score", round(avg,2))

    col3.metric("Practice Sessions", len(st.session_state.history))

    if st.session_state.scores:

        df = pd.DataFrame({
            "Attempt":list(range(1,len(st.session_state.scores)+1)),
            "Score":st.session_state.scores
        })

        fig = px.line(df,x="Attempt",y="Score",markers=True)

        st.plotly_chart(fig,use_container_width=True)

    st.subheader("Interview History")

    if st.session_state.history:

        hist = pd.DataFrame(st.session_state.history)

        st.dataframe(hist,use_container_width=True)

# -------------------------------------------------
# INTERVIEW PRACTICE
# -------------------------------------------------

elif page == "Interview Practice":

    st.header("Practice Interview")

    questions = [
        "Explain linear regression",
        "What is overfitting",
        "Explain gradient descent",
        "What is machine learning"
    ]

    question = random.choice(questions)

    st.write("Question:")

    st.subheader(question)

    answer = st.text_area("Write your answer")

    if st.button("Evaluate Answer"):

        score = random.randint(6,9)

        st.success(f"Score: {score}/10")

        st.session_state.scores.append(score)

        st.session_state.history.append({
            "Question":question,
            "Score":score
        })

# -------------------------------------------------
# RESUME QUESTION GENERATOR
# -------------------------------------------------

elif page == "Resume Questions":

    st.header("Upload Resume")

    uploaded = st.file_uploader("Upload Resume (PDF)",type="pdf")

    if uploaded:

        with pdfplumber.open(uploaded) as pdf:

            text=""

            for page in pdf.pages:
                text+=page.extract_text()

        st.subheader("Generated Questions")

        if "python" in text.lower():
            st.write("Explain a Python project you worked on")

        if "machine learning" in text.lower():
            st.write("Explain a machine learning model you built")

        if "data analysis" in text.lower():
            st.write("How did you clean your dataset")

# -------------------------------------------------
# AI CHAT COACH
# -------------------------------------------------

elif page == "AI Chat Coach":

    st.header("AI Chat Coach")

    user = st.text_input("Ask a question")

    if user:

        st.write("AI Coach:")

        st.success(
        "A strong interview answer should include definition, explanation, and real-world example."
        )
