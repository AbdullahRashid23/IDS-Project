import streamlit as st

# RENAMED FUNCTION TO FORCE UPDATE
def load_project_styles():
    st.markdown("""
    <style>
        /* =============================================
           1. CORE TYPOGRAPHY & IMPORTS
           ============================================= */
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Rajdhani:wght@300;500;700&family=Syncopate:wght@400;700&display=swap');

        /* =============================================
           2. GLOBAL THEME & SCROLLBARS
           ============================================= */
        .stApp {
            background-color: #000000;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(255, 215, 0, 0.08) 0%, transparent 70%),
                radial-gradient(circle at 0% 100%, rgba(50, 40, 0, 0.5) 0%, transparent 50%),
                linear-gradient(0deg, #050505 0%, #121212 100%);
            color: #e0e0e0;
        }

        /* Custom Gold Scrollbar */
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(to bottom, #996515, #FFD700); border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #FFD700; }

        /* =============================================
           3. THE GOLD VAULT CARDS
           ============================================= */
        .nexus-card {
            background: linear-gradient(165deg, rgba(20, 20, 20, 0.95), rgba(10, 10, 10, 0.98));
            border: 1px solid rgba(255, 215, 0, 0.2);
            border-left: 3px solid #FFD700; /* Tactical Left Border */
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 10px 40px -10px rgba(0,0,0,0.8);
            position: relative;
            overflow: hidden;
            
            /* Entrance Animation */
            animation: slideUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
            transition: all 0.4s ease;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Interactive Hover State */
        .nexus-card:hover {
            border-color: #FFD700;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.15);
            transform: translateY(-4px);
        }

        /* Gold Sheen Effect on Hover */
        .nexus-card::after {
            content: "";
            position: absolute;
            top: 0; left: -100%;
            width: 50%; height: 100%;
            background: linear-gradient(to right, transparent, rgba(255, 215, 0, 0.05), transparent);
            transform: skewX(-25deg);
            transition: 0.5s;
            pointer-events: none;
        }
        .nexus-card:hover::after {
            left: 100%;
            transition: 0.7s;
        }

        /* =============================================
           4. TICKER TAPE
           ============================================= */
        .ticker-wrap {
            width: 100%;
            background: #000;
            border-top: 1px solid #FFD700;
            border-bottom: 1px solid #FFD700;
            padding: 10px 0;
            margin-bottom: 30px;
            box-shadow: 0 0 25px rgba(255, 215, 0, 0.15);
            position: relative;
            z-index: 10;
        }
        .ticker-item {
            font-family: 'Syncopate', sans-serif;
            font-weight: 700;
            color: #FFD700;
            font-size: 0.85rem;
            padding: 0 2rem;
            letter-spacing: 3px;
            text-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
        }

        /* =============================================
           5. UI ELEMENTS (Sidebar, Buttons, Inputs)
           ============================================= */
        section[data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #080808, #000000);
            border-right: 1px solid rgba(255, 215, 0, 0.1);
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
            color: #000 !important;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: 1px;
            border: none;
            border-radius: 2px;
            padding: 0.75rem 2rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2);
            text-transform: uppercase;
        }
        .stButton>button:hover {
            transform: scale(1.03);
            box-shadow: 0 0 40px rgba(255, 215, 0, 0.5);
        }

        /* Inputs */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #FFD700 !important;
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 1px;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #FFD700 !important;
            background: #000 !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
        }

        /* =============================================
           6. TYPOGRAPHY & METRICS
           ============================================= */
        h1, h2, h3 {
            font-family: 'Cinzel', serif !important;
            color: #FFD700 !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        /* Hero Text */
        .hero-text {
            background: linear-gradient(to bottom, #FFF8DC, #FFD700, #DAA520);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.8rem;
            font-weight: 800;
            text-shadow: 0 0 40px rgba(255, 215, 0, 0.25);
            font-family: 'Syncopate', sans-serif;
            letter-spacing: -2px;
        }

        /* Metric Styling */
        div[data-testid="stMetricValue"] {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 2.2rem !important;
            color: #ffffff !important;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
        }
        div[data-testid="stMetricLabel"] {
            font-family: 'Cinzel', serif;
            color: #888;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

def render_ticker():
    content = """
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="ticker-item">BTC <span style="color:#fff">$64,200</span></span>
            <span class="ticker-item">GOLD <span style="color:#fff">$2,350</span></span>
            <span class="ticker-item">ETH <span style="color:#fff">$3,400</span></span>
            <span class="ticker-item">SPY <span style="color:#fff">$512.40</span></span>
            <span class="ticker-item">OIL <span style="color:#fff">$86.50</span></span>
            <span class="ticker-item">VIX <span style="color:#fff">14.20</span></span>
            <span class="ticker-item">BTC <span style="color:#fff">$64,200</span></span>
            <span class="ticker-item">GOLD <span style="color:#fff">$2,350</span></span>
            <span class="ticker-item">ETH <span style="color:#fff">$3,400</span></span>
        </div>
    </div>
    """
    st.markdown(content, unsafe_allow_html=True)
