import streamlit as st
import pandas as pd
import plotly.express as px
import time
# Custom Modules
import styles
import nlp_engine
import market_data
import simulator
import reporting

# 1. PAGE CONFIG
st.set_page_config(page_title="Jugar-AI", page_icon="🦁", layout="wide")

# --- FIX IS HERE: CALL THE NEW FUNCTION NAME ---
styles.load_project_styles()

# 2. SESSION STATE INITIALIZATION
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'user_name' not in st.session_state: st.session_state['user_name'] = "Unknown"
if 'portfolio' not in st.session_state: st.session_state['portfolio'] = {'balance': 0, 'shares': 0}
if 'history' not in st.session_state: st.session_state['history'] = []

# ==========================================
# 🔒 PART 1: THE GATEKEEPER (LOGIN SCREEN)
# ==========================================
if not st.session_state['authenticated']:
    # Centered Login Layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; color:#FFD700; font-size:3rem;">Jugar-AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#fafafa; letter-spacing:2px;">SECURE FINANCIAL INTELLIGENCE SUITE BY ABDULLAH RASHID</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="nexus-card" style="margin-top: 30px;">', unsafe_allow_html=True)
        st.markdown("### 🔒 AUTHENTICATION REQUIRED")
        
        # Inputs
        user_input = st.text_input("OPERATOR ID", placeholder="Enter your name (e.g. Abdullah)")
        # No password check logic needed for demo, just visual
        pass_input = st.text_input("SECURITY KEY", type="password", placeholder="••••••••")
        
        st.markdown("---")
        st.markdown("### 💰 INITIAL CAPITAL DEPOSIT")
        balance_input = st.number_input("ENTER STARTING BALANCE ($)", min_value=1000, value=50000, step=1000)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("ACCESS VAULT", use_container_width=True):
            if user_input:
                with st.spinner("VERIFYING BIOMETRICS..."):
                    time.sleep(1.2) # Theatrical Delay
                    # Unlock the App
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
    # 3. SIDEBAR NAVIGATION
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/data-configuration.png", width=50)
        st.title("IDS TERM PROJECT")
        st.caption(f"Operator: {st.session_state['user_name']}")
        
        # Navigation matching Course Requirements
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
        
        # LOAD DATA
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
        # Render Ticker
        styles.render_ticker()
        
        # Header
        st.markdown(f'<h1 style="text-align:center;">ALPHA TERMINAL</h1>', unsafe_allow_html=True)
        st.caption(f"Operator: {st.session_state['user_name']} | Status: ONLINE")
        
        # Initialize Engines
        brain = nlp_engine.SentimentBrain()
        sim = simulator.MarketSim()

        # Terminal Tabs
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
