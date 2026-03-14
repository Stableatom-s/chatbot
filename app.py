import streamlit as st
import pandas as pd
import json
import os

# -----------------------------
# LOAD KNOWLEDGE BASE
# -----------------------------
with open("knowledge_base.json", "r") as f:
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
# SEARCH KNOWLEDGE BASE
# -----------------------------
def search_kb(query):

    query = query.lower()

    for topic, data in KB.items():

        for keyword in data["keywords"]:
            if keyword in query:
                return data["answer"]

    return None


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="IT-Genie", page_icon="🤖")

st.title("🤖 IT-Genie Chatbot")
st.caption("Ask me about college information or timetable.")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! Ask me about placements, ERP, library, sports, doctor, or timetable."
    }]

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------
# USER INPUT
# -----------------------------
prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    user_input = prompt.lower()

    response = None

    # ---- Knowledge Base ----
    response = search_kb(user_input)

    # ---- Timetable Logic ----
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

    if not response:
        response = "I couldn't understand. Try asking about library, placements, ERP, or timetable."

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })