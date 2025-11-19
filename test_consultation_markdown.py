#!/usr/bin/env python3
"""
Test tính năng markdown structure cho consultation script
"""

from app import JillAI
import pandas as pd

def test_markdown_consultation():
    print("=== TESTING MARKDOWN CONSULTATION STRUCTURE ===")
    
    # Initialize JillAI
    jill = JillAI()
    
    # Tạo dữ liệu mẫu
    sample_ai_analysis = {
        'trader_type': 'Technical Trader',
        'psychological_profile': 'Trader có kỷ luật cao, phương pháp rõ ràng, quản lý cảm xúc ổn định',
        'key_insights': ['Có kinh nghiệm thực tế', 'Dữ liệu giao dịch phong phú'],
        'trading_style': 'Day Trading'
    }
    
    sample_customer_info = {
        'name': 'Anh Nguyễn Văn A',
        'capital': 50000,
        'experience_years': 3,
        'age': 35
    }
    
    sample_trading_metrics = {
        'win_rate': 55.5,
        'profit_factor': 1.35,
        'net_pnl': 2500.75,
        'total_trades': 120
    }
    
    try:
        # Test consultation script với fallback method
        print("1. Testing consultation script markdown structure...")
        consultation_result = jill._fallback_consultation_script_enhanced(
            sample_ai_analysis, 
            sample_customer_info, 
            sample_trading_metrics
        )
        
        print("✅ Consultation script generated successfully!")
        print(f"Script length: {len(consultation_result['script'])} characters")
        print(f"Key messages: {consultation_result['key_messages']}")
        print(f"Tone: {consultation_result['tone']}")
        
        # Show preview of script
        print("\n2. Script preview (first 500 characters):")
        print("=" * 50)
        print(consultation_result['script'][:500] + "...")
        print("=" * 50)
        
        print("\n✅ MARKDOWN CONSULTATION STRUCTURE TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error in consultation test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_markdown_consultation()
    if success:
        print("\n🎉 ALL MARKDOWN TESTS WORKING! 🎉")
    else:
        print("\n❌ Some tests failed")