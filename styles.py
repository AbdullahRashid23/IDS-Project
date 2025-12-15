import streamlit as st

def load_nexus_theme():
    st.markdown("""
    <style>
        /* 1. IMPORT FUTURISTIC TYPOGRAPHY */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;500;700&family=Syncopate:wght@400;700&display=swap');

        /* 2. GLOBAL RESET & ANIMATED BACKGROUND */
        .stApp {
            background-color: #000000;
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%),
                radial-gradient(at 0% 100%, rgba(34, 197, 94, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            background-size: cover;
            color: #e0e0e0;
        }
        
        /* 3. NEXUS CARDS (The "Glass" Effect) */
        .nexus-card {
            background: rgba(10, 10, 10, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 30px;
            margin-bottom: 25px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Bouncy transition */
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        }
        
        .nexus-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        }

        .nexus-card:hover {
            transform: translateY(-5px) scale(1.01);
            border-color: rgba(56, 189, 248, 0.4); /* Cyan Glow */
            box-shadow: 0 20px 40px -10px rgba(56, 189, 248, 0.15);
        }

        /* 4. ANIMATED TICKER TAPE */
        .ticker-wrap {
            width: 100%;
            overflow: hidden;
            height: 50px;
            background: rgba(0,0,0,0.8);
            border-bottom: 1px solid #333;
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .ticker {
            display: flex;
            white-space: nowrap;
            animation: marquee 40s linear infinite;
        }
        .ticker-item {
            font-family: 'Orbitron', sans-serif;
            color: #fff;
            padding: 0 2rem;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        @keyframes marquee {
            0% { transform: translateX(0); }
            100% { transform: translateX(-100%); }
        }

        /* 5. SIDEBAR STYLING */
        section[data-testid="stSidebar"] {
            background: rgba(5, 5, 5, 0.95);
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        
        /* 6. NEON BUTTONS */
        .stButton>button {
            background: transparent;
            color: #38bdf8;
            border: 1px solid #38bdf8;
            font-family: 'Syncopate', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-radius: 4px;
            padding: 0.8rem 2rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        .stButton>button::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: #38bdf8;
            transition: all 0.3s ease;
            z-index: -1;
        }
        .stButton>button:hover {
            color: #000;
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.6);
        }
        .stButton>button:hover::before {
            left: 0;
        }

        /* 7. TYPOGRAPHY & METRICS */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .hero-text {
            background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem;
            font-weight: 900;
            text-shadow: 0 0 30px rgba(255,255,255,0.2);
        }
        div[data-testid="stMetricValue"] {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 2rem !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }

        /* 8. INPUT FIELDS */
        .stTextInput input, .stTextArea textarea {
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #fff !important;
            border-radius: 12px;
            transition: all 0.3s;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #38bdf8 !important;
            background: rgba(0,0,0,0.8) !important;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
        }

    </style>
    """, unsafe_allow_html=True)

def render_ticker():
    # Animated infinite scroll header
    content = """
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="ticker-item">BTC <span style="color:#4ade80">▲ 2.4%</span></span>
            <span class="ticker-item">ETH <span style="color:#f87171">▼ 0.8%</span></span>
            <span class="ticker-item">SPY <span style="color:#4ade80">▲ 0.5%</span></span>
            <span class="ticker-item">NDAQ <span style="color:#4ade80">▲ 1.2%</span></span>
            <span class="ticker-item">GOLD <span style="color:#fbbf24">▲ 0.1%</span></span>
            <span class="ticker-item">TSLA <span style="color:#f87171">▼ 3.2%</span></span>
            <span class="ticker-item">VIX <span style="color:#4ade80">▲ 5.4%</span></span>
            <span class="ticker-item">BTC <span style="color:#4ade80">▲ 2.4%</span></span>
            <span class="ticker-item">ETH <span style="color:#f87171">▼ 0.8%</span></span>
            <span class="ticker-item">SPY <span style="color:#4ade80">▲ 0.5%</span></span>
            <span class="ticker-item">NDAQ <span style="color:#4ade80">▲ 1.2%</span></span>
            <span class="ticker-item">GOLD <span style="color:#fbbf24">▲ 0.1%</span></span>
            <span class="ticker-item">TSLA <span style="color:#f87171">▼ 3.2%</span></span>
        </div>
    </div>
    """
    st.markdown(content, unsafe_allow_html=True)
