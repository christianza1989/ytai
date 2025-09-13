#!/usr/bin/env python3
"""
Debug script to check what's actually being served by the dashboard
"""

import requests

def debug_dashboard():
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    
    # Create session and login
    session = requests.Session()
    
    # Login
    login_data = {'password': 'admin123'}
    login_post = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
    
    if login_post.status_code != 200:
        print(f"Login failed: {login_post.status_code}")
        return
    
    # Get dashboard content
    dashboard_content = login_post.text
    
    # Check specific dark mode elements
    checks = [
        ("toggleTheme function", "function toggleTheme()"),
        ("localStorage.setItem", "localStorage.setItem"),
        ("body.dark-theme", "body.dark-theme"),
        (".dark-theme .card", ".dark-theme .card"),
        ("theme toggle onclick", 'onclick="toggleTheme()"'),
        ("DOMContentLoaded listener", "DOMContentLoaded")
    ]
    
    print("🔍 Searching for dark mode elements in dashboard HTML:\n")
    
    for name, search_term in checks:
        found = search_term in dashboard_content
        status = "✅ FOUND" if found else "❌ MISSING"
        print(f"{status} {name}")
        
        if found:
            # Find the line context
            lines = dashboard_content.split('\n')
            for i, line in enumerate(lines):
                if search_term in line:
                    print(f"   Line {i+1}: {line.strip()[:100]}...")
                    break
        print()
    
    # Check if admin_base.html is being used
    if "admin_base.html" in dashboard_content or "AI Music Empire" in dashboard_content:
        print("✅ Using admin_base.html template")
    else:
        print("❌ Not using admin_base.html template")
    
    # Save a portion of the dashboard content for inspection
    with open('/home/user/webapp/dashboard_debug.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_content)
    
    print(f"\n📄 Saved full dashboard HTML to dashboard_debug.html for inspection")
    
    # Check for specific script sections
    if "<script>" in dashboard_content:
        print("\n📜 JavaScript sections found in the page")
        script_sections = dashboard_content.split('<script>')
        for i, section in enumerate(script_sections[1:], 1):
            script_end = section.find('</script>')
            if script_end > 0:
                script_content = section[:script_end]
                if "toggleTheme" in script_content:
                    print(f"   Script {i}: Contains toggleTheme function")
                    # Show a snippet
                    toggle_start = script_content.find("function toggleTheme")
                    if toggle_start >= 0:
                        snippet = script_content[toggle_start:toggle_start+200]
                        print(f"   Snippet: {snippet}...")

if __name__ == "__main__":
    debug_dashboard()