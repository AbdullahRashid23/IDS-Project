import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def get_chart(ticker):
    """Fetches data and builds a High-Fidelity Neon Chart."""
    try:
        # FIX: Use Ticker.history for cleaner data structure
        stock = yf.Ticker(ticker)
        df = stock.history(period="3mo")
        
        if df.empty: return None, None
        
        # Calculate Technicals
        df['SMA_20'] = df['Close'].rolling(window=20).mean()

        # Create Figure
        fig = go.Figure()

        # 1. Main Price Line (Glowing Gradient)
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'],
            mode='lines',
            name='Price',
            line=dict(color='#38bdf8', width=3),
            fill='tozeroy',
            fillcolor='rgba(56, 189, 248, 0.1)' # Subtle fill
        ))

        # 2. SMA Line (Warning Color)
        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_20'],
            mode='lines',
            name='SMA 20',
            line=dict(color='#fbbf24', width=2, dash='dot')
        ))

        # 3. Aesthetics (The "Dark Mode" Look)
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            margin=dict(t=50, b=20, l=20, r=20),
            title=dict(
                text=f"{ticker} // MARKET VECTOR",
                font=dict(size=24, family="Orbitron", color="white")
            ),
            xaxis=dict(showgrid=False, showline=True, linecolor='#333'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            hovermode="x unified"
        )
        
        return fig, df.iloc[-1]
    except Exception as e:
        return None, None
