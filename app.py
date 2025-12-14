import streamlit as st
import pandas as pd
import joblib
import os
import sys
import plotly.express as px

st.set_page_config(page_title="Market Sentiment", layout="wide")
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
try: import preprocessing
except: pass

@st.cache_data
def load_data():
    path = os.path.join("data", "Sentiment_Stock_data.csv")
    if not os.path.exists(path): return None
    df = pd.read_csv(path)
    if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
    df['Label'] = df['Sentiment'].map({0: 'Negative', 1: 'Positive'})
    return df

@st.cache_resource
def load_model():
    mp = os.path.join("models", "model.pkl")
    vp = os.path.join("models", "tfidf.pkl")
    if os.path.exists(mp): return joblib.load(mp), joblib.load(vp)
    return None, None

st.title("📈 Financial News Sentiment AI")
nav = st.sidebar.radio("Navigation", ["Overview", "Dashboard", "Predictor"])
df = load_data()
model, tfidf = load_model()

if nav == "Overview":
    st.info("Predicting stock signals from news headlines.")
    if df is not None: st.write(df.head())

elif nav == "Dashboard":
    if df is not None:
        st.plotly_chart(px.pie(df, names='Label', title='Sentiment Ratio'))
    else: st.warning("No Data")

elif nav == "Predictor":
    txt = st.text_area("Headline:", "Company reports record profits.")
    if st.button("Predict"):
        if model:
            import re
            clean = re.sub(r'[^a-zA-Z\s]', '', txt.lower())
            vec = tfidf.transform([clean])
            pred = model.predict(vec)[0]
            prob = model.predict_proba(vec)[0][pred]
            st.success(f"Prediction: {'POSITIVE' if pred==1 else 'NEGATIVE'} ({prob:.2%})")
        else: st.error("Model not trained.")
