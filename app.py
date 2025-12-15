import streamlit as st
import pandas as pd
import time
# IMPORT MODULES (All in root)
import styles
import nlp_engine
import market_data
import simulator
import reporting

# 1. SETUP & SESSION STATE
st.set_page_config(page_title="The Citadel", page_icon="🏯", layout="wide")

# --- FIX IS HERE: CALL THE NEW FUNCTION NAME ---
styles.load_citadel_theme() 

if 'history' not in st.session_state: st.session_state['history'] = []
if 'portfolio' not in st.session_state: 
    st.session_state['portfolio'] = {'balance': 10000.00, 'shares': 0}

# Initialize Classes
brain = nlp_engine.SentimentBrain()
sim = simulator.MarketSim()

# 2. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("## 📟 NAVIGATION")
    mode = st.radio("Select Module:", 
        ["📡 SENTINEL (Analysis)", 
         "📈 QUANT RADAR (Charts)", 
         "📰 NEWSFLOW (Intel)", 
         "💰 PAPER TRADER (Sim)", 
         "📑 C-SUITE REPORT (Export)"])
    
    st.markdown("---")
    st.markdown(f"**CORE STATUS:** {'🟢 ONLINE' if not brain.use_fallback else '🟠 FALLBACK ACTIVE'}")
    st.metric("PORTFOLIO VALUE", f"${st.session_state['portfolio']['balance']:,.2f}")

styles.render_header()

# 3. MODULE LOGIC

# === MODULE 1: SENTINEL ===
if "SENTINEL" in mode:
    st.markdown('<div class="hud-card"><h3>📡 LIVE SENTIMENT INTERCEPT</h3>', unsafe_allow_html=True)
    user_text = st.text_area("ENTER INTELLIGENCE STREAM:", height=100)
    
    if st.button("INITIALIZE ANALYSIS"):
        if user_text:
            with st.spinner("DECRYPTING SIGNAL..."):
                time.sleep(0.5)
                res = brain.analyze(user_text)
                
                # Save to history
                log_entry = {
                    "time": time.strftime("%H:%M:%S"),
                    "text": user_text,
                    "label": res['label'],
                    "score": res['score']
                }
                st.session_state['history'].insert(0, log_entry)

                # Display Result
                col1, col2, col3 = st.columns(3)
                col1.metric("VERDICT", res['label'])
                col1.markdown(f"<div style='background:{res['color']}; height:10px; width:100%;'></div>", unsafe_allow_html=True)
                col2.metric("CONFIDENCE", f"{res['confidence']*100:.1f}%")
                col3.metric("POLARITY SCORE", f"{res['score']:.3f}")
    st.markdown("</div>", unsafe_allow_html=True)

# === MODULE 2: QUANT RADAR ===
elif "QUANT" in mode:
    st.markdown('<div class="hud-card"><h3>📈 TECHNICAL SURVEILLANCE</h3>', unsafe_allow_html=True)
    ticker = st.text_input("TARGET ASSET TICKER:", value="NVDA").upper()
    
    if ticker:
        with st.spinner(f"ACQUIRING TARGET: {ticker}..."):
            fig, last_row = market_data.get_chart(ticker)
            if fig:
                # Live Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("LATEST PRICE", f"${last_row['Close']:.2f}")
                m2.metric("SMA (20)", f"${last_row['SMA_20']:.2f}")
                
                # Signal Logic
                signal = "BUY" if last_row['Close'] > last_row['SMA_20'] else "SELL"
                sig_color = "normal" if signal == "BUY" else "inverse"
                m3.metric("TECH SIGNAL", signal, delta_color=sig_color)
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("TARGET NOT FOUND OR DATA UNAVAILABLE.")
    st.markdown("</div>", unsafe_allow_html=True)

# === MODULE 3: NEWSFLOW ===
elif "NEWSFLOW" in mode:
    st.markdown('<div class="hud-card"><h3>📰 GLOBAL INTEL STREAM</h3>', unsafe_allow_html=True)
    if st.button("REFRESH FEED"):
        st.session_state['news'] = sim.get_live_feed(5)
    
    news = st.session_state.get('news', sim.get_live_feed(3))
    
    for headline, sentiment in news:
        st.markdown(f"""
        <div style="border-left: 3px solid #334155; padding-left:10px; margin-bottom:10px;">
            <span style="font-size:1.1rem; color: #fff;">{headline}</span><br>
            <span style="font-size:0.8rem; color: #64748b;">IMPLIED SENTIMENT: {sentiment}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"ANALYZE: {headline[:15]}...", key=headline):
            res = brain.analyze(headline)
            st.info(f"AI VERDICT: {res['label']} ({res['score']:.2f})")
    st.markdown("</div>", unsafe_allow_html=True)

# === MODULE 4: PAPER TRADER ===
elif "PAPER" in mode:
    st.markdown('<div class="hud-card"><h3>💰 TACTICAL SIMULATION SANDBOX</h3>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.metric("CASH BALANCE", f"${st.session_state['portfolio']['balance']:,.2f}")
    c2.metric("ASSETS HELD", f"{st.session_state['portfolio']['shares']} SHARES")
    
    st.markdown("---")
    sim_ticker = st.text_input("SIMULATION ASSET", value="SPY").upper()
    sim_price = 450.00 # Mock price for sim simplicity, or fetch real one
    
    st.caption(f"CURRENT MOCK PRICE: ${sim_price}")
    
    b1, b2 = st.columns(2)
    if b1.button("🟢 EXECUTE BUY (1 SHARE)"):
        success, msg = sim.execute_trade(st.session_state['portfolio'], 'buy', sim_price, 1)
        if success: st.success(msg)
        else: st.error(msg)
        
    if b2.button("🔴 EXECUTE SELL (1 SHARE)"):
        success, msg = sim.execute_trade(st.session_state['portfolio'], 'sell', sim_price, 1)
        if success: st.success(msg)
        else: st.error(msg)
    st.markdown("</div>", unsafe_allow_html=True)

# === MODULE 5: REPORTING ===
elif "REPORT" in mode:
    st.markdown('<div class="hud-card"><h3>📑 EXECUTIVE SUMMARY</h3>', unsafe_allow_html=True)
    
    if st.session_state['history']:
        st.dataframe(pd.DataFrame(st.session_state['history']), use_container_width=True)
        
        report_link = reporting.generate_html_report(st.session_state['history'])
        st.markdown(report_link, unsafe_allow_html=True)
    else:
        st.warning("NO DATA LOGGED. INITIATE ANALYSIS IN SENTINEL MODULE.")
    st.markdown("</div>", unsafe_allow_html=True)
