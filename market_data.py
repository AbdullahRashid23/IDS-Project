import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta # Technical Analysis Library

def get_chart(ticker):
    """Fetches data and builds a Tactical Candle Chart."""
    try:
        # 1. Fetch Data
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if df.empty: return None
        
        # 2. Add Technical Indicators (SMA 20)
        # Using simple pandas rolling window for robustness
        df['SMA_20'] = df['Close'].rolling(window=20).mean()

        # 3. Build Plotly Chart
        fig = go.Figure()

        # Candlesticks
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            name='Price',
            increasing_line_color='#00ffa3',
            decreasing_line_color='#ff2a2a'
        ))

        # SMA Overlay
        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_20'],
            mode='lines', name='SMA (20)',
            line=dict(color='#3b82f6', width=2)
        ))

        # Tactical Layout
        fig.update_layout(
            title=f"{ticker} // TACTICAL VIEW",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            font={'family': "Roboto Mono"},
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        return fig, df.iloc[-1] # Return fig and last row data
    except Exception as e:
        return None, None
