"""
Trading Metrics Calculator
==========================
Công cụ tính toán tự động các chỉ số giao dịch từ file CSV broker.

Hướng dẫn sử dụng:
1. Đặt file CSV vào thư mục được chỉ định
2. Chạy script này: python trading_metrics_calculator.py
3. Kết quả sẽ hiển thị trên màn hình và xuất ra file Excel summary
4. Copy/paste các giá trị vào form Agent Jill

Yêu cầu:
- Python 3.7+
- pandas, openpyxl

Cài đặt: pip install pandas openpyxl
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import sys

# === CẤU HÌNH ===
# Đường dẫn mặc định đến folder chứa CSV
DEFAULT_CSV_FOLDER = r"D:\SharkMe Data\Agent-Jill-main\Agent-Jill-main"  # Thay đổi theo thư mục của bạn
OUTPUT_EXCEL_NAME = "Trading_Metrics_Summary.xlsx"

# === HÀM PHỤ TRỢ ===

def standardize_column_names(df):
    """Chuẩn hóa tên cột để tương thích với nhiều format"""
    column_mapping = {
        'Ticket': 'TICKET', 'ticket': 'TICKET', 'TICKET': 'TICKET',
        'Symbol': 'SYMBOL', 'SYMBOL': 'SYMBOL', 'Item': 'SYMBOL', 'item': 'SYMBOL',
        'Type': 'ACTION', 'type': 'ACTION', 'Action': 'ACTION', 'ACTION': 'ACTION',
        'Lots': 'LOTS', 'lots': 'LOTS', 'LOTS': 'LOTS', 'Volume': 'LOTS', 'volume': 'LOTS',
        'Open Time': 'OPEN_TIME', 'OPEN TIME': 'OPEN_TIME', 'open time': 'OPEN_TIME', 'open_time': 'OPEN_TIME',
        'Close Time': 'CLOSE_TIME', 'CLOSE TIME': 'CLOSE_TIME', 'close time': 'CLOSE_TIME', 'close_time': 'CLOSE_TIME',
        'Profit': 'PROFIT', 'profit': 'PROFIT', 'PROFIT': 'PROFIT',
        'Commission': 'COMM', 'COMM': 'COMM', 'comm': 'COMM', 'commission': 'COMM',
        'Swap': 'SWAP', 'swap': 'SWAP', 'SWAP': 'SWAP',
        'Taxes': 'TAXES', 'taxes': 'TAXES', 'TAXES': 'TAXES'
    }
    
    df = df.rename(columns=column_mapping)
    return df

def clean_trading_data(df):
    """Làm sạch dữ liệu - loại bỏ Balance transactions và invalid rows"""
    # Loại bỏ các dòng không phải giao dịch Buy/Sell
    valid_actions = ['Buy', 'Sell', 'buy', 'sell', 'BUY', 'SELL']
    df = df[df['ACTION'].isin(valid_actions)]
    
    # Chuẩn hóa ACTION
    df['ACTION'] = df['ACTION'].str.title()  # Buy, Sell
    
    # Chuyển đổi thời gian
    df['OPEN_TIME'] = pd.to_datetime(df['OPEN_TIME'], errors='coerce')
    df['CLOSE_TIME'] = pd.to_datetime(df['CLOSE_TIME'], errors='coerce')
    
    # Loại bỏ các giao dịch không có thời gian hợp lệ
    df = df.dropna(subset=['OPEN_TIME', 'CLOSE_TIME'])
    
    # Chuyển đổi numeric columns
    numeric_columns = ['LOTS', 'PROFIT']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Optional columns
    for col in ['COMM', 'SWAP', 'TAXES']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0
    
    # Loại bỏ rows với LOTS = 0 hoặc NaN
    df = df[df['LOTS'] > 0]
    
    return df.reset_index(drop=True)

def calculate_metrics(df):
    """Tính toán tất cả các metrics cần thiết"""
    
    if len(df) == 0:
        return None
    
    # Basic metrics
    total_trades = len(df)
    
    # Win rate
    winning_trades = len(df[df['PROFIT'] > 0])
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    # Profit factor
    total_profit = df[df['PROFIT'] > 0]['PROFIT'].sum()
    total_loss = abs(df[df['PROFIT'] < 0]['PROFIT'].sum())
    profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')
    
    # Net PnL (including commission, swap, taxes)
    df['Net_PnL'] = df['PROFIT'] + df['COMM'] + df['SWAP'] + df['TAXES']
    net_pnl = df['Net_PnL'].sum()
    
    # Total lots
    total_lots = df['LOTS'].sum()
    
    # Holding time analysis
    df['Holding_Hours'] = (df['CLOSE_TIME'] - df['OPEN_TIME']).dt.total_seconds() / 3600
    avg_holding_hours = df['Holding_Hours'].mean()
    
    # Trading style breakdown
    scalp_count = len(df[df['Holding_Hours'] < 1])
    intraday_count = len(df[(df['Holding_Hours'] >= 1) & (df['Holding_Hours'] < 8)])
    swing_count = len(df[(df['Holding_Hours'] >= 8) & (df['Holding_Hours'] < 168)])
    position_count = len(df[df['Holding_Hours'] >= 168])
    
    scalp_ratio = (scalp_count / total_trades * 100) if total_trades > 0 else 0
    
    trading_style = {
        'scalp': round((scalp_count / total_trades * 100), 1) if total_trades > 0 else 0,
        'intraday': round((intraday_count / total_trades * 100), 1) if total_trades > 0 else 0,
        'swing': round((swing_count / total_trades * 100), 1) if total_trades > 0 else 0,
        'position': round((position_count / total_trades * 100), 1) if total_trades > 0 else 0
    }
    
    # Asset distribution (top 3)
    asset_dist = df['SYMBOL'].value_counts(normalize=True).head(3) * 100
    dominant_asset = asset_dist.index[0] if len(asset_dist) > 0 else "N/A"
    
    asset_distribution = {}
    for i, (symbol, pct) in enumerate(asset_dist.items(), 1):
        asset_distribution[f'asset{i}_symbol'] = symbol
        asset_distribution[f'asset{i}_pct'] = round(pct, 1)
    
    # Compile results
    metrics = {
        'total_trades': int(total_trades),
        'win_rate': round(win_rate, 1),
        'profit_factor': round(profit_factor, 2) if profit_factor != float('inf') else 999.99,
        'net_pnl': round(net_pnl, 2),
        'total_lots': round(total_lots, 2),
        'avg_holding_hours': round(avg_holding_hours, 1),
        'scalp_ratio': round(scalp_ratio, 1),
        'dominant_asset': dominant_asset,
        'trading_style': trading_style,
        'asset_distribution': asset_distribution
    }
    
    return metrics

def load_and_process_csv(file_path):
    """Đọc và xử lý file CSV"""
    try:
        print(f"📂 Đang đọc file: {os.path.basename(file_path)}")
        
        # Thử đọc với encoding khác nhau
        encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"   ✅ Đọc thành công với encoding: {encoding}")
                break
            except:
                continue
        
        if df is None:
            print(f"   ❌ Không thể đọc file với các encoding thông dụng")
            return None
        
        # Standardize column names
        df = standardize_column_names(df)
        
        # Check required columns
        required_cols = ['SYMBOL', 'ACTION', 'LOTS', 'OPEN_TIME', 'CLOSE_TIME', 'PROFIT']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"   ❌ Thiếu các cột bắt buộc: {missing_cols}")
            print(f"   📋 Các cột hiện có: {list(df.columns)}")
            return None
        
        # Clean data
        df = clean_trading_data(df)
        
        if len(df) == 0:
            print(f"   ❌ Không có dữ liệu giao dịch hợp lệ sau khi làm sạch")
            return None
        
        print(f"   ✅ Xử lý thành công {len(df)} giao dịch")
        return df
        
    except Exception as e:
        print(f"   ❌ Lỗi xử lý file: {str(e)}")
        return None

def find_csv_files(folder_path):
    """Tìm tất cả file CSV trong folder"""
    folder = Path(folder_path)
    if not folder.exists():
        print(f"❌ Thư mục không tồn tại: {folder_path}")
        return []
    
    csv_files = list(folder.glob("*.csv"))
    return csv_files

def export_to_excel(metrics, output_path):
    """Xuất kết quả ra file Excel"""
    try:
        # Create DataFrame for export
        data = {
            'Chỉ Số': [
                'Tổng số giao dịch',
                'Tỷ lệ thắng (%)',
                'Profit Factor',
                'Net PnL (USD)',
                'Tổng khối lượng (lots)',
                'Thời gian nắm giữ TB (giờ)',
                'Tỷ lệ Scalp (%)',
                'Tài sản giao dịch chính',
                '',
                'PHONG CÁCH GIAO DỊCH:',
                'SCALP (< 1h) %',
                'INTRADAY (1-8h) %',
                'SWING (8h-7d) %',
                'POSITION (> 7d) %',
                '',
                'PHÂN BỔ TÀI SẢN TOP 3:',
                'Tài sản #1',
                '% Giao dịch #1',
                'Tài sản #2',
                '% Giao dịch #2',
                'Tài sản #3',
                '% Giao dịch #3'
            ],
            'Giá Trị': [
                metrics['total_trades'],
                metrics['win_rate'],
                metrics['profit_factor'],
                metrics['net_pnl'],
                metrics['total_lots'],
                metrics['avg_holding_hours'],
                metrics['scalp_ratio'],
                metrics['dominant_asset'],
                '',
                '',
                metrics['trading_style']['scalp'],
                metrics['trading_style']['intraday'],
                metrics['trading_style']['swing'],
                metrics['trading_style']['position'],
                '',
                '',
                metrics['asset_distribution'].get('asset1_symbol', ''),
                metrics['asset_distribution'].get('asset1_pct', ''),
                metrics['asset_distribution'].get('asset2_symbol', ''),
                metrics['asset_distribution'].get('asset2_pct', ''),
                metrics['asset_distribution'].get('asset3_symbol', ''),
                metrics['asset_distribution'].get('asset3_pct', '')
            ]
        }
        
        df_export = pd.DataFrame(data)
        
        # Export to Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_export.to_excel(writer, sheet_name='Metrics Summary', index=False)
        
        print(f"\n✅ Đã xuất kết quả ra file: {output_path}")
        
    except Exception as e:
        print(f"\n⚠️ Không thể xuất Excel (có thể thiếu thư viện openpyxl): {str(e)}")

def print_metrics(metrics):
    """Hiển thị metrics trên console"""
    print("\n" + "="*60)
    print("📊 KẾT QUẢ TÍNH TOÁN METRICS")
    print("="*60)
    
    print(f"\n🔢 Tổng số giao dịch: {metrics['total_trades']}")
    print(f"🎯 Tỷ lệ thắng: {metrics['win_rate']:.1f}%")
    print(f"💰 Profit Factor: {metrics['profit_factor']:.2f}")
    print(f"💵 Net PnL: ${metrics['net_pnl']:.2f}")
    print(f"📦 Tổng khối lượng: {metrics['total_lots']:.2f} lots")
    print(f"⏰ Thời gian nắm giữ TB: {metrics['avg_holding_hours']:.1f} giờ")
    print(f"⚡ Tỷ lệ Scalp: {metrics['scalp_ratio']:.1f}%")
    print(f"🏆 Tài sản chính: {metrics['dominant_asset']}")
    
    print(f"\n🎭 PHONG CÁCH GIAO DỊCH:")
    print(f"   ⚡ SCALP (< 1h): {metrics['trading_style']['scalp']:.1f}%")
    print(f"   📊 INTRADAY (1-8h): {metrics['trading_style']['intraday']:.1f}%")
    print(f"   📈 SWING (8h-7d): {metrics['trading_style']['swing']:.1f}%")
    print(f"   📉 POSITION (> 7d): {metrics['trading_style']['position']:.1f}%")
    
    print(f"\n📊 PHÂN BỔ TÀI SẢN TOP 3:")
    for i in range(1, 4):
        symbol = metrics['asset_distribution'].get(f'asset{i}_symbol', 'N/A')
        pct = metrics['asset_distribution'].get(f'asset{i}_pct', 0)
        if symbol != 'N/A':
            print(f"   {i}. {symbol}: {pct:.1f}%")
    
    print("\n" + "="*60)
    print("💡 Copy các giá trị trên vào form Agent Jill")
    print("="*60 + "\n")

# === MAIN FUNCTION ===

def main():
    print("="*60)
    print("📊 TRADING METRICS CALCULATOR")
    print("="*60)
    
    # Get folder path
    if len(sys.argv) > 1:
        csv_folder = sys.argv[1]
    else:
        csv_folder = input(f"\nNhập đường dẫn folder chứa CSV\n(Enter để dùng mặc định: {DEFAULT_CSV_FOLDER}): ").strip()
        if not csv_folder:
            csv_folder = DEFAULT_CSV_FOLDER
    
    print(f"\n🔍 Đang tìm file CSV trong: {csv_folder}")
    
    # Find CSV files
    csv_files = find_csv_files(csv_folder)
    
    if not csv_files:
        print(f"❌ Không tìm thấy file CSV nào trong thư mục")
        return
    
    print(f"\n✅ Tìm thấy {len(csv_files)} file CSV:")
    for i, f in enumerate(csv_files, 1):
        print(f"   {i}. {f.name}")
    
    # Process first CSV file (can be extended to process multiple)
    if len(csv_files) > 1:
        choice = input(f"\nNhập số thứ tự file cần xử lý (1-{len(csv_files)}) hoặc Enter để chọn file đầu tiên: ").strip()
        try:
            file_index = int(choice) - 1 if choice else 0
            if file_index < 0 or file_index >= len(csv_files):
                file_index = 0
        except:
            file_index = 0
    else:
        file_index = 0
    
    csv_file = csv_files[file_index]
    
    # Load and process
    df = load_and_process_csv(csv_file)
    
    if df is None:
        print("\n❌ Không thể xử lý file CSV")
        return
    
    # Calculate metrics
    print("\n⚙️ Đang tính toán metrics...")
    metrics = calculate_metrics(df)
    
    if metrics is None:
        print("\n❌ Không thể tính toán metrics")
        return
    
    # Display results
    print_metrics(metrics)
    
    # Export to Excel
    output_file = Path(csv_folder) / OUTPUT_EXCEL_NAME
    export_to_excel(metrics, output_file)
    
    print("\n✅ Hoàn tất!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Đã hủy bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {str(e)}")
        import traceback
        traceback.print_exc()
