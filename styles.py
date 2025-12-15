import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* FONTS: Poppins for UI, JetBrains Mono for Data */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

        /* GLOBAL THEME */
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            color: #e2e8f0;
            background-color: #0f172a;
        }
        
        /* BACKGROUND GRADIENT */
        .stApp {
            background: radial-gradient(circle at 10% 20%, #0f172a 0%, #020617 90%);
        }

        /* GLASS CARDS */
        .glass-card {
            background: rgba(30, 41, 59, 0.3);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
            transition: transform 0.3s ease;
        }
        .glass-card:hover {
            border-color: rgba(245, 158, 11, 0.3); /* Gold glow on hover */
        }

        /* INPUT FIELDS */
        .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #ffffff !important;
            border-radius: 8px;
        }
        .stTextArea textarea:focus {
            border-color: #f59e0b !important;
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
        }

        /* BUTTONS (The "Gold Standard") */
        .stButton>button {
            background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            width: 100%;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(217, 119, 6, 0.4);
        }

        /* TICKER ANIMATION */
        .ticker-wrap {
            width: 100%;
            background: rgba(0,0,0,0.5);
            border-top: 1px solid #334155;
            border-bottom: 1px solid #334155;
            overflow: hidden;
            white-space: nowrap;
            padding: 8px 0;
            margin-bottom: 2rem;
        }
        .ticker {
            display: inline-block;
            animation: marquee 40s linear infinite;
        }
        .ticker-item {
            display: inline-block;
            padding: 0 2rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #94a3b8;
        }
        .up { color: #10b981; font-weight: bold; }
        .down { color: #ef4444; font-weight: bold; }
        
        @keyframes marquee {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }

        /* METRICS */
        div[data-testid="stMetricValue"] {
            color: #f59e0b !important; /* Gold numbers */
            font-family: 'JetBrains Mono', monospace;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    # Double the content for seamless infinite scroll
    content = """
    <span class="ticker-item">SPY <span class="up">▲ 0.5%</span></span>
    <span class="ticker-item">BTC-USD <span class="down">▼ 1.2%</span></span>
    <span class="ticker-item">TSLA <span class="up">▲ 2.4%</span></span>
    <span class="ticker-item">NVDA <span class="up">▲ 1.8%</span></span>
    <span class="ticker-item">EUR/USD <span class="down">▼ 0.1%</span></span>
    <span class="ticker-item">GOLD <span class="up">▲ 0.3%</span></span>
    """ * 5
    
    st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker">
            {content}
        </div>
    </div>
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="margin:0; font-size: 3.5rem; background: linear-gradient(to right, #fbbf24, #d97706); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 30px rgba(245, 158, 11, 0.3);">
            AEGIS TERMINAL
        </h1>
        <p style="color: #64748b; font-family: 'JetBrains Mono'; margin-top: -10px;">INSTITUTIONAL SENTIMENT & MARKET ANALYZER</p>
    </div>
    """, unsafe_allow_html=True)
