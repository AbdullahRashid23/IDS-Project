import os
import joblib
import pandas as pd
import yfinance as yf
from textblob import TextBlob
import streamlit as st
import re

class SentimentEngine:
    def __init__(self):
        self.use_fallback = False
        self.model = None
        self.vectorizer = None
        self._load_resources()

    def _load_resources(self):
        """Attempts to load trained models; switches to fallback if missing."""
        try:
            # Adjust paths as needed for your specific deployment
            base_path = os.path.dirname(os.path.abspath(__file__))
            # Assuming models are in a folder relative to src or root
            model_path = os.path.join(base_path, '../models/model.pkl')
            tfidf_path = os.path.join(base_path, '../models/tfidf.pkl')

            if os.path.exists(model_path) and os.path.exists(tfidf_path):
                self.model = joblib.load(model_path)
                self.vectorizer = joblib.load(tfidf_path)
            else:
                self.use_fallback = True
        except Exception:
            self.use_fallback = True

    def _clean_text(self, text):
        """Basic text cleaning."""
        text = str(text).lower()
        text = re.sub(r'[^a-z\s]', '', text)
        return text

    def analyze(self, text):
        """
        Returns: { 'score': float (0-1), 'label': str, 'color': str }
        """
        if not text:
            return None

        if self.use_fallback:
            # Fallback: TextBlob Logic (Polarity -1 to 1 -> normalize to 0 to 1)
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            score = (polarity + 1) / 2 # Normalize to 0-1
        else:
            # Trained Model Logic
            clean = self._clean_text(text)
            vec = self.vectorizer.transform([clean])
            # Assuming class 1 is positive
            score = self.model.predict_proba(vec)[0][1]

        # Determine Label
        if score > 0.6:
            label = "BULLISH"
            color = "#10b981" # Green
        elif score < 0.4:
            label = "BEARISH"
            color = "#ef4444" # Red
        else:
            label = "NEUTRAL"
            color = "#94a3b8" # Grey

        return {"score": score, "label": label, "color": color}

    @st.cache_data(ttl=300) # Cache data for 5 mins
    def get_market_data(_self, ticker):
        """Fetches last 3 months of data for context."""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="3mo")
            return df
        except Exception:
            return pd.DataFrame() # Return empty if fail
