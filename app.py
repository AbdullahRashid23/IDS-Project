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
st.set_page_config(page_title="Jugar-AI", page_icon="💠", layout="wide")

# 2. INJECT ASSETS
styles.load_nexus_theme()
styles.render_ticker() # <--- THE ANIMATED HEADER

# 3. INITIALIZATION
if 'history' not in st.session_state: st.session_state['history'] = []
if 'portfolio' not in st.session_state: 
    st.session_state['portfolio'] = {'balance': 50000.00, 'shares': 0}

brain = nlp_engine.SentimentBrain()
sim = simulator.MarketSim()

# 4. SIDEBAR (The Control Deck)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    st.markdown("## OPERATOR CONTROLS")
    
    # Custom Radio with Icons
    mode = st.radio("SYSTEM MODULE", 
        ["💠 SENTINEL CORE", 
         "📈 MARKET VECTOR", 
         "📰 GLOBAL FEED", 
         "💳 TRADE SIMULATOR", 
         "📂 DATA EXPORT"])
    
    st.markdown("---")
    
    # Portfolio Widget
    st.markdown("### 💼 ASSET WALLET")
    st.metric("LIQUIDITY", f"${st.session_state['portfolio']['balance']:,.2f}", "+2.4%")
    
    st.markdown("---")
    st.caption(f"CORE STATUS: {'🟢 ONLINE' if not brain.use_fallback else '🟠 BACKUP ENGAGED'}")

# 5. MAIN HEADER
st.markdown('<div class="hero-text">Jugar-AI</div>', unsafe_allow_html=True)
st.markdown('<div style="color:#94a3b8; font-family:Syncopate; letter-spacing:4px; margin-bottom:40px;">THE ABDULLAH INTELLIGENCE ENGINE</div>', unsafe_allow_html=True)

# 6. MODULES

# === SENTINEL CORE (Analysis) ===
if "SENTINEL" in mode:
    col_input, col_stats = st.columns([1.5, 1])
    
    with col_input:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.markdown("### 📡 SIGNAL INTERCEPT")
        user_text = st.text_area("AWAITING INPUT STREAM...", height=120)
        
        if st.button("EXECUTE ANALYSIS SEQUENCE", use_container_width=True):
            if user_text:
                with st.spinner("DECRYPTING NEURAL PATTERNS..."):
                    time.sleep(0.6) # Theatrical delay
                    res = brain.analyze(user_text)
                    
                    # Store
                    st.session_state['history'].insert(0, {
                        "time": time.strftime("%H:%M:%S"),
                        "text": user_text,
                        "label": res['label'],
                        "score": res['score']
                    })
                    
                    # Result Display
                    st.success("ANALYSIS COMPLETE")
                    st.markdown(f"""
                    <div style="text-align:center; padding: 20px;">
                        <div style="font-size:1.2rem; color:#94a3b8;">VERDICT</div>
                        <div style="font-size:4rem; font-weight:900; color:{res['color']}; text-shadow: 0 0 40px {res['color']};">
                            {res['label']}
                        </div>
                        <div style="font-family:monospace;">CONFIDENCE INTERVAL: {res['confidence']*100:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_stats:
        # Mini Dashboard
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ SYSTEM METRICS")
        c1, c2 = st.columns(2)
        c1.metric("CPU LOAD", "12%", "-2%")
        c2.metric("LATENCY", "42ms", "-5ms")
        st.markdown("---")
        st.markdown("### 🧠 RECENT LOGS")
        if st.session_state['history']:
            last = st.session_state['history'][0]
            st.code(f"[{last['time']}] {last['label']} \n>> {last['text'][:30]}...")
        else:
            st.caption("NO DATA LOGGED")
        st.markdown('</div>', unsafe_allow_html=True)

# === MARKET VECTOR (Charts) ===
elif "MARKET" in mode:
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    c_search, c_btn = st.columns([4, 1])
    with c_search:
        ticker = st.text_input("ENTER ASSET TICKER", value="NVDA").upper()
    with c_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        refresh = st.button("SCAN")
    
    if ticker:
        fig, last_row = market_data.get_chart(ticker)
        if fig:
            # Stats Row - FIX: CAST TO FLOAT TO PREVENT ERRORS
            price = float(last_row['Close'])
            high = float(last_row['High'])
            low = float(last_row['Low'])
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("PRICE", f"${price:.2f}")
            m2.metric("HIGH (24H)", f"${high:.2f}")
            m3.metric("LOW (24H)", f"${low:.2f}")
            
            # Volatility Calc
            vol = ((high - low) / low) * 100
            m4.metric("VOLATILITY", f"{vol:.2f}%")
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("ASSET NOT FOUND IN QUANTUM DATABASE")
    st.markdown('</div>', unsafe_allow_html=True)

# === GLOBAL FEED (News) ===
elif "GLOBAL" in mode:
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    st.subheader("📰 LIVE INTELLIGENCE STREAM")
    
    if st.button("REFRESH UPLINK"):
        st.session_state['news'] = sim.get_live_feed(4)
    
    news = st.session_state.get('news', sim.get_live_feed(4))
    
    for headline, sentiment in news:
        color = "#4ade80" if sentiment == "Bullish" else "#f87171"
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; margin-bottom:10px; border-left:4px solid {color};">
            <div style="font-size:1.1rem; font-weight:bold;">{headline}</div>
            <div style="font-size:0.8rem; color:#94a3b8; margin-top:5px;">AI PREDICTION: <span style="color:{color}">{sentiment}</span></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# === SIMULATOR ===
elif "TRADE" in mode:
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    st.subheader("💳 TACTICAL SIMULATION")
    
    col_sim_1, col_sim_2 = st.columns(2)
    with col_sim_1:
        sim_ticker = st.text_input("ASSET", value="BTC-USD").upper()
        sim_price = 42000.00 # Mock
        st.metric("LIVE PRICE (MOCK)", f"${sim_price:,.2f}")
    
    with col_sim_2:
        action = st.radio("ACTION", ["BUY LONG", "SELL SHORT"], horizontal=True)
        qty = st.number_input("QUANTITY", min_value=1, value=1)
    
    if st.button("EXECUTE ORDER"):
        success, msg = sim.execute_trade(st.session_state['portfolio'], 'buy' if 'BUY' in action else 'sell', sim_price, qty)
        if success:
            st.balloons()
            st.success(msg)
        else:
            st.error(msg)
    st.markdown('</div>', unsafe_allow_html=True)

# === REPORT ===
elif "EXPORT" in mode:
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    st.subheader("📂 C-SUITE REPORT GENERATION")
    if st.session_state['history']:
        st.dataframe(pd.DataFrame(st.session_state['history']), use_container_width=True)
        link = reporting.generate_html_report(st.session_state['history'])
        st.markdown(link, unsafe_allow_html=True)
    else:
        st.info("NO DATA AVAILABLE FOR EXPORT")
    st.markdown('</div>', unsafe_allow_html=True)
