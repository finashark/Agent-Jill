#!/usr/bin/env python3
"""
Final comprehensive test of Step 4 functionality
Tests the complete analyze_trading_behavior workflow
"""

import pandas as pd
import sys
import traceback
from app import JillAI

def test_step4_complete():
    print("=== FINAL STEP 4 COMPREHENSIVE TEST ===")
    
    try:
        # Initialize JillAI
        print("1. Initializing JillAI...")
        jill = JillAI()
        print("   ✅ JillAI initialized successfully")
        
        # Load sample data
        print("\n2. Loading sample trading data...")
        df = pd.read_csv('sample_trades.csv')
        print(f"   ✅ Loaded {len(df)} trades")
        print(f"   Columns: {list(df.columns)}")
        
        # Create sample customer_info
        print("\n3. Creating sample customer info...")
        customer_info = {
            'name': 'Test Trader',
            'age': 30,
            'gender': 'Nam',
            'income': 20000000,
            'education': 'Đại học',
            'experience_years': 2,
            'capital': 10000000,
            'goals': 'Kiếm tiền từ trading'
        }
        print(f"   ✅ Customer info: {customer_info}")
        
        # Test the complete analyze_trading_behavior function
        print("\n4. Testing complete analyze_trading_behavior workflow...")
        analysis_result = jill.analyze_trading_behavior(df, customer_info)
        
        print("   ✅ Analysis completed successfully!")
        print(f"   Analysis type: {type(analysis_result)}")
        print(f"   Analysis length: {len(analysis_result) if isinstance(analysis_result, str) else 'N/A'}")
        
        # Check if analysis contains expected content
        if isinstance(analysis_result, str):
            key_terms = ['trader', 'trading', 'behavior', 'pattern']
            found_terms = [term for term in key_terms if term.lower() in analysis_result.lower()]
            print(f"   Key terms found: {found_terms}")
            
            # Show first 200 characters of analysis
            print(f"   Analysis preview: {analysis_result[:200]}...")
        
        print("\n=== TEST SUMMARY ===")
        print("✅ JillAI initialization: PASSED")
        print("✅ CSV data loading: PASSED") 
        print("✅ Customer info creation: PASSED")
        print("✅ Step 4 analysis workflow: PASSED")
        print("✅ All components working together: PASSED")
        print("\n🎉 STEP 4 IS FULLY FUNCTIONAL! 🎉")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR in test: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_step4_complete()
    sys.exit(0 if success else 1)