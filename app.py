import streamlit as st
import pandas as pd
import time
# IMPORT MODULES
import styles
import nlp_engine
import market_data
import simulator
import reporting

# 1. CONFIGURATION
st.set_page_config(page_title="Jugar-AI", page_icon="🦁", layout="wide")

# 2. INJECT ASSETS (Gold Theme)
styles.load_nexus_theme()

# 3. SESSION STATE INITIALIZATION
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = "Unknown"
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = {'balance': 0, 'shares': 0}
if 'history' not in st.session_state: 
    st.session_state['history'] = []

# --- 4. THE LANDING PAGE (LOGIN) ---
if not st.session_state['authenticated']:
    # Center the login box using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown('<div class="hero-text" style="text-align:center;">Jugar-AI</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#FFD700; letter-spacing:2px; font-family:Syncopate;">SECURE WEALTH MANAGEMENT SYSTEM BY ABDULLAH</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="nexus-card" style="margin-top: 40px;">', unsafe_allow_html=True)
        st.markdown("### 🔒 AUTHENTICATION REQUIRED")
        
        # Inputs
        user_input = st.text_input("OPERATOR ID", placeholder="Enter your name...")
        pass_input = st.text_input("SECURITY KEY", type="password", placeholder="••••••••")
        
        st.markdown("---")
        st.markdown("### 💰 INITIAL CAPITAL DEPOSIT")
        balance_input = st.number_input("ENTER STARTING BALANCE ($)", min_value=1000, value=100000, step=1000)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("ACCESS VAULT", use_container_width=True):
            if user_input:
                with st.spinner("VERIFYING BIOMETRICS..."):
                    time.sleep(1.5) # Theatrical Delay
                    # Set Session Variables
                    st.session_state['authenticated'] = True
                    st.session_state['user_name'] = user_input.upper()
                    st.session_state['portfolio']['balance'] = balance_input
                    st.rerun() # Refresh to show Main App
            else:
                st.error("IDENTITY VERIFICATION FAILED. NAME REQUIRED.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. THE MAIN TERMINAL (Only shows if Authenticated) ---
else:
    # Render the Ticker only once logged in
    styles.render_ticker()

    # Initialize Logic Classes
    brain = nlp_engine.SentimentBrain()
    sim = simulator.MarketSim()

    # SIDEBAR
    with st.sidebar:
        # User Profile
        st.markdown(f"### 👤 OPERATOR: <span style='color:#FFD700'>{st.session_state['user_name']}</span>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("## NAVIGATION")
        mode = st.radio("SELECT MODULE", 
            ["💠 SENTINEL CORE", 
             "📈 WEALTH CHARTS", 
             "📰 GLOBAL INTEL", 
             "💳 TRADE FLOOR", 
             "📂 EXPORT DATA"])
        
        st.markdown("---")
        st.markdown("### 💼 LIVE PORTFOLIO")
        # Dynamic Balance Update
        st.metric("AVAILABLE LIQUIDITY", f"${st.session_state['portfolio']['balance']:,.2f}")
        
        st.caption(f"SYSTEM STATUS: {'🟢 ONLINE' if not brain.use_fallback else '🟠 FALLBACK'}")
        
        # Logout Button
        if st.button("LOGOUT", use_container_width=True):
            st.session_state['authenticated'] = False
            st.rerun()

    # MAIN HEADER
    st.markdown(f'<div class="hero-text">WELCOME, {st.session_state["user_name"]}</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#888; font-family:Syncopate; letter-spacing:4px; margin-bottom:40px;">FINANCIAL WAR ROOM // ONLINE</div>', unsafe_allow_html=True)

    # === SENTINEL CORE (Analysis) ===
    if "SENTINEL" in mode:
        col_input, col_stats = st.columns([1.5, 1])
        
        with col_input:
            st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
            st.markdown("### 📡 SIGNAL INTERCEPT")
            user_text = st.text_area("AWAITING INPUT STREAM...", height=120)
            
            if st.button("EXECUTE ANALYSIS", use_container_width=True):
                if user_text:
                    with st.spinner("PROCESSING NEURAL LAYERS..."):
                        time.sleep(0.6)
                        res = brain.analyze(user_text)
                        
                        st.session_state['history'].insert(0, {
                            "time": time.strftime("%H:%M:%S"),
                            "text": user_text,
                            "label": res['label'],
                            "score": res['score']
                        })
                        
                        st.success("ANALYSIS COMPLETE")
                        st.markdown(f"""
                        <div style="text-align:center; padding: 20px;">
                            <div style="font-size:1.2rem; color:#888;">AI VERDICT</div>
                            <div style="font-size:4rem; font-weight:900; color:{res['color']}; text-shadow: 0 0 30px {res['color']};">
                                {res['label']}
                            </div>
                            <div style="font-family:monospace;">CONFIDENCE: {res['confidence']*100:.2f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_stats:
            st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
            st.markdown("### 🧠 SESSION LOGS")
            if st.session_state['history']:
                last = st.session_state['history'][0]
                st.code(f"[{last['time']}] {last['label']} \n>> {last['text'][:30]}...")
            else:
                st.caption("NO DATA LOGGED")
            st.markdown('</div>', unsafe_allow_html=True)

    # === WEALTH CHARTS ===
    elif "CHARTS" in mode:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([4,1])
        with c1: ticker = st.text_input("ENTER ASSET TICKER", value="GOLD").upper()
        with c2: 
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("SCAN MARKET")
        
        if ticker:
            fig, last_row = market_data.get_chart(ticker)
            if fig:
                price = float(last_row['Close'])
                m1, m2, m3 = st.columns(3)
                m1.metric("CURRENT PRICE", f"${price:,.2f}")
                m2.metric("DAILY HIGH", f"${float(last_row['High']):,.2f}")
                m3.metric("DAILY LOW", f"${float(last_row['Low']):,.2f}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("DATA UPLINK FAILED")
        st.markdown('</div>', unsafe_allow_html=True)

    # === GLOBAL INTEL (News) ===
    elif "GLOBAL" in mode:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("📰 LIVE MARKET WIRE")
        if st.button("REFRESH FEED"):
            st.session_state['news'] = sim.get_live_feed(4)
        
        news = st.session_state.get('news', sim.get_live_feed(4))
        for headline, sentiment in news:
            color = "#4ade80" if sentiment == "Bullish" else "#f87171"
            st.markdown(f"""
            <div style="border-left:4px solid {color}; padding-left:15px; margin-bottom:15px;">
                <div style="font-weight:bold; font-size:1.1rem;">{headline}</div>
                <div style="color:#888; font-size:0.8rem;">AI PROJECTION: <span style="color:{color}">{sentiment}</span></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # === TRADE FLOOR (Sim) ===
    elif "TRADE" in mode:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("💳 ORDER EXECUTION")
        
        col1, col2 = st.columns(2)
        with col1:
            asset = st.text_input("ASSET", value="BTC-USD").upper()
            price = 65000.00 # Mock
            st.metric("MARKET PRICE", f"${price:,.2f}")
        with col2:
            action = st.radio("POSITION", ["BUY", "SELL"], horizontal=True)
            qty = st.number_input("SIZE", min_value=1.0, value=1.0)
        
        if st.button("SUBMIT ORDER"):
            success, msg = sim.execute_trade(st.session_state['portfolio'], action.lower(), price, qty)
            if success:
                st.success(f"ORDER FILLED: {msg}")
            else:
                st.error(f"ORDER REJECTED: {msg}")
        st.markdown('</div>', unsafe_allow_html=True)

    # === EXPORT ===
    elif "EXPORT" in mode:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("📂 GENERATE REPORT")
        if st.session_state['history']:
            st.dataframe(pd.DataFrame(st.session_state['history']), use_container_width=True)
            st.markdown(reporting.generate_html_report(st.session_state['history']), unsafe_allow_html=True)
        else:
            st.info("NO ANALYTICS DATA FOUND")
        st.markdown('</div>', unsafe_allow_html=True)
