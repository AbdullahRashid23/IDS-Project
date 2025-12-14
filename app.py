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

# --- 2. ULTRA-MODERN UI (MOBILE OPTIMIZED) ---
st.markdown("""
<style>
    /* IMPORT NEW FONT (POPPINS) */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    /* 1. GLOBAL TEXT FORCE - FIXES MOBILE VISIBILITY */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: #ffffff !important; /* Force all text white */
    }

    /* 2. BACKGROUND */
    .stApp {
        background: radial-gradient(circle at 0% 0%, #0f172a 0%, #020617 100%);
    }

    /* 3. INPUT AREAS (The text inside the box) */
    .stTextArea textarea {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important; /* iOS Fix */
        font-family: 'Poppins', sans-serif !important;
        font-size: 16px !important; /* Prevents zoom on mobile */
        border-radius: 12px;
    }
    .stTextArea textarea:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
    }
    
    /* 4. LABELS & HEADERS */
    label, .stMarkdown p {
        color: #e2e8f0 !important;
        font-weight: 400;
    }
    h1, h2, h3 {
        color: white !important;
        font-weight: 700;
    }

    /* ABDULLAH'S AI HERO TITLE */
    .hero-title {
        font-size: 3.5rem; /* Slightly smaller for mobile safety */
        font-weight: 800;
        background: linear-gradient(to right, #fbbf24, #f59e0b, #d97706);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(245, 158, 11, 0.3);
        margin-bottom: 5px;
        line-height: 1.2;
    }
    .hero-subtitle {
        color: #94a3b8 !important;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }

    /* TICKER TAPE */
    .ticker-wrap {
        width: 100%;
        background-color: rgba(0,0,0,0.6);
        padding: 10px 0;
        border-top: 1px solid rgba(255,255,255,0.1);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
        white-space: nowrap;
        overflow: hidden;
    }
    .ticker {
        display: inline-block;
        animation: marquee 35s linear infinite;
    }
    .ticker-item {
        display: inline-block;
        padding: 0 2rem;
        font-family: 'JetBrains Mono', monospace;
        color: #34d399 !important; 
        font-size: 0.9rem;
    }
    .ticker-item.neg { color: #f87171 !important; }
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* GLASS CARDS */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
    }

    /* GOLD BUTTONS */
    .stButton>button {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%; /* Full width on mobile */
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(217, 119, 6, 0.5);
    }
    
    /* Toast Fix */
    div[data-baseweb="toast"] {
        background-color: #1e293b !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def load_lottieurl(url: str):
    try:
        from streamlit_lottie import st_lottie
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

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

# --- 4. BACKEND LOGIC ---
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
    if not MODEL_PATH or not TFIDF_PATH:
        if not DATA_PATH: return None, None
        df = pd.read_csv(DATA_PATH)
        df['Sentence'] = df['Sentence'].astype(str)
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
    df['Sentence'] = df['Sentence'].astype(str)
    df['Label'] = df['Sentiment'].map({0: 'Negative', 1: 'Positive'})
    return df

# --- 5. APP LAYOUT ---
model, tfidf = load_model()
df = load_data()

if 'history' not in st.session_state: st.session_state['history'] = []

# HEADER
render_ticker()
st.markdown('<div class="hero-title">ABDULLAH\'S AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Next-Generation Financial Sentiment Engine</div>', unsafe_allow_html=True)

# TABS
tab1, tab2, tab3 = st.tabs(["🚀 Live Terminal", "📊 Market Intel", "📂 Batch Processor"])

# --- TAB 1: LIVE TERMINAL ---
with tab1:
    # Use standard container first for mobile stacking
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📡 Enter Market News")
    
    # Randomizer
    headlines = [
        "Company revenue skyrockets by 200% beating all estimates.",
        "CEO steps down amid scandal, stocks tumble.",
        "Inflation fears grow as federal reserve hints at rate hikes.",
        "New AI partnership announced, investors are thrilled."
    ]
    
    col_r_btn, col_r_txt = st.columns([1, 3])
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
            st.warning("⚠️ Please enter text first!")
        else:
            with st.spinner("Processing..."):
                time.sleep(0.5)
                
                clean = preprocessing.clean_text(user_text)
                vec = tfidf.transform([clean])
                positivity_score = model.predict_proba(vec)[0][1]
                
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
                
    st.markdown('</div>', unsafe_allow_html=True)

    # RESULT SECTION
    if st.session_state['history']:
        last = st.session_state['history'][0]
        score_pct = last['score'] * 100
        if score_pct > 50: gauge_color = "#34d399"
        else: gauge_color = "#f87171"
        
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; border-top: 4px solid {gauge_color}">
            <div style="font-size: 1rem; color: #cbd5e1 !important; margin-bottom: 5px;">AI VERDICT</div>
            <div style="font-size: 2.5rem; font-weight: 800; color: {gauge_color} !important; margin-bottom: 10px;">
                {last['label']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # GAUGE
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score_pct,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Sentiment Score", 'font': {'color': 'white', 'size': 14}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': "white"},
                'bar': {'color': "white", 'thickness': 0.2},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#333",
                'steps': [
                    {'range': [0, 50], 'color': '#ef4444'}, 
                    {'range': [50, 100], 'color': '#10b981'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': score_pct
                }
            }
        ))
        fig.update_layout(height=200, margin=dict(t=30,b=10,l=20,r=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)

    # HISTORY LOG
    if st.session_state['history']:
        st.markdown("### 📝 Recent Analysis")
        h_df = pd.DataFrame(st.session_state['history'])
        st.dataframe(
            h_df[['time', 'label', 'score', 'text']],
            column_config={
                "score": st.column_config.ProgressColumn("Positivity", min_value=0, max_value=1, format="%.2f"),
                "label": st.column_config.TextColumn("Verdict"),
                "text": st.column_config.TextColumn("Headline", width="medium"),
            },
            use_container_width=True,
            hide_index=True
        )

# --- TAB 2: MARKET INTEL ---
with tab2:
    if df is not None:
        m1, m2, m3 = st.columns(3)
        m1.metric("Dataset Size", f"{len(df):,}")
        m2.metric("Bullish News", f"{len(df[df['Sentiment']==1]):,}")
        m3.metric("Bearish News", f"{len(df[df['Sentiment']==0]):,}")
        
        st.markdown("---")
        
        row1_1, row1_2 = st.columns(2)
        with row1_1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Global Sentiment")
            fig_pie = px.pie(df, names='Label', hole=0.5, 
                             color='Label',
                             color_discrete_map={'Positive':'#10b981', 'Negative':'#ef4444'})
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                                  font=dict(color="white"), showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with row1_2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Trending Keywords")
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

# --- TAB 3: BATCH PROCESSOR ---
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📂 Bulk Analysis")
    
    upl = st.file_uploader("Upload File (Must contain 'Sentence' column)", type=['csv'])
    
    if upl:
        if st.button("🚀 Run Process"):
            try:
                b_df = pd.read_csv(upl)
                if 'Sentence' in b_df.columns:
                    b_df['Sentence'] = b_df['Sentence'].astype(str)
                    
                    with st.spinner("Analyzing..."):
                        b_df['clean'] = b_df['Sentence'].apply(preprocessing.clean_text)
                        X_batch = tfidf.transform(b_df['clean'])
                        
                        probs = model.predict_proba(X_batch)
                        b_df['Positivity_Score'] = [p[1] for p in probs]
                        b_df['Prediction'] = ['Bullish' if s > 0.5 else 'Bearish' for s in b_df['Positivity_Score']]
                        
                        st.success("Done!")
                        st.dataframe(b_df.head(), use_container_width=True)
                        
                        csv = b_df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download", csv, "Abdullah_AI_Report.csv", "text/csv")
                else:
                    st.error("Missing 'Sentence' column.")
            except Exception as e:
                st.error(f"Error: {e}")
                
    st.markdown('</div>', unsafe_allow_html=True)
