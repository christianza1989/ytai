import os
import pickle
from typing import Dict, Any, Optional
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

class YouTubeClient:
    """YouTube Data API v3 client with Progressive Authorization (API Key + OAuth)"""

    # YouTube API scopes - Updated for current Google API requirements
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube.readonly',
        'https://www.googleapis.com/auth/youtube'
    ]

    def __init__(self, client_secrets_path=None, channel_id=None):
        # OAuth-only setup for full YouTube access
        self.channel_id = channel_id or os.getenv('YOUTUBE_CHANNEL_ID')
        self.client_secrets_path = client_secrets_path or os.getenv('YOUTUBE_CLIENT_SECRETS_PATH', 'configs/client_secrets.json')
        self.token_path = 'token.pickle'

        # Initialize credentials and service
        self.credentials = None
        self.service = None
        self.read_only = False  # Full access mode
        
        self._authenticate_oauth()

    def _has_oauth_config(self):
        """Check if OAuth configuration is available"""
        return bool(self.client_secrets_path and Path(self.client_secrets_path).exists())

    def _authenticate_oauth(self) -> None:
        """Handle OAuth 2.0 authentication flow (Level 2)"""
        try:
            # Load existing credentials if available
            if Path(self.token_path).exists():
                with open(self.token_path, 'rb') as token:
                    self.credentials = pickle.load(token)

            # Refresh expired credentials
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                try:
                    self.credentials.refresh(Request())
                except RefreshError:
                    print("❌ Failed to refresh credentials, authentication required")
                    self.credentials = None

            # Check if we need new authentication
            if not self.credentials or not self.credentials.valid:
                if not self._has_oauth_config():
                    raise FileNotFoundError(f"OAuth client secrets file not found: {self.client_secrets_path}")

                print("🔐 Starting YouTube OAuth 2.0 authentication...")
                print("📋 A browser window will open for you to authorize the application")

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_path,
                    self.SCOPES
                )

                # Run local server for OAuth callback
                self.credentials = flow.run_local_server(port=8080)

                # Save credentials for future use
                with open(self.token_path, 'wb') as token:
                    pickle.dump(self.credentials, token)

                print("✅ OAuth authentication successful! Credentials saved.")

            # Build YouTube API service with full permissions
            self.service = build('youtube', 'v3', credentials=self.credentials)
            print("🎥 YouTube API service initialized with full upload permissions")

        except Exception as e:
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
        """Check if upload is possible (always true with OAuth)"""
        return self.credentials is not None and self.service is not None

    def get_auth_status(self) -> dict:
        """Get current OAuth authorization status"""
        return {
            'authenticated': bool(self.credentials),
            'can_upload': self.can_upload(),
            'has_oauth': bool(self.credentials),
            'service_initialized': bool(self.service),
            'token_valid': bool(self.credentials and not self.credentials.expired) if self.credentials else False
        }

    def upload_video(self, video_path: str, title: str, description: str,
                    tags: list = None, category_id: str = '10',
                    privacy_status: str = 'private') -> Optional[str]:
        """
        Upload video to YouTube with progress tracking

        Args:
            video_path: Path to the video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID (10 = Music)
            privacy_status: 'public', 'private', or 'unlisted'

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
            print(f"📤 Uploading video: {title}")
            print(f"📁 File: {video_path}")
            print(f"📊 File size: {file_size / (1024*1024):.1f} MB")

            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }

            # Import MediaFileUpload
            from googleapiclient.http import MediaFileUpload

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
                        print(".1f")
                except Exception as e:
                    print(f"⚠️  Upload chunk failed, retrying: {e}")
                    continue

            if response:
                video_id = response.get('id')
                print(f"✅ Video uploaded successfully! ID: {video_id}")
                print(f"🔗 Video URL: https://www.youtube.com/watch?v={video_id}")
                print(f"🔒 Privacy status: {privacy_status}")

                return video_id
            else:
                print("❌ Upload completed but no response received")
                return None

        except HttpError as e:
            error_code = e.resp.status if hasattr(e, 'resp') else 'Unknown'
            if error_code == 403:
                print("❌ Upload quota exceeded or insufficient permissions")
            elif error_code == 400:
                print("❌ Bad request - check video file format and metadata")
            else:
                print(f"❌ YouTube API upload error ({error_code}): {e}")

            return None
        except Exception as e:
            print(f"❌ Failed to upload video: {e}")
            return None

    def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
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
