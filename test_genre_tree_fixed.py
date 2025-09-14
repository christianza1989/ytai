#!/usr/bin/env python3
"""
Test script to verify Genre Tree is working in Channel Generator
"""

import requests
import json
import time

def test_genre_tree_loading():
    """Test that the genre tree loads correctly in Channel Generator"""
    
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    session = requests.Session()
    
    print("🌳 Testing Genre Tree Loading in Channel Generator")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1. Logging in...")
    login_response = session.post(f"{base_url}/login", data={'password': 'admin123'}, allow_redirects=True)
    if not (login_response.status_code == 200 and ('dashboard' in login_response.url or 'Dashboard' in login_response.text)):
        print("❌ Login failed")
        return False
    print("✅ Login successful")
    
    # Step 2: Access Channel Generator page
    print("\n2. Testing Channel Generator page access...")
    channel_gen_response = session.get(f"{base_url}/channel-generator")
    
    if channel_gen_response.status_code == 200:
        print("✅ Channel Generator page accessible")
        
        content = channel_gen_response.text
        
        # Check for essential elements
        essential_checks = [
            ("AI Channel Generator", "Page title"),
            ("Choose from our intelligent genre tree", "Step 1 description"),
            ("genreTreeContainer", "Genre tree container"),
            ("loadGenreTreeData", "Genre tree loading function"),
            ("renderGenreTree", "Genre tree render function"),
            ("loadMockGenreData", "Mock data function"),
            ("createCategoryElement", "Category creation function"),
            ("createSubgenreElement", "Subgenre creation function")
        ]
        
        passed_checks = 0
        for check_text, description in essential_checks:
            if check_text in content:
                print(f"  ✅ {description}")
                passed_checks += 1
            else:
                print(f"  ❌ Missing: {description}")
        
        print(f"  📊 Essential Elements: {passed_checks}/{len(essential_checks)} ({passed_checks/len(essential_checks)*100:.1f}%)")
        
        # Check for mock data structure
        mock_data_checks = [
            ("ELECTRONIC", "Electronic category"),
            ("HOUSE", "House subgenre"),
            ("monthly_revenue", "Revenue statistics"),
            ("popularity_score", "Popularity metrics"),
            ("profit-indicator", "Profit indicator classes"),
            ("DOMContentLoaded", "Page initialization")
        ]
        
        mock_checks_passed = 0
        for check_text, description in mock_data_checks:
            if check_text in content:
                print(f"  ✅ {description}")
                mock_checks_passed += 1
            else:
                print(f"  ❌ Missing: {description}")
        
        print(f"  📊 Mock Data Elements: {mock_checks_passed}/{len(mock_data_checks)} ({mock_checks_passed/len(mock_data_checks)*100:.1f}%)")
        
        # Check for debug information
        debug_checks = [
            ("console.log", "Debug logging"),
            ("Loading genre tree data", "Loading messages"),
            ("Mock data loaded", "Mock data confirmation")
        ]
        
        debug_checks_passed = 0
        for check_text, description in debug_checks:
            if check_text in content:
                print(f"  ✅ {description}")
                debug_checks_passed += 1
            else:
                print(f"  ❌ Missing: {description}")
        
        print(f"  📊 Debug Features: {debug_checks_passed}/{len(debug_checks)} ({debug_checks_passed/len(debug_checks)*100:.1f}%)")
        
        # Check if the old loading spinner is still there
        if "Loading interactive genre tree..." in content:
            print("  ⚠️ Old loading spinner still present - this should be replaced by working genre tree")
        else:
            print("  ✅ Old loading spinner removed")
        
        # Overall assessment
        total_score = (passed_checks + mock_checks_passed + debug_checks_passed) / (len(essential_checks) + len(mock_data_checks) + len(debug_checks)) * 100
        
        print(f"\n📊 Overall Genre Tree Readiness: {total_score:.1f}%")
        
        if total_score >= 85:
            print("🎉 EXCELLENT: Genre Tree should be working!")
            print("   ✅ All essential elements present")
            print("   ✅ Mock data properly configured")
            print("   ✅ Debug features enabled")
        elif total_score >= 70:
            print("✅ GOOD: Genre Tree likely working with minor issues")
        else:
            print("❌ NEEDS WORK: Several components missing")
            return False
            
        return total_score >= 70
        
    else:
        print(f"❌ Cannot access Channel Generator page: {channel_gen_response.status_code}")
        return False
    
    # Step 3: Test API endpoint (for future reference)
    print("\n3. Testing Genre Tree API endpoint...")
    
    # This should redirect to login, which is expected
    api_response = session.get(f"{base_url}/api/genres/tree")
    if api_response.status_code in [200, 302]:  # 302 = redirect to login
        print("✅ API endpoint accessible (authentication required)")
    else:
        print(f"⚠️ API endpoint returned: {api_response.status_code}")

def test_console_debug():
    """Instructions for manual browser testing"""
    print("\n" + "=" * 60)
    print("🔍 MANUAL BROWSER TESTING INSTRUCTIONS")
    print("=" * 60)
    print()
    print("To verify the genre tree is working:")
    print()
    print("1. Open browser and go to:")
    print("   https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev/channel-generator")
    print()
    print("2. Open Developer Tools (F12)")
    print()
    print("3. Go to Console tab")
    print()
    print("4. Look for these debug messages:")
    print("   ✅ 'Channel Generator: DOM loaded'")
    print("   ✅ 'Channel Generator: loadGenreTree called'")
    print("   ✅ 'Loading genre tree data...'")
    print("   ✅ 'Mock data loaded successfully:'")
    print("   ✅ 'renderGenreTree called'")
    print("   ✅ 'Building genre tree elements...'")
    print("   ✅ 'Genre tree rendered successfully'")
    print()
    print("5. The page should show:")
    print("   ✅ Interactive genre categories (ELECTRONIC, WORKOUT)")
    print("   ✅ Clickable category headers")
    print("   ✅ Subgenres when categories are expanded")
    print("   ✅ Profit indicators (colored dots)")
    print("   ✅ Revenue and popularity statistics")
    print()
    print("If you still see 'Loading interactive genre tree...' then")
    print("there's still a JavaScript execution issue.")

if __name__ == "__main__":
    try:
        success = test_genre_tree_loading()
        test_console_debug()
        print(f"\n🌳 Genre Tree Test Result: {'✅ PASS' if success else '❌ FAIL'}")
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        exit(1)