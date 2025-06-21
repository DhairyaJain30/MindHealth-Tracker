import streamlit as st
from agent import analyze_sentiment, suggest_action
from log import log_mood
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Mental Health Buddy", page_icon="🧠")
st.title("🧠 Mental Health Check-In Buddy")

# Show auto-ping welcome message once per session
st.session_state.setdefault("auto_ping", True)

if st.session_state.auto_ping:
    st.chat_message("assistant").markdown("👋 Hi! Just checking in 😊 How are you feeling today?")
    st.session_state.auto_ping = False  # So it doesn't repeat

# Session state to hold conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tabs: Chat + Mood Tracker
tab1, tab2 = st.tabs(["🗣️ Chat", "📈 Mood Tracker"])

# --- Chat Tab ---
with tab1:
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle user input
    if user_input := st.chat_input("How are you feeling?"):
        st.session_state.messages.append({"role": "user", "content": user_input})

        mood = analyze_sentiment(user_input)
        tip = suggest_action(user_input, mood)  # ✅ Fix here

        log_mood(user_input, mood)

        response = f"I sensed you're feeling **{mood}**.\n\n💡 Here's a tip: {tip}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


# --- Mood Tracker Tab ---
with tab2:
    try:
        df = pd.read_csv("mood_logs.csv", header=None, names=["Datetime", "Input", "Mood"])
        df["Datetime"] = pd.to_datetime(df["Datetime"])

        # Mood frequency chart
        mood_counts = df["Mood"].value_counts()
        st.subheader("📊 Mood Frequency")
        st.bar_chart(mood_counts)

        # Mood trend over time
        st.subheader("📅 Mood Over Time")
        mood_numeric = df["Mood"].map({"Positive": 1, "Neutral": 0, "Negative": -1})
        df["MoodValue"] = mood_numeric
        st.line_chart(df.set_index("Datetime")["MoodValue"])

    except Exception as e:
        st.warning("No mood data logged yet.")
