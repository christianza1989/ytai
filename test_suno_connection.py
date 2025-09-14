#!/usr/bin/env python3
"""
Test Suno AI API connection and basic functionality
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.services.suno_client import SunoClient

def test_suno_connection():
    """Test basic Suno AI API connection"""
    print("🧪 Testing Suno AI API Connection")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('SUNO_API_KEY')
    if not api_key:
        print("❌ SUNO_API_KEY not found in environment")
        return False
        
    print(f"✅ API Key: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Initialize client
        print("🔄 Initializing Suno client...")
        suno = SunoClient()
        print("✅ Suno client created successfully")
        
        # Test 1: Get credits
        print("\n🧪 Test 1: Getting credits...")
        try:
            credits = suno.get_credits()
            print(f"✅ Credits retrieved: {credits}")
            
            if credits <= 0:
                print("⚠️ Warning: No credits available for generation")
                return False
                
        except Exception as e:
            print(f"❌ Credits check failed: {e}")
            return False
        
        # Test 2: Simple music generation
        print("\n🧪 Test 2: Testing simple music generation...")
        try:
            test_prompt = "upbeat electronic music, energetic, dance"
            print(f"Prompt: {test_prompt}")
            
            generation_result = suno.generate_music_simple(
                prompt=test_prompt,
                instrumental=True,  # Start with instrumental to avoid lyrics issues
                model="V4"
            )
            
            if generation_result:
                print("✅ Music generation request initiated successfully")
                print(f"📋 Result type: {type(generation_result)}")
                print(f"📋 Result data: {generation_result}")
                
                # Check if we got a task ID
                if isinstance(generation_result, dict):
                    task_id = generation_result.get('taskId') or generation_result.get('id')
                    if task_id:
                        print(f"✅ Task ID received: {task_id}")
                        
                        # Test status check
                        print("\n🧪 Test 3: Checking task status...")
                        status_result = suno.get_task_status(task_id)
                        if status_result:
                            print("✅ Task status retrieved successfully")
                            print(f"📊 Status: {status_result.get('status', 'Unknown')}")
                            print(f"📋 Status data: {status_result}")
                        else:
                            print("❌ Failed to get task status")
                            
                        return True
                    else:
                        print("❌ No task ID in generation result")
                        return False
                else:
                    print(f"🤔 Unexpected result format: {generation_result}")
                    return False
                    
            else:
                print("❌ Music generation failed - no result returned")
                return False
                
        except Exception as e:
            print(f"❌ Music generation test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Suno client initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test the API endpoints directly"""
    print("\n🧪 Testing API Endpoints Directly")
    print("=" * 40)
    
    import requests
    
    api_key = os.getenv('SUNO_API_KEY')
    base_url = "https://api.sunoapi.org/api/v1"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test credits endpoint
    try:
        print("🔄 Testing credits endpoint...")
        credits_url = f"{base_url}/generate/credit"
        response = requests.get(credits_url, headers=headers, timeout=30)
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Credits response: {data}")
        else:
            print(f"❌ Credits request failed: {response.status_code}")
            print(f"📄 Response text: {response.text}")
            
    except Exception as e:
        print(f"❌ Credits endpoint test failed: {e}")
        
    # Test generate endpoint structure
    try:
        print("\n🔄 Testing generate endpoint structure...")
        generate_url = f"{base_url}/generate"
        
        # Try a minimal request to see what happens
        test_payload = {
            "prompt": "test",
            "customMode": False,
            "instrumental": True,
            "model": "V4"
        }
        
        response = requests.post(generate_url, json=test_payload, headers=headers, timeout=30)
        print(f"📡 Generate response status: {response.status_code}")
        
        if response.status_code in [200, 400, 422]:  # 400/422 might give us useful error info
            try:
                data = response.json()
                print(f"📋 Generate response: {data}")
            except:
                print(f"📄 Generate response text: {response.text}")
        else:
            print(f"📄 Generate response text: {response.text}")
            
    except Exception as e:
        print(f"❌ Generate endpoint test failed: {e}")

if __name__ == "__main__":
    print("🎵 Suno AI API Connection Test Suite")
    print("=" * 60)
    
    success = test_suno_connection()
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Suno AI integration appears to be working!")
    else:
        print("❌ Suno AI integration has issues that need to be resolved.")
    print("🏁 Test completed!")