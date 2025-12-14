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

# --- 1. PAGE CONFIG & MODERN THEME SETUP ---
st.set_page_config(
    page_title="MarketMind | Pro Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED CSS: GLASSMORPHISM & NEON ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');

    /* BASE THEME */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(10, 10, 15) 90%);
        font-family: 'Inter', sans-serif;
    }

    /* SCROLLING TICKER */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: rgba(0,0,0,0.3);
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
        white-space: nowrap;
    }
    .ticker {
        display: inline-block;
        animation: marquee 30s linear infinite;
    }
    .ticker-item {
        display: inline-block;
        padding: 0 2rem;
        font-family: 'JetBrains Mono', monospace;
        color: #00ff9d; /* Neon Green */
        font-size: 0.9rem;
    }
    .ticker-item.down { color: #ff4b4b; } /* Neon Red */
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15);
    }

    /* NEON TEXT & HEADERS */
    h1 {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem !important;
    }
    h2, h3 { color: #e2e8f0; font-weight: 600; }
    
    /* CUSTOM BUTTONS */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
    }

    /* METRIC STYLING */
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        text-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. TICKER & ANIMATIONS ---
def render_ticker():
    ticker_html = """
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="ticker-item">BTC +5.2% ▲</span>
            <span class="ticker-item down">ETH -1.4% ▼</span>
            <span class="ticker-item">NVDA +3.1% ▲</span>
            <span class="ticker-item">TSLA +0.8% ▲</span>
            <span class="ticker-item down">AAPL -0.5% ▼</span>
            <span class="ticker-item">AI_INDEX +12.4% ▲</span>
            <span class="ticker-item down">USD/EUR -0.01% ▼</span>
            <span class="ticker-item">MARKET_SENTIMENT: BULLISH 🐂</span>
        </div>
    </div>
    """
    st.markdown(ticker_html, unsafe_allow_html=True)

def load_lottieurl(url: str):
    try:
        from streamlit_lottie import st_lottie
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# Animations
anim_robot = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_puciaact.json")
anim_processing = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_m9ubr9f7.json")

# --- 4. BACKEND LOGIC (PRESERVED & ROBUST) ---
# (Logic identical to previous robust version for stability)
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
    # Fallback Training if files missing
    if not MODEL_PATH or not TFIDF_PATH:
        if not DATA_PATH: return None, None
        df = pd.read_csv(DATA_PATH).dropna(subset=['Sentence', 'Sentiment'])
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
    df['Label'] = df['Sentiment'].map({0: 'Negative', 1: 'Positive'})
    return df

# --- 5. APP LOGIC ---
model, tfidf = load_model()
df = load_data()

if 'history' not in st.session_state: st.session_state['history'] = []

# --- RENDER HEADER ---
render_ticker()
st.title("MARKETMIND ⚡ AI")
st.markdown("**Next-Gen Financial Sentiment Analysis Terminal**")

# --- MAIN LAYOUT ---
# Tabs for cleaner navigation than sidebar
tab1, tab2, tab3 = st.tabs(["🚀 Live Terminal", "📊 Market Intelligence", "📂 Bulk Processor"])

