#!/usr/bin/env python3
"""
Debug Suno API Credits Issue
Test direct API connectivity and credit retrieval
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_suno_api_direct():
    """Test Suno API directly without client wrapper"""
    print("🔧 Testing Suno API Direct Connection...")
    
    api_key = os.getenv('SUNO_API_KEY')
    if not api_key:
        print("  ❌ No SUNO_API_KEY found in environment")
        return False
    
    print(f"  🔑 Using API key: {api_key[:8]}...{api_key[-4:]}")
    
    # Test credits endpoint
    base_url = "https://api.sunoapi.org/api/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print("  📡 Connecting to credits endpoint...")
        url = f"{base_url}/generate/credit"
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"  📊 Response Status: {response.status_code}")
        print(f"  📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  📄 Response JSON: {data}")
                
                if data.get('code') == 200:
                    credits = data.get('data', 0)
                    print(f"  ✅ Credits Retrieved: {credits}")
                    return credits
                else:
                    print(f"  ❌ API Error Code: {data.get('code')}")
                    print(f"  ❌ API Error Message: {data.get('msg')}")
                    return False
            except Exception as json_error:
                print(f"  ❌ JSON Parse Error: {json_error}")
                print(f"  📄 Raw Response: {response.text[:500]}")
                return False
        else:
            print(f"  ❌ HTTP Error: {response.status_code}")
            print(f"  📄 Response Text: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"  ❌ Connection Error: {e}")
        return False

def test_suno_client():
    """Test SunoClient wrapper"""
    print("\n🔧 Testing SunoClient Wrapper...")
    
    try:
        sys.path.append('/home/user/webapp')
        from core.services.suno_client import SunoClient
        
        client = SunoClient()
        print(f"  🔗 Client initialized with API key: {client.api_key[:8]}...{client.api_key[-4:]}")
        
        credits = client.get_credits()
        print(f"  💰 Credits from client: {credits}")
        
        return credits
        
    except Exception as e:
        print(f"  ❌ SunoClient Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_different_endpoints():
    """Test other Suno API endpoints to verify connectivity"""
    print("\n🔧 Testing Other Suno API Endpoints...")
    
    api_key = os.getenv('SUNO_API_KEY')
    base_url = "https://api.sunoapi.org/api/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test different endpoints
    endpoints_to_test = [
        "/generate/credit",
        "/generate",  # Just to see if it responds differently
    ]
    
    for endpoint in endpoints_to_test:
        try:
            print(f"  📡 Testing endpoint: {endpoint}")
            url = f"{base_url}{endpoint}"
            
            if endpoint == "/generate":
                # Test with minimal payload
                response = requests.post(url, headers=headers, json={
                    "prompt": "test",
                    "customMode": False,
                    "model": "V4"
                }, timeout=10)
            else:
                response = requests.get(url, headers=headers, timeout=10)
            
            print(f"    Status: {response.status_code}")
            
            if response.status_code in [200, 400, 422]:  # 400/422 might be expected for incomplete requests
                try:
                    data = response.json()
                    print(f"    Response: {data}")
                except:
                    print(f"    Raw: {response.text[:200]}")
            else:
                print(f"    Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"    Exception: {e}")

def main():
    """Run comprehensive Suno API debug"""
    print("🚀 SUNO API CREDITS DEBUG")
    print("=" * 60)
    
    # Test direct API
    direct_result = test_suno_api_direct()
    
    # Test client wrapper  
    client_result = test_suno_client()
    
    # Test other endpoints
    test_different_endpoints()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEBUG RESULTS:")
    print("=" * 60)
    
    if direct_result is not False:
        print(f"✅ Direct API Credits: {direct_result}")
    else:
        print("❌ Direct API Failed")
    
    if client_result is not False:
        print(f"✅ Client API Credits: {client_result}")
    else:
        print("❌ Client API Failed")
    
    if direct_result == 0 and client_result == 0:
        print("\n⚠️  Credits are actually 0 - API is working but no credits available")
    elif direct_result is False or client_result is False:
        print("\n❌ API connectivity issue detected")
    else:
        print(f"\n✅ API working correctly with {direct_result} credits")

if __name__ == "__main__":
    main()