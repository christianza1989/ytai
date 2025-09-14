#!/usr/bin/env python3
"""
Check current dashboard status to see if fixes are applied
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_suno_client():
    """Check SunoClient methods"""
    try:
        sys.path.append('/home/user/webapp')
        from core.services.suno_client import SunoClient
        
        print("🔍 Testing SunoClient...")
        suno = SunoClient()
        
        # Check if new method exists
        if hasattr(suno, 'get_credits_with_status'):
            print("✅ get_credits_with_status method EXISTS")
            status = suno.get_credits_with_status()
            print(f"📊 Status result: {json.dumps(status, indent=2)}")
        else:
            print("❌ get_credits_with_status method NOT FOUND")
            
        return status if hasattr(suno, 'get_credits_with_status') else None
        
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_admin_app():
    """Check admin_app update_api_status method"""
    try:
        sys.path.append('/home/user/webapp')
        
        # Import the system state from admin_app
        import admin_app
        
        print("\n🔍 Testing admin_app SystemState...")
        system_state = admin_app.system_state
        
        # Call update_api_status
        system_state.update_api_status()
        
        print(f"📊 Suno API status: {json.dumps(system_state.api_status.get('suno', {}), indent=2)}")
        
        return system_state.api_status.get('suno', {})
        
    except Exception as e:
        print(f"💥 Error checking admin_app: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🔍 Checking Current Status Implementation")
    print("=" * 60)
    
    # Check SunoClient
    suno_status = check_suno_client()
    
    # Check admin_app
    admin_status = check_admin_app()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY:")
    
    if suno_status:
        if suno_status.get('status') == 'authentication_error':
            print("✅ SunoClient correctly identifies auth error")
        else:
            print(f"⚠️ SunoClient status: {suno_status.get('status')}")
    else:
        print("❌ SunoClient check failed")
        
    if admin_status:
        if admin_status.get('status') == 'authentication_error':
            print("✅ admin_app correctly identifies auth error")
        else:
            print(f"⚠️ admin_app status: {admin_status.get('status')}")
            print(f"   Credits: {admin_status.get('credits')}")
            print(f"   Error: {admin_status.get('error')}")
    else:
        print("❌ admin_app check failed")