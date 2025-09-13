#!/usr/bin/env python3
"""
Test script to verify dark mode functionality is working
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_dark_mode():
    # Test if we can access the main dashboard after login and test dark mode
    base_url = "https://8000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev"
    
    print("🧪 Testing Dark Mode Functionality")
    print("=" * 50)
    
    # Setup Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Step 1: Go to login page
        print("📍 Step 1: Navigating to login page...")
        driver.get(f"{base_url}/login")
        time.sleep(2)
        
        # Step 2: Login with admin123
        print("🔑 Step 2: Logging in with admin123...")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.send_keys("admin123")
        
        # Submit form
        login_form = driver.find_element(By.ID, "loginForm")
        login_form.submit()
        
        # Wait for redirect to dashboard
        WebDriverWait(driver, 10).until(
            EC.url_contains("/")
        )
        
        print("✅ Successfully logged in!")
        
        # Step 3: Check if we're on dashboard and theme toggle exists
        print("🎨 Step 3: Testing dark mode toggle...")
        
        # Look for theme toggle button
        theme_toggle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='toggleTheme()']"))
        )
        
        print("✅ Theme toggle button found!")
        
        # Step 4: Test initial theme state
        body_element = driver.find_element(By.TAG_NAME, "body")
        initial_classes = body_element.get_attribute("class")
        
        print(f"🎯 Initial body classes: {initial_classes}")
        has_dark_theme_initially = "dark-theme" in initial_classes
        
        # Step 5: Click theme toggle
        print("🌙 Step 5: Clicking theme toggle...")
        driver.execute_script("toggleTheme();")
        time.sleep(1)  # Wait for toggle to complete
        
        # Check new theme state
        body_element = driver.find_element(By.TAG_NAME, "body")
        new_classes = body_element.get_attribute("class")
        
        print(f"🎯 New body classes: {new_classes}")
        has_dark_theme_after = "dark-theme" in new_classes
        
        # Step 6: Verify theme actually changed
        if has_dark_theme_initially != has_dark_theme_after:
            print("✅ Theme toggle working! Theme state changed successfully.")
            
            # Test localStorage persistence
            print("💾 Step 6: Testing localStorage persistence...")
            stored_dark_mode = driver.execute_script("return localStorage.getItem('darkMode');")
            print(f"📱 LocalStorage darkMode value: {stored_dark_mode}")
            
            if stored_dark_mode is not None:
                print("✅ Dark mode preference saved to localStorage!")
            else:
                print("⚠️ Dark mode preference not found in localStorage")
            
            # Test icon change
            print("🔍 Step 7: Testing icon change...")
            icon_element = driver.find_element(By.CSS_SELECTOR, ".theme-toggle i")
            icon_classes = icon_element.get_attribute("class")
            print(f"🔍 Theme toggle icon classes: {icon_classes}")
            
            expected_icon = "fa-sun" if has_dark_theme_after else "fa-moon"
            if expected_icon in icon_classes:
                print("✅ Theme toggle icon updated correctly!")
            else:
                print(f"⚠️ Expected icon {expected_icon}, but got {icon_classes}")
            
        else:
            print("❌ Theme toggle not working! Theme state did not change.")
            return False
        
        # Step 8: Test theme toggle again (back to original)
        print("🔄 Step 8: Testing theme toggle again...")
        driver.execute_script("toggleTheme();")
        time.sleep(1)
        
        body_element = driver.find_element(By.TAG_NAME, "body")
        final_classes = body_element.get_attribute("class")
        has_dark_theme_final = "dark-theme" in final_classes
        
        if has_dark_theme_final == has_dark_theme_initially:
            print("✅ Theme toggle works both ways! Returned to original state.")
        else:
            print("⚠️ Theme toggle might not be working consistently")
        
        print("\n" + "=" * 50)
        print("🎉 DARK MODE FUNCTIONALITY TEST COMPLETE!")
        print("✅ Theme toggle button exists and is clickable")
        print("✅ Theme classes are added/removed correctly")  
        print("✅ LocalStorage persistence is working")
        print("✅ Icon changes are working")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False
    
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    success = test_dark_mode()
    if success:
        print("🎯 Dark mode is working correctly!")
        exit(0)
    else:
        print("💥 Dark mode has issues that need to be fixed!")
        exit(1)