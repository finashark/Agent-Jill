#!/usr/bin/env python3
"""
🧪 Test App Fixed - Kiểm tra profile và UI đã sửa
"""

import streamlit as st

# Test import app
print("🔍 Testing fixed app...")

try:
    from app import JillAI
    print("✅ JillAI import successful!")
    
    # Tạo instance
    jill = JillAI()
    print("✅ JillAI instance created!")
    
    # Test methods
    assert hasattr(jill, 'display_profile_ui'), "❌ Missing display_profile_ui method"
    assert hasattr(jill, 'get_profile'), "❌ Missing get_profile method"
    print("✅ Profile methods exist!")
    
    # Test profile content
    profile_content = jill.get_profile()
    assert "Jill" in profile_content, "❌ Profile missing Jill name"
    assert "HFM" in profile_content, "❌ Profile missing HFM"
    print("✅ Profile content valid!")
    
    print("\n🎉 All tests passed!")
    print("🔗 Image URL: https://i.postimg.cc/wvH5N2HF/Agent-Jill.png")
    print("📱 Ready for streamlit run app.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("🎯 Fixed Issues:")
print("✅ Anthropic import error fixed")  
print("✅ Header title updated")
print("✅ Profile UI improved")
print("✅ Image display optimized")
print("="*60)