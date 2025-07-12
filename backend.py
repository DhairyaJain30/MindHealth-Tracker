import torch
import streamlit as st
import pandas as pd
import pickle
import csv
from datetime import datetime, timedelta
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification
from dotenv import load_dotenv
from text_cleaning import clean_single_text
from google import genai

load_dotenv()

# Constants
MODEL_PATH = "YOUR_MODEL_PATH"
MAX_LEN = 128
MIN_WORDS_AFTER_CLEANING = 2
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ✅ Cache model + tokenizer load (runs only once)
@st.cache_resource
def load_model_and_tokenizer():
    tokenizer = RobertaTokenizerFast.from_pretrained(MODEL_PATH)
    model = RobertaForSequenceClassification.from_pretrained(MODEL_PATH).to(DEVICE)
    model.eval()
    return model, tokenizer

# ✅ Cache label map (optional, since it’s just a dict)
@st.cache_data
def get_label_map():
    return {
        0: "Anxiety",
        1: "Bipolar",
        2: "Depression",
        3: "Normal",
        4: "Personality disorder",
        5: "Stress",
        6: "Suicidal"
    }

# --- Predict user's mental state ---
def predict_mental_state(text: str) -> str:
    model, tokenizer = load_model_and_tokenizer()
    label_id_map = get_label_map()

    if not text.strip():
        return "Empty Input"

    cleaned_text = clean_single_text(text)
    if len(cleaned_text.split()) < MIN_WORDS_AFTER_CLEANING:
        return "Too short to classify"

    encoded = tokenizer.encode_plus(
        cleaned_text,
        add_special_tokens=True,
        max_length=MAX_LEN,
        return_token_type_ids=False,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_tensors="pt"
    )
    input_ids = encoded["input_ids"].to(DEVICE)
    attention_mask = encoded["attention_mask"].to(DEVICE)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        pred_id = torch.argmax(logits, dim=1).item()
        return label_id_map.get(pred_id, "Unknown")


# --- Suggest a self-care tip using Gemini ---
def suggest_action(mental_state: str) -> str:
    prompt = f"""
You are a friendly, supportive mental health assistant. The user is currently experiencing '{mental_state}'.
Suggest one empathetic and practical self-care tip for this emotional state. Be gentle, helpful, and concise.
Avoid medical advice or prescriptions. Provide only one clear suggestion.
"""
    try:
        client = genai.Client()
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text
    except Exception as e:
        print("❌ API error:", e)
        return "⚠️ Sorry, I couldn't fetch a suggestion right now. Try again later."


# --- Log mood input and prediction to CSV ---
def log_mood(user_input: str, mood: str):
    try:
        with open("mood_logs.csv", "a", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), user_input, mood])
    except Exception as e:
        print("❌ Error logging mood:", e)


# --- Weekly mood summary stats ---
def get_weekly_summary():
    try:
        df = pd.read_csv("mood_logs.csv", header=None, names=["Datetime", "Input", "Mood"])
        df["Datetime"] = pd.to_datetime(df["Datetime"])
        one_week_ago = datetime.now() - timedelta(days=7)
        df_week = df[df["Datetime"] >= one_week_ago]
        summary = df_week["Mood"].value_counts().sort_values(ascending=False)
        return summary.to_dict()
    except Exception as e:
        print("❌ Weekly summary error:", e)
        return {}
