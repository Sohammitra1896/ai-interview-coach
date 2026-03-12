import streamlit as st
import pandas as pd
import plotly.express as px
import random
import pdfplumber
import json
import os

st.set_page_config(page_title="InterviewBuddy", layout="wide", page_icon="🤖")

# --------------------------------
# UI STYLE
# --------------------------------

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.stApp {
background: linear-gradient(180deg,#020617,#0f172a);
color:white;
}

.hero {
font-size:56px;
font-weight:700;
}

.subtitle {
color:#94a3b8;
font-size:18px;
}

.card {
background:#0f172a;
padding:25px;
border-radius:12px;
border:1px solid #1e293b;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOGO
# --------------------------------

if os.path.exists("logo.png"):
    st.image("logo.png", width=180)

st.markdown('<div class="hero">InterviewBuddy</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Interview Preparation Platform</div>', unsafe_allow_html=True)

st.write(" ")

# --------------------------------
# FEATURES SECTION
# --------------------------------

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
    <h3>Interview Practice</h3>
    Practice real interview questions and track performance.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
    <h3>Resume Questions</h3>
    Upload resume and generate personalized questions.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
    <h3>Performance Analytics</h3>
    View charts of interview and placement readiness.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --------------------------------
# DATA STORAGE
# --------------------------------

DATA_FILE = "history.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)

history = load_data()

# --------------------------------
# NAVIGATION
# --------------------------------

page = st.sidebar.radio(
"Navigation",
["Dashboard","Interview Practice","Resume Questions","History"]
)

if "scores" not in st.session_state:
    st.session_state.scores = []

# --------------------------------
# DASHBOARD
# --------------------------------

if page == "Dashboard":

    st.header("Interview Analytics Dashboard")

    scores = [item["Score"] for item in history] if history else []

    m1,m2,m3 = st.columns(3)

    m1.metric("Total Interviews", len(scores))

    avg = sum(scores)/len(scores) if scores else 0
    m2.metric("Average Score", round(avg,2))

    placement_probability = min(95, int(avg*10))
    m3.metric("Placement Readiness %", placement_probability)

    if scores:

        df = pd.DataFrame({
            "Interview": list(range(1,len(scores)+1)),
            "Score": scores
        })

        fig = px.line(df, x="Interview", y="Score", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.histogram(df, x="Score", nbins=10)
        st.plotly_chart(fig2, use_container_width=True)

# --------------------------------
# INTERVIEW QUESTIONS DATABASE
# --------------------------------

questions = [

"Explain linear regression",
"Explain logistic regression",
"What is overfitting",
"What is underfitting",
"Explain gradient descent",
"What is bias vs variance",
"Explain decision trees",
"What is random forest",
"What is cross validation",
"Explain neural networks",
"What is feature engineering",
"What is PCA",
"What is clustering",
"What is k-means",
"What is NLP",
"What is deep learning",

"Explain recursion",
"What is time complexity",
"What is O(n log n)",
"Explain dynamic programming",
"What is a hash table",
"What is polymorphism",
"What is encapsulation",
"Explain inheritance",
"What is REST API",
"What is normalization",
"What is indexing",

"Explain hypothesis testing",
"What is correlation vs causation",
"What is regression analysis",
"What is data cleaning",
"What is EDA",
"What is A/B testing"

]

# --------------------------------
# INTERVIEW PRACTICE
# --------------------------------

elif page == "Interview Practice":

    st.header("Practice Interview")

    q = random.choice(questions)

    st.subheader(q)

    ans = st.text_area("Your Answer")

    if st.button("Evaluate"):

        score = random.randint(6,9)

        st.success(f"Score: {score}/10")

        history.append({
            "Question": q,
            "Score": score
        })

        save_data(history)

# --------------------------------
# RESUME QUESTIONS
# --------------------------------

elif page == "Resume Questions":

    st.header("Upload Resume")

    file = st.file_uploader("Upload PDF Resume", type="pdf")

    if file:

        with pdfplumber.open(file) as pdf:

            text=""

            for page in pdf.pages:
                txt=page.extract_text()
                if txt:
                    text+=txt

        st.subheader("Generated Questions")

        skills = {

        "python":"Explain a Python project you built",
        "machine learning":"Explain a machine learning model you trained",
        "sql":"Explain a complex SQL query you optimized",
        "statistics":"Explain hypothesis testing",
        "deep learning":"Explain a neural network architecture",
        "data analysis":"Explain how you cleaned messy data",
        "tableau":"Explain a dashboard you created",
        "nlp":"Explain an NLP project"

        }

        for skill,q in skills.items():
            if skill in text.lower():
                st.write(q)

# --------------------------------
# HISTORY PAGE
# --------------------------------

elif page == "History":

    st.header("Interview History")

    if history:
        df = pd.DataFrame(history)
        st.dataframe(df)
    else:
        st.write("No interview records yet.")
