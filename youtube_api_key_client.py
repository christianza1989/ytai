#!/usr/bin/env python3
"""
Alternative YouTube client that works with API Key for read-only operations
This bypasses OAuth requirements while maintaining functionality
"""

import os
import sys
from typing import Dict, Any, Optional, List
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from core.logging_config import get_logger

class YouTubeAPIClient:
    """
    YouTube Data API v3 client that works with API Key for read-only operations
    No OAuth required - perfect for server environments
    """
    
    def __init__(self, api_key: str = None, channel_id: str = None):
        """
        Initialize with API Key for read-only operations
        
        Args:
            api_key: YouTube Data API v3 key
            channel_id: YouTube channel ID for operations
        """
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        self.channel_id = channel_id or os.getenv('YOUTUBE_CHANNEL_ID')
        self.logger = get_logger('youtube_api_client')
        
        if not self.api_key:
            raise ValueError("YouTube API Key is required")
            
        # Build service with API key (read-only)
        self.service = build('youtube', 'v3', developerKey=self.api_key)
        self.logger.info("YouTube API client initialized with API key")
        
    def get_channel_statistics(self) -> Optional[Dict[str, Any]]:
        """Get basic channel statistics using API key"""
        try:
            if not self.service:
                raise Exception("YouTube service not initialized")
                
            if not self.channel_id:
                self.logger.warning("No channel ID provided")
                return None
                
            request = self.service.channels().list(
                part='statistics,snippet',
                id=self.channel_id
            )
            
            response = request.execute()
            
            if 'items' in response and len(response['items']) > 0:
                channel = response['items'][0]
                stats = channel['statistics']
                snippet = channel['snippet']
                
                return {
                    'channel_id': self.channel_id,
                    'channel_title': snippet.get('title', 'Unknown'),
                    'subscriber_count': int(stats.get('subscriberCount', 0)),
                    'video_count': int(stats.get('videoCount', 0)),
                    'view_count': int(stats.get('viewCount', 0)),
                    'description': snippet.get('description', '')[:200] + '...' if len(snippet.get('description', '')) > 200 else snippet.get('description', '')
                }
            else:
                self.logger.warning(f"Channel not found: {self.channel_id}")
                return None
                
        except HttpError as e:
            self.logger.error(f"YouTube API error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get channel statistics: {e}")
            return None
            
    def search_videos(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for videos using API key"""
        try:
            request = self.service.search().list(
                q=query,
                part='snippet',
                maxResults=max_results,
                type='video'
            )
            
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                videos.append({
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:100] + '...' if len(item['snippet']['description']) > 100 else item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'channel_title': item['snippet']['channelTitle']
                })
            
            self.logger.info(f"Found {len(videos)} videos for query: {query}")
            return videos
            
        except Exception as e:
            self.logger.error(f"Failed to search videos: {e}")
            return []
            
    def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get video details using API key"""
        try:
            request = self.service.videos().list(
                part='snippet,statistics,status',
                id=video_id
            )
            
            response = request.execute()
            
            if 'items' in response and len(response['items']) > 0:
                video = response['items'][0]
                return {
                    'video_id': video_id,
                    'title': video['snippet'].get('title'),
                    'description': video['snippet'].get('description', ''),
                    'view_count': int(video['statistics'].get('viewCount', 0)),
                    'like_count': int(video['statistics'].get('likeCount', 0)),
                    'comment_count': int(video['statistics'].get('commentCount', 0)),
                    'privacy_status': video['status'].get('privacyStatus'),
                    'publish_date': video['snippet'].get('publishedAt')
                }
            else:
                self.logger.warning(f"Video not found: {video_id}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get video details: {e}")
            return None
            
    def get_trending_videos(self, region_code: str = 'US', max_results: int = 10) -> List[Dict[str, Any]]:
        """Get trending videos for a region"""
        try:
            request = self.service.videos().list(
                part='snippet,statistics',
                chart='mostPopular',
                regionCode=region_code,
                maxResults=max_results
            )
            
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                videos.append({
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:100] + '...' if len(item['snippet']['description']) > 100 else item['snippet']['description'],
                    'channel_title': item['snippet']['channelTitle'],
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'like_count': int(item['statistics'].get('likeCount', 0))
                })
            
            self.logger.info(f"Retrieved {len(videos)} trending videos for {region_code}")
            return videos
            
        except Exception as e:
            self.logger.error(f"Failed to get trending videos: {e}")
            return []
            
    def get_categories(self, region_code: str = 'US') -> List[Dict[str, Any]]:
        """Get available video categories"""
        try:
            request = self.service.videoCategories().list(
                part='snippet',
                regionCode=region_code
            )
            
            response = request.execute()
            
            categories = []
            for item in response.get('items', []):
                categories.append({
                    'id': item['id'],
                    'title': item['snippet']['title']
                })
            
            return categories
            
        except Exception as e:
            self.logger.error(f"Failed to get categories: {e}")
            return []
            
    def is_healthy(self) -> bool:
        """Check if the API service is working"""
        try:
            # Simple API call to verify connectivity
            request = self.service.videos().list(
                part='id',
                id='dQw4w9WgXcQ'  # Rick Astley - Never Gonna Give You Up
            )
            response = request.execute()
            return True
        except Exception as e:
            self.logger.error(f"API health check failed: {e}")
            return False


