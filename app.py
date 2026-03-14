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

"doctor":{
"keywords":["doctor","medical","clinic"],
"answer":"🏥 College Doctor\nDr Sheetal S Agale\n📞 9594907410\n🕒 9:45 AM – 4:45 PM"
},

"labs":{
"keywords":["lab","labs","it lab"],
"answer":"💻 IT Department Labs:\n• Centre of Excellence\n• Data Science\n• Software\n• Database Engineering\n\nLab Assistants:\nPriyanka Padval\nPriyanka Patil\nNilam Shinde\nManoj Patode"
},

"academic":{
"keywords":["academic","coordinator","dean"],
"answer":"🎓 Academic Administration\nAcademic Coordinator: Mrs Shantiguru Madam\nDean Academics: Dr Preeti Patil"
},

"placement":{
"keywords":["placement","tpo","job"],
"answer":"💼 Training & Placement\nCoordinator: Shital Borse Madam\n\nEmails:\ntpo@dypcoeakurdi.ac.in\nplacements@dypcoeakurdi.ac.in"
},

"nba":{
"keywords":["nba"],
"answer":"NBA Coordinator\nAmita Madam"
},

"alumni":{
"keywords":["alumni"],
"answer":"Alumni Coordinator\nAmita Madam"
},

"technician":{
"keywords":["technician","internet issue","electric"],
"answer":"🔧 Technician Support\nVinay Nangare\nHandles Internet and Electrical issues"
},

"wifi":{
"keywords":["wifi","internet access"],
"answer":"📶 WiFi Access Instructions\nVisit: http://172.0.0.1\nUse your mobile number as both username and password."
},

"library":{
"keywords":["library","reading room"],
"answer":"📚 Library Location\nD Building\n2nd Floor"
},

"sports":{
"keywords":["sports","ground"],
"answer":"🏀 Sports Department\nLocation: A Building Entrance Ground Floor\nOfficer: Dr Abhaji Mane Sir"
},

"administration":{
"keywords":["administration","student section","marksheet","scholarship","accounts"],
"answer":"🏢 Administration Office\n\nStudent Section (documents / marksheet)\nSamrat Sir\n\nAdmission\nSalunke Sir\n\nScholarship\nWadkar Sir\n\nAccounts (fees)\nSantosh Sir\nRaju Sir"
},

"admission":{
"keywords":["admission","admission contact"],
"answer":"📞 Admission Incharge\nDr K T Jadhav\n\nAdmission Contact Numbers:\n9373775038\n9607957618\n9075345011\n9158195999\n8208018509\n9607957620"
},

"erp":{
"keywords":["erp","attendance","assignment","fees","bonafide","lc","hostel","syllabus"],
"answer":"🖥 ERP Portal\nhttps://erp.dypakurdipune.edu.in/\n\nUse ERP for:\nAttendance\nAssignments\nFees\nBonafide\nLC\nHostel\nSyllabus"
},

"results":{
"keywords":["result","exam","sppu"],
"answer":"📊 SPPU Results Portal\nhttps://sim.unipune.ac.in/SIM_APP/"
},

"itesa":{
"keywords":["itesa","club"],
"answer":"🎓 IT Department Student Club\nITESA\nInstagram:\nhttps://www.instagram.com/itesa.dyp/"
},

"grievance":{
"keywords":["grievance","complaint"],
"answer":"⚖ Grievance Redressal Committee\nChairperson: Dr P Malathi\n📞 9823152302"
},

"transport":{
"keywords":["bus","transport"],
"answer":"🚫 College does not provide bus transport."
},

"website":{
"keywords":["website","college website"],
"answer":"🌐 College Website\nhttps://www.dypcoeakurdi.ac.in/"
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

    reply = f"📅 {day.upper()} TIMETABLE ({class_div.upper()})\n\n"

    for time,subject in row.items():
        if time!="DAY/Time":
            reply += f"{time} → {subject}\n"

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


# ----------------------------
# INFORMATION MENU
# ----------------------------

st.subheader("What information you can ask")

st.markdown("""
### 📚 College Information
• Library location  
• IT Department labs  
• Academic coordinator  
• Dean academics  

### 🏫 Student Services
• ERP portal (attendance, assignments, fees)  
• Bonafide & LC information  
• SPPU results portal  

### 👨‍💼 Administration
• Student section (marksheet & documents)  
• Admission office  
• Scholarship office  
• Accounts / fees  

### 🏥 Campus Facilities
• College doctor  
• WiFi access instructions  
• Technician support  
• Sports department  

### 🎓 Department Activities
• ITESA student club  
• Alumni coordinator  
• NBA coordinator  

### 📞 Contact Information
• Admission contacts  
• College reception  
• College website  

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
        "content":"Hello! Ask me about timetable, ERP, library, WiFi, placements, doctor or college information."
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

    # Search college info
    response = search_info(user_input)

    # Timetable detection
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

    # Default message
    if not response:
        response="Try asking: monday te a, library, ERP, placement, WiFi, doctor."

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role":"assistant","content":response})