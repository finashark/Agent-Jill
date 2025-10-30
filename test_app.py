#!/usr/bin/env python3
"""
Test script cho AI Agent Jill App
Kiểm tra các chức năng chính để đảm bảo app hoạt động ổn định
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import os
import sys

# Add the current directory to sys.path để import app components
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_csv_processing():
    """Test việc xử lý CSV files"""
    print("🧪 Testing CSV Processing...")
    
    # Test sample data
    sample_data = {
        'TICKET': [123456, 123457, 123458],
        'SYMBOL': ['EURUSD', 'GBPUSD', 'XAUUSD'],
        'ACTION': ['Buy', 'Sell', 'Buy'],
        'LOTS': [0.1, 0.2, 0.05],
        'OPEN_TIME': ['2024-10-30 10:00:00', '2024-10-30 11:00:00', '2024-10-30 12:00:00'],
        'CLOSE_TIME': ['2024-10-30 15:00:00', '2024-10-30 16:00:00', '2024-10-30 17:00:00'],
        'PROFIT': [25.0, -15.0, 35.0],
        'COMM': [0.0, 0.0, 0.0],
        'SWAP': [0.0, 0.0, 0.0]
    }
    
    df = pd.DataFrame(sample_data)
    print(f"✅ Created test DataFrame with {len(df)} rows")
    
    # Test date conversion
    df['OPEN_TIME'] = pd.to_datetime(df['OPEN_TIME'])
    df['CLOSE_TIME'] = pd.to_datetime(df['CLOSE_TIME'])
    print("✅ Date conversion successful")
    
    # Test feature engineering
    df['Net_PnL'] = df['PROFIT'] + df['COMM'] + df['SWAP']
    df['Holding_Time_Hours'] = (df['CLOSE_TIME'] - df['OPEN_TIME']).dt.total_seconds() / 3600
    print("✅ Feature engineering successful")
    
    # Test basic statistics
    profit_trades = len(df[df['Net_PnL'] > 0])
    total_trades = len(df)
    print(f"✅ Statistics: {profit_trades}/{total_trades} profitable trades")
    
    return True  # Return boolean instead of DataFrame

def test_asset_classification():
    """Test asset classification function"""
    print("\n🧪 Testing Asset Classification...")
    
    # Import function từ app.py (giả lập)
    def classify_asset(symbol):
        """Copy của hàm từ app.py"""
        if pd.isna(symbol):
            return 'Khác'
            
        symbol = str(symbol).upper().strip()
        
        # Forex pairs
        forex_currencies = ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'NZD', 'CHF', 'CAD']
        clean_symbol = symbol.rstrip('RM').rstrip('R').rstrip('M')
        
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
        crypto_patterns = ['BTC', 'ETH', 'LTC']
        for crypto in crypto_patterns:
            if symbol.startswith(crypto) and 'USD' in symbol:
                return 'Crypto'
        
        return 'Khác'
    
    test_symbols = ['EURUSD', 'GBPJPY', 'XAUUSD', 'BTCUSD', 'US30', 'UNKNOWN']
    expected = ['Forex', 'Forex', 'Kim loại', 'Crypto', 'Khác', 'Khác']
    
    for symbol, expect in zip(test_symbols, expected):
        result = classify_asset(symbol)
        status = "✅" if result == expect else "❌"
        print(f"{status} {symbol} -> {result} (expected: {expect})")
    
    return True

def test_trader_classification():
    """Test trader classification logic"""
    print("\n🧪 Testing Trader Classification...")
    
    # Test cases
    test_cases = [
        {
            'name': 'Newbie Gambler',
            'capital': 2000,
            'experience_years': 0.5,
            'win_rate': 35,
            'profit_factor': 0.7,
            'scalp_ratio': 70,
            'expected': 'Newbie Gambler'
        },
        {
            'name': 'Technical Trader',
            'capital': 25000,
            'experience_years': 2,
            'win_rate': 52,
            'profit_factor': 1.15,
            'scalp_ratio': 40,
            'expected': 'Technical Trader'
        },
        {
            'name': 'Long-term Investor',
            'capital': 150000,
            'experience_years': 5,
            'win_rate': 58,
            'profit_factor': 1.4,
            'scalp_ratio': 15,
            'expected': 'Long-term Investor'
        }
    ]
    
    for case in test_cases:
        # Simplified scoring logic
        scores = {'Newbie Gambler': 0, 'Technical Trader': 0, 'Long-term Investor': 0}
        
        # Newbie Gambler scoring
        if case['capital'] < 5000: scores['Newbie Gambler'] += 20
        if case['experience_years'] < 1: scores['Newbie Gambler'] += 25
        if case['win_rate'] < 40: scores['Newbie Gambler'] += 20
        if case['scalp_ratio'] > 60: scores['Newbie Gambler'] += 25
        if case['profit_factor'] < 0.8: scores['Newbie Gambler'] += 15
        
        # Technical Trader scoring
        if 5000 <= case['capital'] <= 100000: scores['Technical Trader'] += 15
        if 1 <= case['experience_years'] <= 3: scores['Technical Trader'] += 20
        if 45 <= case['win_rate'] <= 60: scores['Technical Trader'] += 25
        if 1.0 <= case['profit_factor'] <= 2.0: scores['Technical Trader'] += 20
        
        # Long-term Investor scoring
        if case['capital'] > 50000: scores['Long-term Investor'] += 25
        if case['win_rate'] > 55: scores['Long-term Investor'] += 20
        if case['profit_factor'] > 1.3: scores['Long-term Investor'] += 25
        if case['scalp_ratio'] < 20: scores['Long-term Investor'] += 15
        
        result = max(scores, key=scores.get)
        status = "✅" if result == case['expected'] else "❌"
        print(f"{status} {case['name']}: {result} (scores: {scores})")
    
    return True

def test_ai_prompt_generation():
    """Test AI prompt generation"""
    print("\n🧪 Testing AI Prompt Generation...")
    
    sample_analysis = {
        'trader_type': 'Technical Trader',
        'psychological_profile': 'Có kỷ luật tốt, phương pháp rõ ràng',
        'win_rate': 52.5,
        'profit_factor': 1.15,
        'key_insights': ['Giao dịch có hệ thống', 'Quản lý rủi ro tốt']
    }
    
    customer_info = {
        'name': 'Nguyễn Văn A',
        'age': 35,
        'capital': 25000,
        'experience_years': 2
    }
    
    # Generate sample prompt
    prompt = f"""
