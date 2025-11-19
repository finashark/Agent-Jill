#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AUTO DASHBOARD GENERATOR - ONE CLICK SOLUTION
Tạo dashboard và chụp ảnh tự động cho Jill AI Analysis

Author: Jill AI System
Version: 1.0
Date: November 5, 2025
"""

import pandas as pd
import os
import sys
import webbrowser
import time
from datetime import datetime
import subprocess
import platform

def install_required_packages():
    """Tự động cài đặt packages cần thiết"""
    required_packages = [
        'pandas',
        'selenium',
        'webdriver-manager',
        'pillow'
    ]
    
    print("🔧 Checking and installing required packages...")
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")

def setup_selenium_driver():
    """Setup Selenium WebDriver cho screenshot tự động"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Chạy không hiển thị browser
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        
        # Setup driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver
        
    except Exception as e:
        print(f"❌ Error setting up Chrome driver: {e}")
        return None

def process_csv_data(csv_file_path):
    """Xử lý dữ liệu CSV và tính toán metrics"""
    try:
        print(f"📊 Processing CSV file: {csv_file_path}")
        
        # Đọc CSV
        df = pd.read_csv(csv_file_path)
        print(f"📈 Loaded {len(df)} rows from CSV")
        
        # Làm sạch dữ liệu - loại bỏ Balance transactions
        df_clean = df[df['SYMBOL'].notna()].copy()
        df_trades = df_clean[~df_clean['SYMBOL'].str.contains('Balance', na=False, case=False)]
        df_trades = df_trades[df_trades['SYMBOL'] != '']
        
        print(f"🔍 Found {len(df_trades)} actual trades (after removing balance transactions)")
        
        # Tính toán metrics
        net_pnl = df_trades['PROFIT'].sum()
        total_trades = len(df_trades)
        
        if total_trades == 0:
            print("⚠️ No trades found in CSV file!")
            return None
            
        win_rate = (df_trades['PROFIT'] > 0).mean() * 100
        
        winning_trades = df_trades[df_trades['PROFIT'] > 0]['PROFIT'].sum()
        losing_trades = abs(df_trades[df_trades['PROFIT'] < 0]['PROFIT'].sum())
        profit_factor = winning_trades / losing_trades if losing_trades > 0 else float('inf')
        
        total_lots = df_trades['LOTS'].sum()
        avg_trade = net_pnl / total_trades
        max_win = df_trades['PROFIT'].max()
        max_loss = df_trades['PROFIT'].min()
        
        # Tính thời gian nắm giữ
        df_trades['OPEN TIME'] = pd.to_datetime(df_trades['OPEN TIME'], errors='coerce')
        df_trades['CLOSE TIME'] = pd.to_datetime(df_trades['CLOSE TIME'], errors='coerce')
        df_trades['DURATION_HOURS'] = (df_trades['CLOSE TIME'] - df_trades['OPEN TIME']).dt.total_seconds() / 3600
        
        # Phân loại trading style
        def classify_style(hours):
            if pd.isna(hours) or hours < 1:
                return 'SCALP'
            elif hours < 8:
                return 'INTRADAY'
            elif hours < 168:  # 7 days
                return 'SWING'
            else:
                return 'POSITION'
        
        df_trades['STYLE'] = df_trades['DURATION_HOURS'].apply(classify_style)
        style_dist = df_trades['STYLE'].value_counts(normalize=True) * 100
        
        # Phân loại asset
        def classify_asset(symbol):
            if pd.isna(symbol):
                return 'Khác'
            symbol = str(symbol).upper()
            if 'XAU' in symbol or 'XAG' in symbol or 'GOLD' in symbol or 'SILVER' in symbol:
                return 'Kim loại'
            elif any(curr in symbol for curr in ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'NZD', 'CAD', 'CHF']):
                return 'Forex'
            elif any(idx in symbol for idx in ['US30', 'US500', 'NAS100', 'SPX', 'DXY']):
                return 'Chỉ số'
            else:
                return 'Khác'
        
        df_trades['ASSET_CLASS'] = df_trades['SYMBOL'].apply(classify_asset)
        asset_dist = df_trades['ASSET_CLASS'].value_counts(normalize=True) * 100
        
        # Tạo dashboard data
        dashboard_data = {
            'net_pnl': round(net_pnl, 2),
            'total_trades': total_trades,
            'win_rate': round(win_rate, 1),
            'profit_factor': round(profit_factor, 2),
            'total_lots': round(total_lots, 1),
            'avg_trade': round(avg_trade, 2),
            'max_win': round(max_win, 2),
            'max_loss': round(max_loss, 2),
            'winning_trades': len(df_trades[df_trades['PROFIT'] > 0]),
            'losing_trades': len(df_trades[df_trades['PROFIT'] < 0])
        }
        
        print("✅ Data processing completed successfully!")
        print(f"📊 Key metrics: Net P&L: ${dashboard_data['net_pnl']}, Win Rate: {dashboard_data['win_rate']}%")
        
        return dashboard_data, style_dist, asset_dist
        
    except Exception as e:
        print(f"❌ Error processing CSV data: {e}")
        return None

