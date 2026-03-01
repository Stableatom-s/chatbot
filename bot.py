import pandas as pd

class ITDeptBot:
    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath
        self.static_knowledge = {
            "hod": "The Head of the IT Department is Dr. Abhijit Patankar.",
            "teacher": "The Class Teacher for TE Div A is Ms. Mrunali Bhong.",
            "website": "The official college website is: https://www.dypcoeakurdi.ac.in/",
            "location": "D. Y. Patil College of Engineering, Akurdi, Pune-44.",
            "coordinator": "The Timetable Coordinators are Mrs. Rajeshwari Thadi and Mrs. Jayashree Pohkar."
        }
        self.abbreviations = {
            "PB": "Mrs. Poonam Bhawke (Data Science and Big Data Analytics)",
            "MB": "Ms. Mrunali Bhong (Cloud Computing)",
            "TF": "Mrs. Trupti Firake (Computer Networks & Security)",
            "HP": "Mrs. Himani Patel (Web Application Development)",
            "JP": "Mrs. Jayshree Pohkar (Web Application Development Lab)"
        }

    def fetch_timetable_for_day(self, day):
        try:
            df = pd.read_csv(self.csv_filepath, skiprows=8)
            df.columns = df.columns.str.strip()
            
            if 'DAY/Time' not in df.columns:
                return "Error: Could not read the 'DAY/Time' column."

            day_data = df[df['DAY/Time'].str.upper() == day.upper()]
            
            if day_data.empty:
                return f"I couldn't find any schedule for {day.capitalize()}."
            
            schedule_dict = day_data.iloc[0].dropna().to_dict()
            
            response = f"📅 *Timetable for {day.capitalize()}*:\n"
            response += "-" * 20 + "\n"
            for time_slot, subject in schedule_dict.items():
                if time_slot != "DAY/Time" and subject.strip():
                    response += f"[{time_slot}]: {subject.strip()}\n"
            return response

        except Exception as e:
            return f"An error occurred reading the timetable: {str(e)}"

    def process_query(self, user_input):
        user_input = user_input.lower().strip()
        
        if "hod" in user_input or "head" in user_input:
            return self.static_knowledge["hod"]
        elif "teacher" in user_input:
            return self.static_knowledge["teacher"]
        elif "website" in user_input or "link" in user_input:
            return self.static_knowledge["website"]
            
        days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        for day in days_of_week:
            if day in user_input:
                return self.fetch_timetable_for_day(day)
                
        for key, value in self.abbreviations.items():
            if key.lower() in user_input:
                return f"The abbreviation '{key}' stands for {value}."

        return "I'm not quite sure how to answer that yet. Try asking about the HOD, the college website, or the timetable for a specific day."