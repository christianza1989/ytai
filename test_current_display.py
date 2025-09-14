#!/usr/bin/env python3
"""
Test what the user would actually see in the browser
"""

import requests
from bs4 import BeautifulSoup

def test_live_api_config():
    """Test what the live API config page shows"""
    print("🌐 Testing live API configuration display...")
    
    try:
        session = requests.Session()
        
        # Login
        login_response = session.post("http://localhost:5000/login", data={"password": "admin123"})
        
        if login_response.status_code in [200, 302]:
            print("✅ Login successful")
            
            # Get API config page
            config_response = session.get("http://localhost:5000/api-config")
            
            if config_response.status_code == 200:
                print("✅ API config page loaded")
                
                # Parse HTML to check input field values
                soup = BeautifulSoup(config_response.text, 'html.parser')
                
                # Check Suno API key input
                suno_input = soup.find('input', {'id': 'sunoApiKey'})
                if suno_input:
                    suno_value = suno_input.get('value', '')
                    suno_configured = suno_input.get('data-configured', 'false')
                    suno_masked = suno_input.get('data-masked-value', '')
                    print(f"🔑 Suno API Key field:")
                    print(f"   Value: '{suno_value}'")
                    print(f"   Configured: {suno_configured}")
                    print(f"   Masked value: '{suno_masked}'")
                    print(f"   Readonly: {suno_input.has_attr('readonly')}")
                
                # Check Gemini API key input  
                gemini_input = soup.find('input', {'id': 'geminiApiKey'})
                if gemini_input:
                    gemini_value = gemini_input.get('value', '')
                    gemini_configured = gemini_input.get('data-configured', 'false')
                    gemini_masked = gemini_input.get('data-masked-value', '')
                    print(f"🧠 Gemini API Key field:")
                    print(f"   Value: '{gemini_value}'")
                    print(f"   Configured: {gemini_configured}")
                    print(f"   Masked value: '{gemini_masked}'")
                    print(f"   Readonly: {gemini_input.has_attr('readonly')}")
                
                # Check for presence of Edit buttons
                edit_buttons = soup.find_all('button', string=lambda text: text and 'Edit' in text)
                print(f"✏️ Edit buttons found: {len(edit_buttons)}")
                
                # Check API status indicators
                status_badges = soup.find_all(class_='status-badge')
                print(f"🔄 Status badges found: {len(status_badges)}")
                for badge in status_badges:
                    print(f"   Status: {badge.get_text().strip()}")
                
                # Check for error indicators
                if 'not_configured' in config_response.text:
                    print("⚠️ 'not_configured' text found in page")
                if 'admin123' in config_response.text:
                    print("⚠️ 'admin123' text found in page")
                else:
                    print("✅ No 'admin123' placeholder found")
                    
            else:
                print(f"❌ Could not load API config page: {config_response.status_code}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_live_api_config()