def generate_dashboard_html(dashboard_data, style_dist, asset_dist, output_file="auto_generated_dashboard.html"):
    """Tạo HTML dashboard với dữ liệu đầy đủ"""
    
    # Helper functions
    def generate_style_bars(style_dist):
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
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px; backdrop-filter: blur(10px);">
                <span style="font-weight: bold; color: white;">{style_names[style]}</span>
                <span style="font-size: 1.4rem; font-weight: bold; color: white;">{percentage:.1f}%</span>
            </div>
            '''
        return bars_html
    
    def generate_asset_items(asset_dist):
        items_html = ""
        asset_icons = {
            'Kim loại': '🥇',
            'Forex': '💱', 
            'Chỉ số': '📊',
            'Khác': '🔸'
        }
        
        for asset, percentage in asset_dist.items():
            icon = asset_icons.get(asset, '🔸')
            items_html += f'''
            <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.2);">
                <span style="font-size: 1.1rem;">{icon} {asset}</span>
                <span style="font-size: 1.2rem;"><strong>{percentage:.1f}%</strong></span>
            </div>
            '''
        return items_html
    
    # Chart.js data  
    asset_labels = list(asset_dist.index)
    asset_values = [round(float(v), 1) for v in asset_dist.values]
    
    style_labels = ['SCALP', 'INTRADAY', 'SWING', 'POSITION'] 
    style_values = [round(style_dist.get(style, 0), 1) for style in style_labels]
    
    html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Performance Dashboard - Auto Generated</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
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
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(102,126,234,0.3);
        }}
        
        .header h1 {{
            font-size: 2.8rem;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.3rem;
            opacity: 0.95;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(0,0,0,0.05);
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        }}
        
        .metric-value {{
            font-size: 2.2rem;
            font-weight: bold;
            margin-bottom: 8px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }}
        
        .metric-value.positive {{ color: #28a745; }}
        .metric-value.negative {{ color: #dc3545; }}
        .metric-value.neutral {{ color: #495057; }}
        
        .metric-label {{
            font-size: 1rem;
            color: #6c757d;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .charts-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 50px;
        }}
        
        .chart-container {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,0,0,0.05);
        }}
        
        .chart-title {{
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 25px;
            text-align: center;
            color: #333;
        }}
        
        .trading-style-section {{
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            box-shadow: 0 10px 20px rgba(255,154,158,0.3);
        }}
        
        .trading-style-section h3 {{
            color: white;
            margin-bottom: 25px;
            font-size: 1.6rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .asset-breakdown {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(102,126,234,0.3);
        }}
        
        .asset-breakdown h3 {{
            margin-bottom: 25px;
            font-size: 1.6rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 25px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            color: #666;
            border: 1px solid rgba(0,0,0,0.05);
        }}
        
        .footer p {{
            margin: 5px 0;
            font-size: 1.1rem;
        }}
        
        .auto-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
            margin-left: 10px;
            box-shadow: 0 3px 6px rgba(40,167,69,0.3);
        }}
        
        @media (max-width: 768px) {{
            .charts-section {{
                grid-template-columns: 1fr;
            }}
            
            .metrics-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>📊 Trading Performance Dashboard</h1>
            <p>Auto-Generated Report <span class="auto-badge">🤖 AUTO</span></p>
            <p style="font-size: 1rem; margin-top: 10px; opacity: 0.8;">Generated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value {'positive' if dashboard_data['net_pnl'] > 0 else 'negative' if dashboard_data['net_pnl'] < 0 else 'neutral'}">${dashboard_data['net_pnl']:,.2f}</div>
                <div class="metric-label">Net P&L</div>
            </div>
            <div class="metric-card">
                <div class="metric-value neutral">{dashboard_data['total_trades']:,}</div>
                <div class="metric-label">Số giao dịch</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'positive' if dashboard_data['win_rate'] > 50 else 'negative' if dashboard_data['win_rate'] < 40 else 'neutral'}">{dashboard_data['win_rate']}%</div>
                <div class="metric-label">Tỷ lệ thắng</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'positive' if dashboard_data['profit_factor'] > 1.2 else 'negative' if dashboard_data['profit_factor'] < 1 else 'neutral'}">{dashboard_data['profit_factor']}</div>
                <div class="metric-label">Profit Factor</div>
            </div>
            <div class="metric-card">
                <div class="metric-value neutral">{dashboard_data['total_lots']}</div>
                <div class="metric-label">Tổng Lots</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'positive' if dashboard_data['avg_trade'] > 0 else 'negative' if dashboard_data['avg_trade'] < 0 else 'neutral'}">${dashboard_data['avg_trade']:,.2f}</div>
                <div class="metric-label">Avg Trade</div>
            </div>
            <div class="metric-card">
                <div class="metric-value positive">${dashboard_data['max_win']:,.2f}</div>
                <div class="metric-label">Max Win</div>
            </div>
            <div class="metric-card">
                <div class="metric-value negative">${dashboard_data['max_loss']:,.2f}</div>
                <div class="metric-label">Max Loss</div>
            </div>
        </div>
        
        <div class="charts-section">
            <div class="chart-container">
                <div class="chart-title">📈 Phân bổ theo nhóm tài sản</div>
                <canvas id="assetChart" width="400" height="300"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">⏱️ Phong cách giao dịch</div>
                <canvas id="styleChart" width="400" height="300"></canvas>
            </div>
        </div>
        
        <div class="trading-style-section">
            <h3>🎯 Trading Style Breakdown</h3>
            {generate_style_bars(style_dist)}
        </div>
        
        <div class="asset-breakdown">
            <h3>💎 Asset Class Distribution</h3>
            {generate_asset_items(asset_dist)}
        </div>
        
        <div class="footer">
            <p><strong>🤖 Dashboard tự động từ Python Script</strong></p>
            <p>📅 Generated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>💡 Ready để screenshot cho Jill AI Analysis!</p>
            <p>🎯 Trades: {dashboard_data['winning_trades']} wins / {dashboard_data['losing_trades']} losses</p>
        </div>
    </div>

    <script>
        // Asset Distribution Pie Chart
        const assetCtx = document.getElementById('assetChart').getContext('2d');
        new Chart(assetCtx, {{
            type: 'pie',
            data: {{
                labels: {asset_labels},
                datasets: [{{
                    data: {asset_values},
                    backgroundColor: [
                        '#FFD700',  // Kim loại - Gold
                        '#4285F4',  // Forex - Blue  
                        '#EA4335',  // Chỉ số - Red
                        '#34A853',  // Khác - Green
                        '#9AA0A6'   // Extra colors
                    ],
                    borderWidth: 3,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            usePointStyle: true,
                            font: {{
                                size: 12,
                                weight: 'bold'
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Trading Style Bar Chart
        const styleCtx = document.getElementById('styleChart').getContext('2d');
        new Chart(styleCtx, {{
            type: 'bar',
            data: {{
                labels: {style_labels},
                datasets: [{{
                    label: 'Tỷ lệ %',
                    data: {style_values},
                    backgroundColor: [
                        '#FF6B6B',  // SCALP - Red
                        '#4ECDC4',  // INTRADAY - Teal
                        '#45B7D1',  // SWING - Blue
                        '#96CEB4'   // POSITION - Green
                    ],
                    borderWidth: 1,
                    borderRadius: 8,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{
                            callback: function(value) {{
                                return value + '%';
                            }},
                            font: {{
                                weight: 'bold'
                            }}
                        }}
                    }},
                    x: {{
                        ticks: {{
                            font: {{
                                weight: 'bold'
                            }}
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''
    
    # Ghi file HTML
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML dashboard created: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ Error creating HTML file: {e}")
        return None

def take_screenshot(html_file, output_image="dashboard_screenshot.png"):
    """Chụp ảnh dashboard tự động bằng Selenium"""
    
    driver = setup_selenium_driver()
    if not driver:
        print("❌ Cannot setup Chrome driver for screenshot")
        return None
    
    try:
        # Get absolute path
        html_path = os.path.abspath(html_file)
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        
        print(f"📸 Taking screenshot of: {file_url}")
        
        # Load page
        driver.get(file_url)
        
        # Wait for page to load completely
        time.sleep(3)
        
        # Wait for charts to render
        print("⏳ Waiting for charts to render...")
        time.sleep(5)
        
        # Get page dimensions and set window size
        page_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, max(1080, page_height + 100))
        
        # Take screenshot
        screenshot_path = os.path.abspath(output_image)
        driver.save_screenshot(screenshot_path)
        
        print(f"✅ Screenshot saved: {screenshot_path}")
        
        # Close driver
        driver.quit()
        
        return screenshot_path
        
    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")
        driver.quit()
        return None

def open_jill_ai():
    """Mở Jill AI trong browser"""
    try:
        jill_url = "http://localhost:8502"
        print(f"🚀 Opening Jill AI: {jill_url}")
        webbrowser.open(jill_url)
        return True
    except Exception as e:
        print(f"❌ Error opening Jill AI: {e}")
        return False

def main():
    """Main function - ONE CLICK SOLUTION"""
    
    print("="*60)
    print("🤖 AUTO DASHBOARD GENERATOR - ONE CLICK SOLUTION")
    print("="*60)
    print(f"📅 Started at: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Bước 1: Install packages
    print("🔧 STEP 1: Installing required packages...")
    install_required_packages()
    print()
    
    # Bước 2: Tìm file CSV
    print("📁 STEP 2: Looking for CSV file...")
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No CSV files found in current directory!")
        print("💡 Please place your CSV file in the same directory as this script")
        input("Press Enter to exit...")
        return
    
    # Chọn file CSV (lấy file đầu tiên hoặc file cụ thể)
    csv_file = None
    for f in csv_files:
        if 'closed_trades' in f.lower() or 'trade' in f.lower():
            csv_file = f
            break
    
    if not csv_file:
        csv_file = csv_files[0]  # Lấy file đầu tiên
    
    print(f"📊 Found CSV file: {csv_file}")
    print()
    
    # Bước 3: Xử lý dữ liệu
    print("⚙️ STEP 3: Processing trading data...")
    result = process_csv_data(csv_file)
    if not result:
        print("❌ Failed to process CSV data!")
        input("Press Enter to exit...")
        return
    
    dashboard_data, style_dist, asset_dist = result
    print()
    
    # Bước 4: Tạo HTML dashboard
    print("🎨 STEP 4: Generating HTML dashboard...")
    html_file = generate_dashboard_html(dashboard_data, style_dist, asset_dist)
    if not html_file:
        print("❌ Failed to generate HTML dashboard!")
        input("Press Enter to exit...")
        return
    print()
    
    # Bước 5: Chụp ảnh tự động
    print("📸 STEP 5: Taking automatic screenshot...")
    screenshot_path = take_screenshot(html_file)
    if not screenshot_path:
        print("❌ Failed to take screenshot!")
        print("💡 You can manually open the HTML file and take screenshot")
    else:
        print(f"✅ Screenshot ready: {screenshot_path}")
    print()
    
    # Bước 6: Mở files
    print("🚀 STEP 6: Opening results...")
    
    # Mở HTML dashboard
    try:
        dashboard_path = os.path.abspath(html_file)
        if platform.system() == "Windows":
            os.startfile(dashboard_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", dashboard_path])
        else:  # Linux
            subprocess.call(["xdg-open", dashboard_path])
        print("✅ Dashboard opened in browser")
    except Exception as e:
        print(f"⚠️ Could not auto-open dashboard: {e}")
    
    # Mở ảnh nếu có
    if screenshot_path and os.path.exists(screenshot_path):
        try:
            if platform.system() == "Windows":
                os.startfile(screenshot_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", screenshot_path])
            else:  # Linux
                subprocess.call(["xdg-open", screenshot_path])
            print("✅ Screenshot opened")
        except Exception as e:
            print(f"⚠️ Could not auto-open screenshot: {e}")
    
    # Mở Jill AI
    print("🤖 Opening Jill AI...")
    open_jill_ai()
    
    print()
    print("="*60)
    print("🎉 ONE CLICK SOLUTION COMPLETED!")
    print("="*60)
    print("📊 Dashboard metrics:")
    print(f"   💰 Net P&L: ${dashboard_data['net_pnl']:,.2f}")
    print(f"   📈 Total Trades: {dashboard_data['total_trades']:,}")
    print(f"   🎯 Win Rate: {dashboard_data['win_rate']}%")
    print(f"   ⚡ Profit Factor: {dashboard_data['profit_factor']}")
    print()
    print("📱 Next steps:")
    print("   1. ✅ Dashboard opened in browser")
    if screenshot_path:
        print("   2. ✅ Screenshot ready for upload")
    print("   3. ✅ Jill AI opened at http://localhost:8502")
    print("   4. 📷 Upload screenshot to Jill AI")
    print("   5. 🤖 Get automatic analysis!")
    print()
    print("💡 Files created:")
    print(f"   📄 Dashboard: {html_file}")
    if screenshot_path:
        print(f"   🖼️ Screenshot: {screenshot_path}")
    print()
    
    input("Press Enter to finish...")

if __name__ == "__main__":
    main()