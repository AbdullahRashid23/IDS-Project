import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* 1. IMPORT FUTURISTIC FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;600&display=swap');

        /* 2. GLOBAL RESET & SCROLLBAR */
        html, body, [class*="css"] {
            font-family: 'Exo 2', sans-serif;
            background-color: #000000;
            color: #e0e0e0;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #00d2ff; }

        /* 3. BACKGROUND ANIMATION (Subtle Pulse) */
        .stApp {
            background: 
                radial-gradient(circle at 15% 50%, rgba(76, 29, 149, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(0, 210, 255, 0.1), transparent 25%);
            background-color: #000000;
        }

        /* 4. TITLE: "ABDULLAH'S AI" */
        .neon-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 4rem;
            font-weight: 900;
            text-align: center;
            background: linear-gradient(to right, #00d2ff, #3a7bd5, #9d00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0, 210, 255, 0.5);
            margin-bottom: 0px;
            animation: glow 3s ease-in-out infinite alternate;
        }
        .subtitle {
            text-align: center;
            color: #64748b;
            font-size: 1.2rem;
            letter-spacing: 2px;
            margin-bottom: 40px;
            text-transform: uppercase;
        }

        @keyframes glow {
            from { text-shadow: 0 0 10px rgba(0, 210, 255, 0.4); }
            to { text-shadow: 0 0 30px rgba(157, 0, 255, 0.6); }
        }

        /* 5. GLASS CARDS (The "Container" Look) */
        .glass-card {
            background: rgba(20, 20, 20, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        .glass-card:hover {
            transform: translateY(-5px);
            border-color: rgba(0, 210, 255, 0.3);
            box-shadow: 0 10px 40px rgba(0, 210, 255, 0.1);
        }

        /* 6. INPUTS & TEXT AREAS */
        .stTextArea textarea, .stTextInput input {
            background-color: #0a0a0a !important;
            border: 1px solid #333 !important;
            color: #fff !important;
            font-family: 'Exo 2', sans-serif;
            border-radius: 12px;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #00d2ff !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.2);
        }

        /* 7. NEON BUTTONS */
        .stButton>button {
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            color: black !important;
            font-family: 'Orbitron', sans-serif;
            font-weight: 800;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
        }

        /* 8. TICKER TAPE */
        .ticker-wrap {
            width: 100%;
            background: #050505;
            border-bottom: 1px solid #222;
            overflow: hidden;
            white-space: nowrap;
            padding: 10px 0;
        }
        .ticker-item {
            font-family: 'Orbitron', sans-serif;
            color: #888;
            font-size: 0.8rem;
            padding: 0 2rem;
        }
        .up { color: #00d2ff; }
        .down { color: #ff0055; }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    # Animated Title
    st.markdown('<div class="neon-title">ABDULLAH\'S AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Neural Sentiment & Market Intelligence</div>', unsafe_allow_html=True)
