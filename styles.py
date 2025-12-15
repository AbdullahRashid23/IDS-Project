import streamlit as st

# RENAMED FUNCTION TO FORCE UPDATE
def load_citadel_theme():
    st.markdown("""
    <style>
        /* IMPORT TACTICAL FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Roboto+Mono:wght@400;700&display=swap');

        /* GLOBAL THEME */
        html, body, [class*="css"] {
            font-family: 'Rajdhani', sans-serif;
            background-color: #050505;
            color: #e0e0e0;
        }

        /* BACKGROUND - DEEP CITADEL */
        .stApp {
            background: linear-gradient(to bottom, #0f172a, #000000);
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 1px solid #1e293b;
        }

        /* HUD CARDS */
        .hud-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid #334155;
            border-left: 4px solid #3b82f6; /* Tactical Blue Accent */
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        }

        /* METRIC CONTAINERS */
        div[data-testid="stMetricValue"] {
            font-family: 'Roboto Mono', monospace;
            color: #00ffa3; /* HUD Green */
        }

        /* BUTTONS */
        .stButton>button {
            background-color: #1e293b;
            color: #00ffa3;
            border: 1px solid #00ffa3;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            border-radius: 0px; /* Sharp corners */
            transition: all 0.2s;
        }
        .stButton>button:hover {
            background-color: #00ffa3;
            color: #000;
            box-shadow: 0 0 15px rgba(0, 255, 163, 0.4);
        }

        /* INPUTS */
        .stTextInput input, .stTextArea textarea {
            background-color: #0a0a0a;
            border: 1px solid #334155;
            color: #fff;
            font-family: 'Roboto Mono', monospace;
        }
        
        /* HEADERS */
        h1, h2, h3 {
            text-transform: uppercase;
            letter-spacing: 2px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; border-bottom: 2px solid #334155; padding-bottom: 10px;">
        <h1 style="margin:0; font-size: 3rem; color: #fff; text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);">
            THE CITADEL
        </h1>
        <p style="font-family: 'Roboto Mono'; color: #64748b; font-size: 0.9rem;">
            FINANCIAL INTELLIGENCE SUITE // <span style="color:#00ffa3">ONLINE</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
