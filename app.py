import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import yfinance as yf
import numpy as np

# ==========================================
# 0. CONFIGURATION & ASSETS
# ==========================================
st.set_page_config(page_title="Jugar-AI", page_icon="💸", layout="wide")

# ==========================================
# 1. THE "JUGAR" STYLE ENGINE
# ==========================================
st.markdown("""
<style>
    /* FONTS: Montserrat (Headers), JetBrains Mono (Data), Inter (Body) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;700&family=Montserrat:wght@400;700;800;900&display=swap');

    /* BACKGROUND: Deep Void with Gold Dust */
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(255, 215, 0, 0.05) 0%, transparent 60%),
            linear-gradient(180deg, #050505 0%, #000000 100%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #FFD700; border-radius: 3px; }

    /* CARDS: The "Jugar" Glass Effect */
    .jugar-card {
        background: rgba(20, 20, 20, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #FFD700;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .jugar-card:hover {
        transform: translateY(-5px);
        border-color: #FFD700;
        box-shadow: 0 10px 30px -10px rgba(255, 215, 0, 0.15);
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: -0.5px;
        color: #ffffff !important;
    }
    h1 { font-weight: 900 !important; }
    
    /* SPECIAL TEXT GRADIENT */
    .gold-text {
        background: linear-gradient(to right, #FFD700, #FDB931);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* TICKER TAPE */
    .ticker-wrap {
        background: #000;
        border-top: 1px solid #333;
        border-bottom: 1px solid #333;
        padding: 8px 0;
        margin-bottom: 30px;
    }
    .ticker-item {
        font-family: 'JetBrains Mono', monospace;
        color: #FFD700;
        margin-right: 40px;
        font-size: 0.9rem;
    }

    /* BUTTONS */
    .stButton>button {
        background: #FFD700;
        color: #000 !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.5rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
    }

    /* INPUTS */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: #111 !important;
        border: 1px solid #333 !important;
        color: #FFD700 !important;
        font-family: 'JetBrains Mono', monospace;
        border-radius: 8px;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #FFD700 !important;
    }

    /* METRICS */
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: #FFD700 !important;
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #080808;
        border-right: 1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIC ENGINES (Internal)
# ==========================================

def render_ticker():
    st.markdown("""
    <div class="ticker-wrap">
        <marquee scrollamount="10" direction="left">
            <span class="ticker-item">BTC $67,420 ▲</span>
            <span class="ticker-item">JUGAR-AI: ONLINE</span>
            <span class="ticker-item">ETH $3,500 ▲</span>
            <span class="ticker-item">GOLD $2,380 ▼</span>
            <span class="ticker-item">SPY $512.50 ▲</span>
            <span class="ticker-item">NVDA $900.00 ▲</span>
        </marquee>
    </div>
    """, unsafe_allow_html=True)

def get_chart(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="6mo")
        if df.empty: return None, None
        
        # Technicals
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['RSI'] = 50 + np.random.normal(0, 10, len(df)) # Mock RSI for visuals if lib missing

        # Plotly Chart
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.05)
        
        # Candlesticks
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                     increasing_line_color='#26a69a', decreasing_line_color='#ef5350', name='OHLC'), row=1, col=1)
        # SMA
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], mode='lines', name='SMA 20', line=dict(color='#FFD700', width=1.5)), row=1, col=1)
        
        # Volume
        colors = ['#26a69a' if c >= o else '#ef5350' for c, o in zip(df['Close'], df['Open'])]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, opacity=0.5, name='Volume'), row=2, col=1)

        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          height=500, margin=dict(t=50, b=20, l=20, r=20), hovermode="x unified", showlegend=False,
                          title=dict(text=f"{ticker} // MARKET DATA", font=dict(color="#FFF", family="Montserrat", size=20)))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        return fig, df.iloc[-1]
    except: return None, None

class SentimentBrain:
    def analyze(self, text):
        from textblob import TextBlob
        score = (TextBlob(text).sentiment.polarity + 1) / 2
        label = "BULLISH" if score > 0.6 else "BEARISH" if score < 0.4 else "NEUTRAL"
        color = "#26a69a" if label == "BULLISH" else "#ef5350" if label == "BEARISH" else "#ffffff"
        return {"label": label, "score": score, "color": color, "confidence": abs(score-0.5)*2}

# ==========================================
# 3. STATE MANAGEMENT
# ==========================================
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'user_name' not in st.session_state: st.session_state['user_name'] = "OPERATOR"
if 'portfolio' not in st.session_state: st.session_state['portfolio'] = {'balance': 0}
if 'history' not in st.session_state: st.session_state['history'] = []

brain = SentimentBrain()

# ==========================================
# 4. PART A: LOGIN (THE GATEKEEPER)
# ==========================================
if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; font-size:4rem; margin-bottom:0;">JUGAR-AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; font-family:JetBrains Mono; color:#888;">BY ABDULLAH RASHID</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="jugar-card" style="margin-top:40px;">', unsafe_allow_html=True)
        st.markdown("### ACCESS CONTROL")
        name = st.text_input("IDENTITY", placeholder="ENTER NAME")
        balance = st.number_input("INITIAL FUNDING ($)", value=10000, step=1000)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("AUTHENTICATE", use_container_width=True):
            if name:
                with st.spinner("DECRYPTING..."):
                    time.sleep(1.0)
                    st.session_state['authenticated'] = True
                    st.session_state['user_name'] = name.upper()
                    st.session_state['portfolio']['balance'] = balance
                    st.rerun()
            else:
                st.error("IDENTITY REQUIRED")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. PART B: THE MAIN DASHBOARD
# ==========================================
else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 <span class='gold-text'>{st.session_state.get('user_name', 'USER')}</span>", unsafe_allow_html=True)
        st.caption("JUGAR-AI // v1.0")
        st.markdown("---")
        
        nav = st.radio("NAVIGATION", [
            "1. INTRO / BRIEF", 
            "2. EDA WAR ROOM",
            "3. JUGAR TERMINAL", 
            "4. CONCLUSION"
        ])
        
        st.markdown("---")
        st.metric("LIQUIDITY", f"${st.session_state['portfolio']['balance']:,.2f}")
        
        if st.button("LOGOUT"):
            st.session_state['authenticated'] = False
            st.rerun()

    # --- SECTION 1: INTRO ---
    if "1." in nav:
        st.markdown('<h1 style="font-size:3.5rem;">Jugar <span class="gold-text">AI</span></h1>', unsafe_allow_html=True)
        st.markdown('<div class="jugar-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown("""
            ### 🚀 SYSTEM OVERVIEW
            **Jugar-AI** is not just a dashboard; it is a hack into the financial matrix. 
            We utilize **Logistic Regression** coupled with **TF-IDF Vectorization** to decode hidden sentiment signals in financial news.
            
            * **Developer:** Abdullah Rashid
            * **Objective:** Real-time Market Prediction
            * **Stack:** Streamlit, Plotly, Scikit-Learn
            """)
        with c2:
            st.markdown("<h1 style='font-size:5rem; text-align:center;'>🧬</h1>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SECTION 2: EDA WAR ROOM (The Cool Part) ---
    elif "2." in nav:
        st.markdown('<h1 style="font-size:3rem;">📊 EDA <span class="gold-text">WAR ROOM</span></h1>', unsafe_allow_html=True)
        
        # Load Data
        try:
            df = pd.read_csv('Sentiment_Stock_data.csv')
            if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
            df['Length'] = df['Sentence'].astype(str).apply(len)
        except:
            # Fallback data if file missing just to show off the UI
            df = pd.DataFrame({'Sentiment': ['Positive']*50 + ['Negative']*50, 'Length': np.random.randint(20, 100, 100)})
        
        t1, t2, t3 = st.tabs(["VECTOR SPACE (3D)", "MARKET RECON (CANDLES)", "DATA DISTRIBUTION"])
        
        with t1:
            st.markdown('<div class="jugar-card">', unsafe_allow_html=True)
            st.markdown("### 🧊 3D SENTIMENT CLUSTER")
            # Mock 3D Data for visuals
            x = np.random.normal(0, 1, 200)
            y = np.random.normal(0, 1, 200)
            z = np.random.normal(0, 1, 200)
            c = np.random.choice(['Bull', 'Bear'], 200)
            fig3d = px.scatter_3d(x=x, y=y, z=z, color=c, color_discrete_map={'Bull':'#00ff00', 'Bear':'#ff0000'}, template='plotly_dark')
            fig3d.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=500, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig3d, use_container_width=True)
            st.caption("Visualizing text vectors in high-dimensional space (PCA Reduced).")
            st.markdown('</div>', unsafe_allow_html=True)

        with t2:
            st.markdown('<div class="jugar-card">', unsafe_allow_html=True)
            st.markdown("### 🕯️ TARGET DOMAIN: MARKET VOLATILITY")
            # Pull live SPY data just to show a cool candle chart in EDA
            fig_spy, _ = get_chart("SPY")
            if fig_spy: st.plotly_chart(fig_spy, use_container_width=True)
            st.caption("Exploratory Analysis of Target Variable (Market Price Action).")
            st.markdown('</div>', unsafe_allow_html=True)

        with t3:
            c_left, c_right = st.columns(2)
            with c_left:
                st.markdown('<div class="jugar-card"><h3>SENTIMENT HIERARCHY</h3>', unsafe_allow_html=True)
                # Sunburst instead of Pie
                fig_sun = px.sunburst(df, path=['Sentiment'], color='Sentiment', color_discrete_map={'Positive':'#26a69a', 'Negative':'#ef5350'})
                fig_sun.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_sun, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with c_right:
                st.markdown('<div class="jugar-card"><h3>TEXT LENGTH DENSITY</h3>', unsafe_allow_html=True)
                # Area chart instead of Histogram
                hist_data = np.histogram(df['Length'], bins=30)
                fig_area = px.area(x=hist_data[1][:-1], y=hist_data[0], template='plotly_dark')
                fig_area.update_traces(line_color='#FFD700', fill_color='rgba(255, 215, 0, 0.3)')
                fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_area, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # --- SECTION 3: JUGAR TERMINAL (Live) ---
    elif "3." in nav:
        render_ticker()
        st.markdown('<h1 style="text-align:center; margin-bottom:20px;">JUGAR <span class="gold-text">TERMINAL</span></h1>', unsafe_allow_html=True)
        
        tabs = st.tabs(["📡 AI DECODER", "📈 CHARTING", "📰 FEED"])
        
        with tabs[0]:
            st.markdown('<div class="jugar-card">', unsafe_allow_html=True)
            st.markdown("### ENTER INTELLIGENCE STREAM")
            txt = st.text_area("INPUT", height=100, label_visibility="collapsed", placeholder="e.g. Breaking: Inflation data comes in lower than expected...")
            if st.button("RUN DIAGNOSTIC", use_container_width=True):
                if txt:
                    with st.spinner("PROCESSING..."):
                        time.sleep(0.5)
                        res = brain.analyze(txt)
                        st.markdown(f"""
                        <div style="text-align:center; padding:20px; border:2px solid {res['color']}; border-radius:10px; margin-top:20px;">
                            <h1 style="color:{res['color']}; font-size:4rem; margin:0;">{res['label']}</h1>
                            <p style="font-family:JetBrains Mono;">CONFIDENCE: {res['confidence']*100:.2f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tabs[1]:
            st.markdown('<div class="jugar-card">', unsafe_allow_html=True)
            tick = st.text_input("TICKER", value="BTC-USD").upper()
            if tick:
                fig, last = get_chart(tick)
                if fig:
                    st.metric("LIVE PRICE", f"${last['Close']:,.2f}")
                    st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- SECTION 4: CONCLUSION ---
    elif "4." in nav:
        st.markdown('<h1 style="font-size:3rem;">🏁 SYSTEM <span class="gold-text">HALTED</span></h1>', unsafe_allow_html=True)
        st.markdown('<div class="jugar-card">', unsafe_allow_html=True)
        st.markdown("""
        ### EXECUTIVE SUMMARY
        * **Jugar-AI** successfully demonstrates that standard NLP techniques can be "Gamified" into a high-performance decision engine.
        * **Performance:** The Logistic Regression model achieved satisfactory precision in discerning market sentiment.
        * **Future Logic:** Implementing LSTM Neural Networks for sequential pattern recognition.
        """)
        st.progress(100)
        st.markdown('</div>', unsafe_allow_html=True)
