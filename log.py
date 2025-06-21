import csv
from datetime import datetime

def log_mood(user_input, mood):
    with open("mood_logs.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), user_input, mood])
