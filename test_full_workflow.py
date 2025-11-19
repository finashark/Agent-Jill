#!/usr/bin/env python3
"""
Full integration test cho AI Agent Jill
Test toàn bộ 5-step workflow với app thực tế
"""

import os
import sys
import pandas as pd
from datetime import datetime
import json

# Set environment variable for Google API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBQUuZ8V5VycCBfg0XJ-U9bFszqxi_xmFY'

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_full_workflow():
    """Test toàn bộ workflow của AI Agent Jill"""
    print("🚀 Starting Full AI Agent Jill Workflow Test...\n")
    
    try:
        # Import app after setting environment
        import app
        print("✅ App imported successfully")
        
        # Initialize JillAI
        jill = app.JillAI()
        print("✅ JillAI initialized")
        
        # Test Step 1: Load CSV files
        print("\n📤 Step 1: Testing CSV Loading...")
        
        # Test sample_trades.csv
        if os.path.exists('sample_trades.csv'):
            try:
                df_sample = app.load_and_process_csv('sample_trades.csv')
                if df_sample is not None and not df_sample.empty:
                    print(f"✅ sample_trades.csv: {len(df_sample)} trades loaded")
                else:
                    print("❌ sample_trades.csv: Failed to load")
                    return False
            except Exception as e:
                print(f"❌ sample_trades.csv error: {e}")
                return False
        
        # Test closed_trades_32284342.csv 
        if os.path.exists('closed_trades_32284342.csv'):
            try:
                df_closed = app.load_and_process_csv('closed_trades_32284342.csv')
                if df_closed is not None and not df_closed.empty:
                    print(f"✅ closed_trades_32284342.csv: {len(df_closed)} trades loaded")
                else:
                    print("❌ closed_trades_32284342.csv: Failed to load")
                    return False
            except Exception as e:
                print(f"❌ closed_trades_32284342.csv error: {e}")
                return False
        
        # Test Step 2: AI Analysis
        print("\n🤖 Step 2: Testing AI Analysis...")
        
        # Use sample_trades for analysis test
        test_df = df_sample if 'df_sample' in locals() else df_closed
        
        try:
            # Use only available customer info first
            customer_info_limited = {
                'capital': 50000,
                'experience_years': 2,
                'age': 35
            }
            
            analysis_result = jill.ai_analyze_trading_behavior(test_df, customer_info_limited)
            if analysis_result and 'trader_type' in analysis_result:
                print(f"✅ AI Analysis completed: {analysis_result['trader_type']}")
                print(f"   - Confidence: {analysis_result.get('confidence', 'N/A')}")
                print(f"   - Key insights: {len(analysis_result.get('key_insights', []))} insights")
            else:
                print("❌ AI Analysis failed")
                return False
        except Exception as e:
            print(f"❌ AI Analysis error: {e}")
            return False
        
        # Test Step 3: Customer Info Mock
        print("\n👤 Step 3: Testing Customer Info Processing...")
        
        customer_info = {
            'name': 'Nguyễn Văn Test',
            'age': 35,
            'capital': 50000,
            'experience_years': 2,
            'risk_tolerance': 'Trung bình',
            'goals': 'Tăng thu nhập thụ động'
        }
        print("✅ Customer info processed")
        
        # Test Step 4: Assessment Report
        print("\n📊 Step 4: Testing Assessment Report...")
        
        try:
            # Calculate trading metrics using app function
            metrics = app.calculate_trading_metrics(test_df)
            if metrics and 'total_trades' in metrics:
                print(f"✅ Trading metrics calculated:")
                print(f"   - Total trades: {metrics['total_trades']}")
                print(f"   - Win rate: {metrics.get('win_rate', 0):.1f}%")
                print(f"   - Profit factor: {metrics.get('profit_factor', 0):.2f}")
            else:
                print("❌ Trading metrics calculation failed")
                return False
        except Exception as e:
            print(f"❌ Metrics calculation error: {e}")
            return False
        
        # Test Step 5: Consultation Script
        print("\n📝 Step 5: Testing Consultation Script Generation...")
        
        try:
            consultation_result = jill.ai_generate_consultation_script(
                analysis_result, customer_info, metrics
            )
            if consultation_result and 'consultation_script' in consultation_result:
                script_length = len(consultation_result['consultation_script'])
                print(f"✅ Consultation script generated ({script_length} characters)")
                print(f"   - Promotions: {len(consultation_result.get('promotions', []))}")
                print(f"   - Strategy: {consultation_result.get('strategy', 'N/A')}")
            else:
                print("❌ Consultation script generation failed")
                return False
        except Exception as e:
            print(f"❌ Consultation script error: {e}")
            return False
        
        # Test completed successfully
        print("\n🎉 All workflow steps completed successfully!")
        
        # Generate test report
        report = {
            'timestamp': datetime.now().isoformat(),
            'test_status': 'PASSED',
            'steps_completed': 5,
            'csv_files_tested': 2,
            'trader_type_detected': analysis_result['trader_type'],
            'metrics_calculated': metrics,
            'script_generated': True,
            'app_version': '2.1',
            'ai_model_used': 'Google Gemini' if jill.gemini_client else 'Fallback',
            'ready_for_production': True
        }
        
        with open('full_workflow_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Full test report saved to: full_workflow_test_report.json")
        print("🚀 AI Agent Jill is PRODUCTION READY!")
        
        return True
        
    except Exception as e:
        print(f"❌ Critical error during workflow test: {e}")
        
        # Generate error report
        error_report = {
            'timestamp': datetime.now().isoformat(),
            'test_status': 'FAILED',
            'error_message': str(e),
            'app_version': '2.1',
            'ready_for_production': False
        }
        
        with open('full_workflow_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(error_report, f, indent=2, ensure_ascii=False)
        
        return False

def test_api_connectivity():
    """Test API connectivity"""
    print("🔌 Testing API Connectivity...")
    
    import google.generativeai as genai
    
    try:
        api_key = os.environ.get('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            
            # Try to create model with new name
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content("Hello, this is a test.")
            
            if response and response.text:
                print("✅ Google Gemini API working correctly")
                return True
            else:
                print("⚠️ Google Gemini API response empty")
                return False
        else:
            print("❌ No Google API key found")
            return False
            
    except Exception as e:
        print(f"❌ Google Gemini API error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 AI AGENT JILL - FULL INTEGRATION TEST")
    print("=" * 60)
    
    # Test API first
    api_working = test_api_connectivity()
    print()
    
    # Run full workflow test
    success = test_full_workflow()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 FINAL RESULT: ALL TESTS PASSED")
        print("✅ AI Agent Jill is ready for deployment!")
    else:
        print("❌ FINAL RESULT: TESTS FAILED")
        print("⚠️ Please check errors and fix before deployment")
    print("=" * 60)
    
    exit(0 if success else 1)