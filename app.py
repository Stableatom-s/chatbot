import streamlit as st
import pandas as pd
import os


# ---------------------------
# TIMETABLE FILE MAPPING
# ---------------------------

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


# ---------------------------
# COLLEGE INFORMATION
# ---------------------------

college_info = {

"library": {
"keywords": ["library","reading room","study"],
"answer": "📚 Library\nLocation: D Building, 2nd Floor"
},

"doctor": {
"keywords": ["doctor","medical","clinic"],
"answer": "🩺 College Doctor\nDr Sheetal S Agale\nPhone: 9594907410\nTime: 9:45 AM – 4:45 PM"
},

"sports": {
"keywords": ["sports","ground","play"],
"answer": "🏀 Sports Department\nLocation: A Building Ground Floor\nOfficer: Dr Abhaji Mane"
},

"placement": {
"keywords": ["placement","tpo","job"],
"answer": "💼 Training & Placement\nCoordinator: Shital Borse Madam"
},

"erp": {
"keywords": ["erp","attendance","assignment","fees","bonafide","lc","hostel"],
"answer": "ERP Portal\nhttps://erp.dypakurdipune.edu.in/\nUse it for attendance, assignments, fees, bonafide, LC, hostel."
},

"results": {
"keywords": ["result","exam","sppu"],
"answer": "SPPU Results Portal\nhttps://sim.unipune.ac.in/SIM_APP/"
},

"technician": {
"keywords": ["internet","wifi","electric","technician"],
"answer": "🔧 Technician\nVinay Nangare\nInternet & Electrical Support"
},

"administration": {
"keywords": ["marksheet","document","student section","scholarship","accounts"],
"answer": """
Administration Office

Student Section – Samrat Sir  
Admission – Salunke Sir  
Scholarship – Wadkar Sir  
Accounts – Santosh Sir, Raju Sir
"""
},

"itesa": {
"keywords": ["itesa","club","it department"],
"answer": "IT Department Student Club\nITESA\nInstagram: https://www.instagram.com/itesa.dyp/"
},

"contact": {
"keywords": ["contact","phone","college number"],
"answer": """
D Y Patil College of Engineering
Sector 29 Nigdi Pradhikaran
Akurdi Pune 411044

Reception
020-27653054 / 020-27653058

Website
https://www.dypcoeakurdi.ac.in/
"""
}

}


# ---------------------------
# TIMETABLE FUNCTION
# ---------------------------

def get_timetable(day, class_div):

    csv_file = timetables.get(class_div)

    if not csv_file:
        return "Class not found."

    if not os.path.exists(csv_file):
        return f"{csv_file} not found."

    df = pd.read_csv(csv_file)

    if "DAY/Time" not in df.columns:
        return "Timetable format incorrect."

    row = df[df["DAY/Time"].str.lower() == day]

    if row.empty:
        return f"No classes on {day}."

    row = row.iloc[0].dropna()

    reply = f"📅 {day.upper()} TIMETABLE ({class_div.upper()})\n\n"

    for time, subject in row.items():
        if time != "DAY/Time":
            reply += f"{time} → {subject}\n"

    return reply


# ---------------------------
# SEARCH COLLEGE INFO
# ---------------------------

def search_info(user_input):

    for topic in college_info.values():

        for keyword in topic["keywords"]:

            if keyword in user_input:
                return topic["answer"]

    return None


# ---------------------------
# STREAMLIT UI
# ---------------------------

st.set_page_config(page_title="IT Genie", page_icon="🤖")

st.title("🤖 IT Genie Chatbot")

st.caption("Ask about timetable or college information.")


# ---------------------------
# CHAT HISTORY
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content":
"""Hello! I can help you with:

• Timetable (example: monday te a)
• Library
• Doctor
• ERP portal
• Placements
• Sports
• Administration
"""
    }]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------------------
# QUICK BUTTONS
# ---------------------------

col1,col2,col3,col4 = st.columns(4)

quick=None

if col1.button("📚 Library"):
    quick="library"

if col2.button("💼 Placement"):
    quick="placement"

if col3.button("🏫 IT Dept"):
    quick="itesa"

if col4.button("🩺 Doctor"):
    quick="doctor"


# ---------------------------
# INPUT
# ---------------------------

typed = st.chat_input("Type your question...")

prompt = typed or quick


if prompt:

    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    user_input = prompt.lower()

    response=None


    # SEARCH COLLEGE INFO
    response = search_info(user_input)


    # TIMETABLE DETECTION
    if not response:

        found_day=None
        found_class=None

        for day in ["monday","tuesday","wednesday","thursday","friday","saturday"]:
            if day in user_input:
                found_day=day

        for cls in timetables:
            if cls in user_input:
                found_class=cls

        if found_day and found_class:
            response=get_timetable(found_day,found_class)


    # DEFAULT MESSAGE
    if not response:
        response = """
I didn't understand.

Try asking:
• monday te a
• library
• ERP
• placement
• doctor
"""


    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role":"assistant",
        "content":response
    })