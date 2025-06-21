from langchain.chat_models import AzureChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("deployment-name"),
    azure_endpoint=os.getenv("endpoint"),
    api_key=os.getenv("api_key"),
    api_version=os.getenv("api_version"),
    temperature=0.5
)

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    if score['compound'] >= 0.5:
        return "Positive"
    elif score['compound'] <= -0.5:
        return "Negative"
    else:
        return "Neutral"

def suggest_action(mood,text):
    prompt = f"""
    You are a compassionate mental health assistant.
    A user just shared the following:
    \"\"\"{text}\"\"\"
    
    The user's mood is detected as {mood.lower()}.
    Based on their words and mood, kindly suggest one or two thoughtful and realistic actions or tips to help improve or maintain their well-being.
    Keep your tone warm, supportive, and non-judgmental.
    """
    response = llm.invoke(prompt)
    return response.content

tools = [
    Tool(name="SentimentAnalyzer", func=analyze_sentiment, description="Analyzes sentiment as Positive, Neutral, or Negative."),
    Tool(name="MoodSuggester", func=suggest_action, description="Provides mental wellness suggestions based on mood.")
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
