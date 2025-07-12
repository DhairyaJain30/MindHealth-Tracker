import streamlit as st
from backend import predict_mental_state, suggest_action,get_weekly_summary,log_mood
import pandas as pd 
import matplotlib.pyplot as plt
from datetime import datetime
import os

st.set_page_config(page_title="Mental Health Buddy", page_icon="🧠")
st.title("🧠 Mental Health Check-In Buddy")

# Show auto-ping welcome message once per session
st.session_state.setdefault("auto_ping", True)

if st.session_state.auto_ping:
    st.chat_message("assistant").markdown("👋 Hi! Just checking in 😊 How are you feeling today?")
    st.session_state.auto_ping = False  

# Session state to hold conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tabs: Chat + Mood Tracker
tab1, tab2 = st.tabs(["🗣️ Chat", "📈 Mood Tracker"])

# --- Chat Tab ---
with tab1:
    if st.button("🧹 Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    # Display all previous messages in order
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle new user input
    if user_input := st.chat_input("How are you feeling?"):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get prediction and tip
        mental_state = predict_mental_state(user_input)
        tip = suggest_action(mental_state)
        log_mood(user_input, mental_state)

        # Prepare assistant response
        response = (
            f"🧠 Based on what you shared, I detected: **{mental_state}**.\n\n"
            f"💡 Here's something you can try: {tip}"
        )

        # Append and display assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


# --- Mood Tracker Tab ---

with tab2:
    try:
        df = pd.read_csv("mood_logs.csv", header=None, names=["Datetime", "Input", "Mood"])
        df["Datetime"] = pd.to_datetime(df["Datetime"])

        st.subheader("📊 Mood Frequency")
        mood_counts = df["Mood"].value_counts()
        st.bar_chart(mood_counts)

        st.subheader("📅 Mood Over Time (Trend)")

        # Assign score values for trend plotting
        mood_order = ['Normal', 'Stress', 'Anxiety', 'Depression', 'Bi-Polar', 'Personality Disorder', 'Suicidal']
        mood_score = {label: idx for idx, label in enumerate(mood_order)}

        df["MoodValue"] = df["Mood"].map(mood_score).fillna(0)
        df_sorted = df.sort_values("Datetime")

        st.line_chart(df_sorted.set_index("Datetime")["MoodValue"])
        
        st.subheader("🗓️ Weekly Mood Summary")

        summary = get_weekly_summary()
        if summary:
            st.write("Here's a breakdown of your moods this week:")
            st.bar_chart(pd.Series(summary))
        else:
            st.info("No data logged in the last 7 days.")

        # Optional: show raw logs
        with st.expander("📄 Show Mood Log Table"):
            st.dataframe(df_sorted)

    except Exception as e:
        st.warning("No mood data logged yet.")

