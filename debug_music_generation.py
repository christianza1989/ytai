#!/usr/bin/env python3
"""
Debug script to test music generation exactly as web interface does
"""

import os
import sys
import time
import traceback
from datetime import datetime
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from core.services.suno_client import SunoClient

def debug_music_generation():
    """Test music generation with detailed logging"""
    print("🔍 DEBUG: Starting music generation test...")
    print(f"🔍 DEBUG: SUNO_API_KEY exists: {bool(os.getenv('SUNO_API_KEY'))}")
    
    try:
        # Step 1: Initialize Suno client
        print("\n📝 Step 1: Initializing Suno client...")
        suno = SunoClient()
        print("✅ Suno client initialized successfully")
        
        # Step 2: Check credits
        print("\n📝 Step 2: Checking credits...")
        credits_status = suno.get_credits_with_status()
        print(f"✅ Credits status: {credits_status}")
        
        if credits_status['status'] != 'connected':
            raise Exception(f"Credits check failed: {credits_status}")
            
        # Step 3: Test simple generation (exactly as web interface)
        print("\n📝 Step 3: Testing simple music generation...")
        test_prompt = "chill lo-fi hip hop beat"
        print(f"Prompt: {test_prompt}")
        
        generation_result = suno.generate_music_simple(
            prompt=test_prompt,
            instrumental=False,
            model='V4'
        )
        
        print(f"✅ Generation request sent successfully")
        print(f"Result: {generation_result}")
        
        # Step 4: Extract task ID
        if isinstance(generation_result, dict) and 'taskId' in generation_result:
            task_id = generation_result['taskId']
        elif isinstance(generation_result, str):
            task_id = generation_result
        else:
            task_id = str(generation_result)
            
        print(f"📋 Task ID: {task_id}")
        
        # Step 5: Test wait for completion (with detailed logging)
        print(f"\n📝 Step 4: Testing wait for completion...")
        print("⏳ This may take 60-120 seconds...")
        
        max_wait_time = 300  # 5 minutes
        start_time = time.time()
        check_interval = 15
        
        while time.time() - start_time < max_wait_time:
            try:
                print(f"\n🔄 Checking status... (elapsed: {int(time.time() - start_time)}s)")
                
                task_data = suno.get_task_status(task_id)
                
                if not task_data:
                    print("❌ Failed to get task status")
                    break
                
                status = task_data.get('status', 'UNKNOWN')
                print(f"📊 Status: {status}")
                print(f"📋 Full task data: {task_data}")
                
                if status in ['SUCCESS', 'TEXT_SUCCESS', 'AUDIO_SUCCESS', 'COMPLETE']:
                    print("✅ Generation completed successfully!")
                    print("📋 Final result:")
                    print(f"   Response: {task_data.get('response')}")
                    return {'success': True, 'result': task_data}
                    
                elif status in ['FAILED', 'CREATE_TASK_FAILED', 'GENERATE_AUDIO_FAILED']:
                    error_msg = task_data.get('errorMessage', task_data.get('msg', 'Unknown error'))
                    print(f"❌ Generation failed: {error_msg}")
                    return {'success': False, 'error': error_msg}
                    
                elif status == 'SENSITIVE_WORD_ERROR':
                    print("❌ Content policy violation")
                    return {'success': False, 'error': 'Content policy violation'}
                
                # Continue waiting
                print(f"⏳ Still processing... waiting {check_interval}s")
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"❌ Error checking status: {e}")
                traceback.print_exc()
                time.sleep(check_interval)
        
        # Timeout
        print(f"⏰ Timeout after {max_wait_time} seconds")
        return {'success': False, 'error': f'Timeout after {max_wait_time}s'}
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    result = debug_music_generation()
    print(f"\n🎯 FINAL RESULT: {result}")