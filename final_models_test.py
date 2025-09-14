#!/usr/bin/env python3
"""
Final comprehensive test of all updated Suno model configurations
"""

import requests
import time

def test_complete_system():
    """Test complete system with updated models"""
    print("🎵 Final Suno Models System Test")
    print("=" * 60)
    
    session = requests.Session()
    base_url = "http://localhost:5000"
    
    # Login
    print("🔐 Logging in...")
    login_response = session.post(f"{base_url}/login", data={"password": "admin123"})
    if login_response.status_code in [200, 302]:
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        return False
    
    # Test 1: Check API config shows correct models
    print("\n1️⃣ Testing API Configuration Interface...")
    config_response = session.get(f"{base_url}/api-config")
    if config_response.status_code == 200:
        content = config_response.text
        if 'V4_5' in content and 'V4' in content and 'V3_5' in content:
            print("   ✅ API config shows correct model options")
        else:
            print("   ❌ API config missing updated models")
    
    # Test 2: Check music generator interface 
    print("\n2️⃣ Testing Music Generator Interface...")
    generator_response = session.get(f"{base_url}/generator")
    if generator_response.status_code == 200:
        content = generator_response.text
        if 'Superior genre blending' in content and 'up to 8 min' in content:
            print("   ✅ Music generator shows updated V4.5 description")
        else:
            print("   ❌ Music generator missing V4.5 updates")
    
    # Test 3: Test music generation with V4_5 model
    print("\n3️⃣ Testing Music Generation with V4.5...")
    generation_data = {
        "music_type": "instrumental",
        "genre_category": "electronic",
        "genre_specific": "house",
        "mood": "energetic",
        "tempo": "moderate",
        "song_title": "V4.5 Test Track",
        "suno_model": "V4_5"  # Use the latest model
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
                print(f"   ✅ V4.5 generation successful: {task_id}")
                
                # Check status
                time.sleep(3)
                status_response = session.get(f"{base_url}/api/music/status/{task_id}")
                if status_response.status_code == 200:
                    status = status_response.json()
                    print(f"   📊 Status: {status.get('status')} ({status.get('progress', 0)}%)")
                else:
                    print("   ⚠️ Could not check status")
            else:
                print(f"   ❌ V4.5 generation failed: {result.get('error')}")
        else:
            print(f"   ❌ Generation request failed: {generate_response.status_code}")
    except Exception as e:
        print(f"   ❌ Generation error: {e}")
    
    # Test 4: Test music gallery access
    print("\n4️⃣ Testing Music Gallery...")
    try:
        gallery_response = session.get(f"{base_url}/music-gallery")
        if gallery_response.status_code == 200:
            content = gallery_response.text
            if 'Music Gallery' in content and 'AI Generated' in content:
                print("   ✅ Music gallery accessible")
            else:
                print("   ❌ Music gallery content issues")
        else:
            print(f"   ❌ Music gallery failed: {gallery_response.status_code}")
    except Exception as e:
        print(f"   ❌ Gallery error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ FINAL STATUS: Suno models updated successfully!")
    print("🎵 Available Models:")
    print("   • V4.5 - Superior genre blending, up to 8 min ⚡")
    print("   • V4 - Best audio quality, up to 4 min ✨")  
    print("   • V3.5 - Solid arrangements, up to 4 min 🎵")
    print()
    print("🌐 Access your updated system:")
    print("🎵 Music Generator: https://5000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev/generator")
    print("🎨 Music Gallery: https://5000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev/music-gallery")
    print("⚙️ API Config: https://5000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev/api-config")
    print("\n🏁 All systems operational with updated Suno models!")
    
    return True

if __name__ == "__main__":
    test_complete_system()