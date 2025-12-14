import streamlit as st
import pandas as pd
import joblib
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from collections import Counter

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Abdullah's AI | Financial Terminal",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ULTRA-MODERN UI (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&family=JetBrains+Mono:wght@400;700&display=swap');

    /* BACKGROUND & FONT */
    .stApp {
        background: radial-gradient(circle at 0% 0%, #1e1b4b 0%, #0f172a 100%);
        font-family: 'Outfit', sans-serif;
    }

    /* ABDULLAH'S AI HERO TITLE */
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(to right, #fbbf24, #f59e0b, #d97706);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(245, 158, 11, 0.3);
        margin-bottom: 0px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }

    /* TICKER TAPE */
    .ticker-wrap {
        width: 100%;
        background-color: rgba(0,0,0,0.5);
        padding: 8px 0;
        border-top: 1px solid rgba(255,255,255,0.1);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 30px;
        white-space: nowrap;
        overflow: hidden;
    }
    .ticker {
        display: inline-block;
        animation: marquee 40s linear infinite;
    }
    .ticker-item {
        display: inline-block;
        padding: 0 2rem;
        font-family: 'JetBrains Mono', monospace;
        color: #34d399; 
    }
    .ticker-item.neg { color: #f87171; }
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* GLASS CARDS */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: #f59e0b; /* Gold accent on hover */
    }

    /* CUSTOM INPUT */
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 12px;
    }
    .stTextArea textarea:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
    }

    /* GOLD BUTTONS */
    .stButton>button {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(217, 119, 6, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS (CRASH-PROOF) ---
def load_lottieurl(url: str):
    try:
        from streamlit_lottie import st_lottie
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# Animations
anim_robot = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_puciaact.json")

# Ticker Render
def render_ticker():
    ticker_html = """
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="ticker-item">ABDULLAH_AI +10.5% ▲</span>
            <span class="ticker-item">BTC +2.1% ▲</span>
            <span class="ticker-item neg">ETH -1.4% ▼</span>
            <span class="ticker-item">GOLD +0.5% ▲</span>
            <span class="ticker-item neg">TSLA -3.2% ▼</span>
            <span class="ticker-item">NVDA +4.1% ▲</span>
            <span class="ticker-item">MARKET_STATUS: OPEN 🟢</span>
        </div>
    </div>
    """
    st.markdown(ticker_html, unsafe_allow_html=True)

# --- 4. BACKEND LOGIC (ROBUST) ---
try:
    import preprocessing 
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    try: import preprocessing
    except ImportError:
        import re
        class MockPrep:
            def clean_text(self, text): return re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
        preprocessing = MockPrep()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def find_file(filename, subfolder=None):
    if os.path.exists(os.path.join(BASE_DIR, filename)): return os.path.join(BASE_DIR, filename)
    if subfolder and os.path.exists(os.path.join(BASE_DIR, subfolder, filename)): return os.path.join(BASE_DIR, subfolder, filename)
    return None

DATA_PATH = find_file('Sentiment_Stock_data.csv', 'data')
MODEL_PATH = find_file('model.pkl', 'models')
TFIDF_PATH = find_file('tfidf.pkl', 'models')

@st.cache_resource
def load_model():
    # If no model files, train one on the fly
    if not MODEL_PATH or not TFIDF_PATH:
        if not DATA_PATH: return None, None
        df = pd.read_csv(DATA_PATH)
        df['Sentence'] = df['Sentence'].astype(str) # Fix for mixed types
        df = df.dropna(subset=['Sentence', 'Sentiment'])
        if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
        
        df['clean'] = df['Sentence'].apply(preprocessing.clean_text)
        tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
        X = tfidf.fit_transform(df['clean'])
        model = LogisticRegression(max_iter=1000).fit(X, df['Sentiment'])
        return model, tfidf
    return joblib.load(MODEL_PATH), joblib.load(TFIDF_PATH)

@st.cache_data
def load_data():
    if not DATA_PATH: return None
    df = pd.read_csv(DATA_PATH)
    if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
    df['Sentence'] = df['Sentence'].astype(str) # Fix for mixed types
    df['Label'] = df['Sentiment'].map({0: 'Negative', 1: 'Positive'})
    return df

# --- 5. APP LAYOUT ---
model, tfidf = load_model()
df = load_data()

if 'history' not in st.session_state: st.session_state['history'] = []

# TITLE SECTION
render_ticker()
st.markdown('<div class="hero-title">ABDULLAH\'S AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Next-Generation Financial Sentiment Engine</div>', unsafe_allow_html=True)

# TABS
tab1, tab2, tab3 = st.tabs(["🚀 Live Terminal", "📊 Market Intel", "📂 Batch Processor"])

# --- TAB 1: LIVE TERMINAL ---
with tab1:
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📡 Enter Market News")
        
        # Randomizer
        headlines = [
            "Company revenue skyrockets by 200% beating all estimates.",
            "CEO steps down amid scandal, stocks tumble.",
            "Inflation fears grow as federal reserve hints at rate hikes.",
            "New AI partnership announced, investors are thrilled."
        ]
        
        col_r_btn, col_r_txt = st.columns([1, 4])
        with col_r_btn:
            if st.button("🎲 Lucky"):
                st.session_state['rand_text'] = random.choice(headlines)
        
        user_text = st.text_area(
            "Headline / Tweet", 
            value=st.session_state.get('rand_text', ""), 
            height=130,
            placeholder="e.g. Apple stocks surge after new iPhone launch..."
        )
        
        if st.button("ANALYZE SIGNAL", use_container_width=True):
            if not user_text:
                st.toast("⚠️ Please enter text first!")
            else:
                with st.spinner("Processing Neural Vectors..."):
                    time.sleep(0.5) # UI Effect
                    
                    # LOGIC:
                    clean = preprocessing.clean_text(user_text)
                    vec = tfidf.transform([clean])
                    
                    # Get "Positivity" Score (Probability of Class 1)
                    positivity_score = model.predict_proba(vec)[0][1]
                    
                    # Determine Label based on Score
                    if positivity_score >= 0.6:
                        label = "BULLISH 🐂"
                        color = "green"
                    elif positivity_score <= 0.4:
                        label = "BEARISH 🐻"
                        color = "red"
                    else:
                        label = "NEUTRAL ⚖️"
                        color = "gray"
                        
                    result = {
                        "text": user_text,
                        "label": label,
                        "score": positivity_score,
                        "time": time.strftime("%H:%M:%S")
                    }
                    st.session_state['history'].insert(0, result)
                    st.toast("Analysis Complete!", icon="✅")
                    
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        if st.session_state['history']:
            last = st.session_state['history'][0]
            score_pct = last['score'] * 100
            
            # Gauge Color Logic
            if score_pct > 50: gauge_color = "#34d399" # Green
            else: gauge_color = "#f87171" # Red
            
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; border-top: 4px solid {gauge_color}">
                <div style="font-size: 1rem; color: #94a3b8; margin-bottom: 5px;">AI VERDICT</div>
                <div style="font-size: 3rem; font-weight: 800; color: {gauge_color}; margin-bottom: 10px;">
                    {last['label']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # POSITIVITY METER (Gauge)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score_pct,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Positivity Meter (0-100)", 'font': {'color': 'white', 'size': 14}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickcolor': "white"},
                    'bar': {'color': "white", 'thickness': 0.2},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#333",
                    'steps': [
                        {'range': [0, 50], 'color': '#ef4444'}, # Red
                        {'range': [50, 100], 'color': '#10b981'} # Green
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': score_pct
                    }
                }
            ))
            fig.update_layout(height=220, margin=dict(t=30,b=10,l=20,r=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            # Empty State
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding: 40px;">
                <h3 style="color: #64748b;">Waiting for Input...</h3>
                <div style="font-size: 3rem;">🦅</div>
            </div>
            """, unsafe_allow_html=True)

    # HISTORY LOG
    if st.session_state['history']:
        st.markdown("### 📝 Recent Analysis")
        # Custom Dataframe
        h_df = pd.DataFrame(st.session_state['history'])
        st.dataframe(
            h_df[['time', 'label', 'score', 'text']],
            column_config={
                "score": st.column_config.ProgressColumn("Positivity", min_value=0, max_value=1, format="%.2f"),
                "label": st.column_config.TextColumn("Verdict"),
                "text": st.column_config.TextColumn("Headline", width="large"),
            },
            use_container_width=True,
            hide_index=True
        )

# --- TAB 2: MARKET INTEL ---
with tab2:
    if df is not None:
        # METRICS
        m1, m2, m3 = st.columns(3)
        m1.metric("Dataset Size", f"{len(df):,}", border=True)
        m2.metric("Bullish News", f"{len(df[df['Sentiment']==1]):,}", border=True)
        m3.metric("Bearish News", f"{len(df[df['Sentiment']==0]):,}", border=True)
        
        st.markdown("---")
        
        row1_1, row1_2 = st.columns(2)
        with row1_1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Global Sentiment Ratio")
            # Fixed Pie Chart
            fig_pie = px.pie(df, names='Label', hole=0.5, 
                             color='Label',
                             color_discrete_map={'Positive':'#10b981', 'Negative':'#ef4444'})
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                                  font=dict(color="white"), showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with row1_2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Top Keywords (Trending)")
            # Fix: Ensure all text is string
            all_text = " ".join(df['Sentence'].astype(str))
            clean_all = preprocessing.clean_text(all_text).split()
            counts = Counter(clean_all).most_common(10)
            w_df = pd.DataFrame(counts, columns=['Word', 'Count'])
            
            fig_bar = px.bar(w_df, x='Count', y='Word', orientation='h', 
                             text='Count', color='Count', color_continuous_scale='Oranges')
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                                  font=dict(color="white"), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        st.error("Dataset not found. Please ensure 'Sentiment_Stock_data.csv' is in the 'data' folder.")

# --- TAB 3: BATCH PROCESSOR ---
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📂 Bulk Analysis (CSV)")
    
    upl = st.file_uploader("Upload File (Must contain 'Sentence' column)", type=['csv'])
    
    if upl:
        if st.button("🚀 Run Batch Process"):
            try:
                b_df = pd.read_csv(upl)
                if 'Sentence' in b_df.columns:
                    b_df['Sentence'] = b_df['Sentence'].astype(str) # Safety Fix
                    
                    with st.spinner("Analyzing thousands of data points..."):
                        # Processing
                        b_df['clean'] = b_df['Sentence'].apply(preprocessing.clean_text)
                        X_batch = tfidf.transform(b_df['clean'])
                        
                        # Get Scores
                        probs = model.predict_proba(X_batch)
                        b_df['Positivity_Score'] = [p[1] for p in probs]
                        b_df['Prediction'] = ['Bullish' if s > 0.5 else 'Bearish' for s in b_df['Positivity_Score']]
                        
                        st.success("Batch Complete!")
                        st.dataframe(b_df.head(), use_container_width=True)
                        
                        # Download
                        csv = b_df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download Report", csv, "Abdullah_AI_Report.csv", "text/csv")
                else:
                    st.error("Error: CSV missing 'Sentence' column.")
            except Exception as e:
                st.error(f"File Error: {e}")
                
    st.markdown('</div>', unsafe_allow_html=True)
