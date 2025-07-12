import re
import contractions
import pandas as pd
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# Initialize once
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

ACRONYM_DICT = {
    "lol": "laugh out loud", "brb": "be right back", "imo": "in my opinion", "idk": "i do not know",
    "tbh": "to be honest", "omg": "oh my god", "btw": "by the way", "fyi": "for your information",
    "imho": "in my humble opinion", "afaik": "as far as i know", "asap": "as soon as possible", "ttyl": "talk to you later",
    "gr8": "great", "l8r": "later", "w8": "wait", "hbd": "happy birthday", "smh": "shaking my head", "rofl": "rolling on the floor laughing",
    "bff": "best friends forever", "irl": "in real life", "jk": "just kidding", "np": "no problem", "nvm": "never mind", "wtf": "what the f***",
    "wth": "what the hell", "dm": "direct message", "ikr": "i know right", "ily": "i love you", "ilysm": "i love you so much", "omw": "on my way",
    "bc": "because", "bday": "birthday", "thx": "thanks", "ty": "thank you", "yw": "you are welcome", "gg": "good game",
    "idc": "i do not care", "g2g": "got to go", "atm": "at the moment", "tmi": "too much information", "ftw": "for the win",
    "lmao": "laughing my ass off", "afk": "away from keyboard", "xoxo": "hugs and kisses",
    # Mental health & emotion-related
    "mh": "mental health", "ocd": "obsessive compulsive disorder", "ptsd": "post traumatic stress disorder",
    "adhd": "attention deficit hyperactivity disorder", "bpd": "borderline personality disorder", "ed": "eating disorder",
    "su": "suicidal", "numb": "emotionally unresponsive", "anx": "anxiety", "depr": "depression", "stfu": "shut the f*** up",
    "fml": "f*** my life", "idwt": "i do not want to", "imsu": "i am suicidal",
    # Sentiment-heavy shorthand
    "ugh": "expression of frustration", "yay": "expression of joy", "meh": "expression of indifference",
    "sry": "sorry", "pls": "please", "plz": "please", "grrr": "expression of anger", "hugs": "virtual hugs",
    "rip": "rest in peace", "sadface": "sad face", "smile": "smiling face"
}
DIGIT_WORD_REPLACEMENTS_GLOBAL = {
    "gr8": "great", "l8r": "later", "w8": "wait", "2day": "today", "4u": "for you", "b4": "before"
}

# ---- Functions ----
def expand_contractions(text):
    return contractions.fix(text) if isinstance(text, str) else ""

def replace_special_tokens(text):
    if not isinstance(text, str): return ""
    text = re.sub(r"http\S+|www\S+|https\S+", "url", text)
    text = re.sub(r"@\w+", "user", text)
    text = re.sub(r"#\w+", "hashtag", text)
    return text

def expand_acronyms(text):
    if not isinstance(text, str): return ""
    return " ".join(ACRONYM_DICT.get(w.lower(), w) for w in text.split())

def handle_words_with_digits(text):
    if not isinstance(text, str): return ""
    words = []
    for w in text.split():
        if w.lower() in DIGIT_WORD_REPLACEMENTS_GLOBAL:
            words.append(DIGIT_WORD_REPLACEMENTS_GLOBAL[w.lower()])
        elif w.isdigit():
            continue
        else:
            words.append(re.sub(r'\d', '', w))
    return " ".join([w for w in words if w])

def reduce_repeated_chars(text):
    return re.sub(r"(.)\1{2,}", r"\1\1", text) if isinstance(text, str) else ""

def remove_stopwords(text):
    return " ".join([w for w in text.split() if w not in stop_words])

def lemmatize(text):
    doc = nlp(text)
    return " ".join([t.lemma_.lower() for t in doc if t.lemma_ != "-PRON-"])

def clean_single_text(text: str) -> str:
    t = str(text)
    t = expand_contractions(t)
    t = t.lower()
    t = replace_special_tokens(t)
    t = expand_acronyms(t)
    t = handle_words_with_digits(t)
    t = reduce_repeated_chars(t)
    t = re.sub(r'[^a-z0-9\s]', '', t)
    t = remove_stopwords(t)
    t = lemmatize(t)
    t = re.sub(r"\s+", " ", t).strip()
    return t
