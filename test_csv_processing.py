#!/usr/bin/env python3
"""
Test CSV processing với cả 2 file mẫu
Test cụ thể cho standardize_column_names function
"""

import pandas as pd
import numpy as np
import os

def standardize_column_names(df):
    """Copy của hàm từ app.py"""
    # Bản đồ chuyển đổi tên cột
    column_mapping = {
        # Standard format mapping
        'Ticket': 'TICKET',
        'Open Time': 'OPEN_TIME', 
        'Close Time': 'CLOSE_TIME',
        'Type': 'ACTION',
        'Item': 'SYMBOL',
        'Lots': 'LOTS',
        'Price': 'CLOSE_PRICE',
        'Commission': 'COMM',
        'Taxes': 'TAXES',
        'Swap': 'SWAP',
        'Profit': 'PROFIT',
        'Comment': 'COMMENT',
        
        # Alternative formats
        'OPEN TIME': 'OPEN_TIME',
        'CLOSE TIME': 'CLOSE_TIME',
        'ACTION': 'ACTION',
        'SYMBOL': 'SYMBOL',
        'OPEN PRICE': 'OPEN_PRICE',
        'CLOSE PRICE': 'CLOSE_PRICE',
        'T/P': 'TP',
        'S/L': 'SL',
        'S / L': 'SL',
        'T / P': 'TP'
    }
    
    # Tạo bản sao để không thay đổi DataFrame gốc
    df_processed = df.copy()
    
    # Thay đổi tên cột
    df_processed.columns = [column_mapping.get(col, col) for col in df_processed.columns]
    
    return df_processed

def classify_asset(symbol):
    """Copy của hàm từ app.py"""
    if pd.isna(symbol) or symbol == '':
        return 'Khác'
        
    symbol = str(symbol).upper().strip()
    
    # Remove common suffixes
    clean_symbol = symbol.rstrip('RM').rstrip('R').rstrip('M')
    
    # Forex pairs
    forex_currencies = ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'NZD', 'CHF', 'CAD']
    
    if len(clean_symbol) >= 6:
        for curr1 in forex_currencies:
            if clean_symbol.startswith(curr1):
                remaining = clean_symbol[len(curr1):]
                if remaining in forex_currencies:
                    return 'Forex'
    
    # Metals
    if any(metal in symbol for metal in ['XAU', 'XAG', 'GOLD', 'SILVER']):
        return 'Kim loại'
    
    # Crypto
    crypto_patterns = ['BTC', 'ETH', 'LTC', 'ADA', 'DOT', 'LINK']
    for crypto in crypto_patterns:
        if symbol.startswith(crypto) and 'USD' in symbol:
            return 'Crypto'
    
    # Indices
    if any(index in symbol for index in ['SPX', 'NAS', 'DAX', 'FTSE', 'NIKKEI', 'US30', 'US100']):
        return 'Chỉ số'
    
    return 'Khác'

