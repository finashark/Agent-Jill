#!/usr/bin/env python3
"""
Test cụ thể cho BƯỚC 4: Báo Cáo Nhận Định Hành Vi
Tìm và fix lỗi total_trades
"""

import os
import sys
import pandas as pd
from datetime import datetime
import traceback

# Set environment variable
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBQUuZ8V5VycCBfg0XJ-U9bFszqxi_xmFY'

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_step4_detailed():
    """Test chi tiết bước 4"""
    print("🔍 Testing BƯỚC 4: Báo Cáo Nhận Định Hành Vi\n")
    
    try:
        # Import app
        import app
        print("✅ App imported")
        
        # Load và process CSV
        df = pd.read_csv('sample_trades.csv')
        print(f"✅ Raw CSV loaded: {len(df)} rows")
        
        # Apply column standardization like in app
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
        
        df_processed = df.copy()
        df_processed.columns = [column_mapping.get(col, col) for col in df_processed.columns]
        print(f"✅ Columns standardized: {list(df_processed.columns)}")
        
        # Initialize Jill
        jill = app.JillAI()
        print("✅ JillAI initialized")
        
        # Test _calculate_trading_metrics function
        print("\n📊 Testing _calculate_trading_metrics...")
        try:
            metrics = jill._calculate_trading_metrics(df_processed)
            print("✅ _calculate_trading_metrics SUCCESS")
            print(f"   Metrics keys: {list(metrics.keys())}")
            if 'total_trades' in metrics:
                print(f"   total_trades: {metrics['total_trades']}")
            else:
                print("❌ total_trades missing in metrics!")
                
        except Exception as e:
            print(f"❌ _calculate_trading_metrics ERROR: {e}")
            print("Traceback:")
            traceback.print_exc()
            return False
        
        # Test customer info mock
        customer_info = {
            'capital': 50000,
            'experience_years': 2,
            'age': 35,
            'name': 'Test User'
        }
        print("\n👤 Customer info prepared")
        
        # Test analyze_trading_behavior function (bước 4 chính)
        print("\n🧠 Testing analyze_trading_behavior (Main Step 4)...")
        try:
            print("   Debug: About to call analyze_trading_behavior...")
            print(f"   Debug: df_processed shape: {df_processed.shape}")
            print(f"   Debug: df_processed columns: {list(df_processed.columns)}")
            analysis_result = jill.analyze_trading_behavior(df_processed, customer_info)
            
            if 'error' in analysis_result:
                print(f"❌ analyze_trading_behavior ERROR: {analysis_result['error']}")
                return False
            else:
                print("✅ analyze_trading_behavior SUCCESS")
                print(f"   Result keys: {list(analysis_result.keys())}")
                
                # Check metrics specifically
                if 'metrics' in analysis_result:
                    metrics = analysis_result['metrics']
                    print(f"   Metrics keys: {list(metrics.keys())}")
                    if 'total_trades' in metrics:
                        print(f"   ✅ total_trades found: {metrics['total_trades']}")
                    else:
                        print("   ❌ total_trades missing in metrics!")
                        return False
                else:
                    print("   ❌ metrics missing in analysis_result!")
                    return False
                    
        except Exception as e:
            print(f"❌ analyze_trading_behavior ERROR: {e}")
            print("Traceback:")
            traceback.print_exc()
            return False
        
        # Test accessing the specific fields that step 4 uses
        print("\n📋 Testing Step 4 field access...")
        try:
            trader_type = analysis_result['trader_type']
            metrics = analysis_result['metrics']
            
            # These are the fields that step 4 tries to access
            fields_to_check = [
                'total_trades', 'win_rate', 'profit_factor', 
                'avg_holding_hours', 'net_pnl', 'total_lots'
            ]
            
            for field in fields_to_check:
                if field in metrics:
                    print(f"   ✅ {field}: {metrics[field]}")
                else:
                    print(f"   ❌ {field}: MISSING")
                    
            # Check trading_style
            if 'trading_style' in analysis_result:
                trading_style = analysis_result['trading_style']
                print(f"   ✅ trading_style: {trading_style}")
            else:
                print(f"   ❌ trading_style: MISSING")
                
        except Exception as e:
            print(f"❌ Field access ERROR: {e}")
            return False
        
        print("\n🎉 BƯỚC 4 test hoàn toàn thành công!")
        return True
        
    except Exception as e:
        print(f"❌ Critical error in step 4 test: {e}")
        print("Traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 AI AGENT JILL - BƯỚC 4 DETAILED TEST")
    print("=" * 60)
    
    success = test_step4_detailed()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 BƯỚC 4 WORKING PERFECTLY!")
        print("✅ Lỗi total_trades đã được fix hoàn toàn!")
    else:
        print("❌ BƯỚC 4 STILL HAS ISSUES")
        print("⚠️ Cần fix thêm các lỗi được phát hiện")
    print("=" * 60)
    
    exit(0 if success else 1)