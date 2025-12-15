import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def get_chart(ticker):
    """Fetches data and builds a Luxury Gold Chart."""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="3mo")
        
        if df.empty: return None, None
        
        # Calculate Technicals
        df['SMA_20'] = df['Close'].rolling(window=20).mean()

        # Create Figure
        fig = go.Figure()

        # 1. GOLD PRICE LINE
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'],
            mode='lines',
            name='Price',
            line=dict(color='#FFD700', width=3), # PURE GOLD
            fill='tozeroy',
            fillcolor='rgba(255, 215, 0, 0.1)' # Gold Mist
        ))

        # 2. SMA Line (Platinum White)
        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_20'],
            mode='lines',
            name='SMA 20',
            line=dict(color='#ffffff', width=1, dash='dot')
        ))

        # 3. Aesthetics
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            margin=dict(t=50, b=20, l=20, r=20),
            title=dict(
                text=f"{ticker} // WEALTH VECTOR",
                font=dict(size=24, family="Cinzel", color="#FFD700")
            ),
            xaxis=dict(showgrid=False, linecolor='#333'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,215,0,0.1)'), # Gold Grid
            hovermode="x unified"
        )
        
        return fig, df.iloc[-1]
    except Exception as e:
        return None, None
