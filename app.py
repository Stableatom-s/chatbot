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

static_info = {
    "hod": "The Head of the IT Department is Dr. Abhijit Patankar.",
    "website": "The official college website is: https://www.dypcoeakurdi.ac.in/",
    "location": "We are located at D. Y. Patil College of Engineering, Akurdi, Pune-44."
}

# 2. Core Timetable Function (Unchanged!)
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
        
        # Build the final text response using Markdown for a better UI look
        reply = f"### 📅 {day.upper()} TIMETABLE FOR {class_div.upper()}\n\n"
        for time, subject in schedule.items():
            if time != "DAY/Time" and subject.strip():
                reply += f"**[{time}]** 👉  {subject.strip()}\n\n"
        
        return reply
        
    except EmptyDataError:
        return f"❌ ERROR: Pandas could not read '{csv_file}' because there is no data inside it."
    except Exception as e:
        return f"❌ FATAL ERROR reading '{csv_file}': {str(e)}"


# 3. Streamlit Web UI Setup
st.set_page_config(page_title="IT-Genie", page_icon="🤖")
st.title("🤖 IT-Genie Chatbot")
st.caption("Ask me about the HOD, Website, or daily timetables (e.g., 'show me monday te a')")

# Initialize chat history memory
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there! What schedule do you need today?"}]

# Display chat messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# React to user input
if prompt := st.chat_input("Type your message here..."):
    
    # Display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot Logic Processing
    user_input = prompt.lower().strip()
    response = ""

    if "hod" in user_input or "head" in user_input:
        response = static_info["hod"]
    elif "website" in user_input or "link" in user_input:
        response = static_info["website"]
    elif "location" in user_input or "address" in user_input:
        response = static_info["location"]
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
            response = "I can answer questions about the HOD, Website, or daily timetables (e.g., 'show me monday te a')."

    # Display bot response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})