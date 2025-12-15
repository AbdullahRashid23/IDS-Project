import streamlit as st
import pandas as pd
import time
# IMPORT YOUR FILES
import styles
import engine
import plots

# 1. PAGE SETUP
st.set_page_config(page_title="Abdullah's AI", page_icon="🤖", layout="wide")
styles.load_css()
engine_core = engine.SentimentEngine()

# 2. SIDEBAR (The Control Center)
with st.sidebar:
    st.markdown("### 🎛️ CONTROL CENTER")
    selected_ticker = st.text_input("TARGET TICKER", value="SPY").upper()
    
    st.markdown("---")
    # Status Indicator
    if engine_core.use_fallback:
        st.error("⚠️ SYSTEM STATUS: OFFLINE")
        st.caption("Running on fallback logic.")
    else:
        st.success("🟢 SYSTEM STATUS: ONLINE")
        st.caption("Neural Networks Active.")

# 3. MAIN UI
styles.render_header()

# Create Tabs with Icons
tab1, tab2 = st.tabs(["⚡ LIVE ANALYSIS", "📂 BATCH DATA"])

with tab1:
    col1, col2 = st.columns([1, 1.2])

    # Left Column: User Input
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📡 INPUT SIGNAL")
        user_text = st.text_area("Enter Headline / Tweet / Market News", height=160, placeholder="e.g. Breaking: Tech stocks rally as inflation cools down...")
        
        # The Action Button
        if st.button("RUN DIAGNOSTIC", use_container_width=True):
            if user_text:
                with st.spinner("Compiling Neural Nodes..."):
                    # Artifical delay for "tech" feel
                    time.sleep(0.6) 
                    result = engine_core.analyze(user_text)
                    
                    # Store result in session state to persist
                    st.session_state['last_result'] = result
            else:
                st.warning("Input required.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Show Results if they exist
        if 'last_result' in st.session_state:
            res = st.session_state['last_result']
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {res['color']}">
                <h2 style="color:{res['color']}; margin:0;">{res['label']}</h2>
                <p style="color:#888;">Confidence Score: {int(res['score']*100)}%</p>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(plots.plot_gauge(res['score']), use_container_width=True)

    # Right Column: Market Data
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"### 📊 MARKET CONTEXT: <span style='color:#00d2ff'>{selected_ticker}</span>", unsafe_allow_html=True)
        
        with st.spinner(f"Establishing Uplink to {selected_ticker}..."):
            df_stock = engine_core.get_market_data(selected_ticker)
            
            if not df_stock.empty:
                # Calculate metrics
                current = df_stock['Close'].iloc[-1]
                prev = df_stock['Close'].iloc[-2]
                change = current - prev
                pct = (change / prev) * 100
                color = "#00d2ff" if change >= 0 else "#ff0055"
                
                # Custom Metric Display
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; margin-bottom:20px;">
                    <div>
                        <div style="color:#888; font-size:0.8rem;">CURRENT PRICE</div>
                        <div style="font-size:2rem; font-weight:bold; font-family:'Orbitron';">${current:.2f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="color:#888; font-size:0.8rem;">24H CHANGE</div>
                        <div style="font-size:2rem; font-weight:bold; color:{color}; font-family:'Orbitron';">
                            {change:+.2f} ({pct:+.2f}%)
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.plotly_chart(plots.plot_stock_history(selected_ticker, df_stock), use_container_width=True)
            else:
                st.error("Data Uplink Failed. Check Ticker.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📂 BATCH PROCESSOR")
    upl = st.file_uploader("Upload CSV Data", type=['csv'])
    if upl and st.button("EXECUTE BATCH"):
        st.info("Batch processing logic here...")
    st.markdown('</div>', unsafe_allow_html=True)
