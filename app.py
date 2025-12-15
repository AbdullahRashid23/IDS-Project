import streamlit as st
import pandas as pd
from src import styles, engine, plots

# 1. SETUP
st.set_page_config(page_title="Aegis Financial Terminal", page_icon="🦅", layout="wide")
styles.load_css() # Inject CSS
engine_core = engine.SentimentEngine() # Initialize Logic

# 2. HEADER
styles.render_header()

# 3. SIDEBAR CONTROLS
with st.sidebar:
    st.header("⚙️ CONFIGURATION")
    selected_ticker = st.text_input("MARKET TICKER", value="SPY", help="e.g. AAPL, BTC-USD").upper()
    
    st.markdown("---")
    st.markdown("### SYSTEM STATUS")
    if engine_core.use_fallback:
        st.warning("⚠️ MODE: FALLBACK (TextBlob)")
        st.caption("Training models not found. Using rule-based analysis.")
    else:
        st.success("🟢 MODE: NEURAL (Sklearn)")
        st.caption("Trained models loaded successfully.")

# 4. MAIN INTERFACE
tab_live, tab_batch = st.tabs(["📡 LIVE SIGNAL", "📂 BATCH PROCESSOR"])

# --- TAB 1: LIVE ANALYSIS ---
with tab_live:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Input Intelligence")
        user_text = st.text_area("Paste News / Tweet / Headline", height=150, placeholder="e.g., Inflation data shows cooling trends, markets rally...")
        
        analyze_btn = st.button("ANALYZE SENTIMENT")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if analyze_btn and user_text:
            # ANALYSIS LOGIC
            result = engine_core.analyze(user_text)
            
            # GAUGE CARD
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.metric("VERDICT", result['label'])
            st.plotly_chart(plots.plot_gauge(result['score']), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # MARKET CONTEXT
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader(f"Market Context: {selected_ticker}")
        
        with st.spinner(f"Fetching live data for {selected_ticker}..."):
            df_stock = engine_core.get_market_data(selected_ticker)
            
            if not df_stock.empty:
                # Calculate simple return for metric
                last_close = df_stock['Close'].iloc[-1]
                prev_close = df_stock['Close'].iloc[-2]
                delta = last_close - prev_close
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Last Price", f"${last_close:.2f}", f"{delta:.2f}")
                m2.metric("Volume", f"{df_stock['Volume'].iloc[-1]/1000000:.1f}M")
                m3.metric("Volatility", f"{(df_stock['High'].iloc[-1] - df_stock['Low'].iloc[-1]):.2f}")
                
                st.plotly_chart(plots.plot_stock_history(selected_ticker, df_stock), use_container_width=True)
            else:
                st.error(f"Could not fetch data for {selected_ticker}. Check spelling.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: BATCH CSV ---
with tab_batch:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Bulk File Processor")
    uploaded_file = st.file_uploader("Upload CSV (Required column: 'Sentence')", type="csv")
    
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        if 'Sentence' in df_upload.columns:
            if st.button("PROCESS DATASET"):
                with st.spinner("Running Neural Engine..."):
                    # Process rows
                    results = df_upload['Sentence'].apply(lambda x: pd.Series(engine_core.analyze(x)))
                    df_final = pd.concat([df_upload, results], axis=1)
                    
                    st.success("Analysis Complete")
                    st.dataframe(df_final.head(), use_container_width=True)
                    
                    # Download
                    csv = df_final.to_csv(index=False).encode('utf-8')
                    st.download_button("DOWNLOAD REPORT", csv, "Aegis_Report.csv", "text/csv")
        else:
            st.error("CSV must contain a 'Sentence' column.")
    st.markdown('</div>', unsafe_allow_html=True)
