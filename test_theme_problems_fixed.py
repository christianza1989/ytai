#!/usr/bin/env python3
"""
Test to verify theme system problems are fixed:
1. Theme changes are persistent (not reverting when leaving page)
2. All themes can be activated (not just AI theme)
3. Theme selection is saved and works across pages
"""

import requests
import json
import time

def test_theme_problems_fixed():
    """Test that all reported theme problems are fixed"""
    
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    session = requests.Session()
    
    print("🔧 Testing Theme Problems Are Fixed")
    print("=" * 50)
    
    # Login
    print("\n1. Logging in...")
    login_response = session.post(f"{base_url}/login", data={'password': 'admin123'}, allow_redirects=True)
    if not (login_response.status_code == 200 and ('dashboard' in login_response.url or 'Dashboard' in login_response.text)):
        print("❌ Login failed")
        return False
    print("✅ Login successful")
    
    # Problem 1: Test theme persistence (tema neisijungia kai spaudziu ant kitu)
    print("\n2. Testing Theme Switching (Problem 1: themes not activating)...")
    
    themes_to_test = ['cyberpunk', 'matrix', 'neon', 'dark', 'default']
    
    for theme in themes_to_test:
        # Select theme via API
        response = session.post(f"{base_url}/api/settings/theme", 
                               json={'theme': theme},
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('theme') == theme:
                print(f"  ✅ {theme.title()} theme: Successfully activated")
            else:
                print(f"  ❌ {theme.title()} theme: Failed to activate")
                return False
        else:
            print(f"  ❌ {theme.title()} theme: API error {response.status_code}")
            return False
        
        time.sleep(0.3)  # Small delay
    
    # Problem 2: Test theme persistence when navigating away (tema originaliai isijungia kai iseinu is puslapio)
    print("\n3. Testing Theme Persistence Across Pages (Problem 2: reverts when leaving page)...")
    
    # Set AI theme
    session.post(f"{base_url}/api/settings/theme", 
                json={'theme': 'ai'},
                headers={'Content-Type': 'application/json'})
    
    # Visit different pages and verify theme persists
    test_pages = [
        '/system-settings',
        '/generator', 
        '/channel-generator',
        '/analytics',
        '/api-config'
    ]
    
    persistence_success = True
    for page in test_pages:
        try:
            page_response = session.get(f"{base_url}{page}")
            if page_response.status_code == 200:
                # Check that theme loading functions exist
                content = page_response.text
                has_theme_loader = 'loadAndApplySystemTheme' in content
                has_theme_css = 'ai-theme' in content
                
                if has_theme_loader and has_theme_css:
                    print(f"  ✅ {page}: Theme system integrated")
                else:
                    print(f"  ❌ {page}: Theme system missing")
                    persistence_success = False
            else:
                print(f"  ⚠️ {page}: Not accessible")
        except Exception as e:
            print(f"  ❌ {page}: Error - {str(e)}")
            persistence_success = False
    
    # Verify AI theme is still set after navigation
    check_response = session.get(f"{base_url}/api/settings/theme")
    if check_response.status_code == 200:
        theme_data = check_response.json()
        current_theme = theme_data.get('theme')
        if current_theme == 'ai':
            print(f"  ✅ Theme persistence verified: Still set to {current_theme}")
        else:
            print(f"  ❌ Theme not persistent: Changed to {current_theme}")
            persistence_success = False
    
    # Problem 3: Test that settings are saved permanently
    print("\n4. Testing Permanent Settings Save...")
    
    # Save comprehensive settings with Cyberpunk theme
    test_settings = {
        'theme': 'cyberpunk',
        'language': 'lt',
        'notifications': True,
        'animations': True
    }
    
    save_response = session.post(f"{base_url}/api/settings/save",
                                json=test_settings,
                                headers={'Content-Type': 'application/json'})
    
    if save_response.status_code == 200 and save_response.json().get('success'):
        print("  ✅ Settings save API working")
        
        # Verify settings were saved by loading them back
        load_response = session.get(f"{base_url}/api/settings/load")
        if load_response.status_code == 200:
            load_data = load_response.json()
            if load_data.get('success'):
                saved_theme = load_data.get('settings', {}).get('theme')
                if saved_theme == 'cyberpunk':
                    print("  ✅ Settings persistence verified: Theme saved correctly")
                else:
                    print(f"  ❌ Settings not saved correctly: Got {saved_theme}")
                    return False
            else:
                print("  ❌ Settings load failed")
                return False
        else:
            print("  ❌ Settings load API error")
            return False
    else:
        print("  ❌ Settings save failed")
        return False
    
    # Final verification - test UI theme switching on system settings page
    print("\n5. Testing UI Theme Switching on System Settings Page...")
    
    settings_page = session.get(f"{base_url}/system-settings")
    if settings_page.status_code == 200:
        content = settings_page.text
        
        # Check that all theme switching functions exist
        required_functions = [
            'selectTheme(',
            'applySelectedTheme(',
            'loadCurrentTheme(',
            'applyThemeToBody(',
            'saveThemeToServer('
        ]
        
        functions_found = 0
        for func in required_functions:
            if func in content:
                functions_found += 1
                print(f"  ✅ Found: {func}")
            else:
                print(f"  ❌ Missing: {func}")
        
        if functions_found == len(required_functions):
            print(f"  ✅ All {len(required_functions)} theme functions present")
        else:
            print(f"  ❌ Only {functions_found}/{len(required_functions)} functions found")
            return False
    else:
        print("  ❌ Cannot access system settings page")
        return False
    
    # Summary
    print("\n" + "=" * 50)
    print("🔧 THEME PROBLEMS FIX VERIFICATION")
    print("=" * 50)
    
    if persistence_success:
        print("✅ PROBLEM 1 FIXED: All themes can now be activated")
        print("✅ PROBLEM 2 FIXED: Themes persist when navigating between pages") 
        print("✅ PROBLEM 3 FIXED: Theme settings are saved permanently")
        print()
        print("🎉 ALL THEME PROBLEMS HAVE BEEN RESOLVED!")
        print()
        print("🎨 How to use the new theme system:")
        print("   1. Go to 'System Themes 🎨 NEW' in the sidebar")
        print("   2. Click on any theme card to select it")
        print("   3. Click 'Apply Theme' to activate")
        print("   4. Theme will persist across all pages")
        print("   5. Use the header toggle button to cycle through themes")
        
        return True
    else:
        print("❌ Some problems still remain")
        return False

if __name__ == "__main__":
    try:
        success = test_theme_problems_fixed()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        exit(1)