#!/usr/bin/env python
"""
Test method analyze_trading_behavior có tồn tại không
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_method_existence():
    """Test xem method có tồn tại không"""
    
    print("🔍 CHECKING METHOD EXISTENCE")
    print("=" * 50)
    
    try:
        # Import without running Streamlit
        import pandas as pd
        from datetime import datetime
        
        # Mock Streamlit để tránh lỗi
        class MockStreamlit:
            def warning(self, msg): print(f"WARNING: {msg}")
            def error(self, msg): print(f"ERROR: {msg}")
            def info(self, msg): print(f"INFO: {msg}")
            def success(self, msg): print(f"SUCCESS: {msg}")
            class sidebar:
                @staticmethod
                def warning(msg): print(f"SIDEBAR WARNING: {msg}")
                @staticmethod
                def error(msg): print(f"SIDEBAR ERROR: {msg}")
                @staticmethod
                def info(msg): print(f"SIDEBAR INFO: {msg}")
                @staticmethod
                def success(msg): print(f"SIDEBAR SUCCESS: {msg}")
        
        # Mock streamlit trong sys.modules
        import sys
        sys.modules['streamlit'] = MockStreamlit()
        
        # Import JillAI
        from app import JillAI
        
        # Create instance
        jill = JillAI()
        
        print("✅ JillAI imported successfully")
        
        # Check methods
        methods_to_check = [
            'analyze_trading_behavior',
            'ai_analyze_trading_behavior', 
            'greet',
            '_fallback_consultation_script_enhanced',
            '_classify_trader_comprehensive'
        ]
        
        print("\n🔍 CHECKING METHODS:")
        print("-" * 30)
        
        for method_name in methods_to_check:
            if hasattr(jill, method_name):
                method = getattr(jill, method_name)
                if callable(method):
                    print(f"✅ {method_name} - EXISTS & CALLABLE")
                else:
                    print(f"⚠️ {method_name} - EXISTS but NOT CALLABLE")
            else:
                print(f"❌ {method_name} - MISSING")
        
        print("\n🎯 METHOD SIGNATURES:")
        print("-" * 30)
        
        if hasattr(jill, 'analyze_trading_behavior'):
            import inspect
            sig = inspect.signature(jill.analyze_trading_behavior)
            print(f"analyze_trading_behavior{sig}")
        
        print("\n✅ ALL CHECKS COMPLETED")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_method_existence()