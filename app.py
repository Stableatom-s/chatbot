import streamlit as st
import pandas as pd
import os


# ----------------------------
# TIMETABLE FILES
# ----------------------------

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


# ----------------------------
# COLLEGE INFORMATION DATABASE
# ----------------------------

college_info = {

"principal":{
"keywords":["principal"],
"answer":"""
### 🎓 Principal

Dr. Mrs. P. Malathi  
Principal

📧 Email  
principal@dypcoeakurdi.ac.in
"""
},

"dean_admin":{
"keywords":["dean administration","administration dean"],
"answer":"""
### 🏢 Dean Administration

Dr. S. S. Sarnobat  

📧 Email  
dean_admin@dypcoeakurdi.ac.in
"""
},

"academic":{
"keywords":["academic","coordinator","dean academics","autonomy"],
"answer":"""
### 🎓 Dean Academics & Autonomy

Dr. Preeti Patil  

📧 Email  
dean_academics@dypcoeakurdi.ac.in

Academic Coordinator  
Mrs. Shantiguru Madam
"""
},

"placement":{
"keywords":["placement","tpo","placement officer","job"],
"answer":"""
### 💼 Training & Placement Cell

Training & Placement Officer  
Shashi Kant Sharma  

📧 Email  
tpo@dypcoeakurdi.ac.in

Placement Coordinator  
Shital Borse Madam
"""
},

"doctor":{
"keywords":["doctor","medical","clinic"],
"answer":"""
### 🏥 College Doctor

Dr. Sheetal S Agale  

📞 Phone  
9594907410  

🕒 Available  
9:45 AM – 4:45 PM
"""
},

"labs":{
"keywords":["lab","labs","software lab","fpl","database lab","vertusa","data science lab"],
"answer":"""
### 💻 IT Department Labs

### 🔹 Software Lab (FPL Lab)
Assistants
- Priyanka Padval
- Priyanka Patil

### 🔹 Database Engineering Lab (Vertusa Lab)
Assistant
- Nilam Shinde

### 🔹 Centre of Excellence Lab
Assistant
- Manoj Patode

### 🔹 Data Science Lab
Assistant
- Manoj Patode
"""
},

"nba":{
"keywords":["nba"],
"answer":"""
### 🏅 NBA Coordinator

Amita Madam
"""
},

"alumni":{
"keywords":["alumni"],
"answer":"""
### 👥 Alumni Coordinator

Amita Madam
"""
},

"technician":{
"keywords":["technician","internet issue","electric"],
"answer":"""
### 🔧 Technical Support

Vinay Nangare  

Handles:
- Internet issues
- Electrical issues
"""
},

"wifi":{
"keywords":["wifi","internet access"],
"answer":"""
### 📶 WiFi Access Instructions

1. Visit  
http://172.0.0.1

2. Login using  
Username: Your Mobile Number  
Password: Your Mobile Number
"""
},

"library":{
"keywords":["library","reading room"],
"answer":"""
### 📚 Library

Location  
D Building  
2nd Floor
"""
},

"sports":{
"keywords":["sports","ground"],
"answer":"""
### 🏀 Sports Department

Location  
A Building Entrance  
Ground Floor

Officer  
Dr. Abhaji Mane Sir
"""
},

"administration":{
"keywords":["administration","student section","marksheet","scholarship","accounts"],
"answer":"""
### 🏢 Administration Office

Student Section (Documents / Marksheet)  
Samrat Sir  

Admission  
Salunke Sir  

Scholarship  
Wadkar Sir  

Accounts (Fees Related)  
Santosh Sir  
Raju Sir
"""
},

"admission":{
"keywords":["admission","admission contact"],
"answer":"""
### 📞 Admission Department

Admission Incharge  
Dr. K. T. Jadhav  

Contact Numbers
- 9373775038
- 9607957618
- 9075345011
- 9158195999
- 8208018509
- 9607957620
"""
},

"erp":{
"keywords":["erp","attendance","assignment","fees","bonafide","lc","hostel","syllabus"],
"answer":"""
### 🖥 ERP Portal

https://erp.dypakurdipune.edu.in/

Use ERP for:
- Attendance
- Assignments
- Fees
- Bonafide Certificate
- Leaving Certificate
- Hostel Information
- Syllabus
"""
},

"results":{
"keywords":["result","exam","sppu"],
"answer":"""
### 📊 SPPU Results

https://sim.unipune.ac.in/SIM_APP/
"""
},

"itesa":{
"keywords":["itesa","club"],
"answer":"""
### 🎓 ITESA Student Club

Instagram  
https://www.instagram.com/itesa.dyp/
"""
},

"grievance":{
"keywords":["grievance","complaint"],
"answer":"""
### ⚖ Grievance Redressal Committee

Chairperson  
Dr. P. Malathi  

📞 Contact  
9823152302
"""
},

"transport":{
"keywords":["bus","transport"],
"answer":"""
### 🚌 Transport

College does **not provide bus transport**.
"""
},

"website":{
"keywords":["website","college website"],
"answer":"""
### 🌐 College Website

https://www.dypcoeakurdi.ac.in/
"""
}

}


# ----------------------------
# TIMETABLE FUNCTION
# ----------------------------

def get_timetable(day, class_div):

    csv_file = timetables.get(class_div)

    if not csv_file:
        return "Class not found."

    if not os.path.exists(csv_file):
        return f"{csv_file} not found."

    df = pd.read_csv(csv_file)

    if "DAY/Time" not in df.columns:
        return "Timetable format incorrect."

    row = df[df["DAY/Time"].str.lower()==day]

    if row.empty:
        return f"No classes on {day}."

    row = row.iloc[0].dropna()

    reply = f"### 📅 {day.upper()} TIMETABLE ({class_div.upper()})\n\n"

    for time,subject in row.items():
        if time!="DAY/Time":
            reply += f"- **{time}** → {subject}\n"

    return reply


# ----------------------------
# SEARCH FUNCTION
# ----------------------------

def search_info(user_input):

    for topic in college_info.values():
        for keyword in topic["keywords"]:
            if keyword in user_input:
                return topic["answer"]

    return None


# ----------------------------
# STREAMLIT UI
# ----------------------------

st.set_page_config(page_title="IT Genie",page_icon="🤖")

st.title("🤖 IT Genie Chatbot")

st.caption("Assistant for IT Department – D Y Patil College of Engineering Akurdi")


st.subheader("What information you can ask")

st.markdown("""
### 📚 College Information
• Principal  
• Dean Administration  
• Dean Academics  
• Library location  
• IT Department labs  

### 🏫 Student Services
• ERP portal  
• SPPU results portal  

### 👨‍💼 Administration
• Student section  
• Admission office  
• Scholarship office  
• Accounts  

### 🏥 Campus Facilities
• College doctor  
• WiFi access  
• Technician support  
• Sports department  

### 🎓 Department Activities
• ITESA student club  
• Alumni coordinator  
• NBA coordinator  

### 📅 Timetable
Type like:

`monday te a`

`wednesday se b`
""")


# ----------------------------
# CHAT HISTORY
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages=[{
        "role":"assistant",
        "content":"Hello! Ask me about timetable, principal, ERP, library, WiFi, placements, doctor or college information."
    }]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ----------------------------
# USER INPUT
# ----------------------------

prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    user_input = prompt.lower()

    response=None

    response = search_info(user_input)

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

    if not response:
        response="Try asking: principal, monday te a, library, ERP, placement, WiFi, doctor."

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role":"assistant","content":response})