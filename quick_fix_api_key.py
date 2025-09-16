#!/usr/bin/env python3
"""
Quick fix script to add YouTube API Key to existing channel
"""

from core.database.youtube_channels_db import YouTubeChannelsDB
import sys

def update_channel_api_key():
    """Update channel with API key"""
    
    print("🔧 YouTube Channel API Key Update")
    print("=" * 40)
    
    # Get API key from user
    api_key = input("Enter your YouTube API Key (starts with 'AIza'): ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
        
    if not api_key.startswith('AIza'):
        print("❌ Invalid API key format. YouTube API keys start with 'AIza'")
        return False
    
    if len(api_key) < 30:
        print("❌ API key too short. YouTube API keys are typically 39+ characters")
        return False
    
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        db = YouTubeChannelsDB()
        channels = db.list_channels()
        
        if not channels:
            print("❌ No channels found in database")
            return False
        
        # Find the channel that needs API key
        target_channel = None
        for channel in channels:
            if not channel.get('api_key'):
                target_channel = channel
                break
        
        if not target_channel:
            print("✅ All channels already have API keys configured")
            return True
            
        channel_id = target_channel['id']
        channel_name = target_channel['channel_name']
        
        print(f"📝 Updating channel: {channel_name} (ID: {channel_id})")
        
        # Update with API key
        result = db.update_channel(channel_id, {'api_key': api_key})
        
        if result['success']:
            print("✅ API key updated successfully!")
            print("🎥 Channel is now ready for video uploads!")
            print("💡 Try uploading your video again from the Music Gallery")
            return True
        else:
            print(f"❌ Update failed: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    update_channel_api_key()