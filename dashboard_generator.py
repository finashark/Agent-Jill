import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime
import numpy as np

def create_trading_dashboard(csv_file_path):
    """
    Tạo dashboard trading từ file CSV
    """
    # Đọc và xử lý dữ liệu
    df = pd.read_csv(csv_file_path)
    
    # Loại bỏ Balance transactions
    df_trades = df[df['SYMBOL'] != ''].copy()
    df_trades = df_trades[~df_trades['SYMBOL'].str.contains('Balance', na=False)]
    
    # Tính toán các metrics
    net_pnl = df_trades['PROFIT'].sum()
    total_trades = len(df_trades)
    win_rate = (df_trades['PROFIT'] > 0).mean() * 100
    
    winning_trades = df_trades[df_trades['PROFIT'] > 0]['PROFIT'].sum()
    losing_trades = abs(df_trades[df_trades['PROFIT'] < 0]['PROFIT'].sum())
    profit_factor = winning_trades / losing_trades if losing_trades > 0 else float('inf')
    
    # Tính thời gian nắm giữ
    df_trades['OPEN TIME'] = pd.to_datetime(df_trades['OPEN TIME'])
    df_trades['CLOSE TIME'] = pd.to_datetime(df_trades['CLOSE TIME'])
    df_trades['DURATION_HOURS'] = (df_trades['CLOSE TIME'] - df_trades['OPEN TIME']).dt.total_seconds() / 3600
    
    # Phân loại trading style
    def classify_style(hours):
        if hours < 1:
            return 'SCALP'
        elif hours < 8:
            return 'INTRADAY'
        elif hours < 168:  # 7 days
            return 'SWING'
        else:
            return 'POSITION'
    
    df_trades['STYLE'] = df_trades['DURATION_HOURS'].apply(classify_style)
    
    # Phân loại asset
    def classify_asset(symbol):
        if pd.isna(symbol):
            return 'Khác'
        symbol = str(symbol).upper()
        if 'XAU' in symbol or 'XAG' in symbol or 'GOLD' in symbol:
            return 'Kim loại'
        elif any(curr in symbol for curr in ['USD', 'EUR', 'JPY', 'GBP', 'AUD']):
            return 'Forex'
        else:
            return 'Khác'
    
    df_trades['ASSET_CLASS'] = df_trades['SYMBOL'].apply(classify_asset)
    
    # Tạo dashboard metrics
    dashboard_data = {
        'net_pnl': round(net_pnl, 2),
        'total_trades': total_trades,
        'win_rate': round(win_rate, 1),
        'profit_factor': round(profit_factor, 2),
        'total_lots': round(df_trades['LOTS'].sum(), 1),
        'avg_trade': round(net_pnl / total_trades, 2) if total_trades > 0 else 0,
        'max_win': round(df_trades['PROFIT'].max(), 2),
        'max_loss': round(df_trades['PROFIT'].min(), 2)
    }
    
    # Trading style distribution
    style_dist = df_trades['STYLE'].value_counts(normalize=True) * 100
    
    # Asset distribution  
    asset_dist = df_trades['ASSET_CLASS'].value_counts(normalize=True) * 100
    
    return dashboard_data, style_dist, asset_dist, df_trades

def generate_dashboard_html(dashboard_data, style_dist, asset_dist):
    """
    Tạo HTML dashboard với dữ liệu thực
    """
    
    html_template = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Performance Dashboard</title>
    <style>
        /* CSS styles giống như trên */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .dashboard {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        
        .metric-value.positive {{ color: #28a745; }}
        .metric-value.negative {{ color: #dc3545; }}
        .metric-value.neutral {{ color: #6c757d; }}
        
        .metric-label {{
            font-size: 0.9rem;
            color: #666;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>📊 Trading Performance Dashboard</h1>
            <p>Phân tích từ dữ liệu thực - Generated on {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value {'positive' if dashboard_data['net_pnl'] > 0 else 'negative'}">${dashboard_data['net_pnl']:,.2f}</div>
                <div class="metric-label">Net P&L</div>
            </div>
            <div class="metric-card">
                <div class="metric-value neutral">{dashboard_data['total_trades']:,}</div>
                <div class="metric-label">Số giao dịch</div>
            </div>
            <div class="metric-card">
                <div class="metric-value neutral">{dashboard_data['win_rate']}%</div>
                <div class="metric-label">Tỷ lệ thắng</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'positive' if dashboard_data['profit_factor'] > 1 else 'negative'}">{dashboard_data['profit_factor']}</div>
                <div class="metric-label">Profit Factor</div>
            </div>
            <div class="metric-card">
                <div class="metric-value neutral">{dashboard_data['total_lots']}</div>
                <div class="metric-label">Tổng Lots</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'positive' if dashboard_data['avg_trade'] > 0 else 'negative'}">${dashboard_data['avg_trade']:,.2f}</div>
                <div class="metric-label">Avg Trade</div>
            </div>
        </div>
        
        <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); padding: 25px; border-radius: 15px; margin-bottom: 30px;">
            <h3 style="color: white; margin-bottom: 20px;">🎯 Trading Style Distribution</h3>
            {generate_style_bars(style_dist)}
        </div>
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px;">
            <h3 style="margin-bottom: 20px;">💎 Asset Class Distribution</h3>
            {generate_asset_items(asset_dist)}
        </div>
        
        <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 15px; color: #666;">
            <p>🤖 <strong>Dashboard được tạo tự động từ CSV data</strong></p>
            <p>📅 Generated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>💡 Ready để screenshot cho Jill AI Analysis!</p>
        </div>
    </div>
</body>
</html>
    """
    
    return html_template

def generate_style_bars(style_dist):
    """Tạo bars cho trading style"""
    bars_html = ""
    style_names = {
        'SCALP': 'SCALP (< 1h)',
        'INTRADAY': 'INTRADAY (1-8h)', 
        'SWING': 'SWING (8h-7d)',
        'POSITION': 'POSITION (>7d)'
    }
    
    for style in ['SCALP', 'INTRADAY', 'SWING', 'POSITION']:
        percentage = style_dist.get(style, 0)
        bars_html += f'''
        <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <span style="font-weight: bold; color: white;">{style_names[style]}</span>
            <span style="font-size: 1.2rem; font-weight: bold; color: white;">{percentage:.1f}%</span>
        </div>
        '''
    
    return bars_html

def generate_asset_items(asset_dist):
    """Tạo items cho asset distribution"""
    items_html = ""
    asset_icons = {
        'Kim loại': '🥇',
        'Forex': '💱', 
        'Khác': '📊'
    }
    
    for asset, percentage in asset_dist.items():
        icon = asset_icons.get(asset, '📊')
        items_html += f'''
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.2);">
            <span>{icon} {asset}</span>
            <span><strong>{percentage:.1f}%</strong></span>
        </div>
        '''
    
    return items_html

# Main function để chạy
if __name__ == "__main__":
    # Path to CSV file
    csv_path = "closed_trades_32284342.csv"
    
    try:
        # Tạo dashboard
        dashboard_data, style_dist, asset_dist, df_trades = create_trading_dashboard(csv_path)
        
        # Generate HTML
        html_content = generate_dashboard_html(dashboard_data, style_dist, asset_dist)
        
        # Save HTML file
        with open("generated_dashboard.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print("✅ Dashboard đã được tạo: generated_dashboard.html")
        print(f"📊 Metrics: Net P&L: ${dashboard_data['net_pnl']}, Trades: {dashboard_data['total_trades']}")
        print("📱 Sẵn sàng để screenshot cho Jill AI!")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")