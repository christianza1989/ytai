#!/usr/bin/env python3
"""
Create a test YouTube channel for testing video upload functionality
"""

import json
import requests
import sys

def create_test_youtube_channel():
    """Create a test YouTube channel with proper configuration"""
    
    # Test channel data
    channel_data = {
        "channel_name": "AI Music Studio Test",
        "channel_url": "https://youtube.com/channel/test",
        "youtube_channel_id": "UCTestChannelId123",
        "description": "Test channel for AI-generated music content",
        
        # API credentials (test values)
        "api_key": "test_youtube_api_key_12345",
        "client_id": "test_client_id.apps.googleusercontent.com",
        "client_secret": "test_client_secret_abc123",
        
        # Genre selection
        "selected_genres": ["electronic", "lo-fi", "ambient", "chill"],
        
        # Upload configuration
        "style": "chill-electronic",
        "upload_schedule": "daily",
        "upload_hours": [
            {"hour": 14, "minute": 0, "vocal_probability": 0.8},
            {"hour": 18, "minute": 30, "vocal_probability": 0.6},
            {"hour": 20, "minute": 0, "vocal_probability": 0.7}
        ],
        
        # Content settings
        "content_strategy": "consistent-quality",
        "target_audience": "study-relaxation",
        "branding_style": "minimal-modern",
        
        # Statistics (mock data)
        "subscribers": 1250,
        "total_videos": 45,
        "average_views": 850,
        "performance_score": 0.75,
        
        # Automation settings
        "automation_enabled": True,
        "auto_upload": True,
        "auto_optimize": True,
        "batch_size": 5,
        
        # Status
        "status": "active",
        "last_upload": "2025-09-15T10:30:00"
    }
    
    # Make API request to create channel
    try:
        response = requests.post(
            'http://localhost:3000/api/youtube/channels/save',
            json=channel_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Test YouTube channel created successfully!")
                print(f"📺 Channel: {channel_data['channel_name']}")
                print(f"🎯 Style: {channel_data['style']}")
                print(f"📅 Schedule: {channel_data['upload_schedule']}")
                print(f"🎵 Genres: {', '.join(channel_data['selected_genres'])}")
                print(f"👥 Subscribers: {channel_data['subscribers']}")
                return True
            else:
                print(f"❌ Failed to create channel: {result.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask application is running on port 3000")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = create_test_youtube_channel()
    sys.exit(0 if success else 1)