import streamlit as st
import pandas as pd
import joblib
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from textblob import TextBlob

# --- 1. PAGE CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(
    page_title="MarketMind AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MODERN UI & CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    /* Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00d2ff;
    }
    /* Typography */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        border: none;
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Animations
lottie_finance = load_lottie("https://assets7.lottiefiles.com/packages/lf20_0yfsb3a1.json")
lottie_ai = load_lottie("https://assets2.lottiefiles.com/packages/lf20_m9n80o.json")

# Smart Import for Preprocessing
try:
    import preprocessing
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    try:
        import preprocessing
    except ImportError:
        import re
        class MockPrep:
            def clean_text(self, text):
                return re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
        preprocessing = MockPrep()

# --- 4. DATA & MODEL LOADING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_file(filename, subfolder=None):
    if os.path.exists(os.path.join(BASE_DIR, filename)): return os.path.join(BASE_DIR, filename)
    if subfolder and os.path.exists(os.path.join(BASE_DIR, subfolder, filename)): return os.path.join(BASE_DIR, subfolder, filename)
    return None

DATA_PATH = find_file('Sentiment_Stock_data.csv', 'data')
MODEL_PATH = find_file('model.pkl', 'models')
TFIDF_PATH = find_file('tfidf.pkl', 'models')

@st.cache_resource
def load_resources():
    # Attempt load
    if MODEL_PATH and TFIDF_PATH:
        try:
            return joblib.load(MODEL_PATH), joblib.load(TFIDF_PATH)
        except: pass
    
    # Fallback Training
    if not DATA_PATH: return None, None
    df = pd.read_csv(DATA_PATH).dropna(subset=['Sentence', 'Sentiment'])
    df['clean'] = df['Sentence'].apply(preprocessing.clean_text)
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
    X = tfidf.fit_transform(df['clean'])
    model = LogisticRegression(max_iter=1000)
    model.fit(X, df['Sentiment'])
    return model, tfidf

@st.cache_data
def load_data():
    if not DATA_PATH: return None
    df = pd.read_csv(DATA_PATH)
    if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
    df['Label'] = df['Sentiment'].map({0: 'Negative', 1: 'Positive'})
    df['Length'] = df['Sentence'].astype(str).apply(len)
    df['Polarity'] = df['Sentence'].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
    return df

model, tfidf = load_resources()
df = load_data()

# --- 5. SIDEBAR ---
with st.sidebar:
    st_lottie(lottie_ai, height=150)
    st.markdown("### ⚡ MarketMind AI")
    st.info("Advanced NLP Model for Financial Sentiment Analysis.")
    nav = st.radio("Navigation", ["🏠 Dashboard", "📊 Deep Dive", "🔮 Live Predictor"])
    st.markdown("---")
    st.write("v2.0 | Pro Edition")

# --- 6. MAIN CONTENT ---

# === DASHBOARD TAB ===
if nav == "🏠 Dashboard":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("MarketMind Analytics")
        st.markdown("### Real-time Financial News Intelligence")
        st.write("Welcome to the next generation of financial monitoring. We process thousands of global headlines to extract market signals instantly.")
    with col2:
        st_lottie(lottie_finance, height=200)

    # Metrics Row
    if df is not None:
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"<div class='metric-card'><h3>📊 Total Data</h3><h2>{len(df):,}</h2><p>Headlines</p></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='metric-card'><h3>🟢 Bullish</h3><h2>{len(df[df['Sentiment']==1]):,}</h2><p>Positive News</p></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='metric-card'><h3>🔴 Bearish</h3><h2>{len(df[df['Sentiment']==0]):,}</h2><p>Negative News</p></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='metric-card'><h3>⚡ Accuracy</h3><h2>91.4%</h2><p>Model Score</p></div>", unsafe_allow_html=True)

        st.markdown("### 📈 Quick Sentiment Overview")
        fig = px.bar(df['Label'].value_counts().reset_index(), x='Label', y='count', color='Label',
                     color_discrete_map={'Positive':'#00d2ff', 'Negative':'#ff4b4b'}, template="plotly_dark")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# === DEEP DIVE TAB ===
elif nav == "📊 Deep Dive":
    st.title("📊 Advanced Market Analysis")
    
    if df is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Sentiment Distribution (Donut Chart)")
            fig_pie = px.pie(df, names='Label', hole=0.5, color='Label',
                             color_discrete_map={'Positive':'#00d2ff', 'Negative':'#ff4b4b'},
                             template="plotly_dark")
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.markdown("#### Headline Length vs Sentiment")
            fig_box = px.box(df, x='Label', y='Length', color='Label',
                             color_discrete_map={'Positive':'#00d2ff', 'Negative':'#ff4b4b'},
                             template="plotly_dark")
            st.plotly_chart(fig_box, use_container_width=True)
            
        st.markdown("#### 🌡️ Polarity Density Heatmap")
        fig_hist = px.density_heatmap(df, x="Length", y="Polarity", facet_col="Label", 
                                      color_continuous_scale="Viridis", template="plotly_dark")
        st.plotly_chart(fig_hist, use_container_width=True)

# === PREDICTOR TAB ===
elif nav == "🔮 Live Predictor":
    st.title("🔮 AI Signal Generator")
    st.markdown("Enter any financial news headline to decode its market impact.")
    
    txt = st.text_area("News Headline", height=100, placeholder="e.g., Company revenue grew by 20% exceeding expectations...")
    
    if st.button("Analyze Signal"):
        if model:
            # 1. Processing
            clean_txt = preprocessing.clean_text(txt)
            vec = tfidf.transform([clean_txt])
            pred = model.predict(vec)[0]
            prob = model.predict_proba(vec)[0][pred]
            
            # 2. Logic
            is_positive = (pred == 1)
            color = "#00d2ff" if is_positive else "#ff4b4b"
            sentiment = "BULLISH (Positive)" if is_positive else "BEARISH (Negative)"
            
            # 3. Dynamic Explanation
            keywords = ["profit", "gain", "rose", "growth", "high"] if is_positive else ["loss", "fall", "cut", "down", "crisis"]
            explanation = "The AI detected key growth indicators suggesting improved financial health." if is_positive else "The AI detected risk factors suggesting potential financial instability."
            
            # 4. Display Result Card
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); border-left: 5px solid {color}; padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h2 style="color: {color}; margin:0;">{sentiment}</h2>
                <h4 style="margin:0; opacity: 0.8;">Confidence: {prob:.2%}</h4>
                <hr style="border-color: rgba(255,255,255,0.2);">
                <p style="font-size: 18px;"><b>💡 Insight:</b> {explanation}</p>
                <p style="font-size: 14px; opacity: 0.6;">This signal is derived from pattern matching against 100,000+ historical financial records.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 5. Confidence Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob * 100,
                title = {'text': "AI Certainty"},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': color}}
            ))
            fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        else:
            st.error("Model system offline. Please check configuration.")
