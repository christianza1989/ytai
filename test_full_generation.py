#!/usr/bin/env python3
"""
Test full music generation workflow end-to-end
"""

import os
import sys
import requests
import json
import time
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_web_interface_generation():
    """Test music generation through web interface"""
    print("🌐 Testing Music Generation via Web Interface")
    print("=" * 50)
    
    try:
        session = requests.Session()
        base_url = "http://localhost:5000"
        
        # Step 1: Login
        print("🔐 Logging in...")
        login_response = session.post(f"{base_url}/login", data={"password": "admin123"})
        if login_response.status_code not in [200, 302]:
            print(f"❌ Login failed: {login_response.status_code}")
            return False
        print("✅ Login successful")
        
        # Step 2: Submit music generation request
        print("🎵 Submitting music generation request...")
        generation_data = {
            "music_type": "instrumental",
            "genre_category": "electronic",
            "genre_specific": "house",
            "mood": "energetic",
            "tempo": "moderate",
            "song_title": "Test AI Track",
            "suno_model": "V4",
            "wait_audio": True
        }
        
        generate_response = session.post(
            f"{base_url}/api/music/generate",
            json=generation_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📡 Generation response status: {generate_response.status_code}")
        
        if generate_response.status_code == 200:
            result = generate_response.json()
            print(f"✅ Generation request submitted: {result}")
            
            if result.get('success'):
                task_id = result.get('task_id')
                print(f"📋 Task ID: {task_id}")
                
                # Step 3: Monitor progress
                print("⏳ Monitoring generation progress...")
                
                for i in range(30):  # Check for up to 5 minutes
                    time.sleep(10)  # Wait 10 seconds between checks
                    
                    status_response = session.get(f"{base_url}/api/music/status/{task_id}")
                    if status_response.status_code == 200:
                        status = status_response.json()
                        current_status = status.get('status', 'unknown')
                        progress = status.get('progress', 0)
                        step = status.get('current_step', 'Working...')
                        
                        print(f"📊 Progress: {progress}% - {current_status} - {step}")
                        
                        if current_status == 'completed':
                            print("🎉 Generation completed successfully!")
                            result_data = status.get('result', {})
                            if result_data:
                                print(f"🎧 Audio URL: {result_data.get('audio_url')}")
                                print(f"🎬 Video URL: {result_data.get('video_url')}")
                                print(f"📝 Title: {result_data.get('title')}")
                                print(f"⏱️ Duration: {result_data.get('duration')}")
                            return True
                            
                        elif current_status == 'failed':
                            print(f"❌ Generation failed: {step}")
                            error_result = status.get('result', {})
                            if error_result:
                                print(f"🔍 Error details: {error_result.get('error')}")
                            return False
                    else:
                        print(f"❌ Status check failed: {status_response.status_code}")
                
                print("⏰ Timeout waiting for completion")
                return False
                
            else:
                print(f"❌ Generation request failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Generation request failed: {generate_response.status_code}")
            print(f"📄 Response: {generate_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_quick_suno_generation():
    """Test a quick Suno generation to verify it's working"""
    print("\n🚀 Testing Quick Suno Generation")
    print("=" * 40)
    
    try:
        load_dotenv()
        
        from core.services.suno_client import SunoClient
        
        suno = SunoClient()
        print("✅ Suno client initialized")
        
        # Get credits
        credits = suno.get_credits()
        print(f"💳 Credits available: {credits}")
        
        if credits < 5:
            print("⚠️ Not enough credits for generation test")
            return False
        
        # Generate a simple track
        print("🎵 Starting quick generation...")
        result = suno.generate_music_simple(
            prompt="upbeat electronic house music, energetic, danceable",
            instrumental=True,
            model="V4"
        )
        
        if result:
            task_id = result.get('taskId')
            print(f"✅ Generation started: {task_id}")
            
            # Wait a bit and check status
            print("⏳ Waiting 15 seconds before checking status...")
            time.sleep(15)
            
            status = suno.get_task_status(task_id)
            if status:
                print(f"📊 Current status: {status.get('status')}")
                print(f"📋 Full status: {status}")
                
                return True
            else:
                print("❌ Could not get task status")
                return False
        else:
            print("❌ Generation failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Quick generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎼 Full Music Generation Workflow Test")
    print("=" * 60)
    
    # Test 1: Quick Suno generation
    quick_success = test_quick_suno_generation()
    
    # Test 2: Full web interface generation
    web_success = test_web_interface_generation()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"🚀 Quick Suno Test: {'✅ PASSED' if quick_success else '❌ FAILED'}")
    print(f"🌐 Web Interface Test: {'✅ PASSED' if web_success else '❌ FAILED'}")
    
    if quick_success and web_success:
        print("\n🎉 All tests passed! Music generation is working!")
    elif quick_success:
        print("\n⚠️ Suno API works, but web interface has issues")
    else:
        print("\n❌ Music generation has issues that need fixing")
    
    print("🏁 Full test completed!")