#!/usr/bin/env python3
"""
Test direct import to see if changes are in the file
"""

import os
import sys
sys.path.append('/home/user/webapp')

def test_admin_app_imports():
    """Test importing admin_app and checking if debug endpoint exists"""
    
    try:
        print("🔍 Importing admin_app...")
        import admin_app
        
        print("✅ Import successful!")
        
        # Check if the Flask app exists
        if hasattr(admin_app, 'app'):
            app = admin_app.app
            print(f"✅ Flask app found: {app}")
            
            # Get all routes
            routes = []
            for rule in app.url_map.iter_rules():
                routes.append(rule.rule)
                
            print(f"📋 Total routes: {len(routes)}")
            
            # Look for our debug route
            debug_route = '/debug/suno-status'
            if debug_route in routes:
                print(f"✅ Debug route found: {debug_route}")
            else:
                print(f"❌ Debug route NOT found: {debug_route}")
                print("🔍 Available routes containing 'debug':")
                debug_routes = [r for r in routes if 'debug' in r.lower()]
                for route in debug_routes:
                    print(f"  - {route}")
                
                print("🔍 Available routes containing 'suno':")
                suno_routes = [r for r in routes if 'suno' in r.lower()]
                for route in suno_routes:
                    print(f"  - {route}")
                    
            # Test SystemState
            if hasattr(admin_app, 'system_state'):
                print("✅ SystemState found")
                system_state = admin_app.system_state
                
                print("🔄 Updating API status...")
                system_state.update_api_status()
                
                suno_status = system_state.api_status.get('suno', {})
                print(f"📊 Suno status: {suno_status}")
                
                if suno_status.get('status') == 'authentication_error':
                    print("✅ SystemState correctly identifies auth error")
                else:
                    print(f"⚠️ SystemState status: {suno_status.get('status')}")
            else:
                print("❌ SystemState not found")
                
        else:
            print("❌ Flask app not found")
            
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Testing Direct Admin App Import")
    print("=" * 50)
    test_admin_app_imports()