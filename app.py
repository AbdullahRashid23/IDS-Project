import streamlit as st
import pandas as pd
import joblib
import os
import sys
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Page Configuration
st.set_page_config(page_title="Market Sentiment AI", layout="wide")

# 2. SMART IMPORT: Find 'preprocessing.py' whether it's in root or src/
try:
    import preprocessing  # Check root first
except ImportError:
    # Check src folder
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    try:
        import preprocessing
    except ImportError:
        # Fallback if file is missing completely
        import re
        class MockPrep:
            def clean_text(self, text):
                return re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
        preprocessing = MockPrep()

# 3. SMART PATHS: Find models/data whether in root or folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_file(filename, subfolder=None):
    # Check root first
    if os.path.exists(os.path.join(BASE_DIR, filename)):
        return os.path.join(BASE_DIR, filename)
    # Check subfolder
    if subfolder and os.path.exists(os.path.join(BASE_DIR, subfolder, filename)):
        return os.path.join(BASE_DIR, subfolder, filename)
    return None

# Locate Files
DATA_PATH = find_file('Sentiment_Stock_data.csv', 'data')
MODEL_PATH = find_file('model.pkl', 'models')
TFIDF_PATH = find_file('tfidf.pkl', 'models')

# 4. EMERGENCY TRAINING (Runs if models are still missing)
def train_model_on_fly():
    with st.spinner("⚙️ Models not found. Training a new one on the cloud..."):
        if not DATA_PATH or not os.path.exists(DATA_PATH):
            st.error("CRITICAL ERROR: 'Sentiment_Stock_data.csv' not found in root OR data/ folder.")
            st.stop()
            
        df = pd.read_csv(DATA_PATH)
        if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
        df = df.dropna(subset=['Sentence', 'Sentiment'])
        
        # Clean
        df['clean'] = df['Sentence'].apply(preprocessing.clean_text)
        
        # Train
        tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
        X = tfidf.fit_transform(df['clean'])
        y = df['Sentiment']
        
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)
        
        return model, tfidf

# 5. LOAD RESOURCES
@st.cache_resource
def load_resources():
    # If we found the files on disk, load them
    if MODEL_PATH and TFIDF_PATH:
        try:
            return joblib.load(MODEL_PATH), joblib.load(TFIDF_PATH)
        except:
            pass # If load fails (version mismatch), fall through to retrain
            
    # If not found or failed load, Train New
    return train_model_on_fly()

@st.cache_data
def load_data():
    if not DATA_PATH: return None
    df = pd.read_csv(DATA_PATH)
    if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
    df['Label'] = df['Sentiment'].map({0: 'Negative', 1: 'Positive'})
    return df

# --- UI LOGIC ---
st.title("📈 Financial News Sentiment AI")
st.markdown("### IDS Term Project")

model, tfidf = load_resources()
df = load_data()

# Navigation
nav = st.sidebar.radio("Menu", ["🏠 Overview", "📊 Analysis", "🤖 Live Prediction"])

if nav == "🏠 Overview":
    st.info("Goal: Predict stock movement signals (Buy/Sell) from news headlines.")
    st.markdown("""
    **How it works:**
    1. Reads financial news.
    2. Cleans text (NLP).
    3. Uses Logistic Regression to classify sentiment.
    """)

elif nav == "📊 Analysis":
    st.header("Exploratory Data Analysis")
    if df is not None:
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.pie(df, names='Label', title='Sentiment Distribution'), use_container_width=True)
        c2.plotly_chart(px.histogram(df, x='Label', title='Sentiment Counts'), use_container_width=True)
    else:
        st.warning("Data not loaded.")

elif nav == "🤖 Live Prediction":
    st.header("Test the AI")
    txt = st.text_area("Enter a Headline:", "Operating profit rose by 15% this quarter.")
    
    if st.button("Predict"):
        if model:
            clean_txt = preprocessing.clean_text(txt)
            vec = tfidf.transform([clean_txt])
            pred = model.predict(vec)[0]
            prob = model.predict_proba(vec)[0][pred]
            
            lbl = "POSITIVE (Good News)" if pred == 1 else "NEGATIVE (Bad News)"
            clr = "green" if pred == 1 else "red"
            
            st.markdown(f"## Prediction: <span style='color:{clr}'>{lbl}</span>", unsafe_allow_html=True)
            st.write(f"Confidence: **{prob:.2%}**")
        else:
            st.error("Model failed to load.")
