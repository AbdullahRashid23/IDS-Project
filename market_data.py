import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculate_rsi(data, window=14):
    """Helper to calculate RSI without external heavy libraries"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_chart(ticker):
    """
    Fetches 6 months of data and builds a Pro-Level Technical Analysis Chart
    Features: Candlesticks, SMA-20, Bollinger Bands, and Volume.
    """
    try:
        # 1. Fetch Data (Extended period for better context)
        stock = yf.Ticker(ticker)
        df = stock.history(period="6mo")
        
        if df.empty: return None, None
        
        # 2. Calculate Technical Indicators
        # SMA 20
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        
        # Bollinger Bands (2 Standard Deviations)
        df['STD_20'] = df['Close'].rolling(window=20).std()
        df['Upper_BB'] = df['SMA_20'] + (df['STD_20'] * 2)
        df['Lower_BB'] = df['SMA_20'] - (df['STD_20'] * 2)
        
        # RSI
        df['RSI'] = calculate_rsi(df['Close'])

        # 3. Create Subplots (Row 1: Price, Row 2: Volume)
        fig = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.05, 
            row_heights=[0.75, 0.25]
        )

        # --- MAIN CHART (CANDLESTICKS) ---
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            name='OHLC',
            increasing_line_color='#00ff00', # Bright Green
            decreasing_line_color='#ff2a2a'  # Bright Red
        ), row=1, col=1)

        # SMA 20 (The Gold Line)
        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_20'], 
            mode='lines', name='SMA 20', 
            line=dict(color='#FFD700', width=2)
        ), row=1, col=1)

        # Bollinger Bands (Subtle Shading)
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Upper_BB'], 
            mode='lines', name='Upper BB',
            line=dict(width=0), showlegend=False
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Lower_BB'], 
            mode='lines', name='Lower BB',
            line=dict(width=0), fill='tonexty', 
            fillcolor='rgba(255, 215, 0, 0.1)', # Gold Mist
            showlegend=False
        ), row=1, col=1)

        # --- VOLUME CHART (BOTTOM) ---
        colors = ['#00ff00' if c >= o else '#ff2a2a' for c, o in zip(df['Close'], df['Open'])]
        fig.add_trace(go.Bar(
            x=df.index, y=df['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.5
        ), row=2, col=1)

        # 4. LUXURY STYLING
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            title=dict(
                text=f"{ticker} MARKET VECTOR",
                font=dict(color="#FFD700", family="Orbitron", size=20)
            ),
            margin=dict(t=50, b=20, l=20, r=20),
            hovermode="x unified",
            xaxis_rangeslider_visible=False,
            showlegend=False
        )

        # Clean Gridlines
        fig.update_xaxes(showgrid=False, row=1, col=1)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', row=1, col=1)
        fig.update_yaxes(showgrid=False, row=2, col=1)

        # Return the figure and the last row (with RSI added)
        return fig, df.iloc[-1]
        
    except Exception as e:
        return None, None
