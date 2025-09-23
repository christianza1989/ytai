#!/usr/bin/env python3
"""
Test script for enhanced YouTube client functionality
Tests all the new features from youtube_uploader.py
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_youtube_client():
    """Test the enhanced YouTube client"""
    try:
        print("🚀 Testing Enhanced YouTube Client...")
        
        # Import the enhanced client
        from core.services.youtube_client import YouTubeClient
        
        print("📋 Initializing YouTube client...")
        
        # Initialize client (will prompt for OAuth if needed)
        client = YouTubeClient()
        
        print("✅ YouTube client initialized successfully!")
        
        # Test authentication status
        auth_status = client.get_auth_status()
        print(f"🔐 Auth Status: {auth_status}")
        
        if not auth_status['authenticated']:
            print("❌ Authentication required. Please complete OAuth flow.")
            return False
            
        # Test channel statistics
        print("📊 Testing channel statistics...")
        stats = client.get_channel_statistics()
        if stats:
            print(f"📈 Channel: {stats['channel_title']}")
            print(f"👥 Subscribers: {stats['subscriber_count']:,}")
            print(f"🎥 Videos: {stats['video_count']:,}")
            print(f"👀 Views: {stats['view_count']:,}")
        else:
            print("⚠️ Could not retrieve channel statistics")
        
        # Test video listing
        print("📝 Testing video listing...")
        videos = client.list_channel_videos(max_results=3)
        if videos:
            print(f"✅ Found {len(videos)} videos:")
            for i, video in enumerate(videos[:3], 1):
                print(f"  {i}. {video['title'][:50]}...")
        else:
            print("⚠️ No videos found or error occurred")
        
        # Test enhanced upload features
        print("🎥 Testing enhanced upload features...")
        
        # Test upload with scheduling
        print("📅 Testing scheduled upload feature...")
        future_time = datetime.now() + timedelta(hours=2)
        
        # Test upload (if we have a test video file)
        test_video_path = "demo_assets/test_video.mp4"
        if Path(test_video_path).exists():
            print(f"🚀 Testing video upload with scheduling...")
            video_id = client.upload_video(
                video_path=test_video_path,
                title="Test Video - Enhanced Client",
                description="This is a test video uploaded using the enhanced YouTube client with scheduling",
                tags=["test", "enhanced", "client"],
                privacy_status="private",
                publish_at=future_time
            )
            
            if video_id:
                print(f"✅ Video uploaded successfully! ID: {video_id}")
                print(f"🔗 URL: https://www.youtube.com/watch?v={video_id}")
                
                # Test video details retrieval
                print("ℹ️ Testing video details retrieval...")
                details = client.get_video_details(video_id)
                if details:
                    print(f"📋 Title: {details['title']}")
                    print(f"👀 Views: {details['view_count']}")
                    print(f"👍 Likes: {details['like_count']}")
                    print(f"💬 Comments: {details['comment_count']}")
                    print(f"🔒 Privacy: {details['privacy_status']}")
                
                # Test video update
                print("🔄 Testing video metadata update...")
                success = client.update_video_metadata(
                    video_id=video_id,
                    title="Updated Test Video - Enhanced Client",
                    description="Updated description for test video"
                )
                if success:
                    print("✅ Video metadata updated successfully!")
                
                # Test privacy update
                print("🔒 Testing privacy status update...")
                success = client.update_video_privacy(video_id, "unlisted")
                if success:
                    print("✅ Video privacy updated to unlisted!")
                
                # Note: Skipping delete test to preserve the video
                print("⚠️ Skipping delete test to preserve the video")
                
            else:
                print("❌ Video upload failed")
        else:
            print(f"⚠️ Test video file not found: {test_video_path}")
            print("Upload test skipped - no test video available")
        
        print("✅ All enhanced YouTube client tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ YouTube client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_youtube_client()
    sys.exit(0 if success else 1)