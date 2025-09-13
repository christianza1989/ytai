#!/usr/bin/env python3
"""
Test script to verify Channel Generator is accessible
"""

import requests

def test_channel_generator():
    """Test that Channel Generator is accessible in navigation"""
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    
    print("🧪 Testing Channel Generator Navigation")
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
        
        # Step 2: Check if Channel Generator link exists in navigation
        print("🔍 Step 2: Checking dashboard navigation...")
        dashboard_content = login_post.text
        
        navigation_checks = {
            "Channel Generator Link": "Channel Generator" in dashboard_content,
            "Enhanced Channel Route": "enhanced-channel-creation" in dashboard_content,
            "Generator Icon": "fa-plus-circle" in dashboard_content,
            "AI Badge": "🎯 AI" in dashboard_content
        }
        
        print("\n📋 Navigation Check:")
        all_passed = True
        
        for check_name, passed in navigation_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {'FOUND' if passed else 'MISSING'}")
            if not passed:
                all_passed = False
        
        # Step 3: Try to access Channel Generator page
        print("\n🎯 Step 3: Testing Channel Generator page access...")
        
        channel_gen_response = session.get(f"{base_url}/enhanced-channel-creation")
        
        if channel_gen_response.status_code == 200:
            print("✅ Channel Generator page accessible")
            
            # Check if it has expected content
            content = channel_gen_response.text
            content_checks = [
                "Channel Creation",
                "Enhanced Channel", 
                "AI-powered",
                "Genre Intelligence"
            ]
            
            content_found = sum(1 for check in content_checks if check in content)
            content_percentage = (content_found / len(content_checks)) * 100
            
            print(f"   📋 Content completeness: {content_percentage:.1f}% ({content_found}/{len(content_checks)})")
            
        else:
            print(f"❌ Channel Generator page failed: {channel_gen_response.status_code}")
            all_passed = False
        
        # Step 4: Test Unlimited Empire as well
        print("\n🚀 Step 4: Testing Unlimited Empire page access...")
        
        unlimited_response = session.get(f"{base_url}/unlimited-empire")
        
        if unlimited_response.status_code == 200:
            print("✅ Unlimited Empire page accessible")
        else:
            print(f"❌ Unlimited Empire page failed: {unlimited_response.status_code}")
            all_passed = False
        
        # Summary
        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 CHANNEL GENERATOR TEST PASSED!")
            print("✅ Channel Generator is visible in navigation")
            print("✅ Enhanced Channel Creation page is accessible")
            print("✅ Unlimited Empire is also working")
        else:
            print("⚠️ Some channel generator features need attention")
        
        print(f"\n🌐 Direct URLs:")
        print(f"   📋 Dashboard: {base_url}")
        print(f"   🎯 Channel Generator: {base_url}/enhanced-channel-creation")
        print(f"   🚀 Unlimited Empire: {base_url}/unlimited-empire")
        print("🔑 Login: admin123")
        print("=" * 50)
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_channel_generator()
    if success:
        print("\n🎯 Channel Generator is now accessible!")
    else:
        print("\n💥 Channel Generator access needs fixes!")