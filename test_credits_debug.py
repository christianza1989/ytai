#!/usr/bin/env python3
"""
Test script to debug Suno credits API call
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_suno_credits_direct():
    """Test Suno credits API directly"""
    api_key = os.getenv('SUNO_API_KEY')
    if not api_key:
        print("❌ No SUNO_API_KEY found in environment")
        return
    
    print(f"🔑 Testing with API Key: {api_key[:10]}...")
    
    # Direct API call to credits endpoint
    url = "https://api.sunoapi.org/api/v1/generate/credit"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"🌐 Making request to: {url}")
        print(f"🔑 Headers: {json.dumps({k: v[:20] + '...' if k == 'Authorization' else v for k, v in headers.items()}, indent=2)}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📝 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response Data: {json.dumps(data, indent=2)}")
            
            if data.get('code') == 200:
                credits = data.get('data', 0)
                print(f"💰 Credits Found: {credits}")
                return credits
            else:
                print(f"❌ API Error Code: {data.get('code')}")
                print(f"❌ API Error Message: {data.get('msg')}")
                return 0
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"❌ Response Text: {response.text}")
            response.raise_for_status()
            
    except Exception as e:
        print(f"💥 Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return 0

def test_suno_client():
    """Test using SunoClient class"""
    try:
        sys.path.append('/home/user/webapp')
        from core.services.suno_client import SunoClient
        
        print("\n🧪 Testing SunoClient class...")
        suno = SunoClient()
        credits = suno.get_credits()
        print(f"💰 Credits from SunoClient: {credits}")
        return credits
        
    except Exception as e:
        print(f"💥 SunoClient Exception: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == "__main__":
    print("🔍 Starting Suno Credits Debug Test")
    print("=" * 50)
    
    # Test direct API call
    direct_credits = test_suno_credits_direct()
    
    print("\n" + "=" * 50)
    
    # Test SunoClient class
    client_credits = test_suno_client()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    print(f"   Direct API Call: {direct_credits} credits")
    print(f"   SunoClient Call: {client_credits} credits")
    
    if direct_credits != client_credits:
        print("⚠️ WARNING: Results differ between direct and client calls!")
    else:
        print("✅ Results consistent between methods")