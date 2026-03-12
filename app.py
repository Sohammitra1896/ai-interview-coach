import streamlit as st
import pandas as pd
import plotly.express as px
import random
import pdfplumber
import json
import os

st.set_page_config(page_title="InterviewBuddy", layout="wide")

# ----------------------------
# UI STYLE
# ----------------------------

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.hero{
font-size:50px;
font-weight:bold;
}

.subtitle{
color:gray;
}

.card{
background:#0f172a;
padding:20px;
border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------

if os.path.exists("logo.png"):
    st.image("logo.png", width=180)

st.markdown('<div class="hero">InterviewBuddy</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Interview Preparation Platform</div>', unsafe_allow_html=True)

st.divider()

# ----------------------------
# DATA STORAGE
# ----------------------------

DATA_FILE="history.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)

history=load_data()

# ----------------------------
# NAVIGATION
# ----------------------------

page=st.sidebar.radio(
"Navigation",
[
"Dashboard",
"Interview Practice",
"PYQ Bank",
"Resume Questions",
"Interview Records"
]
)

# ----------------------------
# QUESTION BANK
# ----------------------------

question_bank = {

"Data Science":[
"Explain linear regression",
"What is logistic regression",
"Explain gradient descent",
"What is overfitting",
"What is random forest",
"What is PCA",
"What is clustering",
"What is feature engineering"
],

"Programming":[
"What is recursion",
"Explain dynamic programming",
"What is time complexity",
"What is polymorphism",
"What is encapsulation",
"What is inheritance",
"What is hashing"
],

"Data Analyst":[
"What is data cleaning",
"What is exploratory data analysis",
"Explain correlation vs causation",
"What is hypothesis testing",
"What is A/B testing",
"What is SQL indexing"
]

}

# ----------------------------
# DASHBOARD
# ----------------------------

if page=="Dashboard":

    st.header("Interview Analytics")

    scores=[item["Score"] for item in history] if history else []

    col1,col2,col3=st.columns(3)

    col1.metric("Total Interviews",len(scores))

    avg=sum(scores)/len(scores) if scores else 0
    col2.metric("Average Score",round(avg,2))

    readiness=min(95,int(avg*10))
    col3.metric("Placement Readiness %",readiness)

    if scores:

        df=pd.DataFrame({
        "Attempt":list(range(1,len(scores)+1)),
        "Score":scores
        })

        st.subheader("Score Progression")

        fig=px.line(df,x="Attempt",y="Score",markers=True)
        st.plotly_chart(fig,use_container_width=True)

        st.subheader("Score Distribution")

        fig2=px.histogram(df,x="Score",nbins=10)
        st.plotly_chart(fig2,use_container_width=True)

    # topic analytics
    if history:

        topics=[item["Topic"] for item in history]

        topic_df=pd.DataFrame({"Topic":topics})

        fig3=px.histogram(topic_df,x="Topic")

        st.subheader("Topic Distribution")

        st.plotly_chart(fig3,use_container_width=True)

# ----------------------------
# INTERVIEW PRACTICE
# ----------------------------

elif page=="Interview Practice":

    st.header("Practice Interview")

    topic=st.selectbox(
    "Choose Topic",
    list(question_bank.keys())
    )

    question=random.choice(question_bank[topic])

    st.subheader(question)

    ans=st.text_area("Your Answer")

    if st.button("Evaluate"):

        score=random.randint(6,9)

        st.success(f"Score: {score}/10")

        history.append({
        "Question":question,
        "Topic":topic,
        "Score":score
        })

        save_data(history)

# ----------------------------
# PYQ BANK
# ----------------------------

elif page=="PYQ Bank":

    st.header("Previous Interview Questions")

    for topic,qs in question_bank.items():

        st.subheader(topic)

        for q in qs:
            st.write("-",q)

# ----------------------------
# RESUME QUESTIONS
# ----------------------------

elif page=="Resume Questions":

    st.header("Upload Resume")

    file=st.file_uploader("Upload Resume PDF",type="pdf")

    if file:

        with pdfplumber.open(file) as pdf:

            text=""

            for p in pdf.pages:
                txt=p.extract_text()
                if txt:
                    text+=txt

        st.subheader("Generated Questions")

        skills={

        "python":"Explain a Python project you built",
        "machine learning":"Explain a machine learning model you trained",
        "sql":"Explain a SQL query you optimized",
        "statistics":"Explain hypothesis testing",
        "deep learning":"Explain a neural network architecture",
        "data analysis":"Explain how you cleaned messy data",
        "tableau":"Explain a dashboard you created",
        "nlp":"Explain an NLP project"

        }

        for skill,q in skills.items():

            if skill in text.lower():
                st.write(q)

# ----------------------------
# INTERVIEW RECORDS
# ----------------------------

elif page=="Interview Records":

    st.header("Interview Records")

    if history:

        df=pd.DataFrame(history)

        st.dataframe(df)

    else:
        st.write("No records yet")
