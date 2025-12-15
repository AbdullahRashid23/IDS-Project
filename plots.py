import plotly.graph_objects as go

def plot_gauge(score):
    score_pct = score * 100
    # Cyan for Bullish, Hot Pink for Bearish
    color = "#00d2ff" if score > 0.5 else "#ff0055"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score_pct,
        number = {'font': {'color': color, 'family': "Orbitron"}},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "#333"},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 100], 'color': 'rgba(20,20,20,0.8)'} # Dark track
            ],
        }
    ))
    fig.update_layout(
        height=200, 
        margin=dict(t=20,b=20,l=20,r=20), 
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#fff", 'family': "Exo 2"}
    )
    return fig

def plot_stock_history(ticker, df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        increasing_line_color= '#00d2ff', # Neon Cyan
        decreasing_line_color= '#ff0055'  # Neon Pink
    )])

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(t=30, b=0, l=0, r=0),
        xaxis_rangeslider_visible=False,
        font={'family': "Exo 2", 'size': 10}
    )
    return fig
