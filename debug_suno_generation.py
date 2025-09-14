#!/usr/bin/env python3
"""
Debug Suno Generation Process
Test the complete generation workflow to see where clips are lost
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_complete_suno_workflow():
    """Test the complete Suno generation workflow"""
    print("🚀 Testing Complete Suno Generation Workflow")
    print("=" * 60)
    
    try:
        sys.path.append('/home/user/webapp')
        from core.services.suno_client import SunoClient
        
        client = SunoClient()
        
        # Step 1: Test simple generation
        print("\n1️⃣ Testing Simple Generation...")
        generation_result = client.generate_music_simple(
            prompt="upbeat electronic dance music",
            model='V4',
            instrumental=False
        )
        
        print(f"🔍 Generation Result Type: {type(generation_result)}")
        print(f"🔍 Generation Result: {generation_result}")
        
        if not generation_result:
            print("❌ Generation failed - no result returned")
            return
        
        # Step 2: Extract task ID
        if isinstance(generation_result, dict):
            if 'taskId' in generation_result:
                task_id = generation_result['taskId']
            elif 'id' in generation_result:
                task_id = generation_result['id']
            else:
                task_id = str(generation_result)
        else:
            task_id = str(generation_result)
        
        print(f"\n2️⃣ Extracted Task ID: {task_id}")
        
        # Step 3: Check initial task status
        print(f"\n3️⃣ Checking Initial Task Status...")
        initial_status = client.get_task_status(task_id)
        print(f"🔍 Initial Status Type: {type(initial_status)}")
        print(f"🔍 Initial Status: {initial_status}")
        
        # Step 4: Wait a bit and check again
        print(f"\n4️⃣ Waiting 30 seconds and checking again...")
        time.sleep(30)
        
        updated_status = client.get_task_status(task_id)
        print(f"🔍 Updated Status Type: {type(updated_status)}")
        print(f"🔍 Updated Status: {updated_status}")
        
        # Step 5: Check what data structure we're getting
        if updated_status:
            print(f"\n5️⃣ Analyzing Data Structure...")
            
            if isinstance(updated_status, dict):
                print(f"📋 Keys in status: {list(updated_status.keys())}")
                
                # Check for audio clips
                if 'data' in updated_status:
                    clips = updated_status['data']
                    print(f"🎵 Clips found in 'data': {clips}")
                elif 'clips' in updated_status:
                    clips = updated_status['clips'] 
                    print(f"🎵 Clips found in 'clips': {clips}")
                elif 'audio_url' in updated_status:
                    print(f"🎵 Direct audio_url: {updated_status['audio_url']}")
                else:
                    print("❌ No clips/audio found in expected locations")
                    print(f"🔍 All data: {updated_status}")
            
        # Step 6: Test the wait_for_completion method
        print(f"\n6️⃣ Testing wait_for_completion method...")
        try:
            final_result = client.wait_for_generation_completion(task_id, max_wait_time=120)
            print(f"🔍 Final Result Type: {type(final_result)}")
            print(f"🔍 Final Result: {final_result}")
            
            if final_result:
                print(f"\n📊 Final Result Analysis:")
                if isinstance(final_result, dict):
                    print(f"📋 Keys: {list(final_result.keys())}")
                    
                    # Look for clips in various locations
                    locations_to_check = ['data', 'clips', 'audio_url', 'results']
                    for loc in locations_to_check:
                        if loc in final_result:
                            print(f"🎵 Found {loc}: {final_result[loc]}")
        
        except Exception as wait_error:
            print(f"❌ Wait for completion error: {wait_error}")
            
    except Exception as e:
        print(f"❌ Workflow test error: {e}")
        import traceback
        traceback.print_exc()

def test_api_response_structure():
    """Test what the raw API responses look like"""
    print("\n🔧 Testing Raw API Response Structure")
    print("=" * 60)
    
    try:
        sys.path.append('/home/user/webapp')
        from core.services.suno_client import SunoClient
        import requests
        
        client = SunoClient()
        
        # Test raw API call to see actual response structure
        print("\n📡 Testing Raw Generation API Call...")
        
        url = f"{client.base_url}/generate"
        payload = {
            "prompt": "test music",
            "customMode": False,
            "model": "V4"
        }
        
        response = requests.post(url, json=payload, headers=client.headers, timeout=30)
        print(f"🔍 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"🔍 Raw Response Data: {data}")
                
                if data.get('code') == 200:
                    task_data = data.get('data', {})
                    print(f"🔍 Task Data: {task_data}")
                    
                    if 'taskId' in task_data:
                        task_id = task_data['taskId']
                        print(f"🆔 Task ID from raw response: {task_id}")
                        
                        # Test raw status check
                        print(f"\n📊 Testing Raw Status Check...")
                        status_url = f"{client.base_url}/generate/record-info"
                        status_response = requests.get(status_url, headers=client.headers, params={"taskId": task_id}, timeout=10)
                        
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            print(f"🔍 Raw Status Response: {status_data}")
                            
                            if status_data.get('code') == 200:
                                actual_data = status_data.get('data')
                                print(f"🔍 Actual Task Data: {actual_data}")
                        else:
                            print(f"❌ Status check failed: {status_response.status_code} - {status_response.text}")
                else:
                    print(f"❌ Generation API error: {data.get('msg')}")
            except Exception as json_error:
                print(f"❌ JSON parse error: {json_error}")
                print(f"📄 Raw response: {response.text}")
        else:
            print(f"❌ API call failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Raw API test error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all debug tests"""
    print("🚀 SUNO GENERATION DEBUG SUITE")
    print("=" * 80)
    
    # Test complete workflow
    test_complete_suno_workflow()
    
    # Test raw API responses
    test_api_response_structure()
    
    print("\n" + "=" * 80)
    print("🏁 Debug tests completed!")
    print("=" * 80)

if __name__ == "__main__":
    main()