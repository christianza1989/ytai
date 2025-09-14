#!/usr/bin/env python3
"""
Test script to verify API key persistence functionality
"""

import os
import sys
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_env_loading():
    """Test .env file loading"""
    print("🧪 Testing .env file loading...")
    
    # Load .env file
    load_dotenv()
    
    # Check if keys are loaded
    suno_key = os.getenv('SUNO_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY') 
    gemini_model = os.getenv('GEMINI_MODEL')
    
    print(f"✅ SUNO_API_KEY: {'✓' if suno_key else '✗'} ({suno_key[:8] + '...' if suno_key else 'NOT_SET'})")
    print(f"✅ GEMINI_API_KEY: {'✓' if gemini_key else '✗'} ({gemini_key[:8] + '...' if gemini_key else 'NOT_SET'})")
    print(f"✅ GEMINI_MODEL: {'✓' if gemini_model else '✗'} ({gemini_model})")
    
    return suno_key, gemini_key, gemini_model

def test_api_config_route():
    """Test the API configuration route to see what it returns"""
    print("\n🧪 Testing API configuration route...")
    
    # Make request to the application's API config endpoint
    url = "http://localhost:5000/api-config"
    
    try:
        # First try to login and get session
        login_url = "http://localhost:5000/login"
        login_data = {"password": "admin123"}
        
        session = requests.Session()
        
        # Get login page first
        login_response = session.get(login_url)
        print(f"📄 Login page status: {login_response.status_code}")
        
        # Post login credentials
        login_post = session.post(login_url, data=login_data)
        print(f"🔐 Login attempt status: {login_post.status_code}")
        
        if login_post.status_code == 302 or "dashboard" in login_post.text:
            print("✅ Login successful!")
            
            # Now try to access API config page
            config_response = session.get(url)
            print(f"⚙️ API Config page status: {config_response.status_code}")
            
            if config_response.status_code == 200:
                print("✅ API config page accessible")
                
                # Check if the page contains masked API keys
                if "de16083e...2a3" in config_response.text or "de16083e" in config_response.text:
                    print("✅ API keys are displayed (masked or full)")
                else:
                    print("❌ API keys not found in page content")
                    print("🔍 Checking for 'not_configured' placeholder...")
                    if "not_configured" in config_response.text:
                        print("❌ API keys showing as 'not_configured'")
                    else:
                        print("🤔 Unknown state - keys may be there but not visible")
            else:
                print(f"❌ Could not access API config page: {config_response.status_code}")
        else:
            print("❌ Login failed")
            
    except Exception as e:
        print(f"❌ Error testing API config route: {e}")

def test_env_reload():
    """Test environment variable reloading"""
    print("\n🧪 Testing environment variable reloading...")
    
    # Test 1: Check current values
    load_dotenv()
    original_suno = os.getenv('SUNO_API_KEY')
    print(f"📋 Original SUNO_API_KEY: {original_suno[:8]}..." if original_suno else "NOT_SET")
    
    # Test 2: Modify .env file temporarily
    env_path = Path('.env')
    if env_path.exists():
        # Read current content
        with open(env_path, 'r') as f:
            original_content = f.read()
        
        # Write test content
        test_content = original_content.replace(
            f"SUNO_API_KEY={original_suno}", 
            "SUNO_API_KEY=test_key_12345678"
        )
        
        with open(env_path, 'w') as f:
            f.write(test_content)
        
        # Test 3: Reload and check
        load_dotenv(override=True)
        new_suno = os.getenv('SUNO_API_KEY')
        print(f"🔄 After reload SUNO_API_KEY: {new_suno}")
        
        if new_suno == "test_key_12345678":
            print("✅ Environment reload working correctly")
        else:
            print("❌ Environment reload not working")
        
        # Test 4: Restore original content
        with open(env_path, 'w') as f:
            f.write(original_content)
        
        load_dotenv(override=True)
        restored_suno = os.getenv('SUNO_API_KEY')
        print(f"↩️ Restored SUNO_API_KEY: {restored_suno[:8]}..." if restored_suno else "NOT_SET")
        
        if restored_suno == original_suno:
            print("✅ .env file restoration successful")
        else:
            print("❌ .env file restoration failed")

def test_api_save_endpoint():
    """Test the API save endpoint directly"""
    print("\n🧪 Testing API save endpoint...")
    
    url = "http://localhost:5000/api/config/save"
    
    try:
        session = requests.Session()
        
        # Login first
        login_response = session.post("http://localhost:5000/login", data={"password": "admin123"})
        
        if login_response.status_code in [200, 302]:
            # Test saving a new API key
            test_data = {
                "suno_api_key": "test_suno_key_for_persistence",
                "gemini_api_key": "test_gemini_key_for_persistence",
                "gemini_model": "gemini-2.5-flash"
            }
            
            save_response = session.post(url, json=test_data)
            print(f"💾 Save response status: {save_response.status_code}")
            
            if save_response.status_code == 200:
                result = save_response.json()
                print(f"📨 Save response: {result}")
                
                if result.get('success'):
                    print("✅ API save endpoint working")
                    
                    # Verify the .env file was updated
                    with open('.env', 'r') as f:
                        env_content = f.read()
                    
                    if "test_suno_key_for_persistence" in env_content:
                        print("✅ .env file updated correctly")
                        
                        # Restore original keys
                        print("🔄 Restoring original API keys...")
                        restore_data = {
                            "suno_api_key": "de16083e178d256640ae85c65688d2a3",
                            "gemini_api_key": "AIzaSyDZC0065cPheJfw5oqtChgVJCB_qEgDO84",
                            "gemini_model": "gemini-2.5-flash"
                        }
                        
                        restore_response = session.post(url, json=restore_data)
                        if restore_response.status_code == 200:
                            print("✅ Original keys restored")
                        else:
                            print("❌ Failed to restore original keys")
                    else:
                        print("❌ .env file not updated")
                else:
                    print(f"❌ API save failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ Save request failed: {save_response.status_code}")
        else:
            print("❌ Could not login for API save test")
            
    except Exception as e:
        print(f"❌ Error testing API save endpoint: {e}")

if __name__ == "__main__":
    print("🧪 API Persistence Test Suite")
    print("=" * 50)
    
    # Run all tests
    test_env_loading()
    test_api_config_route()
    test_env_reload()
    test_api_save_endpoint()
    
    print("\n" + "=" * 50)
    print("🏁 Test suite completed!")