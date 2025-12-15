import pandas as pd
import base64
import time

def generate_html_report(history_data):
    """
    history_data: List of dicts [{'time':..., 'text':..., 'label':..., 'score':...}]
    Returns: HTML string link for download
    """
    if not history_data:
        return None

    df = pd.DataFrame(history_data)
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Helvetica, sans-serif; color: #333; }}
            h1 {{ color: #0f172a; border-bottom: 2px solid #3b82f6; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background: #0f172a; color: white; padding: 10px; text-align: left; }}
            td {{ border-bottom: 1px solid #ddd; padding: 8px; }}
            .bull {{ color: green; font-weight: bold; }}
            .bear {{ color: red; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>CITADEL INTELLIGENCE REPORT</h1>
        <p><strong>Generated:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Session ID:</strong> {hash(time.time())}</p>
        <hr>
        <h3>ANALYSIS LOG</h3>
        {df.to_html(index=False, classes='table')}
    </body>
    </html>
    """
    
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="Citadel_Report.html" style="text-decoration:none; padding:10px 20px; background:#3b82f6; color:white; border-radius:5px;">📥 DOWNLOAD INTELLIGENCE REPORT</a>'
