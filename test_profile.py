#!/usr/bin/env python3
"""
Test script để kiểm tra profile function của Jill AI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import JillAI

def test_jill_profile():
    """Test profile function của Jill"""
    
    print("🧪 Testing Jill Profile Function...")
    print("=" * 50)
    
    # Khởi tạo Jill AI
    jill = JillAI()
    
    # Test get_profile function
    print("\n📋 Testing get_profile():")
    print("-" * 30)
    
    try:
        profile = jill.get_profile()
        print("✅ Profile function works!")
        print(f"📄 Profile length: {len(profile)} characters")
        print(f"🔍 Contains image tag: {'<img' in profile}")
        print(f"🔍 Contains markdown headers: {'##' in profile}")
        print(f"🔍 Contains table: {'|' in profile}")
        
        # Hiển thị một phần profile
        print("\n📖 Preview of profile (first 300 chars):")
        print("-" * 50)
        print(profile[:300] + "...")
        
    except Exception as e:
        print(f"❌ Error testing profile: {e}")
    
    # Test chat response với profile keywords
    print("\n\n💬 Testing chat response with profile keywords:")
    print("-" * 50)
    
    test_questions = [
        "Jill là ai?",
        "Giới thiệu về bạn",
        "Profile của em",
        "Em là ai?",
        "Thông tin về Jill"
    ]
    
    for question in test_questions:
        try:
            print(f"\n🤔 Question: {question}")
            response = jill.ai_chat_response(question)
            
            # Kiểm tra xem có trả về profile không
            if "Profile - AI Agent Jill" in response:
                print("✅ Correctly returned profile!")
            elif len(response) > 1000:  # Profile thường dài
                print("✅ Returned long response (likely profile)")
            else:
                print("⚠️ Response might not be profile")
                print(f"📏 Response length: {len(response)}")
                
        except Exception as e:
            print(f"❌ Error with question '{question}': {e}")
    
    print("\n" + "=" * 50)
    print("✅ Profile testing completed!")

if __name__ == "__main__":
    test_jill_profile()