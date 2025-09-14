#!/usr/bin/env python3
"""
Quick test of music generation endpoint
"""

import requests
import json
import time

def test_music_generation_endpoint():
    """Test just the generation endpoint"""
    print("🧪 Quick Music Generation Test")
    print("=" * 40)
    
    try:
        session = requests.Session()
        base_url = "http://localhost:5000"
        
        # Login
        print("🔐 Logging in...")
        login_response = session.post(f"{base_url}/login", data={"password": "admin123"})
        
        if login_response.status_code in [200, 302]:
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            return False
        
        # Submit generation request
        print("🎵 Submitting generation request...")
        
        generation_data = {
            "music_type": "instrumental",
            "genre_category": "electronic",
            "genre_specific": "house", 
            "mood": "energetic",
            "tempo": "moderate",
            "song_title": "Quick Test Track",
            "suno_model": "V4"
        }
        
        generate_response = session.post(
            f"{base_url}/api/music/generate",
            json=generation_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📡 Response status: {generate_response.status_code}")
        
        if generate_response.status_code == 200:
            result = generate_response.json()
            print(f"📋 Response: {result}")
            
            if result.get('success'):
                task_id = result.get('task_id')
                print(f"✅ Generation request successful! Task ID: {task_id}")
                
                # Check status after a few seconds
                time.sleep(5)
                
                status_response = session.get(f"{base_url}/api/music/status/{task_id}")
                if status_response.status_code == 200:
                    status = status_response.json()
                    print(f"📊 Initial status: {status.get('status')} - Progress: {status.get('progress', 0)}%")
                    print(f"📝 Current step: {status.get('current_step')}")
                    
                    # Check for any immediate errors
                    if status.get('status') == 'failed':
                        print(f"❌ Generation failed immediately: {status.get('current_step')}")
                        if 'result' in status and 'error' in status['result']:
                            print(f"🔍 Error details: {status['result']['error']}")
                        return False
                    else:
                        print("✅ Generation appears to be working!")
                        return True
                else:
                    print(f"❌ Status check failed: {status_response.status_code}")
                    return False
            else:
                print(f"❌ Generation request failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Request failed: {generate_response.status_code}")
            print(f"📄 Response text: {generate_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_music_generation_endpoint()
    print("\n" + "=" * 40)
    if success:
        print("🎉 Music generation endpoint is working!")
    else:
        print("❌ Music generation has issues")
    print("🏁 Test completed!")