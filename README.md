# MindHealth Tracker 🧠📈

**MindHealth Tracker** is a personalized mental wellness check-in tool built using Streamlit, Transformers, and an LLM API.  
Users describe how they're feeling, and the app classifies their mental state (like depression, anxiety, or stress) using a fine-tuned RoBERTa model trained on a Kaggle mental health dataset. It then suggests mood-improving activities and tracks emotional trends over time with beautiful visualizations.

---

## 🔧 Features

- 🤖 Detects mental state from free-form user text
- 📊 Tracks mood over time with weekly summaries
- 🧠 RoBERTa model fine-tuned on 7 mental health categories
- 💬 Personalized wellness suggestions via LLM (e.g., OpenAI)
- 📈 Matplotlib visualizations & CSV logging
- 🌐 Clean Streamlit UI with session chat

---

## ⚙️ Installation
# Clone the repository
```bash
git clone https://github.com/DhairyaJain30/MindHealth-Tracker.git
cd MindHealth-Tracker

```

# Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

# Install dependencies
```bash
pip install -r requirements.txt
```

## 💻 How to Use

### 🟢 Run the App

Once you've installed the dependencies, launch the Streamlit app:
```bash
streamlit run app.py
```
## Using the Fine-Tuned RoBERTa Model
This app uses a fine-tuned RoBERTa model trained on a labeled mental health dataset. The model files are large, so they are not included in this GitHub repo.

###  Download the Model from the link
📦 https://drive.google.com/file/d/18c9tv2mS8oID8bkqxbupq9BhlcE9ydQa/view?usp=sharing

### After downloading:

Unzip the file. You’ll get a folder named roberta_model/

Place this folder in the root of your project directory (i.e., next to app.py)

Your folder structure should look like this:
```bash
MindHealth-Tracker/
├── app.py
├── roberta_model/
│   ├── config.json
│   ├── pytorch_model.safetensors
│   ├── tokenizer_config.json
│   ├── vocab.json
│   └── merges.txt
```

📦 Tech Stack
- Streamlit – UI
- Transformers (HuggingFace) – RoBERTa model
- Gemini API – Suggestions
- Matplotlib / Pandas – Logging & visualization

```markdown
![Home Page](assets/home.png)
