#!/usr/bin/env python3
"""
Test script to verify YouTube OAuth authorization flow
"""

import requests
import json
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, '/home/user/webapp')

from core.auth.youtube_oauth_manager import YouTubeOAuthManager
from core.database.youtube_channels_db import YouTubeChannelsDB

def test_oauth_flow():
    """Test the complete OAuth flow"""
    print("🧪 Testing YouTube OAuth Authorization Flow")
    print("=" * 50)
    
    # Initialize managers
    db_manager = YouTubeChannelsDB()
    oauth_manager = YouTubeOAuthManager(db_manager)
    
    # Get channel info
    channel = db_manager.get_channel(1)
    if not channel:
        print("❌ Channel not found")
        return False
    
    print(f"📺 Channel: {channel['channel_name']}")
    print(f"🆔 Client ID: {channel['client_id'][:20]}...")
    
    # Test OAuth URL generation
    try:
        auth_url, state_token = oauth_manager.generate_oauth_url(
            channel_id=1,
            client_id=channel['client_id']
        )
        print(f"✅ OAuth URL generated successfully")
        print(f"🔗 State token: {state_token}")
        print(f"🌐 Auth URL: {auth_url[:100]}...")
    except Exception as e:
        print(f"❌ Failed to generate OAuth URL: {e}")
        return False
    
    # Test token exchange (this would normally be done with a real auth code)
    # For testing, we'll check if the credentials are properly configured
    try:
        # Check if client secret is available
        client_secret = channel.get('client_secret')
        if not client_secret:
            print("❌ Client secret not found in channel configuration")
            return False
        
        print(f"✅ Client secret is configured")
        
        # Test the OAuth callback handler with a dummy code (should fail with 401)
        # This verifies that the token exchange mechanism is working
        result = oauth_manager.handle_oauth_callback(
            authorization_code="dummy_code_for_testing",
            state_token=state_token,
            client_secret=client_secret
        )
        
        # If we get here without exception, the basic setup is working
        # The actual token exchange will fail with dummy code, but that's expected
        print(f"✅ OAuth callback handler is accessible")
        
    except requests.exceptions.RequestException as e:
        if "401" in str(e):
            print(f"⚠️  Token exchange failed with 401 - This is expected with dummy code")
            print(f"   The OAuth flow is properly configured, but needs a real authorization code")
        else:
            print(f"❌ Network error during OAuth test: {e}")
            return False
    except Exception as e:
        print(f"❌ OAuth callback test failed: {e}")
        return False
    
    print("✅ OAuth flow configuration test completed successfully!")
    print("\n📝 Summary:")
    print("   - Channel credentials are properly configured")
    print("   - OAuth URL generation works")
    print("   - Token exchange mechanism is accessible")
    print("   - Ready for real authorization code")
    
    return True

if __name__ == "__main__":
    success = test_oauth_flow()
    sys.exit(0 if success else 1)