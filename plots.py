import plotly.graph_objects as go
import plotly.express as px

def plot_gauge(score):
    """Renders a speedometer gauge for sentiment."""
    score_pct = score * 100
    color = "#10b981" if score > 0.5 else "#ef4444"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score_pct,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [60, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score_pct
            }
        }
    ))
    fig.update_layout(
        height=250, 
        margin=dict(t=10,b=10,l=20,r=20), 
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Poppins"}
    )
    return fig

def plot_stock_history(ticker, df):
    """Renders a professional candlestick chart."""
    if df.empty:
        return None

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        increasing_line_color= '#10b981', 
        decreasing_line_color= '#ef4444'
    )])

    fig.update_layout(
        title=f"{ticker} Price Action",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(t=40, b=20, l=20, r=20),
        font={'family': "JetBrains Mono"},
        xaxis_rangeslider_visible=False
    )
    return fig
