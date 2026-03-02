import streamlit as st
import pandas as pd
import os
from pandas.errors import EmptyDataError

# 1. Setup Data Mapping
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

# 2. Static Information Database
static_info = {
    "hod": "The Head of the IT Department is Dr. Abhijit Patankar.",
    "website": "The official college website is: https://www.dypcoeakurdi.ac.in/",
    "about_text": "🏫 **About D. Y. Patil Akurdi:**\nThe D Y Patil Group at Akurdi strongly believes that leadership positions drive growth. The Akurdi campus attracts faculty talent and meritorious students, providing an encouraging environment for teaching, learning, innovation, incubation, and entrepreneurship that fosters societal change and contributes to nation-building.",
    "address": "📍 **Address:** Dr D. Y. Patil Educational Complex, Sector 29, Nigdi Pradhikaran, Akurdi, Pune, 411044.",
    "affiliations": "🎓 **Affiliations:** NAAC 'A' GRADE ACCREDITED, APPROVED BY AICTE RECOGNIZED BY DTE & PERMANENTLY Affiliated To Savitribai Phule Pune University.",
    "facilities": "🏢 **Facilities we provide:**\n* Computer Center\n* Library\n* Seminar Hall\n* Language Laboratory\n* Amphi Theatre\n* Dnyanaprasad Sabhagruha\n* Transport\n* Canteen\n* Sports Ground\n* Medical Room",
    "placements": "💼 **Placement Details:**\n* **Placement Record:** [Click here to view](https://bit.ly/2QVb6b2)\n* **Top Recruiters:** [Click here to view](https://bit.ly/2WRKfjT)",
    "contacts": "📞 **Contact Details:**\n* **Reception:** 020-65108447 | 020-27657868\n* **Email:** info@dypakurdipune.edu.in | admission@dypakurdipune.edu.in"
}

# 3. Core Timetable Function
def get_timetable(day, class_div):
    csv_file = timetables.get(class_div)
    
    if not os.path.exists(csv_file):
        return f"❌ ERROR: I cannot find '{csv_file}'. Please create it in your folder."
    if os.path.getsize(csv_file) == 0:
        return f"❌ ERROR: '{csv_file}' is completely empty! Please paste the timetable data inside and save."

    try:
        df = pd.read_csv(csv_file)
        if df.empty or len(df.columns) == 0:
            return f"❌ ERROR: '{csv_file}' has no valid columns. Please check the text formatting inside."
            
        df.columns = df.columns.str.strip()
        if 'DAY/Time' not in df.columns:
            return f"❌ ERROR: '{csv_file}' is missing the 'DAY/Time' column header."

        day_data = df[df['DAY/Time'].str.upper() == day.upper()]
        
        if day_data.empty:
            return f"⚠️ No classes found for {day.capitalize()} in {class_div.upper()}."
            
        schedule = day_data.iloc[0].dropna().to_dict()
        
        reply = f"### 📅 {day.upper()} TIMETABLE FOR {class_div.upper()}\n\n"
        for time, subject in schedule.items():
            if time != "DAY/Time" and subject.strip():
                reply += f"**[{time}]** 👉  {subject.strip()}\n\n"
        
        return reply
        
    except EmptyDataError:
        return f"❌ ERROR: Pandas could not read '{csv_file}' because there is no data inside it."
    except Exception as e:
        return f"❌ FATAL ERROR reading '{csv_file}': {str(e)}"

# 4. Streamlit Web UI Setup
st.set_page_config(page_title="IT-Genie", page_icon="🤖")
st.title("🤖 IT-Genie Chatbot")
st.caption("Ask me about timetables (e.g., 'monday te a'), placements, facilities, or contacts!")

# Initialize chat history memory
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there! I can fetch your timetable or tell you about college facilities, contacts, and placements. What do you need today?"}]

# Display chat messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- QUICK REPLY BUTTONS ---
st.write("") 
col1, col2, col3, col4 = st.columns(4)

quick_prompt = None

if col1.button("🏫 About College", use_container_width=True):
    quick_prompt = "about"
if col2.button("🏢 Facilities", use_container_width=True):
    quick_prompt = "facilities"
if col3.button("💼 Placements", use_container_width=True):
    quick_prompt = "placements"
if col4.button("📞 Contact Details", use_container_width=True):
    quick_prompt = "contact"

# --- INPUT LOGIC ---
typed_prompt = st.chat_input("Type your message here...")
prompt = typed_prompt or quick_prompt

if prompt:
    # Display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot Logic Processing
    user_input = prompt.lower().strip()
    response = ""

    # --- STATIC INFO CHECKS ---
    if "hod" in user_input or "head" in user_input:
        response = static_info["hod"]
    elif "website" in user_input or "link" in user_input:
        response = static_info["website"]
    elif "about" in user_input or "address" in user_input or "location" in user_input:
        # Combines the new About text, Address, and Affiliations into one mega-response
        response = f"{static_info['about_text']}\n\n{static_info['address']}\n\n{static_info['affiliations']}"
    elif "affiliation" in user_input or "accredited" in user_input or "naac" in user_input:
        response = static_info["affiliations"]
    elif "facility" in user_input or "facilities" in user_input:
        response = static_info["facilities"]
    elif "placement" in user_input or "recruiter" in user_input or "package" in user_input:
        response = static_info["placements"]
    elif "contact" in user_input or "email" in user_input or "phone" in user_input or "number" in user_input:
        response = static_info["contacts"]
        
    # --- TIMETABLE CHECKS ---
    else:
        found_day = None
        found_class = None
        
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
            if day in user_input:
                found_day = day
                break
                
        for cls in sorted(timetables.keys(), key=len, reverse=True):
            if cls in user_input:
                found_class = cls
                break
        
        if found_day and found_class:
            response = get_timetable(found_day, found_class)
        elif found_day and not found_class:
            response = f"I see you asked for **{found_day.capitalize()}**, but which class? (e.g., 'monday te a')"
        elif found_class and not found_day:
            response = f"You asked about **{found_class.upper()}**, but for which day? (e.g., 'monday te a')"
        else:
            # --- DEFAULT FALLBACK ---
            response = "I couldn't quite understand that. You can ask me to fetch a timetable (e.g., 'monday te a'), or click one of the buttons above for quick info!"

    # Display bot response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()