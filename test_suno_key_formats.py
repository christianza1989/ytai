#!/usr/bin/env python3
"""
Test different Suno API key formats and endpoints
Sometimes API services change their authentication requirements
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_different_auth_formats():
    """Test different authentication formats"""
    print("🔧 Testing Different Authentication Formats...")
    
    api_key = os.getenv('SUNO_API_KEY')
    base_url = "https://api.sunoapi.org/api/v1"
    
    # Try different header formats
    auth_formats = [
        {"Authorization": f"Bearer {api_key}"},
        {"Authorization": f"Token {api_key}"},  
        {"X-API-Key": api_key},
        {"apikey": api_key},
        {"Authorization": api_key},
    ]
    
    for i, headers in enumerate(auth_formats):
        print(f"\n  📡 Testing format {i+1}: {list(headers.keys())}")
        headers["Content-Type"] = "application/json"
        
        try:
            response = requests.get(f"{base_url}/generate/credit", headers=headers, timeout=10)
            data = response.json() if response.status_code == 200 else response.text
            print(f"    Status: {response.status_code}")
            print(f"    Response: {data}")
            
            if response.status_code == 200 and isinstance(data, dict) and data.get('code') == 200:
                print(f"    ✅ SUCCESS! Credits: {data.get('data')}")
                return headers, data.get('data')
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    return None, None

def test_suno_api_status():
    """Check if Suno API service is having issues"""
    print("\n🌐 Testing Suno API Service Status...")
    
    try:
        # Test basic connectivity
        response = requests.get("https://api.sunoapi.org", timeout=10)
        print(f"  📊 Base URL Status: {response.status_code}")
        
        # Test if it's a general service issue
        response = requests.get("https://api.sunoapi.org/api/v1", timeout=10)
        print(f"  📊 API Base Status: {response.status_code}")
        print(f"  📄 Response: {response.text[:200] if response.text else 'No content'}")
        
    except Exception as e:
        print(f"  ❌ Service connectivity error: {e}")

def check_api_key_format():
    """Verify API key format"""
    print("\n🔍 Checking API Key Format...")
    
    api_key = os.getenv('SUNO_API_KEY')
    if not api_key:
        print("  ❌ No API key found")
        return
    
    print(f"  📏 API Key Length: {len(api_key)}")
    print(f"  🔤 API Key Format: {api_key[:8]}...{api_key[-8:]}")
    print(f"  📝 First 4 chars: {api_key[:4]}")
    print(f"  📝 Last 4 chars: {api_key[-4:]}")
    
    # Common API key patterns
    if len(api_key) < 20:
        print("  ⚠️  API key seems too short")
    elif len(api_key) > 200:
        print("  ⚠️  API key seems too long")
    else:
        print("  ✅ API key length looks reasonable")

def test_api_documentation_endpoint():
    """Test if there's a documentation or info endpoint"""
    print("\n📚 Testing Documentation Endpoints...")
    
    base_urls = [
        "https://api.sunoapi.org/api/v1",
        "https://api.sunoapi.org/docs",
        "https://api.sunoapi.org/health",
        "https://api.sunoapi.org/status"
    ]
    
    for url in base_urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"  📡 {url}: {response.status_code}")
            if response.status_code == 200 and response.text:
                print(f"    Content preview: {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ {url}: {e}")

def main():
    """Run comprehensive API key debugging"""
    print("🚀 SUNO API KEY DEBUG")
    print("=" * 60)
    
    # Check API key format
    check_api_key_format()
    
    # Test service status
    test_suno_api_status()
    
    # Test documentation endpoints
    test_api_documentation_endpoint()
    
    # Test different auth formats
    working_auth, credits = test_different_auth_formats()
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSIS:")
    print("=" * 60)
    
    if working_auth:
        print(f"✅ Found working authentication format!")
        print(f"✅ Credits available: {credits}")
        print(f"📋 Use headers: {working_auth}")
    else:
        print("❌ All authentication formats failed")
        print("🔍 Possible issues:")
        print("   - API key has expired or been revoked")
        print("   - Suno API service is having issues")
        print("   - Authentication method has changed")
        print("   - Rate limiting or account suspension")
        print("\n💡 Recommended actions:")
        print("   1. Check Suno API dashboard for account status")
        print("   2. Verify API key is still valid")
        print("   3. Check for any service announcements")
        print("   4. Contact Suno API support if needed")

if __name__ == "__main__":
    main()