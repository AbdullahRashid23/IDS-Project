import streamlit as st

# RENAMED TO MATCH YOUR FILE
def load_nexus_theme():
    st.markdown("""
    <style>
        /* 1. IMPORT LUXURY FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Rajdhani:wght@300;500;700&family=Syncopate:wght@400;700&display=swap');

        /* 2. THE VAULT BACKGROUND */
        .stApp {
            background-color: #000000;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(255, 215, 0, 0.15) 0%, transparent 60%),
                linear-gradient(0deg, rgba(0,0,0,1) 0%, rgba(10,10,10,1) 100%);
            color: #e0e0e0;
        }
        
        /* 3. GOLD GLASS CARDS */
        .nexus-card {
            background: linear-gradient(145deg, rgba(20, 20, 20, 0.9), rgba(10, 10, 10, 0.95));
            border: 1px solid rgba(255, 215, 0, 0.15); /* Subtle Gold Border */
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        
        .nexus-card:hover {
            border-color: #FFD700; /* Bright Gold on Hover */
            box-shadow: 0 0 25px rgba(255, 215, 0, 0.2);
            transform: translateY(-3px);
        }

        /* 4. THE TICKER TAPE (Black & Gold) */
        .ticker-wrap {
            width: 100%;
            background: #000;
            border-top: 2px solid #FFD700;
            border-bottom: 2px solid #FFD700;
            padding: 12px 0;
            margin-bottom: 30px;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        }
        .ticker-item {
            font-family: 'Syncopate', sans-serif;
            font-weight: 700;
            color: #FFD700;
            font-size: 0.9rem;
            padding: 0 2rem;
            letter-spacing: 2px;
        }

        /* 5. SIDEBAR (Carbon Fiber Look) */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #333;
        }
        
        /* 6. LUXURY BUTTONS */
        .stButton>button {
            background: linear-gradient(45deg, #FFD700, #FDB931);
            color: #000 !important;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 800;
            font-size: 1.1rem;
            text-transform: uppercase;
            border: none;
            border-radius: 4px;
            padding: 0.8rem 2rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        }
        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
            color: #000;
        }

        /* 7. TYPOGRAPHY */
        h1, h2, h3 {
            font-family: 'Cinzel', serif !important; /* The "Bank" Font */
            color: #FFD700 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* The Big Title */
        .hero-text {
            background: linear-gradient(to bottom, #FFD700, #FDB931, #996515);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 4rem;
            font-weight: 900;
            text-shadow: 0 0 50px rgba(255, 215, 0, 0.3);
            font-family: 'Syncopate', sans-serif;
            letter-spacing: -2px;
        }

        /* Metrics (Prices) */
        div[data-testid="stMetricValue"] {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            color: #fff !important;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }
        div[data-testid="stMetricLabel"] {
            color: #888;
            font-family: 'Cinzel', serif;
        }

        /* 8. INPUTS (Matte Black) */
        .stTextInput input, .stTextArea textarea {
            background: #0a0a0a !important;
            border: 1px solid #333 !important;
            color: #FFD700 !important;
            border-radius: 8px;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #FFD700 !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)

def render_ticker():
    # GOLD TICKER
    content = """
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="ticker-item">BTC <span style="color:#fff">$64,200</span></span>
            <span class="ticker-item">GOLD <span style="color:#fff">$2,350</span></span>
            <span class="ticker-item">ETH <span style="color:#fff">$3,400</span></span>
            <span class="ticker-item">SPY <span style="color:#fff">$512.40</span></span>
            <span class="ticker-item">OIL <span style="color:#fff">$86.50</span></span>
            <span class="ticker-item">BTC <span style="color:#fff">$64,200</span></span>
            <span class="ticker-item">GOLD <span style="color:#fff">$2,350</span></span>
        </div>
    </div>
    """
    st.markdown(content, unsafe_allow_html=True)
