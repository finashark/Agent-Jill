#!/usr/bin/env python3
"""
Test script để kiểm tra tất cả imports cho AI Agent Jill
"""

print("🧪 Testing imports for AI Agent Jill...")

try:
    import streamlit as st
    print("✅ Streamlit - OK")
except ImportError as e:
    print(f"❌ Streamlit - Error: {e}")

try:
    import pandas as pd
    print("✅ Pandas - OK") 
except ImportError as e:
    print(f"❌ Pandas - Error: {e}")

try:
    import numpy as np
    print("✅ Numpy - OK")
except ImportError as e:
    print(f"❌ Numpy - Error: {e}")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    print("✅ Plotly - OK")
except ImportError as e:
    print(f"❌ Plotly - Error: {e}")

try:
    import json
    print("✅ JSON - OK")
except ImportError as e:
    print(f"❌ JSON - Error: {e}")

try:
    import datetime
    print("✅ Datetime - OK")
except ImportError as e:
    print(f"❌ Datetime - Error: {e}")

# Test AI SDK imports
try:
    import openai
    print("✅ OpenAI - OK")
except ImportError as e:
    print(f"❌ OpenAI - Error: {e}")

try:
    import anthropic
    print("✅ Anthropic - OK") 
except ImportError as e:
    print(f"❌ Anthropic - Error: {e}")

try:
    import google.generativeai as genai
    print("✅ Google GenerativeAI - OK")
except ImportError as e:
    print(f"❌ Google GenerativeAI - Error: {e}")

print("\n🎉 All import tests completed!")
print("💖 Jill AI Agent is ready to serve Ken!")