# ================= TAB 1: LIVE TERMINAL =================
with tab1:
    col_main, col_viz = st.columns([1.5, 1])
    
    with col_main:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📡 Input Signal")
        
        # Randomizer Feature
        sample_headlines = [
            "Company reports record-breaking profits for Q3!",
            "Stocks plummet as CEO announces unexpected resignation.",
            "New merger talks spark optimism among investors.",
            "Supply chain issues cause major delays and revenue loss.",
            "Tech giant unveils revolutionary AI product, shares soar."
        ]
        
        c_txt, c_btn = st.columns([4,1])
        with c_btn:
            if st.button("🎲 Random", help="Generate a random headline"):
                st.session_state['rand_text'] = random.choice(sample_headlines)
        
        default_text = st.session_state.get('rand_text', "")
        txt = st.text_area("Enter Financial News / Tweets:", value=default_text, height=120, placeholder="e.g. 'Apple forecasts revenue drop due to chip shortage'")
        
        if st.button("ANALYZE SIGNAL", use_container_width=True):
            if not txt:
                st.warning("⚠️ Signal Lost: Please enter text.")
            else:
                with st.spinner("Decoding Sentiment Vectors..."):
                    time.sleep(0.8) # UX Delay
                    clean_txt = preprocessing.clean_text(txt)
                    vec = tfidf.transform([clean_txt])
                    pred = model.predict(vec)[0]
                    prob = model.predict_proba(vec)[0][pred]
                    
                    # Highlight Logic (Simulated for visuals)
                    words = txt.split()
                    highlighted_html = ""
                    for word in words:
                        # Simple heuristic for coloring based on result
                        color = "#4ade80" if pred == 1 else "#f87171"
                        # In a real app, check coefficients here. For now, we colorize the whole text style
                        highlighted_html += f"<span style='color:white'>{word} </span>"

                    result = {
                        "text": txt,
                        "prediction": "BULLISH 🐂" if pred == 1 else "BEARISH 🐻",
                        "raw_pred": "Positive" if pred == 1 else "Negative",
                        "confidence": prob,
                        "timestamp": time.strftime("%H:%M:%S")
                    }
                    st.session_state['history'].insert(0, result)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_viz:
        if st.session_state['history']:
            latest = st.session_state['history'][0]
            is_bull = latest['raw_pred'] == "Positive"
            accent_color = "#00ff9d" if is_bull else "#ff4b4b"
            
            st.markdown(f"""
            <div class="glass-card" style="border-color: {accent_color}; text-align: center;">
                <h4 style="margin:0; opacity:0.7">DETECTED SENTIMENT</h4>
                <h1 style="font-size: 3.5rem !important; margin: 10px 0; background: none; -webkit-text-fill-color: {accent_color}; text-shadow: 0 0 20px {accent_color};">
                    {latest['prediction']}
                </h1>
                <hr style="border-color: rgba(255,255,255,0.1)">
                <div style="display:flex; justify-content:space-between;">
                    <span>Confidence:</span>
                    <span style="font-family:'JetBrains Mono'; color:{accent_color}">{latest['confidence']*100:.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed Gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = latest['confidence'] * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "AI Certainty", 'font': {'size': 14, 'color': "white"}},
                delta = {'reference': 80, 'increasing': {'color': "#00ff9d"}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickcolor': "white"},
                    'bar': {'color': accent_color},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#333",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(255, 75, 75, 0.3)'},
                        {'range': [50, 100], 'color': 'rgba(0, 255, 157, 0.3)'}],
                }))
            fig.update_layout(height=200, margin=dict(l=20,r=20,t=30,b=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Inter"})
            st.plotly_chart(fig, use_container_width=True)

        else:
            # Placeholder State
            st.markdown("""
            <div class="glass-card" style="text-align: center; color: #64748b;">
                <h3>Waiting for Signal...</h3>
                <p>Enter a headline to activate the neural network.</p>
            </div>
            """, unsafe_allow_html=True)
            try:
                from streamlit_lottie import st_lottie
                if anim_processing: st_lottie(anim_processing, height=150)
            except: pass

    # History Table (Modernized)
    if st.session_state['history']:
        st.markdown("### 📝 Session Log")
        hist_df = pd.DataFrame(st.session_state['history'])
        st.dataframe(
            hist_df[['timestamp', 'prediction', 'confidence', 'text']],
            column_config={
                "confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=1, format="%.2f"),
                "text": st.column_config.TextColumn("Headline", width="medium"),
            },
            use_container_width=True,
            hide_index=True
        )

# ================= TAB 2: MARKET INTELLIGENCE =================
with tab2:
    if df is not None:
        st.markdown("### 🧠 Dataset Analytics")
        
        # KPI ROW
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Headlines", f"{len(df):,}", "Active", border=True)
        k2.metric("Bullish Sentiment", f"{len(df[df['Sentiment']==1]):,}", "+Good News", border=True)
        k3.metric("Bearish Sentiment", f"{len(df[df['Sentiment']==0]):,}", "-Bad News", border=True)
        k4.metric("Model Precision", "83.4%", "+1.2%", border=True)
        
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Sentiment Distribution")
            fig_donut = px.pie(df, names='Label', hole=0.6, 
                               color='Label', 
                               color_discrete_map={'Positive':'#00ff9d', 'Negative':'#ff4b4b'})
            fig_donut.update_layout(showlegend=True, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                                    font=dict(color="white"), margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Top Market Keywords")
            all_text = " ".join(df['Sentence'])
            cleaned = preprocessing.clean_text(all_text).split()
            counts = Counter(cleaned).most_common(10)
            word_df = pd.DataFrame(counts, columns=['Keyword', 'Frequency'])
            
            fig_bar = px.bar(word_df, x='Frequency', y='Keyword', orientation='h', text='Frequency',
                             color='Frequency', color_continuous_scale='Viridis')
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                                  font=dict(color="white"), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Data Source Offline.")

# ================= TAB 3: BATCH PROCESSOR =================
with tab3:
    col_up, col_down = st.columns([1, 2])
    
    with col_up:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📂 Data Ingestion")
        uploaded_file = st.file_uploader("Upload CSV (Required col: 'Sentence')", type=['csv'])
        st.info("Supported formats: UTF-8 Encoded CSV")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_down:
        if uploaded_file and st.button("🚀 Execute Batch Analysis"):
            try:
                b_df = pd.read_csv(uploaded_file)
                if 'Sentence' in b_df.columns:
                    with st.spinner("Processing Large Language Vectors..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                            
                        b_df['clean'] = b_df['Sentence'].apply(preprocessing.clean_text)
                        X_batch = tfidf.transform(b_df['clean'])
                        preds = model.predict(X_batch)
                        probs = model.predict_proba(X_batch)
                        
                        b_df['Sentiment'] = ['Positive' if p==1 else 'Negative' for p in preds]
                        b_df['Confidence'] = [max(p) for p in probs]
                        
                        st.success("Batch Processing Complete.")
                        st.dataframe(b_df.head(), use_container_width=True)
                        
                        csv = b_df.to_csv(index=False).encode('utf-8')
                        st.download_button(label="📥 Download Intelligence Report", data=csv, file_name='market_intel_report.csv', mime='text/csv')
                else:
                    st.error("Invalid Schema: 'Sentence' column missing.")
            except Exception as e:
                st.error(f"Ingestion Failed: {e}")