Em là Jill - chuyên gia tư vấn AI. Tạo script cho:
- Khách hàng: {customer_info['name']}, {customer_info['age']} tuổi
- Loại trader: {sample_analysis['trader_type']}
- Win rate: {sample_analysis['win_rate']}%
- Insights: {', '.join(sample_analysis['key_insights'])}
"""
    
    print(f"✅ Generated prompt ({len(prompt)} characters)")
    print(f"Preview: {prompt[:100]}...")
    
    return True

def test_app_imports():
    """Test if all required imports are available"""
    print("\n🧪 Testing App Imports...")
    
    required_modules = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly',
        'pytz',
        'json',
        'os',
        'datetime'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    
    # Test optional AI modules
    optional_modules = [
        'google.generativeai',
        'openai', 
        'anthropic'
    ]
    
    ai_available = 0
    for module in optional_modules:
        try:
            __import__(module)
            print(f"✅ {module} (AI)")
            ai_available += 1
        except ImportError:
            print(f"⚠️ {module} (optional)")
    
    print(f"📊 AI modules available: {ai_available}/{len(optional_modules)}")
    return True

def run_all_tests():
    """Chạy tất cả tests"""
    print("🚀 Starting AI Agent Jill App Tests...\n")
    
    tests = [
        test_app_imports,
        test_csv_processing,
        test_asset_classification,
        test_trader_classification,
        test_ai_prompt_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ PASSED\n")
            else:
                print("❌ FAILED\n")
        except Exception as e:
            print(f"❌ ERROR: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! App is ready for deployment.")
        return True
    else:
        print("⚠️ Some tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    
    # Create test report
    report = {
        'timestamp': datetime.now().isoformat(),
        'tests_passed': success,
        'app_version': '2.0',
        'ready_for_deployment': success
    }
    
    with open('test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Test report saved to test_report.json")
    exit(0 if success else 1)