def test_sample_trades_csv():
    """Test file sample_trades.csv"""
    print("🧪 Testing sample_trades.csv...")
    
    file_path = "sample_trades.csv"
    if not os.path.exists(file_path):
        print("❌ File not found")
        return False
    
    try:
        # Load CSV
        df = pd.read_csv(file_path)
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
        print(f"📋 Original columns: {list(df.columns)}")
        
        # Standardize columns
        df_std = standardize_column_names(df)
        print(f"📋 Standardized columns: {list(df_std.columns)}")
        
        # Check required columns
        required_cols = ['TICKET', 'SYMBOL', 'ACTION', 'LOTS', 'OPEN_TIME', 'CLOSE_TIME', 'PROFIT']
        missing_cols = [col for col in required_cols if col not in df_std.columns]
        
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
            return False
        else:
            print("✅ All required columns present")
        
        # Test date conversion
        df_std['OPEN_TIME'] = pd.to_datetime(df_std['OPEN_TIME'])
        df_std['CLOSE_TIME'] = pd.to_datetime(df_std['CLOSE_TIME'])
        print("✅ Date conversion successful")
        
        # Test asset classification
        if 'SYMBOL' in df_std.columns:
            df_std['Asset_Class'] = df_std['SYMBOL'].apply(classify_asset)
            asset_counts = df_std['Asset_Class'].value_counts()
            print(f"📊 Asset classes: {dict(asset_counts)}")
        
        # Test basic calculations
        if 'COMM' not in df_std.columns:
            df_std['COMM'] = 0.0
        if 'SWAP' not in df_std.columns:
            df_std['SWAP'] = 0.0
            
        df_std['Net_PnL'] = df_std['PROFIT'] + df_std['COMM'] + df_std['SWAP']
        df_std['Holding_Time_Hours'] = (df_std['CLOSE_TIME'] - df_std['OPEN_TIME']).dt.total_seconds() / 3600
        
        # Statistics
        total_trades = len(df_std)
        profitable_trades = len(df_std[df_std['Net_PnL'] > 0])
        win_rate = (profitable_trades / total_trades) * 100 if total_trades > 0 else 0
        total_profit = df_std['Net_PnL'].sum()
        
        print(f"📊 Statistics:")
        print(f"   - Total trades: {total_trades}")
        print(f"   - Profitable: {profitable_trades} ({win_rate:.1f}%)")
        print(f"   - Total P&L: ${total_profit:.2f}")
        print(f"   - Avg holding time: {df_std['Holding_Time_Hours'].mean():.1f} hours")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_closed_trades_csv():
    """Test file closed_trades_32284342.csv"""
    print("\n🧪 Testing closed_trades_32284342.csv...")
    
    file_path = "closed_trades_32284342.csv"
    if not os.path.exists(file_path):
        print("❌ File not found")
        return False
    
    try:
        # Load CSV
        df = pd.read_csv(file_path)
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
        print(f"📋 Original columns: {list(df.columns[:10])}...")  # Show first 10 columns
        
        # Remove empty rows
        df = df.dropna(subset=['TICKET'])
        print(f"✅ After removing empty rows: {len(df)} rows")
        
        # Filter out Balance entries
        if 'ACTION' in df.columns:
            df = df[df['ACTION'] != 'Balance']
            print(f"✅ After filtering balance entries: {len(df)} rows")
        
        # Standardize columns
        df_std = standardize_column_names(df)
        print(f"📋 Standardized columns: {list(df_std.columns[:10])}...")
        
        # Check required columns
        required_cols = ['TICKET', 'SYMBOL', 'ACTION', 'LOTS', 'OPEN_TIME', 'CLOSE_TIME', 'PROFIT']
        missing_cols = [col for col in required_cols if col not in df_std.columns]
        
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
            # Show available columns for debugging
            print(f"📋 Available columns: {list(df_std.columns)}")
            return False
        else:
            print("✅ All required columns present")
        
        # Test date conversion
        df_std['OPEN_TIME'] = pd.to_datetime(df_std['OPEN_TIME'])
        df_std['CLOSE_TIME'] = pd.to_datetime(df_std['CLOSE_TIME'])
        print("✅ Date conversion successful")
        
        # Clean numeric columns
        numeric_cols = ['PROFIT', 'COMM', 'SWAP', 'LOTS']
        for col in numeric_cols:
            if col in df_std.columns:
                df_std[col] = pd.to_numeric(df_std[col], errors='coerce').fillna(0)
        
        # Test asset classification
        if 'SYMBOL' in df_std.columns:
            # Handle empty symbols
            df_std = df_std[df_std['SYMBOL'].notna() & (df_std['SYMBOL'] != '')]
            print(f"✅ After removing empty symbols: {len(df_std)} rows")
            
            df_std['Asset_Class'] = df_std['SYMBOL'].apply(classify_asset)
            asset_counts = df_std['Asset_Class'].value_counts()
            print(f"📊 Asset classes: {dict(asset_counts)}")
        
        # Test basic calculations
        df_std['Net_PnL'] = df_std['PROFIT'] + df_std['COMM'] + df_std['SWAP']
        df_std['Holding_Time_Hours'] = (df_std['CLOSE_TIME'] - df_std['OPEN_TIME']).dt.total_seconds() / 3600
        
        # Statistics
        total_trades = len(df_std)
        profitable_trades = len(df_std[df_std['Net_PnL'] > 0])
        win_rate = (profitable_trades / total_trades) * 100 if total_trades > 0 else 0
        total_profit = df_std['Net_PnL'].sum()
        
        print(f"📊 Statistics:")
        print(f"   - Total trades: {total_trades}")
        print(f"   - Profitable: {profitable_trades} ({win_rate:.1f}%)")
        print(f"   - Total P&L: ${total_profit:.2f}")
        print(f"   - Avg holding time: {df_std['Holding_Time_Hours'].mean():.1f} hours")
        
        # Show sample symbols
        sample_symbols = df_std['SYMBOL'].unique()[:10]
        print(f"📋 Sample symbols: {list(sample_symbols)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_csv_tests():
    """Chạy tất cả CSV tests"""
    print("🚀 Starting CSV Processing Tests...\n")
    
    test1_passed = test_sample_trades_csv()
    test2_passed = test_closed_trades_csv()
    
    print("\n📊 CSV Test Results:")
    print(f"✅ sample_trades.csv: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ closed_trades_32284342.csv: {'PASSED' if test2_passed else 'FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All CSV tests passed! Both formats are supported.")
        return True
    else:
        print("\n⚠️ Some CSV tests failed. Please review the issues.")
        return False

if __name__ == "__main__":
    success = run_csv_tests()
    exit(0 if success else 1)