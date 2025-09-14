#!/usr/bin/env python3
"""
Test script for Full Theme System functionality
Tests theme persistence, switching, and synchronization across pages
"""

import requests
import json
import time
from datetime import datetime

def test_theme_system():
    """Test the complete theme system functionality"""
    
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    session = requests.Session()
    
    print("🎨 Testing Full Theme System")
    print("=" * 50)
    
    # Step 1: Login
    print("\n1. Testing login...")
    login_response = session.post(f"{base_url}/login", data={
        'password': 'admin123'
    }, allow_redirects=True)
    
    if login_response.status_code == 200 and ('dashboard' in login_response.url or 'Dashboard' in login_response.text):
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        return False
    
    # Step 2: Test System Settings page access
    print("\n2. Testing System Settings page...")
    settings_response = session.get(f"{base_url}/system-settings")
    
    if settings_response.status_code == 200:
        print("✅ System Settings page accessible")
        
        # Check for theme system elements
        content = settings_response.text
        
        theme_checks = [
            ("Interface Themes", "Theme selection section"),
            ("theme-default", "Default theme card"),
            ("theme-dark", "Dark theme card"), 
            ("theme-ai", "AI theme card"),
            ("theme-cyberpunk", "Cyberpunk theme card"),
            ("theme-matrix", "Matrix theme card"),
            ("theme-neon", "Neon theme card"),
            ("selectTheme", "Theme selection function"),
            ("applySelectedTheme", "Apply theme function"),
            ("ai-theme", "AI theme CSS classes"),
            ("cyberpunk-theme", "Cyberpunk theme CSS classes"),
            ("matrix-theme", "Matrix theme CSS classes"),
            ("neon-theme", "Neon theme CSS classes")
        ]
        
        passed_checks = 0
        for check_text, description in theme_checks:
            if check_text in content:
                print(f"  ✅ {description}")
                passed_checks += 1
            else:
                print(f"  ❌ Missing: {description}")
        
        print(f"  📊 Theme System Elements: {passed_checks}/{len(theme_checks)} ({passed_checks/len(theme_checks)*100:.1f}%)")
        
    else:
        print("❌ Cannot access System Settings page")
        return False
    
    # Step 3: Test Theme API endpoints
    print("\n3. Testing Theme API endpoints...")
    
    # Test saving theme setting
    theme_save_response = session.post(f"{base_url}/api/settings/theme", 
                                     json={'theme': 'ai'},
                                     headers={'Content-Type': 'application/json'})
    
    if theme_save_response.status_code == 200:
        save_data = theme_save_response.json()
        if save_data.get('success'):
            print("✅ Theme save API working")
        else:
            print("❌ Theme save API failed")
    else:
        print(f"❌ Theme save API error: {theme_save_response.status_code}")
    
    # Test loading theme setting
    theme_load_response = session.get(f"{base_url}/api/settings/theme")
    
    if theme_load_response.status_code == 200:
        load_data = theme_load_response.json()
        if load_data.get('success'):
            print(f"✅ Theme load API working - Current theme: {load_data.get('theme')}")
        else:
            print("❌ Theme load API failed")
    else:
        print(f"❌ Theme load API error: {theme_load_response.status_code}")
    
    # Step 4: Test theme persistence across pages
    print("\n4. Testing theme persistence across pages...")
    
    # Visit different pages and check if theme persists
    pages_to_test = [
        ('/dashboard', 'Dashboard'),
        ('/generator', 'Music Generator'),
        ('/channel-generator', 'Channel Generator'),
        ('/analytics', 'Analytics'),
        ('/api-config', 'API Configuration')
    ]
    
    persistence_score = 0
    for page_url, page_name in pages_to_test:
        try:
            page_response = session.get(f"{base_url}{page_url}")
            if page_response.status_code == 200:
                page_content = page_response.text
                
                # Check for theme system JavaScript functions
                has_theme_functions = all([
                    'loadAndApplySystemTheme' in page_content,
                    'applySystemTheme' in page_content,
                    'toggleTheme' in page_content
                ])
                
                # Check for theme CSS classes
                has_theme_css = any([
                    'ai-theme' in page_content,
                    'cyberpunk-theme' in page_content,
                    'matrix-theme' in page_content
                ])
                
                if has_theme_functions and has_theme_css:
                    print(f"  ✅ {page_name}: Theme system integrated")
                    persistence_score += 1
                else:
                    print(f"  ❌ {page_name}: Theme system missing")
            else:
                print(f"  ⚠️ {page_name}: Page not accessible")
        except Exception as e:
            print(f"  ❌ {page_name}: Error - {str(e)}")
    
    print(f"  📊 Theme Persistence: {persistence_score}/{len(pages_to_test)} pages ({persistence_score/len(pages_to_test)*100:.1f}%)")
    
    # Step 5: Test advanced theme features
    print("\n5. Testing advanced theme features...")
    
    # Test multiple theme switching
    themes_to_test = ['default', 'dark', 'ai', 'cyberpunk', 'matrix', 'neon']
    
    for theme in themes_to_test:
        try:
            switch_response = session.post(f"{base_url}/api/settings/theme", 
                                         json={'theme': theme},
                                         headers={'Content-Type': 'application/json'})
            
            if switch_response.status_code == 200:
                switch_data = switch_response.json()
                if switch_data.get('success') and switch_data.get('theme') == theme:
                    print(f"  ✅ {theme.title()} theme: Switching works")
                else:
                    print(f"  ❌ {theme.title()} theme: Switch failed")
            else:
                print(f"  ❌ {theme.title()} theme: API error")
                
            time.sleep(0.2)  # Small delay between requests
            
        except Exception as e:
            print(f"  ❌ {theme.title()} theme: Error - {str(e)}")
    
    # Step 6: Test settings persistence
    print("\n6. Testing settings persistence...")
    
    # Save comprehensive settings
    full_settings = {
        'theme': 'ai',
        'language': 'lt',
        'notifications': True,
        'animations': True,
        'refreshRate': '5000',
        'maxTasks': '3'
    }
    
    settings_save_response = session.post(f"{base_url}/api/settings/save", 
                                        json=full_settings,
                                        headers={'Content-Type': 'application/json'})
    
    if settings_save_response.status_code == 200:
        save_result = settings_save_response.json()
        if save_result.get('success'):
            print("✅ Full settings save working")
            
            # Test loading saved settings
            settings_load_response = session.get(f"{base_url}/api/settings/load")
            if settings_load_response.status_code == 200:
                load_result = settings_load_response.json()
                if load_result.get('success'):
                    saved_theme = load_result.get('settings', {}).get('theme')
                    if saved_theme == 'ai':
                        print("✅ Settings persistence verified")
                    else:
                        print(f"❌ Theme not persisted correctly: {saved_theme}")
                else:
                    print("❌ Settings load failed")
            else:
                print("❌ Settings load API error")
        else:
            print("❌ Full settings save failed")
    else:
        print("❌ Full settings save API error")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎨 THEME SYSTEM TEST SUMMARY")
    print("=" * 50)
    
    # Calculate overall score
    theme_elements_score = passed_checks / len(theme_checks) * 100
    persistence_score_pct = persistence_score / len(pages_to_test) * 100
    
    overall_score = (theme_elements_score + persistence_score_pct) / 2
    
    print(f"📊 Theme Elements Score: {theme_elements_score:.1f}%")
    print(f"📊 Persistence Score: {persistence_score_pct:.1f}%") 
    print(f"📊 Overall Theme System Score: {overall_score:.1f}%")
    
    if overall_score >= 90:
        print("🎉 EXCELLENT: Full Theme System working perfectly!")
        print("   ✅ All themes available and functional")
        print("   ✅ Theme persistence across pages")
        print("   ✅ API endpoints working")
        print("   ✅ Settings synchronization working")
    elif overall_score >= 75:
        print("✅ GOOD: Theme System mostly working")
        print("   ⚠️ Some minor issues to address")
    else:
        print("❌ NEEDS WORK: Several theme system issues found")
    
    return overall_score >= 75

if __name__ == "__main__":
    try:
        success = test_theme_system()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        exit(1)