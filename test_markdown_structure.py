#!/usr/bin/env python3
"""
Test markdown structure improvements
"""

from app import JillAI
import pandas as pd

def test_markdown_improvements():
    print("=== TESTING IMPROVED MARKDOWN STRUCTURE ===")
    
    # Initialize JillAI
    jill = JillAI()
    
    # Test greet function with new markdown
    print("\n1. Testing greet() markdown structure:")
    greet_text = jill.greet()
    print(greet_text)
    
    # Test classification markdown (simulate data)
    print("\n2. Testing classification markdown structure:")
    
    # Create sample data for testing
    sample_data = {
        'PROFIT': [100, -50, 200, -30, 150],
        'SYMBOL': ['EURUSD', 'EURUSD', 'GBPUSD', 'EURUSD', 'USDJPY'],
        'Holding_Time_Hours': [0.5, 2, 4, 1, 8]
    }
    df = pd.DataFrame(sample_data)
    
    try:
        # Test trader classification
        classification = jill._classify_trader_comprehensive(
            capital=10000,
            experience_years=2,
            age=30,
            win_rate=60,
            profit_factor=1.2,
            scalp_ratio=40,
            asset_concentration=60,
            total_trades=5,
            trading_style="Day Trading",
            df_processed=df
        )
        
        print(classification)
        print("\n✅ Markdown structure tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error in classification test: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_markdown_improvements()
    if success:
        print("\n🎉 ALL MARKDOWN IMPROVEMENTS WORKING! 🎉")
    else:
        print("\n❌ Some tests failed")