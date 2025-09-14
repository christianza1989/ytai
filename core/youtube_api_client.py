#!/usr/bin/env python3
"""
YouTube API Client
Real YouTube Data Integration for Channel Statistics
"""

import os
import logging
from typing import Dict, List, Optional, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from datetime import datetime, timedelta

class YouTubeAPIClient:
    """Professional YouTube API Client for channel statistics and data"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        # Note: API credentials are now provided per-channel, not global
        # Each method accepts api_key parameter for per-channel authentication
    
    def _get_service(self, api_key: str):
        """Create YouTube Data API v3 service with provided API key"""
        try:
            if not api_key:
                self.logger.warning("No YouTube API key provided")
                return None
                
            # Build YouTube Data API v3 service with provided key
            service = build('youtube', 'v3', developerKey=api_key)
            self.logger.info("✅ YouTube API service created successfully")
            return service
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create YouTube API service: {e}")
            # Re-raise the exception so calling methods can handle it properly
            raise e
    
    def test_connection(self, api_key: str = None) -> Dict[str, Any]:
        """Test YouTube API connection and quota"""
        try:
            # Use provided api_key or fallback to environment variable
            if not api_key:
                api_key = os.getenv('YOUTUBE_API_KEY')
                print(f"🔌 No API key provided, using env var: {len(api_key) if api_key else 0} chars")
            else:
                print(f"🔌 Using provided api_key: {len(api_key)} chars")
            
            if not api_key:
                print(f"❌ No API key found in parameters or environment")
                return {
                    'success': False,
                    'error': 'No YouTube API key provided (check environment variables)',
                    'quota_used': 0
                }
                
            youtube_service = self._get_service(api_key)
            if not youtube_service:
                return {
                    'success': False,
                    'error': 'Failed to create YouTube API service. Check API key.',
                    'quota_used': 0
                }
            
            # Simple API call to test connection (costs 1 quota unit)
            response = youtube_service.search().list(
                part='snippet',
                q='test',
                maxResults=1,
                type='video'
            ).execute()
            
            return {
                'success': True,
                'message': 'YouTube API connection successful',
                'quota_used': 100,  # Search costs 100 quota units
                'api_version': 'v3'
            }
            
        except HttpError as e:
            error_details = json.loads(e.content.decode())
            return {
                'success': False,
                'error': f"YouTube API Error: {error_details.get('error', {}).get('message', str(e))}",
                'quota_used': 0
            }
        except Exception as e:
            print(f"❌ Exception in test_connection: {e}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")
            return {
                'success': False,
                'error': f"Connection test failed: {str(e)}",
                'quota_used': 0
            }
    
    def get_channel_statistics(self, channel_id: str, api_key: str = None) -> Dict[str, Any]:
        """
        Get comprehensive channel statistics from YouTube API
        
        Args:
            channel_id: YouTube channel ID (e.g., 'UCqCf7mwxUz4w7rRIh_fLAbg')
            api_key: YouTube Data API v3 key for this specific channel
            
        Returns:
            Dict with channel statistics or error info
        """
        try:
            # Use provided api_key or fallback to environment variable
            if not api_key:
                api_key = os.getenv('YOUTUBE_API_KEY')
                print(f"🔍 Using env YOUTUBE_API_KEY for channel {channel_id}")
                
            if not api_key:
                return {
                    'success': False,
                    'error': 'No YouTube API key provided for this channel (check environment variables)'
                }
                
            youtube_service = self._get_service(api_key)
            if not youtube_service:
                return {
                    'success': False,
                    'error': 'Failed to create YouTube API service. Check API key.'
                }
            
            self.logger.info(f"🔍 Fetching statistics for channel: {channel_id}")
            
            # Get channel statistics (costs 1 quota unit)
            response = youtube_service.channels().list(
                part='statistics,snippet,brandingSettings',
                id=channel_id
            ).execute()
            
            if not response.get('items'):
                return {
                    'success': False,
                    'error': f'Channel not found: {channel_id}'
                }
            
            channel_data = response['items'][0]
            statistics = channel_data.get('statistics', {})
            snippet = channel_data.get('snippet', {})
            branding = channel_data.get('brandingSettings', {})
            
            # Extract comprehensive data
            result = {
                'success': True,
                'channel_id': channel_id,
                'channel_title': snippet.get('title', 'Unknown'),
                'description': snippet.get('description', ''),
                'published_at': snippet.get('publishedAt'),
                'country': snippet.get('country', ''),
                'custom_url': snippet.get('customUrl', ''),
                
                # Statistics (main focus)
                'subscriber_count': int(statistics.get('subscriberCount', 0)),
                'video_count': int(statistics.get('videoCount', 0)),
                'view_count': int(statistics.get('viewCount', 0)),
                'hidden_subscriber_count': statistics.get('hiddenSubscriberCount', False),
                
                # Thumbnails
                'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                'thumbnail_medium': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
                
                # Branding info
                'keywords': branding.get('channel', {}).get('keywords', ''),
                
                # Metadata
                'fetched_at': datetime.now().isoformat(),
                'quota_used': 1
            }
            
            self.logger.info(f"✅ Channel stats: {result['subscriber_count']} subs, {result['video_count']} videos")
            return result
            
        except HttpError as e:
            error_details = json.loads(e.content.decode())
            error_msg = error_details.get('error', {}).get('message', str(e))
            
            self.logger.error(f"❌ YouTube API Error for channel {channel_id}: {error_msg}")
            return {
                'success': False,
                'error': f"YouTube API Error: {error_msg}",
                'channel_id': channel_id
            }
            
        except Exception as e:
            self.logger.error(f"❌ Unexpected error for channel {channel_id}: {e}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'channel_id': channel_id
            }
    
    def get_multiple_channels_statistics(self, channels_data: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Get statistics for multiple channels using their individual API keys
        
        Args:
            channels_data: List of dicts with 'channel_id' and 'api_key' keys
            
        Returns:
            Dict with results for all channels
        """
        try:
            if not channels_data:
                return {
                    'success': True,
                    'results': {},
                    'quota_used': 0
                }
            
            self.logger.info(f"🔍 Fetching statistics for {len(channels_data)} channels")
            
            results = {}
            total_quota_used = 0
            
            # Process each channel individually with its own API key
            for channel_data in channels_data:
                channel_id = channel_data.get('channel_id')
                api_key = channel_data.get('api_key')
                
                if not channel_id or not api_key:
                    results[channel_id] = {
                        'success': False,
                        'error': 'Missing channel ID or API key',
                        'channel_id': channel_id
                    }
                    continue
                
                # Get statistics for this channel
                channel_result = self.get_channel_statistics(channel_id, api_key)
                results[channel_id] = channel_result
                
                if channel_result.get('success'):
                    total_quota_used += channel_result.get('quota_used', 1)
            
            results = {}
            quota_used = 1
            
            for channel_data in response.get('items', []):
                channel_id = channel_data['id']
                statistics = channel_data.get('statistics', {})
                snippet = channel_data.get('snippet', {})
                branding = channel_data.get('brandingSettings', {})
                
                results[channel_id] = {
                    'success': True,
                    'channel_id': channel_id,
                    'channel_title': snippet.get('title', 'Unknown'),
                    'description': snippet.get('description', ''),
                    'published_at': snippet.get('publishedAt'),
                    'country': snippet.get('country', ''),
                    'custom_url': snippet.get('customUrl', ''),
                    
                    # Statistics
                    'subscriber_count': int(statistics.get('subscriberCount', 0)),
                    'video_count': int(statistics.get('videoCount', 0)),
                    'view_count': int(statistics.get('viewCount', 0)),
                    'hidden_subscriber_count': statistics.get('hiddenSubscriberCount', False),
                    
                    # Thumbnails
                    'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    
                    # Metadata
                    'fetched_at': datetime.now().isoformat()
                }
                
                self.logger.info(f"✅ {channel_id}: {results[channel_id]['subscriber_count']} subs")
            
            # Add errors for channels not found
            found_ids = set(results.keys())
            for channel_id in channel_ids:
                if channel_id not in found_ids:
                    results[channel_id] = {
                        'success': False,
                        'error': f'Channel not found: {channel_id}',
                        'channel_id': channel_id
                    }
            
            return {
                'success': True,
                'results': results,
                'quota_used': total_quota_used,
                'channels_processed': len(channels_data),
                'channels_found': len([r for r in results.values() if r.get('success')])
            }
            
        except HttpError as e:
            error_details = json.loads(e.content.decode())
            error_msg = error_details.get('error', {}).get('message', str(e))
            
            self.logger.error(f"❌ YouTube API Error for batch request: {error_msg}")
            return {
                'success': False,
                'error': f"YouTube API Error: {error_msg}",
                'results': {}
            }
            
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in batch request: {e}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'results': {}
            }
    
    def get_recent_videos(self, channel_id: str, api_key: str, max_results: int = 10) -> Dict[str, Any]:
        """Get recent videos from a channel"""
        try:
            # Use provided api_key or fallback to environment variable
            if not api_key:
                api_key = os.getenv('YOUTUBE_API_KEY')
                print(f"🔍 Using env YOUTUBE_API_KEY for channel {channel_id}")
                
            if not api_key:
                return {
                    'success': False,
                    'error': 'No YouTube API key provided for this channel (check environment variables)'
                }
                
            youtube_service = self._get_service(api_key)
            if not youtube_service:
                return {
                    'success': False,
                    'error': 'Failed to create YouTube API service. Check API key.'
                }
            
            # Get channel's uploads playlist
            channels_response = youtube_service.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channels_response.get('items'):
                return {
                    'success': False,
                    'error': f'Channel not found: {channel_id}'
                }
            
            uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get recent videos from uploads playlist
            videos_response = youtube_service.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=max_results
            ).execute()
            
            videos = []
            for item in videos_response.get('items', []):
                video_snippet = item['snippet']
                videos.append({
                    'video_id': video_snippet['resourceId']['videoId'],
                    'title': video_snippet['title'],
                    'published_at': video_snippet['publishedAt'],
                    'thumbnail': video_snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
                    'description': video_snippet.get('description', '')[:200]  # Truncate
                })
            
            return {
                'success': True,
                'videos': videos,
                'quota_used': 2  # 1 for channels + 1 for playlistItems
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error getting recent videos: {str(e)}"
            }
    
    def search_channel_by_username(self, username: str, api_key: str) -> Dict[str, Any]:
        """Search for channel by username and get channel ID"""
        try:
            if not api_key:
                return {
                    'success': False,
                    'error': 'No YouTube API key provided'
                }
                
            youtube_service = self._get_service(api_key)
            if not youtube_service:
                return {
                    'success': False,
                    'error': 'Failed to create YouTube API service. Check API key.'
                }
            
            # Search for channels by username
            response = youtube_service.search().list(
                part='snippet',
                q=username,
                type='channel',
                maxResults=5
            ).execute()
            
            channels = []
            for item in response.get('items', []):
                channels.append({
                    'channel_id': item['snippet']['channelId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet'].get('description', ''),
                    'thumbnail': item['snippet'].get('thumbnails', {}).get('medium', {}).get('url', '')
                })
            
            return {
                'success': True,
                'channels': channels,
                'quota_used': 100  # Search costs 100 units
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error searching channel: {str(e)}"
            }

# Global instance
youtube_client = YouTubeAPIClient()