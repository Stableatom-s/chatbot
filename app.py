import streamlit as st
import pandas as pd
import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# LOAD KNOWLEDGE BASE
# -----------------------------

with open("knowledge_base.json") as f:
    KB = json.load(f)


# -----------------------------
# TIMETABLE FILE MAPPING
# -----------------------------

timetables = {
    "se a": "SE_A.csv", "sy a": "SE_A.csv",
    "se b": "SE_B.csv", "sy b": "SE_B.csv",
    "se c": "SE_C.csv", "sy c": "SE_C.csv",
    "te a": "TE_A.csv",
    "te b": "TE_B.csv",
    "te c": "TE_C.csv",
    "be a": "BE_A.csv",
    "be b": "BE_B.csv",
    "be c": "BE_C.csv"
}


# -----------------------------
# SMART AI SEARCH
# -----------------------------

def ai_search(query):

    questions = []
    answers = []

    for topic,data in KB.items():
        for q in data["keywords"]:
            questions.append(q)
            answers.append(data["answer"])

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(questions + [query])

    similarity = cosine_similarity(vectors[-1], vectors[:-1])

    best_match = similarity.argmax()

    score = similarity[0][best_match]

    if score > 0.25:
        return answers[best_match]

    return None


# -----------------------------
# TIMETABLE FUNCTION
# -----------------------------

def get_timetable(day, class_div):

    csv_file = timetables.get(class_div)

    if not csv_file:
        return "I couldn't find that class."

    if not os.path.exists(csv_file):
        return f"❌ Timetable file {csv_file} not found."

    df = pd.read_csv(csv_file)

    if "DAY/Time" not in df.columns:
        return "Timetable format incorrect."

    day_data = df[df["DAY/Time"].str.lower() == day.lower()]

    if day_data.empty:
        return f"No classes on {day}."

    schedule = day_data.iloc[0].dropna()

    reply = f"📅 **{day.upper()} TIMETABLE ({class_div.upper()})**\n\n"

    for time, subject in schedule.items():
        if time != "DAY/Time":
            reply += f"**{time}** → {subject}\n\n"

    return reply


# -----------------------------
# STREAMLIT UI
# -----------------------------

st.set_page_config(page_title="IT-Genie", page_icon="🤖")

st.title("🤖 IT-Genie Chatbot")
st.caption("Ask about college info, ERP, placements, facilities or timetable.")


# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role":"assistant",
        "content":"Hello! Ask me anything about IT department, ERP, library, placements or timetable."
    }]


# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------
# QUICK BUTTONS
# -----------------------------

st.write("")
col1,col2,col3,col4 = st.columns(4)

quick_prompt = None

if col1.button("📚 Library",use_container_width=True):
    quick_prompt = "library"

if col2.button("💼 Placement",use_container_width=True):
    quick_prompt = "placement"

if col3.button("🏫 IT Dept",use_container_width=True):
    quick_prompt = "it department"

if col4.button("🩺 Doctor",use_container_width=True):
    quick_prompt = "doctor"


# -----------------------------
# USER INPUT
# -----------------------------

typed_prompt = st.chat_input("Ask something...")

prompt = typed_prompt or quick_prompt


if prompt:

    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    user_input = prompt.lower()

    response = None


    # -----------------------------
    # AI SEARCH
    # -----------------------------

    response = ai_search(user_input)


    # -----------------------------
    # TIMETABLE DETECTION
    # -----------------------------

    if not response:

        found_day = None
        found_class = None

        for day in ["monday","tuesday","wednesday","thursday","friday","saturday"]:
            if day in user_input:
                found_day = day
                break

        for cls in timetables:
            if cls in user_input:
                found_class = cls
                break

        if found_day and found_class:
            response = get_timetable(found_day, found_class)


    # -----------------------------
    # DEFAULT RESPONSE
    # -----------------------------

    if not response:
        response = "I couldn't understand that. Try asking about library, ERP, placements, sports, doctor, or timetable."


    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role":"assistant",
        "content":response
    })