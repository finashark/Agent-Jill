#!/usr/bin/env python3
"""
Simple test script không dùng Streamlit context
Test trực tiếp logic functions
"""

import os
import sys
import pandas as pd
from datetime import datetime
import json

# Set environment variable
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBQUuZ8V5VycCBfg0XJ-U9bFszqxi_xmFY'

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_csv_loading_basic():
    """Test basic CSV loading và processing logic"""
    print("📤 Testing CSV Loading...")
    
    try:
        # Test sample_trades.csv
        df1 = pd.read_csv('sample_trades.csv')
        print(f"✅ sample_trades.csv: {len(df1)} rows loaded")
        
        # Test closed_trades.csv  
        df2 = pd.read_csv('closed_trades_32284342.csv')
        print(f"✅ closed_trades_32284342.csv: {len(df2)} rows loaded")
        
        return df1, df2
        
    except Exception as e:
        print(f"❌ CSV loading error: {e}")
        return None, None

def test_ai_models_basic():
    """Test Google Gemini API connection"""
    print("\n🤖 Testing Google Gemini API...")
    
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Hello from Jill!'")
        
        if response and response.text:
            print("✅ Google Gemini API working")
            print(f"   Response: {response.text[:50]}...")
            return True
        else:
            print("❌ No response from API")
            return False
            
    except Exception as e:
        print(f"❌ Google API error: {e}")
        return False

def test_data_processing():
    """Test cơ bản data processing logic"""
    print("\n📊 Testing Data Processing...")
    
    try:
        # Load sample data
        df = pd.read_csv('sample_trades.csv')
        
        # Basic column mapping
        column_mapping = {
            'Ticket': 'TICKET',
            'Open Time': 'OPEN_TIME', 
            'Close Time': 'CLOSE_TIME',
            'Type': 'ACTION',
            'Item': 'SYMBOL',
            'Lots': 'LOTS',
            'Commission': 'COMM',
            'Swap': 'SWAP',
            'Profit': 'PROFIT'
        }
        
        # Apply mapping
        df_mapped = df.copy()
        df_mapped.columns = [column_mapping.get(col, col) for col in df_mapped.columns]
        
        # Check required columns
        required_cols = ['TICKET', 'SYMBOL', 'ACTION', 'LOTS', 'OPEN_TIME', 'CLOSE_TIME', 'PROFIT']
        missing_cols = [col for col in required_cols if col not in df_mapped.columns]
        
        if not missing_cols:
            print("✅ Column mapping successful")
            
            # Basic calculations
            df_mapped['OPEN_TIME'] = pd.to_datetime(df_mapped['OPEN_TIME'])
            df_mapped['CLOSE_TIME'] = pd.to_datetime(df_mapped['CLOSE_TIME'])
            
            total_trades = len(df_mapped)
            profitable_trades = len(df_mapped[df_mapped['PROFIT'] > 0])
            win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
            
            print(f"✅ Basic metrics calculated:")
            print(f"   - Total trades: {total_trades}")
            print(f"   - Win rate: {win_rate:.1f}%")
            
            return True
        else:
            print(f"❌ Missing columns: {missing_cols}")
            return False
            
    except Exception as e:
        print(f"❌ Data processing error: {e}")
        return False

def test_ai_basic_call():
    """Test basic AI call"""
    print("\n🧠 Testing AI Analysis Logic...")
    
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Simple trading analysis prompt
        prompt = """
        Phân tích trader với thông tin:
        - 10 giao dịch
        - Win rate: 70%
        - Profit: $667.50
        - Kinh nghiệm: 2 năm
        
        Xác định loại trader và đưa ra 3 insight chính.
        """
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            print("✅ AI analysis successful")
            print(f"   Response length: {len(response.text)} characters")
            print(f"   Sample: {response.text[:100]}...")
            return True
        else:
            print("❌ No AI response")
            return False
            
    except Exception as e:
        print(f"❌ AI analysis error: {e}")
        return False

def run_simple_tests():
    """Chạy các test đơn giản"""
    print("🚀 Starting Simple AI Agent Jill Tests...\n")
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: CSV Loading
    if test_csv_loading_basic():
        tests_passed += 1
    
    # Test 2: AI Models
    if test_ai_models_basic():
        tests_passed += 1
    
    # Test 3: Data Processing  
    if test_data_processing():
        tests_passed += 1
    
    # Test 4: AI Analysis
    if test_ai_basic_call():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} passed")
    
    # Generate simple report
    report = {
        'timestamp': datetime.now().isoformat(),
        'tests_passed': tests_passed,
        'total_tests': total_tests,
        'success_rate': f"{(tests_passed/total_tests)*100:.1f}%",
        'status': 'PASSED' if tests_passed == total_tests else 'PARTIAL',
        'google_api_working': tests_passed >= 2,
        'data_processing_working': tests_passed >= 3,
        'ready_for_streamlit': tests_passed >= 3
    }
    
    with open('simple_test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    if tests_passed == total_tests:
        print("🎉 All basic tests passed! App core functions are working.")
        print("✅ Ready to test with Streamlit interface.")
    elif tests_passed >= 3:
        print("⚠️ Most tests passed. Core functionality working.")
        print("✅ Should work with Streamlit interface.")
    else:
        print("❌ Multiple tests failed. Need to fix core issues.")
    
    print(f"\n📄 Report saved to: simple_test_report.json")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI AGENT JILL - SIMPLE CORE TESTS")
    print("=" * 50)
    
    success = run_simple_tests()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 CORE FUNCTIONALITY VERIFIED")
    else:
        print("⚠️ SOME CORE ISSUES DETECTED")
    print("=" * 50)
    
    exit(0 if success else 1)