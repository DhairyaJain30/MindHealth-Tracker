import schedule
import time
import webbrowser

def ping_user():
    print("🤖 Pinging user: How are you feeling today?")
    webbrowser.open("http://localhost:8501")

# Simulate ping every 1 minute (for demo)
schedule.every(1).minutes.do(ping_user)

print("Scheduler is running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)

