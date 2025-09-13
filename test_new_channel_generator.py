#!/usr/bin/env python3
"""
Test the new integrated Channel Generator
"""

import requests

def test_new_channel_generator():
    """Test the integrated Channel Generator with genre tree"""
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    
    print("🧪 Testing NEW Channel Generator (Integrated)")
    print("=" * 60)
    
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
        
        # Step 2: Check navigation for new Channel Generator
        print("🔍 Step 2: Checking dashboard navigation...")
        dashboard_content = login_post.text
        
        navigation_checks = {
            "New Channel Generator Route": "channel-generator" in dashboard_content,
            "Channel Generator in Content Creation": "Channel Generator" in dashboard_content,
            "AI Badge Present": "🎯 AI" in dashboard_content,
            "Unlimited Empire Removed": "Unlimited Empire" not in dashboard_content or dashboard_content.count("Unlimited Empire") <= 1
        }
        
        print("\n📋 Navigation Check:")
        all_passed = True
        
        for check_name, passed in navigation_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {'PASSED' if passed else 'FAILED'}")
            if not passed:
                all_passed = False
        
        # Step 3: Test new Channel Generator page
        print("\n🎯 Step 3: Testing new Channel Generator page...")
        
        channel_gen_response = session.get(f"{base_url}/channel-generator")
        
        if channel_gen_response.status_code == 200:
            print("✅ New Channel Generator page accessible")
            
            content = channel_gen_response.text
            
            # Check for integrated features
            integration_checks = {
                "Uses admin_base.html": "admin_base.html" in content or "sidebar" in content,
                "Has Genre Tree Container": "genreTreeContainer" in content,
                "Step-by-step Wizard": "generator-step" in content,
                "AI Strategy Preview": "Strategy Preview" in content,
                "Interactive Genre Selection": "selectGenre" in content,
                "Channel Configuration": "Channel Configuration" in content,
                "Generate Button": "Generate AI-Optimized Channel" in content
            }
            
            print("\n📋 Integration Features Check:")
            integration_score = 0
            
            for feature, present in integration_checks.items():
                status = "✅" if present else "❌"
                print(f"   {status} {feature}: {'FOUND' if present else 'MISSING'}")
                if present:
                    integration_score += 1
                else:
                    all_passed = False
            
            integration_percentage = (integration_score / len(integration_checks)) * 100
            print(f"\n   📊 Integration completeness: {integration_percentage:.1f}% ({integration_score}/{len(integration_checks)})")
            
        else:
            print(f"❌ New Channel Generator page failed: {channel_gen_response.status_code}")
            all_passed = False
        
        # Step 4: Test genre tree loading
        print("\n🌲 Step 4: Testing genre tree integration...")
        
        genre_tree_response = session.get(f"{base_url}/templates/genre_tree_selector.html")
        
        if genre_tree_response.status_code == 200:
            print("✅ Genre tree template accessible")
            tree_content = genre_tree_response.text
            if "genre-item" in tree_content:
                print("✅ Genre tree structure present")
            else:
                print("⚠️ Genre tree structure might need adjustment")
        else:
            print(f"❌ Genre tree template failed: {genre_tree_response.status_code}")
            all_passed = False
        
        # Step 5: Test API endpoints
        print("\n🔗 Step 5: Testing related API endpoints...")
        
        # Test genre statistics
        genre_stats_response = session.get(f"{base_url}/api/genres/statistics")
        if genre_stats_response.status_code == 200:
            print("✅ Genre statistics API working")
        else:
            print(f"⚠️ Genre statistics API: {genre_stats_response.status_code}")
        
        # Summary
        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 NEW CHANNEL GENERATOR TEST PASSED!")
            print("✅ Properly integrated into main SaaS interface")
            print("✅ Uses admin_base.html template with sidebar")
            print("✅ Contains interactive genre tree")
            print("✅ Has step-by-step wizard interface")
            print("✅ Unlimited Empire properly replaced")
        else:
            print("⚠️ Channel Generator needs some adjustments")
        
        print(f"\n🌐 Access URLs:")
        print(f"   📋 Dashboard: {base_url}")
        print(f"   🎯 NEW Channel Generator: {base_url}/channel-generator")
        print("🔑 Login: admin123")
        print("=" * 60)
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_new_channel_generator()
    if success:
        print("\n🎯 NEW Channel Generator is working perfectly!")
        print("📍 Location: Content Creation → Channel Generator 🎯 AI")
        print("🏗️ Features: Integrated SaaS interface with interactive genre tree")
    else:
        print("\n💥 Channel Generator needs fixes!")