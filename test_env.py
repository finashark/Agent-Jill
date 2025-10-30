import os
from dotenv import load_dotenv

# Test load .env file
print("Testing .env file loading...")

# Load .env
load_dotenv()

# Check API key
google_key = os.getenv('GOOGLE_API_KEY')
print(f"GOOGLE_API_KEY: {google_key}")

if google_key:
    print("✅ API Key loaded successfully!")
    print(f"Key length: {len(google_key)}")
    print(f"Key starts with: {google_key[:10]}...")
else:
    print("❌ API Key NOT found!")
    
# Check file exists
import os.path
env_file = '.env'
if os.path.exists(env_file):
    print(f"✅ .env file exists at: {os.path.abspath(env_file)}")
else:
    print("❌ .env file not found!")