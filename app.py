import streamlit as st
import random
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

st.title("AI Interview Preparation Coach")

questions = [
("Explain linear regression",
"Linear regression models the relationship between variables using a linear equation"),

("What is overfitting",
"Overfitting occurs when a model learns noise instead of general patterns"),

("Explain time complexity",
"Time complexity measures how algorithm runtime grows with input size")
]

if "scores" not in st.session_state:
    st.session_state.scores = []

question, ideal_answer = random.choice(questions)

st.subheader("Interview Question")
st.write(question)

user_answer = st.text_area("Your Answer")

def evaluate_answer(user_answer, ideal_answer):

    emb1 = model.encode(user_answer, convert_to_tensor=True)
    emb2 = model.encode(ideal_answer, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2)

    return float(score)

if st.button("Evaluate Answer"):

    if user_answer:

        score = evaluate_answer(user_answer, ideal_answer)

        score10 = round(score*10,2)

        st.session_state.scores.append(score10)

        st.success(f"Score: {score10}/10")

        if score10 > 8:
            st.write("Excellent explanation")
        elif score10 > 6:
            st.write("Good answer but add examples")
        else:
            st.write("Needs improvement")

if st.session_state.scores:

    st.subheader("Performance Graph")

    fig, ax = plt.subplots()

    ax.plot(st.session_state.scores, marker="o")

    ax.set_xlabel("Question Number")
    ax.set_ylabel("Score")

    st.pyplot(fig)
st.image("logo.png", width=220)
