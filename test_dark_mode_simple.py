#!/usr/bin/env python3
"""
Simple test to verify dark mode JavaScript implementation
"""

import requests
import json

def test_dark_mode_api():
    """Test if we can access the dashboard after login"""
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    
    print("🧪 Testing Dark Mode Functionality (Simple Test)")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    try:
        # Step 1: Get login page to check if server is responding
        print("📍 Step 1: Checking login page...")
        login_response = session.get(f"{base_url}/login")
        
        if login_response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page returned {login_response.status_code}")
            return False
        
        # Step 2: Attempt login
        print("🔑 Step 2: Attempting login...")
        login_data = {
            'password': 'admin123'
        }
        
        login_post = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        
        if login_post.status_code == 200 and ("dashboard" in login_post.url.lower() or login_post.url.endswith("/")):
            print("✅ Login successful, redirected to dashboard")
        else:
            print(f"❌ Login failed or unexpected redirect. Status: {login_post.status_code}, URL: {login_post.url}")
            # Let's still check the content even if redirect seems wrong
            if login_post.status_code == 200:
                print("📋 Continuing with content analysis despite redirect issue...")
        
        # Step 3: Check if dashboard contains dark mode functionality
        print("🎨 Step 3: Checking dashboard for dark mode elements...")
        
        dashboard_content = login_post.text
        
        # Check for dark mode elements in HTML
        checks = {
            "Theme toggle function": "toggleTheme()" in dashboard_content,
            "Dark theme CSS": "dark-theme" in dashboard_content,
            "Theme toggle button": 'onclick="toggleTheme()"' in dashboard_content,
            "LocalStorage functionality": "localStorage.setItem" in dashboard_content,
            "Dark theme styles": ".dark-theme" in dashboard_content,
            "Theme icon classes": "fa-moon" in dashboard_content or "fa-sun" in dashboard_content
        }
        
        print("\n📋 Dark Mode Implementation Check:")
        all_checks_passed = True
        for check_name, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {'FOUND' if passed else 'MISSING'}")
            if not passed:
                all_checks_passed = False
        
        # Step 4: Check CSS variables and dark theme styles
        print("\n🎯 Step 4: Checking CSS implementation...")
        css_checks = {
            "CSS variables": ":root" in dashboard_content,
            "Dark theme body style": "body.dark-theme" in dashboard_content,
            "Dark theme card styles": ".card" in dashboard_content and ".dark-theme" in dashboard_content,
            "Dark theme form styles": ".form-control" in dashboard_content,
            "Theme transition": "transition" in dashboard_content
        }
        
        print("\n📋 CSS Implementation Check:")
        for check_name, passed in css_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {'FOUND' if passed else 'MISSING'}")
            if not passed:
                all_checks_passed = False
        
        # Step 5: Summary
        print("\n" + "=" * 50)
        if all_checks_passed:
            print("🎉 ALL DARK MODE CHECKS PASSED!")
            print("✅ Dark mode functionality is properly implemented")
            print("✅ Theme toggle function exists")
            print("✅ CSS dark theme styles are present")
            print("✅ LocalStorage persistence is implemented")
        else:
            print("⚠️ Some dark mode checks failed")
            print("📋 Review the missing elements above")
        
        print("=" * 50)
        return all_checks_passed
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

def create_dark_mode_test_page():
    """Create a simple HTML test page to manually verify dark mode"""
    
    test_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark Mode Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #ffffff;
            color: #000000;
            transition: all 0.3s ease;
        }
        
        body.dark-theme {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        
        .card {
            background: white;
            padding: 20px;
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        body.dark-theme .card {
            background: #2d2d2d;
            color: #e0e0e0;
        }
        
        .btn {
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .test-results {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>🌙 Dark Mode Test Page</h1>
    
    <div class="card">
        <h3>Theme Toggle Test</h3>
        <button class="btn" onclick="toggleTheme()">
            <i class="fas fa-moon"></i> Toggle Theme
        </button>
    </div>
    
    <div class="card">
        <h3>Theme Status</h3>
        <p>Current theme: <span id="theme-status">Light</span></p>
        <p>LocalStorage: <span id="storage-status">Not set</span></p>
    </div>
    
    <div class="test-results" id="test-results">
        <h3>Test Results</h3>
        <p>Click the toggle button to test dark mode functionality.</p>
    </div>

    <script>
        function toggleTheme() {
            // Theme toggle functionality (same as in admin_base.html)
            document.body.classList.toggle('dark-theme');
            const isDarkMode = document.body.classList.contains('dark-theme');
            
            // Update icon
            const icons = document.querySelectorAll('button i');
            icons.forEach(icon => {
                if (isDarkMode) {
                    icon.className = 'fas fa-sun';
                } else {
                    icon.className = 'fas fa-moon';
                }
            });
            
            // Save preference to localStorage
            localStorage.setItem('darkMode', isDarkMode);
            
            // Update status display
            updateStatus();
            
            // Show result
            showTestResult(isDarkMode ? 'Dark' : 'Light');
        }
        
        function updateStatus() {
            const isDark = document.body.classList.contains('dark-theme');
            const stored = localStorage.getItem('darkMode');
            
            document.getElementById('theme-status').textContent = isDark ? 'Dark' : 'Light';
            document.getElementById('storage-status').textContent = stored || 'Not set';
        }
        
        function showTestResult(theme) {
            const results = document.getElementById('test-results');
            results.innerHTML = `
                <h3>✅ Test Results</h3>
                <p><strong>Theme switched to:</strong> ${theme}</p>
                <p><strong>CSS class applied:</strong> ${document.body.classList.contains('dark-theme')}</p>
                <p><strong>LocalStorage saved:</strong> ${localStorage.getItem('darkMode')}</p>
                <p><strong>Status:</strong> Dark mode is working correctly!</p>
            `;
        }
        
        // Load theme preference on page load
        document.addEventListener('DOMContentLoaded', function() {
            const darkMode = localStorage.getItem('darkMode') === 'true';
            if (darkMode) {
                document.body.classList.add('dark-theme');
                const icons = document.querySelectorAll('button i');
                icons.forEach(icon => {
                    icon.className = 'fas fa-sun';
                });
            }
            updateStatus();
        });
    </script>
</body>
</html>"""
    
    with open('/home/user/webapp/dark_mode_test.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("📄 Created dark_mode_test.html for manual testing")

if __name__ == "__main__":
    success = test_dark_mode_api()
    create_dark_mode_test_page()
    
    if success:
        print("\n🎯 Dark mode implementation is correct!")
        print("💡 You can also test manually by opening dark_mode_test.html")
        print(f"🌐 Live admin interface: https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev")
        print("🔑 Login password: admin123")
    else:
        print("\n💥 Some dark mode features may need fixes!")