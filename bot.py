import pandas as pd
import sys
import os
from pandas.errors import EmptyDataError

# 1. Setup Data Mapping
# This dictionary links what the user types to the exact CSV file name
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

# 2. Static Information
static_info = {
    "hod": "The Head of the IT Department is Dr. Abhijit Patankar.",
    "website": "The official college website is: https://www.dypcoeakurdi.ac.in/",
    "location": "We are located at D. Y. Patil College of Engineering, Akurdi, Pune-44."
}

# 3. Core Function to fetch the schedule with Advanced Error Handling
def get_timetable(day, class_div):
    # Get the correct filename based on the class requested
    csv_file = timetables.get(class_div)
    
    # ERROR CHECK 1: Does the file even exist?
    if not os.path.exists(csv_file):
        return f"❌ ERROR: I cannot find '{csv_file}'. Please create it in your folder."

    # ERROR CHECK 2: Is the file completely empty? (0 bytes)
    if os.path.getsize(csv_file) == 0:
        return f"❌ ERROR: '{csv_file}' is completely empty! Please paste the timetable data inside and save."

    try:
        # Try to read the CSV (no skiprows needed for clean files)
        df = pd.read_csv(csv_file)
        
        # ERROR CHECK 3: Did Pandas find any columns?
        if df.empty or len(df.columns) == 0:
            return f"❌ ERROR: '{csv_file}' has no valid columns. Please check the text formatting inside."
            
        df.columns = df.columns.str.strip()
        
        # ERROR CHECK 4: Is the 'DAY/Time' header missing?
        if 'DAY/Time' not in df.columns:
            return f"❌ ERROR: '{csv_file}' is missing the 'DAY/Time' column header. Did you accidentally delete the top row?"

        # Find the row for the requested day
        day_data = df[df['DAY/Time'].str.upper() == day.upper()]
        
        if day_data.empty:
            return f"⚠️ No classes found for {day.capitalize()} in {class_div.upper()}."
            
        # Clean and format the row into a dictionary
        schedule = day_data.iloc[0].dropna().to_dict()
        
        # Build the final text response
        reply = f"\n📅 --- {day.upper()} TIMETABLE FOR {class_div.upper()} ---\n"
        reply += "-" * 35 + "\n"
        for time, subject in schedule.items():
            if time != "DAY/Time" and subject.strip():
                reply += f"[{time}]: {subject.strip()}\n"
        reply += "-" * 35 + "\n"
        
        return reply
        
    except EmptyDataError:
        return f"❌ ERROR: Pandas could not read '{csv_file}' because there is no data inside it."
    except Exception as e:
        return f"❌ FATAL ERROR reading '{csv_file}': {str(e)}"

# 4. The Main Chat Loop
def run_bot():
    print("🤖 IT-Genie is running! Type 'exit' or 'quit' to close.")
    print("Try asking: 'show me monday te a' or 'who is the hod?'\n")

    while True:
        try:
            user_input = input("You: ").lower().strip()
            
            # Handle empty inputs
            if not user_input:
                continue
            
            # Exit command
            if user_input in ['exit', 'quit', 'bye']:
                print("Bot: Goodbye! Have a great semester.")
                sys.exit()
                
            # Static Information Check
            elif "hod" in user_input or "head" in user_input:
                print("Bot:", static_info["hod"])
            elif "website" in user_input or "link" in user_input:
                print("Bot:", static_info["website"])
            elif "location" in user_input or "address" in user_input:
                print("Bot:", static_info["location"])
                
            # Timetable Check
            else:
                # 1. Identify the day and class independently
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
                
                # 2. Respond based on what we found
                if found_day and found_class:
                    print("Bot:", get_timetable(found_day, found_class))
                elif found_day and not found_class:
                    print(f"Bot: I see you asked for {found_day.capitalize()}, but which class? (e.g., 'monday te a')")
                elif found_class and not found_day:
                    print(f"Bot: You asked about {found_class.upper()}, but for which day? (e.g., 'monday te a')")
                else:
                    print("Bot: I can answer questions about the HOD, Website, or daily timetables (e.g., 'show me monday te a').")
                    
        except KeyboardInterrupt:
            # Handles if you press Ctrl+C to quit
            print("\nBot: Goodbye!")
            sys.exit()
        except Exception as e:
            # SAFETY NET: Catches any other error so the bot NEVER stops running
            print(f"Bot: Oops, I encountered a tiny glitch ({str(e)}). But I'm still here! Try asking something else.")

# Start the application
if __name__ == "__main__":
    run_bot()