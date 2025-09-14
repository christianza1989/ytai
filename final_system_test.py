#!/usr/bin/env python3
"""
Final comprehensive system test - verify all components working
"""

import requests
import time
import os
from dotenv import load_dotenv

def test_complete_system():
    """Test the entire music generation system end-to-end"""
    print("🎼 Final Music Generation System Test")
    print("=" * 60)
    
    results = {}
    
    # Test 1: API Key Persistence
    print("1️⃣ Testing API Key Persistence...")
    try:
        load_dotenv()
        suno_key = os.getenv('SUNO_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        if suno_key and len(suno_key) > 20:
            results['api_persistence'] = '✅ PASS'
            print(f"   ✅ Suno key configured: {suno_key[:8]}...")
        else:
            results['api_persistence'] = '❌ FAIL'
            print("   ❌ Suno key not properly configured")
            
        if gemini_key and len(gemini_key) > 20:
            print(f"   ✅ Gemini key configured: {gemini_key[:8]}...")
        else:
            results['api_persistence'] = '❌ FAIL'
            print("   ❌ Gemini key not properly configured")
            
    except Exception as e:
        results['api_persistence'] = '❌ ERROR'
        print(f"   ❌ Error: {e}")
    
    # Test 2: Web Interface Access
    print("\n2️⃣ Testing Web Interface Access...")
    try:
        session = requests.Session()
        base_url = "http://localhost:5000"
        
        # Test login
        login_response = session.post(f"{base_url}/login", data={"password": "admin123"})
        if login_response.status_code in [200, 302]:
            results['web_interface'] = '✅ PASS'
            print("   ✅ Login successful")
            
            # Test API config page
            config_response = session.get(f"{base_url}/api-config")
            if config_response.status_code == 200:
                print("   ✅ API config page accessible")
            else:
                print("   ⚠️ API config page issues")
        else:
            results['web_interface'] = '❌ FAIL'
            print(f"   ❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        results['web_interface'] = '❌ ERROR'
        print(f"   ❌ Error: {e}")
    
    # Test 3: Suno API Connection
    print("\n3️⃣ Testing Suno API Connection...")
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from core.services.suno_client import SunoClient
        
        suno = SunoClient()
        credits = suno.get_credits()
        
        if credits > 0:
            results['suno_api'] = '✅ PASS'
            print(f"   ✅ Suno API connected: {credits} credits")
        else:
            results['suno_api'] = '⚠️ LOW CREDITS'
            print(f"   ⚠️ Suno API connected but low credits: {credits}")
            
    except Exception as e:
        results['suno_api'] = '❌ ERROR'
        print(f"   ❌ Suno API error: {e}")
    
    # Test 4: Music Generation Workflow
    print("\n4️⃣ Testing Music Generation Workflow...")
    try:
        # Submit generation request
        generation_data = {
            "music_type": "instrumental",
            "genre_category": "electronic",
            "genre_specific": "house",
            "mood": "energetic",
            "tempo": "moderate",
            "song_title": "System Test Track",
            "suno_model": "V4"
        }
        
        generate_response = session.post(
            f"{base_url}/api/music/generate",
            json=generation_data,
            headers={"Content-Type": "application/json"}
        )
        
        if generate_response.status_code == 200:
            result = generate_response.json()
            if result.get('success'):
                task_id = result.get('task_id')
                print(f"   ✅ Generation request successful: {task_id}")
                
                # Check initial status
                time.sleep(3)
                status_response = session.get(f"{base_url}/api/music/status/{task_id}")
                if status_response.status_code == 200:
                    status = status_response.json()
                    current_status = status.get('status')
                    progress = status.get('progress', 0)
                    
                    if current_status in ['processing', 'completed']:
                        results['music_generation'] = '✅ PASS'
                        print(f"   ✅ Generation working: {current_status} ({progress}%)")
                    elif current_status == 'failed':
                        results['music_generation'] = '❌ FAIL'
                        error_msg = status.get('current_step', 'Unknown error')
                        print(f"   ❌ Generation failed: {error_msg}")
                    else:
                        results['music_generation'] = '⏳ IN PROGRESS'
                        print(f"   ⏳ Generation in progress: {current_status}")
                else:
                    results['music_generation'] = '❌ FAIL'
                    print("   ❌ Status check failed")
            else:
                results['music_generation'] = '❌ FAIL'
                print(f"   ❌ Generation request failed: {result.get('error')}")
        else:
            results['music_generation'] = '❌ FAIL'
            print(f"   ❌ Request failed: {generate_response.status_code}")
            
    except Exception as e:
        results['music_generation'] = '❌ ERROR'
        print(f"   ❌ Error: {e}")
    
    # Test 5: System Health Check
    print("\n5️⃣ Testing System Health...")
    try:
        health_response = session.get(f"{base_url}/api/system/status")
        if health_response.status_code == 200:
            health_data = health_response.json()
            api_status = health_data.get('api_status', {})
            
            suno_status = api_status.get('suno', {}).get('status')
            gemini_status = api_status.get('gemini', {}).get('status')
            
            if suno_status == 'connected' and gemini_status == 'connected':
                results['system_health'] = '✅ PASS'
                print("   ✅ All APIs connected")
            else:
                results['system_health'] = '⚠️ PARTIAL'
                print(f"   ⚠️ API status: Suno={suno_status}, Gemini={gemini_status}")
        else:
            results['system_health'] = '❌ FAIL'
            print(f"   ❌ Health check failed: {health_response.status_code}")
            
    except Exception as e:
        results['system_health'] = '❌ ERROR'
        print(f"   ❌ Error: {e}")
    
    # Results Summary
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS:")
    print("=" * 60)
    
    for test_name, result in results.items():
        test_display = test_name.replace('_', ' ').title()
        print(f"{test_display:.<30} {result}")
    
    # Overall Status
    print("\n" + "=" * 60)
    pass_count = sum(1 for r in results.values() if '✅' in r)
    total_tests = len(results)
    
    if pass_count == total_tests:
        print("🎉 OVERALL STATUS: ALL SYSTEMS OPERATIONAL")
        print("✅ Music generation system is fully functional!")
        print("🌐 Ready for production use")
    elif pass_count >= total_tests - 1:
        print("✅ OVERALL STATUS: MOSTLY OPERATIONAL") 
        print("⚠️ Minor issues detected but system is usable")
    else:
        print("❌ OVERALL STATUS: ISSUES DETECTED")
        print("🔧 Some components need attention")
    
    print(f"\n📈 Test Score: {pass_count}/{total_tests} ({int(pass_count/total_tests*100)}%)")
    print("\n🌐 Application URL: https://5000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev/")
    print("🏁 System test completed!")

if __name__ == "__main__":
    test_complete_system()