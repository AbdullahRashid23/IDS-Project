import pandas as pd
import joblib
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import preprocessing

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'Sentiment_Stock_data.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
TFIDF_PATH = os.path.join(BASE_DIR, 'models', 'tfidf.pkl')

def train():
    print("   [Train Script] Loading Data...")
    if not os.path.exists(DATA_PATH):
        print("   [Train Script] ❌ DATA NOT FOUND.")
        return

    df = pd.read_csv(DATA_PATH)
    if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
    df = df.dropna(subset=['Sentence', 'Sentiment'])
    
    print("   [Train Script] Cleaning...")
    df['clean'] = df['Sentence'].apply(preprocessing.clean_text)
    
    print("   [Train Script] Vectorizing...")
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
    X = tfidf.fit_transform(df['clean'])
    y = df['Sentiment']
    
    print("   [Train Script] Training...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    
    print("   [Train Script] Saving Models...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(tfidf, TFIDF_PATH)
    print(f"   [Train Script] ✅ SAVED: {MODEL_PATH}")

if __name__ == "__main__":
    train()
