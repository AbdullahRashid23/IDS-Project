import os
import joblib
import re
from textblob import TextBlob
import streamlit as st

class SentimentBrain:
    def __init__(self):
        self.use_fallback = False
        self.model = None
        self.vectorizer = None
        self._initialize_core()

    def _initialize_core(self):
        """Loads Neural Core or engages Fallback Protocols."""
        try:
            # Look in ROOT directory
            base_path = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_path, 'model.pkl')
            tfidf_path = os.path.join(base_path, 'tfidf.pkl')

            if os.path.exists(model_path) and os.path.exists(tfidf_path):
                self.model = joblib.load(model_path)
                self.vectorizer = joblib.load(tfidf_path)
                print(">> CITADEL: Neural Core Online.")
            else:
                raise FileNotFoundError("Models missing.")
        except Exception as e:
            print(f">> CITADEL: {e}")
            print(">> CITADEL: Engaging Fallback Protocol (TextBlob).")
            self.use_fallback = True

    def _clean(self, text):
        return re.sub(r'[^a-zA-Z\s]', '', str(text).lower())

    def analyze(self, text):
        """Returns {'score': 0-1, 'label': str, 'color': hex}"""
        if not text: return None

        if self.use_fallback:
            # TextBlob Logic (-1.0 to 1.0 -> Normalize to 0.0 to 1.0)
            polarity = TextBlob(text).sentiment.polarity
            score = (polarity + 1) / 2
            confidence = abs(polarity) # Rough proxy for confidence
        else:
            # Sklearn Logic
            clean_text = self._clean(text)
            vec = self.vectorizer.transform([clean_text])
            score = self.model.predict_proba(vec)[0][1]
            confidence = score if score > 0.5 else (1 - score)

        # Classification
        if score > 0.6:
            label = "BULLISH"
            color = "#00ffa3" # HUD Green
        elif score < 0.4:
            label = "BEARISH"
            color = "#ff2a2a" # Alert Red
        else:
            label = "NEUTRAL"
            color = "#a0a0a0" # Grey

        return {
            "score": score,
            "label": label,
            "color": color,
            "confidence": confidence
        }