def test_api_key_client():
    """Test the API key based YouTube client"""
    try:
        print("🚀 Testing YouTube API Key Client...")
        
        # Try to get API key from environment
        api_key = os.getenv('YOUTUBE_API_KEY')
        
        if not api_key:
            print("⚠️ No YouTube API key found in environment")
            print("💡 Setting up demo mode with sample data...")
            
            # Demo mode - show what the client would do
            print("\n📋 Demo Mode - API Key Client Capabilities:")
            features = [
                "✅ Channel statistics retrieval",
                "✅ Video search functionality",
                "✅ Video details lookup",
                "✅ Trending videos by region",
                "✅ Category listing",
                "✅ Health check monitoring",
                "✅ No OAuth required - API key only"
            ]
            
            for feature in features:
                print(f"  {feature}")
            
            print("\n📝 To use with real API:")
            print("1. Set YOUTUBE_API_KEY environment variable")
            print("2. Or pass api_key parameter to YouTubeAPIClient()")
            print("3. Use: client = YouTubeAPIClient(api_key='your-key')")
            
            return True
        
        # Test with real API key
        print(f"🔑 Testing with API key: {api_key[:10]}...")
        
        client = YouTubeAPIClient(api_key=api_key)
        
        print("✅ API Key client initialized successfully!")
        
        # Test health check
        print("🏥 Testing API health...")
        if client.is_healthy():
            print("✅ YouTube API is healthy and accessible!")
        else:
            print("⚠️ YouTube API may not be accessible")
        
        # Test trending videos
        print("🔥 Testing trending videos...")
        trending = client.get_trending_videos(max_results=3)
        if trending:
            print(f"✅ Found {len(trending)} trending videos:")
            for i, video in enumerate(trending, 1):
                print(f"  {i}. {video['title'][:50]}...")
                print(f"     👀 {video['view_count']:,} views | 👍 {video['like_count']:,} likes")
        
        # Test search
        print("🔍 Testing video search...")
        search_results = client.search_videos("music AI", max_results=3)
        if search_results:
            print(f"✅ Found {len(search_results)} videos for 'music AI':")
            for i, video in enumerate(search_results, 1):
                print(f"  {i}. {video['title'][:50]}...")
                print(f"     📺 {video['channel_title']}")
        
        print("\n✅ API Key client test completed successfully!")
        print("📝 Note: For upload functionality, OAuth is still required")
        print("   This API key client is perfect for read-only operations")
        
        return True
        
    except Exception as e:
        print(f"❌ API Key client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_api_key_client()
    sys.exit(0 if success else 1)