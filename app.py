import streamlit as st
import random
import pandas as pd
import plotly.express as px
import json
import pdfplumber
from sentence_transformers import SentenceTransformer, util

# ----------------------------
# PAGE SETTINGS
# ----------------------------

st.set_page_config(page_title="InterviewBuddy", layout="wide")

# ----------------------------
# LOAD AI MODEL
# ----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# DATA STORAGE
# ----------------------------

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

# ----------------------------
# LOGO
# ----------------------------

st.image("logo.png", width=220)

st.title("InterviewBuddy – AI Interview Preparation Platform")

# ----------------------------
# LOGIN
# ----------------------------

email = st.sidebar.text_input("Sign in with Email")

if email:
    st.sidebar.success("Logged in")

# ----------------------------
# NAVIGATION
# ----------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Interview Practice",
        "Resume Questions",
        "AI Chat Coach"
    ]
)

# ----------------------------
# SESSION STORAGE
# ----------------------------

if "scores" not in st.session_state:
    st.session_state.scores = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# AI SCORING FUNCTION
# ----------------------------

def evaluate_answer(user_answer, ideal_answer):

    emb1 = model.encode(user_answer, convert_to_tensor=True)
    emb2 = model.encode(ideal_answer, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2)

    return float(score) * 10

# ----------------------------
# DASHBOARD
# ----------------------------

if page == "Dashboard":

    st.header("Dashboard")

    st.metric("Interviews Taken", len(st.session_state.scores))

    if st.session_state.scores:

        avg = sum(st.session_state.scores) / len(st.session_state.scores)

        st.metric("Average Score", round(avg,2))

        df = pd.DataFrame({
            "Interview": list(range(1,len(st.session_state.scores)+1)),
            "Score": st.session_state.scores
        })

        fig = px.line(
            df,
            x="Interview",
            y="Score",
            markers=True,
            title="Interview Performance"
        )

        st.plotly_chart(fig,use_container_width=True)

    st.subheader("Past Conversations")

    if history:
        df = pd.DataFrame(history)
        st.dataframe(df)

# ----------------------------
# INTERVIEW PRACTICE
# ----------------------------

elif page == "Interview Practice":

    st.header("Practice Interview")

    questions = [
        (
            "Explain linear regression",
            "Linear regression models the relationship between variables using a linear equation."
        ),
        (
            "What is overfitting",
            "Overfitting happens when a model learns noise in the training data instead of general patterns."
        ),
        (
            "Explain gradient descent",
            "Gradient descent is an optimization algorithm used to minimize loss by updating model parameters."
        )
    ]

    question,ideal = random.choice(questions)

    st.write("Question:")
    st.write(question)

    answer = st.text_area("Your Answer")

    if st.button("Evaluate Answer"):

        if answer:

            score = evaluate_answer(answer,ideal)

            score = round(score,2)

            st.success(f"Score: {score}/10")

            st.session_state.scores.append(score)

            history.append({
                "question":question,
                "answer":answer,
                "score":score
            })

            save_history(history)

# ----------------------------
# RESUME QUESTION GENERATOR
# ----------------------------

elif page == "Resume Questions":

    st.header("Upload Resume")

    uploaded = st.file_uploader("Upload Resume (PDF)", type="pdf")

    if uploaded:

        with pdfplumber.open(uploaded) as pdf:

            text = ""

            for page in pdf.pages:
                text += page.extract_text()

        st.subheader("Generated Questions")

        if "python" in text.lower():
            st.write("Explain a Python project you built")

        if "machine learning" in text.lower():
            st.write("Explain a machine learning model you trained")

        if "data analysis" in text.lower():
            st.write("How did you clean your dataset")

# ----------------------------
# CHATGPT STYLE CHAT COACH
# ----------------------------

elif page == "AI Chat Coach":

    st.header("AI Interview Coach")

    prompt = st.chat_input("Ask an interview question")

    if prompt:

        response = "A strong interview answer should include definition, explanation, and a real example."

        st.session_state.messages.append(("user",prompt))
        st.session_state.messages.append(("assistant",response))

        history.append({
            "question":prompt,
            "answer":response
        })

        save_history(history)

    for role,msg in st.session_state.messages:

        if role=="user":
            st.chat_message("user").write(msg)

        else:
            st.chat_message("assistant").write(msg)
