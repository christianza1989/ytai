#!/usr/bin/env python3
"""
Direct test of API status endpoint
"""

import requests
import json
import time

def test_api_endpoint():
    """Test the API status endpoint directly"""
    
    url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev/api/system/status"
    
    # Test with login first
    login_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev/login"
    
    session = requests.Session()
    
    try:
        # Get login page to get any CSRF tokens
        print("🔐 Getting login page...")
        login_response = session.get(login_url, timeout=10)
        print(f"📊 Login page status: {login_response.status_code}")
        
        # Login (assuming admin/admin credentials)
        print("🔐 Attempting login...")
        login_data = {
            'password': 'admin'  # Default password from admin_app.py
        }
        
        login_post = session.post(login_url, data=login_data, timeout=10)
        print(f"📊 Login POST status: {login_post.status_code}")
        
        if login_post.status_code == 200 or 'dashboard' in login_post.text.lower():
            print("✅ Login successful!")
            
            # Now test API status
            print("🔍 Testing API status endpoint...")
            api_response = session.get(url, timeout=10)
            print(f"📊 API Status response: {api_response.status_code}")
            
            if api_response.status_code == 200:
                data = api_response.json()
                print("✅ API Status successful!")
                print(f"📄 Response: {json.dumps(data, indent=2)}")
                
                # Check Suno status
                suno_status = data.get('api_status', {}).get('suno', {})
                if suno_status:
                    print(f"\n🎵 Suno API Analysis:")
                    print(f"   Status: {suno_status.get('status')}")
                    print(f"   Credits: {suno_status.get('credits')}")
                    print(f"   Error: {suno_status.get('error')}")
                    print(f"   Message: {suno_status.get('message')}")
                    
                    if suno_status.get('status') == 'authentication_error':
                        print(f"✅ Correctly shows authentication error!")
                        return True
                    else:
                        print(f"⚠️ Status is not authentication_error: {suno_status.get('status')}")
                        return False
                else:
                    print(f"❌ No Suno status found")
                    return False
            else:
                print(f"❌ API Status failed: {api_response.status_code}")
                print(f"Response: {api_response.text[:500]}")
                return False
        else:
            print(f"❌ Login failed")
            print(f"Response content: {login_post.text[:200]}")
            return False
            
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing API Status Endpoint Directly")
    print("=" * 60)
    
    success = test_api_endpoint()
    
    print(f"\n📋 Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    if success:
        print("\n✅ API correctly identifies authentication error!")
        print("🔧 The issue might be browser cache.")
        print("💡 Try hard refresh (Ctrl+F5) or clear browser cache.")
    else:
        print("\n❌ API still not working correctly")
        print("🔧 Need to investigate further")