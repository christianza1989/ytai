#!/usr/bin/env python3
"""
Test script to verify the API status endpoint returns correct status information
"""

import requests
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_status():
    """Test the /api/status endpoint"""
    
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    
    # Test without authentication first
    try:
        print("🌐 Testing API status endpoint...")
        print(f"📍 URL: {base_url}/api/status")
        
        response = requests.get(f"{base_url}/api/status", timeout=10)
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received successfully")
            print(f"📄 Full Response:")
            print(json.dumps(data, indent=2))
            
            # Check Suno API status specifically
            if 'suno' in data:
                suno_status = data['suno']
                print(f"\n🎵 Suno API Status Analysis:")
                print(f"   Status: {suno_status.get('status', 'unknown')}")
                print(f"   Credits: {suno_status.get('credits', 'unknown')}")
                print(f"   Error: {suno_status.get('error', 'none')}")
                print(f"   Message: {suno_status.get('message', 'none')}")
                
                # Check if status correctly identifies auth error
                if suno_status.get('status') == 'authentication_error':
                    print(f"✅ Correctly identified authentication error")
                elif suno_status.get('status') == 'connected':
                    print(f"⚠️ Status shows connected but credits are {suno_status.get('credits', 0)}")
                else:
                    print(f"ℹ️ Status: {suno_status.get('status')}")
            else:
                print(f"❌ No Suno status in response")
                
        elif response.status_code == 401:
            print(f"🔒 Endpoint requires authentication")
            print(f"Response: {response.text}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"💥 Exception occurred: {e}")
        return False
        
    return True

def test_direct_suno_client():
    """Test SunoClient directly to compare"""
    try:
        print(f"\n🔧 Testing SunoClient directly...")
        sys.path.append('/home/user/webapp')
        from core.services.suno_client import SunoClient
        
        suno = SunoClient()
        
        # Test old method
        credits_old = suno.get_credits()
        print(f"📊 Old get_credits(): {credits_old}")
        
        # Test new method
        status_new = suno.get_credits_with_status()
        print(f"📊 New get_credits_with_status():")
        print(json.dumps(status_new, indent=2))
        
        return status_new
        
    except Exception as e:
        print(f"💥 SunoClient Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🔍 Testing API Status Endpoint")
    print("=" * 50)
    
    # Test API endpoint
    endpoint_success = test_api_status()
    
    print("\n" + "=" * 50)
    
    # Test SunoClient directly
    direct_status = test_direct_suno_client()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    if endpoint_success:
        print("✅ API endpoint accessible")
    else:
        print("❌ API endpoint failed")
        
    if direct_status and direct_status.get('status') == 'authentication_error':
        print("✅ SunoClient correctly identifies authentication error")
        print(f"🔑 API Key: {os.getenv('SUNO_API_KEY', 'not found')[:10]}...")
        print("💡 This means the API key has expired or been revoked")
        print("🔧 User needs to update their Suno API key")
    elif direct_status:
        print(f"ℹ️ SunoClient status: {direct_status.get('status')}")
    else:
        print("❌ SunoClient test failed")