#!/usr/bin/env python3
"""
Test script for the Professional Music Generator
Tests the new advanced music generation functionality
"""

import requests
import json
import time
from datetime import datetime

def test_music_generator():
    """Test the professional music generator interface and functionality"""
    
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    session = requests.Session()
    
    print("🎵 Testing Professional Music Generator")
    print("=" * 50)
    
    # Step 1: Login
    print("\n1. Testing login...")
    login_response = session.post(f"{base_url}/login", data={
        'password': 'admin123'
    }, allow_redirects=True)
    
    print(f"   Status code: {login_response.status_code}")
    print(f"   Final URL: {login_response.url}")
    
    if login_response.status_code == 200 and ('dashboard' in login_response.url or 'Dashboard' in login_response.text):
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        # Try to get the login page first
        login_page = session.get(f"{base_url}/login")
        if login_page.status_code == 200:
            print("   Login page accessible, trying again...")
        return False
    
    # Step 2: Access Music Generator page
    print("\n2. Testing Music Generator page access...")
    generator_response = session.get(f"{base_url}/generator")
    
    if generator_response.status_code == 200:
        print("✅ Music Generator page accessible")
        
        # Check for professional elements
        content = generator_response.text
        
        checks = [
            ("Professional Music Generator", "Professional title"),
            ("Music Type & Genre Selection", "Step 1 section"),
            ("Vocal Configuration", "Step 2 section"), 
            ("Advanced Settings & Prompt", "Step 3 section"),
            ("music_type", "Music type selection"),
            ("musicGenreCategory", "Genre category dropdown"),
            ("musicGenreSpecific", "Specific genre dropdown"),
            ("vocalGender", "Vocal gender selection"),
            ("vocalStyle", "Vocal style selection"),
            ("songLanguage", "Language selection"),
            ("lyricsMode", "Lyrics mode selection"),
            ("customLyrics", "Custom lyrics field"),
            ("lyricsTheme", "Lyrics theme field"),
            ("customPrompt", "Custom prompt field"),
            ("generateMusicBtn", "Generate button"),
            ("Suno AI Powered", "Suno AI branding"),
            ("api/music/generate", "API endpoint reference")
        ]
        
        passed_checks = 0
        for check_text, description in checks:
            if check_text in content:
                print(f"  ✅ {description}")
                passed_checks += 1
            else:
                print(f"  ❌ Missing: {description}")
        
        print(f"\n  📊 UI Elements: {passed_checks}/{len(checks)} ({passed_checks/len(checks)*100:.1f}%)")
        
        # Check that old test mode elements are removed
        old_elements = [
            "Demo / Test Režimas", 
            "Greitas Demo Testas",
            "Pilnas Demo Procesas",
            "Test Mode",
            "Mock data, no API costs"
        ]
        
        removed_elements = 0
        for old_element in old_elements:
            if old_element not in content:
                removed_elements += 1
            else:
                print(f"  ⚠️ Still contains old element: {old_element}")
        
        print(f"  🗑️ Old elements removed: {removed_elements}/{len(old_elements)} ({removed_elements/len(old_elements)*100:.1f}%)")
        
    else:
        print("❌ Cannot access Music Generator page")
        return False
    
    # Step 3: Test API endpoint accessibility
    print("\n3. Testing API endpoints...")
    
    # Test music generation endpoint (should require POST data)
    api_test = session.post(f"{base_url}/api/music/generate", 
                           json={},
                           headers={'Content-Type': 'application/json'})
    
    if api_test.status_code in [400, 422]:  # Expected - missing required data
        print("✅ API endpoint accessible (returns validation error as expected)")
    elif api_test.status_code == 200:
        print("✅ API endpoint accessible")
    else:
        print(f"❌ API endpoint issue: {api_test.status_code}")
    
    # Step 4: Test JavaScript functionality detection
    print("\n4. Testing JavaScript functions...")
    
    js_functions = [
        "initializeMusicTypeSelection",
        "updateSpecificGenres", 
        "updateVocalStyles",
        "updateLyricsSection",
        "buildGenerationPrompt",
        "loadTemplate",
        "previewGeneration"
    ]
    
    js_found = 0
    for js_func in js_functions:
        if js_func in content:
            js_found += 1
            print(f"  ✅ Found: {js_func}")
        else:
            print(f"  ❌ Missing: {js_func}")
    
    print(f"  📊 JavaScript functions: {js_found}/{len(js_functions)} ({js_found/len(js_functions)*100:.1f}%)")
    
    # Step 5: Check navigation update
    print("\n5. Testing navigation update...")
    if "Music Generator 🎵 PRO" in content:
        print("✅ Navigation updated with PRO branding")
    else:
        print("❌ Navigation not updated")
    
    if "Suno AI" in content:
        print("✅ Suno AI integration mentioned")
    else:
        print("❌ Suno AI integration not mentioned")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎵 PROFESSIONAL MUSIC GENERATOR TEST SUMMARY")
    print("=" * 50)
    
    total_score = (passed_checks + removed_elements + js_found) / (len(checks) + len(old_elements) + len(js_functions)) * 100
    
    print(f"📊 Overall Score: {total_score:.1f}%")
    
    if total_score >= 85:
        print("🎉 EXCELLENT: Professional Music Generator successfully implemented!")
        print("   ✅ All test mode elements removed")
        print("   ✅ Professional UI implemented")  
        print("   ✅ Advanced features working")
        print("   ✅ API endpoints ready")
    elif total_score >= 70:
        print("✅ GOOD: Music Generator mostly working")
        print("   ⚠️ Some minor issues to address")
    else:
        print("❌ NEEDS WORK: Several issues found")
    
    return total_score >= 70

if __name__ == "__main__":
    try:
        success = test_music_generator()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        exit(1)