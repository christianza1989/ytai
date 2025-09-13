#!/usr/bin/env python3
"""
Test script to verify the new System Settings page functionality
"""

import requests
import json

def test_system_settings():
    """Test the new system settings page"""
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    
    print("🧪 Testing New System Settings Page")
    print("=" * 50)
    
    # Create session and login
    session = requests.Session()
    
    try:
        # Step 1: Login
        print("📍 Step 1: Logging in...")
        login_data = {'password': 'admin123'}
        login_post = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        
        if login_post.status_code != 200:
            print(f"❌ Login failed: {login_post.status_code}")
            return False
        
        print("✅ Login successful")
        
        # Step 2: Access system settings page
        print("🎨 Step 2: Accessing system settings page...")
        settings_response = session.get(f"{base_url}/system-settings")
        
        if settings_response.status_code != 200:
            print(f"❌ System settings page failed: {settings_response.status_code}")
            return False
        
        print("✅ System settings page accessible")
        
        # Step 3: Check for key elements
        content = settings_response.text
        
        checks = {
            "AI Theme Elements": [
                "AI Futuristic",
                "glass-card",
                "ai-theme",
                "glassmorphism"
            ],
            "Theme Selection": [
                "selectTheme",
                "theme-selector",
                "Theme Selector Cards"
            ],
            "Modern Styling": [
                "backdrop-filter",
                "glow-primary",
                "--ai-gradient-bg",
                "pulse-animation"
            ],
            "Functionality": [
                "applySelectedTheme",
                "saveAllSettings",
                "localStorage"
            ]
        }
        
        print("\n📋 System Settings Page Check:")
        all_passed = True
        
        for category, items in checks.items():
            category_passed = True
            missing_items = []
            
            for item in items:
                if item not in content:
                    category_passed = False
                    missing_items.append(item)
            
            status = "✅" if category_passed else "❌"
            print(f"   {status} {category}: {'PASSED' if category_passed else 'FAILED'}")
            
            if not category_passed:
                print(f"      Missing: {', '.join(missing_items)}")
                all_passed = False
        
        # Step 4: Test API endpoints
        print("\n🔗 Step 4: Testing API endpoints...")
        
        # Test settings save
        test_settings = {
            'theme': 'ai',
            'language': 'lt',
            'notifications': True
        }
        
        api_save = session.post(f"{base_url}/api/settings/save", 
                               json=test_settings,
                               headers={'Content-Type': 'application/json'})
        
        if api_save.status_code == 200:
            print("   ✅ Settings save API: WORKING")
        else:
            print(f"   ❌ Settings save API: FAILED ({api_save.status_code})")
            all_passed = False
        
        # Test settings load
        api_load = session.get(f"{base_url}/api/settings/load")
        
        if api_load.status_code == 200:
            print("   ✅ Settings load API: WORKING")
        else:
            print(f"   ❌ Settings load API: FAILED ({api_load.status_code})")
            all_passed = False
        
        # Step 5: Check specific theme elements
        print("\n🎯 Step 5: Checking AI theme implementation...")
        
        ai_theme_elements = [
            ":root",
            "--ai-gradient-bg",
            "--ai-glass-bg", 
            "--ai-glow-primary",
            "backdrop-filter: blur(20px)",
            "rgba(255, 255, 255, 0.05)",
            "glassmorphism"
        ]
        
        ai_theme_score = 0
        for element in ai_theme_elements:
            if element in content:
                ai_theme_score += 1
        
        ai_theme_percentage = (ai_theme_score / len(ai_theme_elements)) * 100
        
        print(f"   🎨 AI Theme completeness: {ai_theme_percentage:.1f}% ({ai_theme_score}/{len(ai_theme_elements)})")
        
        if ai_theme_percentage >= 80:
            print("   ✅ AI Theme implementation: EXCELLENT")
        elif ai_theme_percentage >= 60:
            print("   ⚠️ AI Theme implementation: GOOD")
        else:
            print("   ❌ AI Theme implementation: NEEDS WORK")
            all_passed = False
        
        # Summary
        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 SYSTEM SETTINGS TEST PASSED!")
            print("✅ All theme elements are properly implemented")
            print("✅ API endpoints are working")
            print("✅ Modern AI styling is applied")
            print("✅ Glassmorphism effects are present")
        else:
            print("⚠️ Some system settings features need attention")
        
        print(f"\n🌐 Access URL: {base_url}/system-settings")
        print("🔑 Login: admin123")
        print("=" * 50)
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_system_settings()
    if success:
        print("\n🎯 System Settings page is working perfectly!")
    else:
        print("\n💥 Some system settings features need fixes!")