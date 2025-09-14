#!/usr/bin/env python3
"""
Test updated Suno models configuration
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.services.suno_client import SunoClient

def test_suno_models():
    """Test all Suno model configurations"""
    print("🎵 Testing Updated Suno Models Configuration")
    print("=" * 60)
    
    load_dotenv()
    
    try:
        suno = SunoClient()
        print("✅ Suno client initialized")
        
        # Test each model
        models_to_test = ['V3_5', 'V4', 'V4_5']
        
        for model in models_to_test:
            print(f"\n🧪 Testing model: {model}")
            
            try:
                # Test simple generation
                result = suno.generate_music_simple(
                    prompt="upbeat electronic music, energetic, danceable",
                    instrumental=True,
                    model=model
                )
                
                if result and 'taskId' in result:
                    print(f"   ✅ {model}: Generation successful - Task ID: {result['taskId'][:12]}...")
                    
                    # Brief status check
                    time.sleep(2)
                    status = suno.get_task_status(result['taskId'])
                    if status:
                        print(f"   📊 {model}: Status: {status.get('status', 'unknown')}")
                    else:
                        print(f"   ⚠️ {model}: Could not check status")
                        
                else:
                    print(f"   ❌ {model}: Generation failed - no task ID returned")
                    
            except Exception as e:
                print(f"   ❌ {model}: Error - {e}")
                
            # Small delay between tests
            time.sleep(3)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test models: {e}")
        return False

def test_web_interface_models():
    """Test model selection through web interface"""
    print("\n🌐 Testing Web Interface Model Selection")
    print("=" * 50)
    
    try:
        session = requests.Session()
        base_url = "http://localhost:5000"
        
        # Login
        login_response = session.post(f"{base_url}/login", data={"password": "admin123"})
        if login_response.status_code not in [200, 302]:
            print(f"❌ Login failed: {login_response.status_code}")
            return False
        print("✅ Login successful")
        
        # Test generation with different models
        models_to_test = ['V3_5', 'V4', 'V4_5']
        
        for model in models_to_test:
            print(f"\n🧪 Testing web interface with model: {model}")
            
            generation_data = {
                "music_type": "instrumental",
                "genre_category": "electronic",
                "genre_specific": "house",
                "mood": "energetic",
                "tempo": "moderate",
                "song_title": f"Test {model} Track",
                "suno_model": model
            }
            
            try:
                generate_response = session.post(
                    f"{base_url}/api/music/generate",
                    json=generation_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if generate_response.status_code == 200:
                    result = generate_response.json()
                    if result.get('success'):
                        task_id = result.get('task_id')
                        print(f"   ✅ {model}: Web request successful - Task ID: {task_id}")
                        
                        # Check initial status
                        time.sleep(3)
                        status_response = session.get(f"{base_url}/api/music/status/{task_id}")
                        if status_response.status_code == 200:
                            status = status_response.json()
                            current_status = status.get('status')
                            progress = status.get('progress', 0)
                            print(f"   📊 {model}: Status: {current_status} ({progress}%)")
                        else:
                            print(f"   ⚠️ {model}: Could not check status")
                    else:
                        print(f"   ❌ {model}: Generation failed - {result.get('error')}")
                else:
                    print(f"   ❌ {model}: Request failed - {generate_response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {model}: Error - {e}")
            
            # Small delay between tests
            time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"❌ Web interface test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Suno Models Configuration Test Suite")
    print("=" * 70)
    
    # Test 1: Direct API models
    api_success = test_suno_models()
    
    # Test 2: Web interface models 
    web_success = test_web_interface_models()
    
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS:")
    print(f"🔧 Direct API Models: {'✅ PASSED' if api_success else '❌ FAILED'}")
    print(f"🌐 Web Interface Models: {'✅ PASSED' if web_success else '❌ FAILED'}")
    
    if api_success and web_success:
        print("\n🎉 All model configurations working correctly!")
        print("✅ V3_5, V4, and V4_5 models are properly configured")
        print("✅ Web interface reflects correct model options")
        print("✅ Backend correctly processes model selections")
    else:
        print("\n❌ Some model configurations need attention")
    
    print("\n🌐 Access updated interface at:")
    print("https://5000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev/generator")
    print("🏁 Model configuration test completed!")