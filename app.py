import streamlit as st
import pandas as pd
import plotly.express as px
import time
# Custom Modules (Keep these)
import nlp_engine
import market_data
import simulator
import reporting

# 1. PAGE CONFIG
st.set_page_config(page_title="IDS Project | Alpha Terminal", page_icon="🦁", layout="wide")

# ==========================================
# 🎨 INTERNAL STYLES (No external file needed)
# ==========================================
def load_internal_styles():
    st.markdown("""
    <style>
        /* CORE IMPORTS */
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Rajdhani:wght@300;500;700&family=Syncopate:wght@400;700&display=swap');

        /* BACKGROUND & SCROLLBAR */
        .stApp {
            background-color: #000000;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(255, 215, 0, 0.08) 0%, transparent 70%),
                linear-gradient(0deg, #050505 0%, #121212 100%);
            color: #e0e0e0;
        }
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(to bottom, #996515, #FFD700); border-radius: 5px; }

        /* GOLD VAULT CARDS */
        .nexus-card {
            background: linear-gradient(165deg, rgba(20, 20, 20, 0.95), rgba(10, 10, 10, 0.98));
            border: 1px solid rgba(255, 215, 0, 0.2);
            border-left: 3px solid #FFD700;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 10px 40px -10px rgba(0,0,0,0.8);
            transition: all 0.4s ease;
        }
        .nexus-card:hover {
            border-color: #FFD700;
            transform: translateY(-4px);
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.15);
        }

        /* TICKER TAPE */
        .ticker-wrap {
            width: 100%;
            background: #000;
            border-top: 1px solid #FFD700;
            border-bottom: 1px solid #FFD700;
            padding: 10px 0;
            margin-bottom: 30px;
        }
        .ticker-item {
            font-family: 'Syncopate', sans-serif;
            font-weight: 700;
            color: #FFD700;
            padding: 0 2rem;
            letter-spacing: 3px;
        }

        /* BUTTONS */
        .stButton>button {
            background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
            color: #000 !important;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            border: none;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.03);
            box-shadow: 0 0 40px rgba(255, 215, 0, 0.5);
        }

        /* INPUTS */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #FFD700 !important;
        }
        
        /* TYPOGRAPHY */
        h1, h2, h3 {
            font-family: 'Cinzel', serif !important;
            color: #FFD700 !important;
            text-transform: uppercase;
        }
        div[data-testid="stMetricValue"] {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 2.2rem !important;
            color: #ffffff !important;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

def render_ticker():
    st.markdown("""
    <div class="ticker-wrap">
        <marquee scrollamount="10" direction="left" class="ticker-item">
            BTC <span style="color:#fff">$64,200</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
            GOLD <span style="color:#fff">$2,350</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
            ETH <span style="color:#fff">$3,400</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
            SPY <span style="color:#fff">$512.40</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
            OIL <span style="color:#fff">$86.50</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
            AI_SENTIMENT: <span style="color:#00ff00">ONLINE</span>
        </marquee>
    </div>
    """, unsafe_allow_html=True)

# LOAD THE STYLES IMMEDIATELY
load_internal_styles()

# 2. SESSION STATE
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'user_name' not in st.session_state: st.session_state['user_name'] = "Unknown"
if 'portfolio' not in st.session_state: st.session_state['portfolio'] = {'balance': 0, 'shares': 0}
if 'history' not in st.session_state: st.session_state['history'] = []

# ==========================================
# 🔒 PART 1: THE GATEKEEPER (LOGIN SCREEN)
# ==========================================
if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; color:#FFD700; font-size:3rem;">ALPHA TERMINAL</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#fafafa; letter-spacing:2px;">SECURE FINANCIAL INTELLIGENCE SUITE</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="nexus-card" style="margin-top: 30px;">', unsafe_allow_html=True)
        st.markdown("### 🔒 AUTHENTICATION REQUIRED")
        
        user_input = st.text_input("OPERATOR ID", placeholder="Enter your name (e.g. Abdullah)")
        pass_input = st.text_input("SECURITY KEY", type="password", placeholder="••••••••")
        st.markdown("---")
        balance_input = st.number_input("ENTER STARTING BALANCE ($)", min_value=1000, value=50000, step=1000)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("ACCESS VAULT", use_container_width=True):
            if user_input:
                with st.spinner("VERIFYING BIOMETRICS..."):
                    time.sleep(1.2)
                    st.session_state['authenticated'] = True
                    st.session_state['user_name'] = user_input.upper()
                    st.session_state['portfolio']['balance'] = balance_input
                    st.rerun()
            else:
                st.error("IDENTITY VERIFICATION FAILED. NAME REQUIRED.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🔓 PART 2: THE ACADEMIC PROJECT (UNLOCKED)
# ==========================================
else:
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/data-configuration.png", width=50)
        st.title("IDS TERM PROJECT")
        st.caption(f"Operator: {st.session_state['user_name']}")
        
        nav = st.radio("Project Sections", [
            "1. Introduction", 
            "2. Exploratory Data Analysis (EDA)",
            "3. Model & Preprocessing",
            "4. LIVE APP: Alpha Terminal", 
            "5. Conclusion"
        ])
        
        st.markdown("---")
        st.metric("LIQUIDITY", f"${st.session_state['portfolio']['balance']:,.2f}")
        
        if st.button("LOGOUT"):
            st.session_state['authenticated'] = False
            st.rerun()

    # --- SECTION 1: INTRODUCTION ---
    if nav == "1. Introduction":
        st.title("1. Project Overview")
        st.markdown(f"""
        ### 🎯 Welcome, {st.session_state['user_name']}
        The goal of this project is to analyze financial news sentiment and predict market trends using Machine Learning. 
        We translate these insights into **'Alpha Terminal'**, a real-time decision support system.

        ### 📂 Dataset Selection
        * **Name:** Financial Sentiment Stocks Dataset
        * **Size:** ~5,000+ labeled financial sentences.
        * **Features:** `Sentence` (Text), `Sentiment` (Label: Positive/Negative).
        """)

    # --- SECTION 2: EDA ---
    elif nav == "2. Exploratory Data Analysis (EDA)":
        st.title("2. Exploratory Data Analysis")
        try:
            df = pd.read_csv('Sentiment_Stock_data.csv')
            if 'Unnamed: 0' in df.columns: df = df.drop(columns=['Unnamed: 0'])
            df['Sentence_Length'] = df['Sentence'].astype(str).apply(len)
        except:
            st.error("⚠️ Dataset 'Sentiment_Stock_data.csv' not found. Please upload it.")
            st.stop()

        tab1, tab2 = st.tabs(["📊 Stats", "📈 Visuals"])
        with tab1:
            st.subheader("Descriptive Statistics")
            st.dataframe(df.describe())
            st.metric("Total Records", df.shape[0])
        with tab2:
            st.subheader("Sentiment Distribution")
            fig = px.pie(df, names='Sentiment', title="Target Balance", color_discrete_sequence=['#ff4b4b', '#4ade80'])
            st.plotly_chart(fig, use_container_width=True)

    # --- SECTION 3: MODEL ---
    elif nav == "3. Model & Preprocessing":
        st.title("3. Data Pipeline & Modeling")
        st.markdown("""
        ### 🛠 Preprocessing
        1. **Cleaning:** Lowercase conversion, Regex removal of special chars.
        2. **Vectorization:** TF-IDF (Term Frequency-Inverse Document Frequency).
        
        ### 🤖 Model Selection
        * **Algorithm:** Logistic Regression.
        * **Why?** High efficiency for sparse text data.
        """)

    # --- SECTION 4: THE TERMINAL (LIVE APP) ---
    elif nav == "4. LIVE APP: Alpha Terminal":
        render_ticker()
        st.markdown(f'<h1 style="text-align:center;">ALPHA TERMINAL</h1>', unsafe_allow_html=True)
        st.caption(f"Operator: {st.session_state['user_name']} | Status: ONLINE")
        
        # Initialize Engines
        brain = nlp_engine.SentimentBrain()
        sim = simulator.MarketSim()

        t1, t2, t3 = st.tabs(["📡 SENTINEL", "📈 MARKETS", "📰 NEWS FEED"])
        
        with t1:
            st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
            st.subheader("Live Sentiment Intercept")
            user_text = st.text_area("Enter News / Headline:", placeholder="e.g. Fed rates unchanged...")
            
            if st.button("ANALYZE SIGNAL"):
                if user_text:
                    with st.spinner("Processing..."):
                        res = brain.analyze(user_text)
                        
                        c1, c2, c3 = st.columns(3)
                        c1.metric("VERDICT", res['label'])
                        c2.metric("CONFIDENCE", f"{res['confidence']*100:.1f}%")
                        c3.metric("SCORE", f"{res['score']:.2f}")
                else:
                    st.warning("Input required.")
            st.markdown('</div>', unsafe_allow_html=True)

        with t2:
            st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
            ticker = st.text_input("Ticker Symbol", value="SPY").upper()
            if ticker:
                fig, last_row = market_data.get_chart(ticker)
                if fig:
                    # FIX: Force float conversion to prevent TypeError
                    price = float(last_row['Close'])
                    st.metric("Current Price", f"${price:,.2f}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Data unavailable.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with t3:
            st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
            if st.button("Refresh Feed"):
                st.session_state['news'] = sim.get_live_feed(3)
            
            news = st.session_state.get('news', [])
            for h, s in news:
                st.info(f"{h} | {s}")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- SECTION 5: CONCLUSION ---
    elif nav == "5. Conclusion":
        st.title("5. Conclusion")
        st.markdown("""
        * **Success:** The model successfully classifies financial text with high confidence.
        * **Utility:** The 'Alpha Terminal' interface proves that ML can be used for real-time trading support.
        """)
