import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.http import MediaFileUpload

from core.logging_config import get_logger

class YouTubeClient:
    """YouTube Data API v3 client with Progressive Authorization (API Key + OAuth) and Enhanced Upload Features"""

    # YouTube API scopes - Updated for current Google API requirements
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube.readonly',
        'https://www.googleapis.com/auth/youtube'
    ]

    def __init__(self, client_secrets_path=None, channel_id=None, api_key=None):
        """
        Initialize YouTube client with multiple authentication methods
        
        Args:
            client_secrets_path: Path to OAuth client secrets (for upload)
            channel_id: YouTube channel ID
            api_key: YouTube API key (for read-only operations)
        """
        self.channel_id = channel_id or os.getenv('YOUTUBE_CHANNEL_ID')
        self.client_secrets_path = client_secrets_path or os.getenv('YOUTUBE_CLIENT_SECRETS_PATH', 'configs/client_secrets.json')
        self.token_path = 'token.pickle'
        self.logger = get_logger('youtube_client')
        
        # Try API key mode first (read-only)
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        self.service = None
        self.credentials = None
        self.read_only = True
        
        # Initialize with appropriate method
        if self.api_key:
            self._authenticate_api_key()
        else:
            # Try OAuth for full functionality
            try:
                self._authenticate_oauth()
                self.read_only = False
            except Exception as e:
                self.logger.warning(f"OAuth authentication failed, falling back to read-only mode: {e}")
                if self.api_key:
                    self._authenticate_api_key()
                else:
                    raise Exception("No valid authentication method available. Provide API key or set up OAuth.")

    def _has_oauth_config(self):
        """Check if OAuth configuration is available"""
        return bool(self.client_secrets_path and Path(self.client_secrets_path).exists())

    def _authenticate_api_key(self) -> None:
        """Authenticate using API key for read-only operations"""
        try:
            if not self.api_key:
                raise ValueError("API key is required for API key authentication")
                
            self.service = build('youtube', 'v3', developerKey=self.api_key)
            self.logger.info("YouTube API service initialized with API key (read-only)")
            print("🔑 YouTube API service initialized with API key (read-only mode)")
            
        except Exception as e:
            self.logger.error(f"API key authentication failed: {e}")
            raise Exception(f"API key authentication failed: {e}")
            
    def _authenticate_oauth(self) -> None:
        """Handle OAuth 2.0 authentication flow with enhanced error handling and credential refresh"""
        try:
            # Load existing credentials if available
            if Path(self.token_path).exists():
                self.logger.info("Loading existing YouTube credentials...")
                with open(self.token_path, 'rb') as token:
                    self.credentials = pickle.load(token)

            # Refresh expired credentials with enhanced error handling
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                try:
                    self.logger.info("Refreshing expired YouTube credentials...")
                    self.credentials.refresh(Request())
                    # Save refreshed credentials
                    with open(self.token_path, 'wb') as token:
                        pickle.dump(self.credentials, token)
                    self.logger.info("Credentials refreshed successfully.")
                except RefreshError as e:
                    self.logger.error(f"Failed to refresh credentials: {e}")
                    # Remove invalid token file
                    if Path(self.token_path).exists():
                        Path(self.token_path).unlink()
                    self.credentials = None

            # Check if we need new authentication
            if not self.credentials or not self.credentials.valid:
                if not self._has_oauth_config():
                    # Don't fail if no OAuth config, just use API key mode
                    self.logger.info("No OAuth configuration found, using API key mode")
                    if self.api_key:
                        return self._authenticate_api_key()
                    else:
                        raise FileNotFoundError(f"OAuth client secrets file not found: {self.client_secrets_path}")

                self.logger.info("Starting YouTube OAuth 2.0 authentication...")
                print("🔐 Starting YouTube OAuth 2.0 authentication...")
                print("📋 A browser window will open for you to authorize the application")

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_path,
                    self.SCOPES
                )

                # Run local server for OAuth callback with timeout
                self.credentials = flow.run_local_server(port=8080, timeout=120)

                # Save credentials for future use
                with open(self.token_path, 'wb') as token:
                    pickle.dump(self.credentials, token)

                print("✅ OAuth authentication successful! Credentials saved.")
                self.logger.info("OAuth authentication successful")

            # Build YouTube API service with full permissions
            self.service = build('youtube', 'v3', credentials=self.credentials)
            print("🎥 YouTube API service initialized with full upload permissions")
            self.logger.info("YouTube API service initialized")

        except Exception as e:
            self.logger.error(f"OAuth authentication failed: {e}")
            # Try to fall back to API key if available
            if self.api_key:
                self.logger.info("Falling back to API key authentication")
                return self._authenticate_api_key()
            else:
                print(f"❌ OAuth authentication failed: {e}")
                raise Exception(f"YouTube OAuth setup required for upload functionality: {e}")

    def get_channel_statistics(self) -> Optional[Dict[str, Any]]:
        """Get basic channel statistics"""
        try:
            if not self.service:
                raise Exception("YouTube service not initialized")

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
                print(f"❌ Channel not found: {self.channel_id}")
                return None

        except HttpError as e:
            print(f"❌ YouTube API error: {e}")
            return None
        except Exception as e:
            print(f"❌ Failed to get channel statistics: {e}")
            return None

    def can_upload(self) -> bool:
        """Check if upload is possible (requires OAuth)"""
        return self.credentials is not None and self.service is not None and not self.read_only

    def get_auth_status(self) -> dict:
        """Get current authorization status"""
        return {
            'authenticated': bool(self.service),
            'can_upload': self.can_upload(),
            'has_oauth': bool(self.credentials),
            'has_api_key': bool(self.api_key),
            'service_initialized': bool(self.service),
            'token_valid': bool(self.credentials and not self.credentials.expired) if self.credentials else False,
            'read_only_mode': self.read_only
        }

    def upload_video(self, video_path: str, title: str, description: str,
                    tags: list = None, category_id: str = '10',
                    privacy_status: str = 'private', publish_at: Optional[datetime] = None) -> Optional[str]:
        """
        Upload video to YouTube with enhanced features including scheduling and progress tracking

        Args:
            video_path: Path to the video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID (10 = Music)
            privacy_status: 'public', 'private', or 'unlisted'
            publish_at: Optional datetime for scheduled publishing (forces privacy_status='private')

        Returns:
            Video ID if successful, None otherwise
        """
        try:
            if not self.can_upload():
                raise Exception("Upload requires OAuth authorization. Please complete OAuth setup first.")

            if not self.service:
                raise Exception("YouTube service not initialized")

            if not Path(video_path).exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")

            # Get file size for progress calculation
            file_size = Path(video_path).stat().st_size
            self.logger.info(f"Uploading video: {title[:50]}...")
            print(f"📤 Uploading video: {title}")
            print(f"📁 File: {video_path}")
            print(f"📊 File size: {file_size / (1024*1024):.1f} MB")

            # Nustatome privatumo būseną. Jei nurodytas 'publish_at', vaizdo įrašas PRIVALO būti 'private'.
            final_privacy_status = "private" if publish_at else privacy_status

            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title[:100],  # YouTube title limit
                    'description': description[:5000],  # YouTube description limit
                    'tags': tags or [],
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': final_privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }

            # Add scheduled publishing if provided
            if publish_at:
                # Ensure publish time is at least 5 minutes in the future
                min_publish = datetime.now() + timedelta(minutes=5)
                if publish_at < min_publish:
                    self.logger.warning(f"Scheduled time {publish_at} is too soon, adjusting to {min_publish}")
                    publish_at = min_publish
                body["status"]["publishAt"] = publish_at.strftime('%Y-%m-%dT%H:%M:%SZ')
                self.logger.info(f"Video scheduled for: {publish_at}")
                print(f"📅 Video scheduled for: {publish_at}")

            # Create media upload request with resumable upload
            media = MediaFileUpload(
                video_path,
                chunksize=1024*1024,  # 1MB chunks
                resumable=True,
                mimetype='video/mp4'
            )

            # Create upload request
            request = self.service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )

            # Execute upload with progress tracking
            response = None
            uploaded_bytes = 0

            while response is None:
                try:
                    status, response = request.next_chunk()
                    if status:
                        uploaded_bytes = status.resumable_progress
                        progress = (uploaded_bytes / file_size) * 100
                        print(f"📈 Upload progress: {progress:.1f}%")
                        self.logger.info(f"Upload progress: {progress:.1f}%")
                except Exception as e:
                    print(f"⚠️ Upload chunk failed, retrying: {e}")
                    self.logger.warning(f"Upload chunk failed, retrying: {e}")
                    continue

            if response:
                video_id = response.get('id')
                if video_id:
                    print(f"✅ Video uploaded successfully! ID: {video_id}")
                    print(f"🔗 Video URL: https://www.youtube.com/watch?v={video_id}")
                    print(f"🔒 Privacy status: {final_privacy_status}")
                    if publish_at:
                        print(f"📅 Scheduled for: {publish_at}")
                    self.logger.info(f"Video uploaded successfully: {video_id}")
                    return video_id
                else:
                    self.logger.error("Upload completed but no video ID received")
                    print("❌ Upload completed but no video ID received")
                    return None
            else:
                self.logger.error("Upload failed - no response received")
                print("❌ Upload failed - no response received")
                return None

        except HttpError as e:
            error_code = e.resp.status if hasattr(e, 'resp') else 'Unknown'
            if error_code == 403:
                print("❌ Upload quota exceeded or insufficient permissions")
                self.logger.error(f"Upload quota exceeded or permissions error: {e}")
            elif error_code == 400:
                print("❌ Bad request - check video file format and metadata")
                self.logger.error(f"Bad request error: {e}")
            else:
                print(f"❌ YouTube API upload error ({error_code}): {e}")
                self.logger.error(f"YouTube API upload error ({error_code}): {e}")
            return None
        except Exception as e:
            print(f"❌ Failed to upload video: {e}")
            self.logger.error(f"Failed to upload video: {e}")
            self.logger.error(f"Exception type: {type(e)}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    def update_video_privacy(self, video_id: str, privacy_status: str = "public") -> bool:
        """
        Update video privacy status.

        Args:
            video_id: YouTube video ID
            privacy_status: New privacy status (public, private, unlisted)

        Returns:
            bool: Success status
        """
        if not self.service:
            self.logger.error("YouTube service not initialized")
            return False

        try:
            request = self.service.videos().update(
                part="status",
                body={
                    "id": video_id,
                    "status": {
                        "privacyStatus": privacy_status
                    }
                }
            )
            request.execute()
            self.logger.info(f"Updated video {video_id} privacy to {privacy_status}")
            print(f"✅ Updated video {video_id} privacy to {privacy_status}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update video privacy: {e}")
            print(f"❌ Failed to update video privacy: {e}")
            return False

    def delete_video(self, video_id: str) -> bool:
        """
        Delete a video from YouTube.

        Args:
            video_id: YouTube video ID to delete

        Returns:
            bool: Success status
        """
        if not self.service:
            self.logger.error("YouTube service not initialized")
            return False

        try:
            request = self.service.videos().delete(id=video_id)
            request.execute()
            self.logger.info(f"Successfully deleted video: {video_id}")
            print(f"✅ Successfully deleted video: {video_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete video: {e}")
            print(f"❌ Failed to delete video: {e}")
            return False
        """Get details about a specific video"""
        try:
            if not self.service:
                raise Exception("YouTube service not initialized")

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
                print(f"❌ Video not found: {video_id}")
                return None

        except Exception as e:
            print(f"❌ Failed to get video details: {e}")
            return None

    def list_channel_videos(self, max_results: int = 10) -> list:
        """List recent videos from the channel"""
        try:
            if not self.service:
                raise Exception("YouTube service not initialized")

            request = self.service.search().list(
                part='snippet',
                channelId=self.channel_id,
                order='date',
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
                    'published_at': item['snippet']['publishedAt']
                })

            return videos

        except Exception as e:
            print(f"❌ Failed to list channel videos: {e}")
            return []

    def update_video_metadata(self, video_id: str, title: str = None,
                            description: str = None, tags: list = None) -> bool:
        """Update video metadata"""
        try:
            if not self.service:
                raise Exception("YouTube service not initialized")

            # Get current video data
            current_video = self.service.videos().list(
                part='snippet',
                id=video_id
            ).execute()

            if not current_video.get('items'):
                print(f"❌ Video not found: {video_id}")
                return False

            # Update fields
            snippet = current_video['items'][0]['snippet']

            if title:
                snippet['title'] = title
            if description:
                snippet['description'] = description
            if tags:
                snippet['tags'] = tags

            # Update video
            update_request = self.service.videos().update(
                part='snippet',
                body={
                    'id': video_id,
                    'snippet': snippet
                }
            )

            update_request.execute()
            print(f"✅ Video metadata updated: {video_id}")
            return True

        except Exception as e:
            print(f"❌ Failed to update video metadata: {e}")
            return False

    def get_videos_statistics(self, video_ids: list) -> dict:
        """
        Get statistics for multiple YouTube videos

        Args:
            video_ids: List of YouTube video IDs (max 50 per request)

        Returns:
            Dictionary with video_id as key and statistics as value
        """
        try:
            if not self.service:
                raise Exception("YouTube service not initialized")

            if not video_ids:
                return {}

            if len(video_ids) > 50:
                print(f"⚠️  Warning: YouTube API allows max 50 videos per request, got {len(video_ids)}")
                video_ids = video_ids[:50]

            # Convert list to comma-separated string
            video_ids_str = ','.join(video_ids)

            # Make API request
            request = self.service.videos().list(
                part='statistics',
                id=video_ids_str,
                maxResults=len(video_ids)
            )

            response = request.execute()

            # Process response
            statistics = {}
            for item in response.get('items', []):
                video_id = item['id']
                stats = item.get('statistics', {})

                statistics[video_id] = {
                    'view_count': int(stats.get('viewCount', 0)),
                    'like_count': int(stats.get('likeCount', 0)),
                    'comment_count': int(stats.get('commentCount', 0)),
                    'favorite_count': int(stats.get('favoriteCount', 0))
                }

            print(f"✅ Retrieved statistics for {len(statistics)} videos")
            return statistics

        except HttpError as e:
            error_code = e.resp.status if hasattr(e, 'resp') else 'Unknown'
            if error_code == 403:
                print("❌ Statistics access denied - check API permissions")
            elif error_code == 404:
                print("❌ Some videos not found")
            else:
                print(f"❌ YouTube API statistics error ({error_code}): {e}")
            return {}
        except Exception as e:
            print(f"❌ Failed to get video statistics: {e}")
            return {}
