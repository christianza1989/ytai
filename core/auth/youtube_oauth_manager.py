#!/usr/bin/env python3
"""
YouTube OAuth Manager
Comprehensive OAuth 2.0 authentication system for YouTube API
Handles all OAuth flows, token management, and credential storage
"""

import os
import json
import uuid
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any
from urllib.parse import urlencode, parse_qs
import requests
from pathlib import Path

class YouTubeOAuthManager:
    """
    Centralized YouTube OAuth 2.0 authentication manager
    Handles authorization flows, token refresh, and credential persistence
    """
    
    def __init__(self, db_manager=None):
        self.logger = logging.getLogger(__name__)
        self.db_manager = db_manager
        
        # OAuth 2.0 endpoints
        self.auth_uri = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_uri = "https://oauth2.googleapis.com/token"
        self.revoke_uri = "https://oauth2.googleapis.com/revoke"
        
        # YouTube API scopes
        self.scopes = [
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube.force-ssl"
        ]
        
        # Session storage for OAuth states
        self.oauth_sessions = {}
        
        # Credentials cache
        self.credentials_cache = {}
        
    def generate_oauth_url(self, channel_id: int, client_id: str, 
                          redirect_uri: str = None) -> Tuple[str, str]:
        """
        Generate OAuth 2.0 authorization URL for YouTube channel
        
        Args:
            channel_id: Internal database channel ID
            client_id: Google OAuth client ID
            redirect_uri: OAuth callback URL (optional)
            
        Returns:
            Tuple of (authorization_url, state_token)
        """
        try:
            # Generate secure state token
            state_token = secrets.token_urlsafe(32)
            
            # Default redirect URI
            if not redirect_uri:
                redirect_uri = f"{os.getenv('BASE_URL', 'http://localhost:3000')}/oauth/youtube/callback"
            
            # Store OAuth session data
            session_data = {
                'channel_id': channel_id,
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'timestamp': datetime.now().isoformat(),
                'scopes': self.scopes,
                'state': state_token
            }
            
            self.oauth_sessions[state_token] = session_data
            
            # Build authorization URL
            auth_params = {
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'scope': ' '.join(self.scopes),
                'response_type': 'code',
                'state': state_token,
                'access_type': 'offline',  # For refresh tokens
                'prompt': 'consent',       # Force consent screen
                'include_granted_scopes': 'true'
            }
            
            authorization_url = f"{self.auth_uri}?{urlencode(auth_params)}"
            
            self.logger.info(f"Generated OAuth URL for channel {channel_id}")
            
            return authorization_url, state_token
            
        except Exception as e:
            self.logger.error(f"Error generating OAuth URL: {e}")
            raise Exception(f"Failed to generate OAuth URL: {str(e)}")
    
    def handle_oauth_callback(self, authorization_code: str, state_token: str, 
                             client_secret: str) -> Dict[str, Any]:
        """
        Handle OAuth callback and exchange code for tokens
        
        Args:
            authorization_code: Authorization code from Google
            state_token: State token to verify session
            client_secret: Google OAuth client secret
            
        Returns:
            Dictionary with success status and channel info
        """
        try:
            # Verify state token
            if state_token not in self.oauth_sessions:
                raise Exception("Invalid or expired OAuth state token")
            
            session_data = self.oauth_sessions[state_token]
            channel_id = session_data['channel_id']
            client_id = session_data['client_id']
            redirect_uri = session_data['redirect_uri']
            
            # Exchange authorization code for tokens
            token_data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'code': authorization_code,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri
            }
            
            self.logger.info(f"Exchanging OAuth code for tokens (channel {channel_id})")
            
            response = requests.post(self.token_uri, data=token_data, timeout=30)
            response.raise_for_status()
            
            token_response = response.json()
            
            if 'error' in token_response:
                raise Exception(f"OAuth token error: {token_response['error_description']}")
            
            # Extract tokens
            access_token = token_response.get('access_token')
            refresh_token = token_response.get('refresh_token')
            expires_in = token_response.get('expires_in', 3600)
            
            if not access_token:
                raise Exception("No access token received from Google")
            
            # Calculate token expiry
            expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            # Prepare credentials data
            credentials = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': expires_at.isoformat(),
                'token_type': token_response.get('token_type', 'Bearer'),
                'scope': token_response.get('scope', ' '.join(self.scopes)),
                'created_at': datetime.now().isoformat()
            }
            
            # Get YouTube channel info using the new token
            youtube_info = self._get_youtube_channel_info(access_token)
            
            # Store credentials in database
            if self.db_manager:
                oauth_data = {
                    'oauth_credentials': json.dumps(credentials),
                    'oauth_authorized': True,
                    'youtube_channel_id': youtube_info.get('channel_id'),
                    'channel_url': youtube_info.get('channel_url')
                }
                
                # Update channel with OAuth credentials
                result = self.db_manager.update_channel(channel_id, oauth_data)
                
                if not result.get('success'):
                    self.logger.error(f"Failed to store OAuth credentials: {result.get('error')}")
            
            # Cache credentials
            self.credentials_cache[channel_id] = credentials
            
            # Clean up OAuth session
            del self.oauth_sessions[state_token]
            
            self.logger.info(f"OAuth authorization completed for channel {channel_id}")
            
            return {
                'success': True,
                'channel_id': channel_id,
                'youtube_info': youtube_info,
                'credentials_stored': True,
                'message': f'Channel "{youtube_info.get("title")}" successfully authorized!'
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"OAuth callback request error: {e}")
            return {
                'success': False,
                'error': f'Network error during OAuth: {str(e)}',
                'message': 'Failed to complete OAuth authorization'
            }
        except Exception as e:
            self.logger.error(f"OAuth callback error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to complete OAuth authorization'
            }
    
    def _get_youtube_channel_info(self, access_token: str) -> Dict[str, Any]:
        """Get YouTube channel information using access token"""
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json'
            }
            
            # Get channel info
            response = requests.get(
                'https://www.googleapis.com/youtube/v3/channels',
                headers=headers,
                params={
                    'part': 'id,snippet,statistics,brandingSettings',
                    'mine': 'true'
                },
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            if not data.get('items'):
                return {'error': 'No YouTube channel found for this account'}
            
            channel = data['items'][0]
            snippet = channel.get('snippet', {})
            statistics = channel.get('statistics', {})
            
            return {
                'channel_id': channel['id'],
                'title': snippet.get('title', 'Unknown Channel'),
                'description': snippet.get('description', ''),
                'thumbnail_url': snippet.get('thumbnails', {}).get('default', {}).get('url'),
                'channel_url': f"https://www.youtube.com/channel/{channel['id']}",
                'subscriber_count': int(statistics.get('subscriberCount', 0)),
                'video_count': int(statistics.get('videoCount', 0)),
                'view_count': int(statistics.get('viewCount', 0)),
                'created_at': snippet.get('publishedAt')
            }
            
        except Exception as e:
            self.logger.error(f"Error getting YouTube channel info: {e}")
            return {'error': str(e)}
    
    def get_valid_credentials(self, channel_id: int) -> Optional[Dict[str, Any]]:
        """
        Get valid credentials for channel, refreshing if necessary
        
        Args:
            channel_id: Internal database channel ID
            
        Returns:
            Valid credentials dictionary or None
        """
        try:
            # Check cache first
            if channel_id in self.credentials_cache:
                credentials = self.credentials_cache[channel_id]
                if self._are_credentials_valid(credentials):
                    return credentials
            
            # Load from database
            if self.db_manager:
                channel = self.db_manager.get_channel(channel_id)
                if not channel or not channel.get('oauth_credentials'):
                    return None
                
                credentials = json.loads(channel['oauth_credentials'])
                
                # Check if credentials need refresh
                if not self._are_credentials_valid(credentials):
                    # Try to refresh
                    credentials = self._refresh_credentials(channel_id, credentials, channel)
                
                if credentials:
                    self.credentials_cache[channel_id] = credentials
                    return credentials
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting valid credentials for channel {channel_id}: {e}")
            return None
    
    def _are_credentials_valid(self, credentials: Dict[str, Any]) -> bool:
        """Check if credentials are still valid (not expired)"""
        try:
            if not credentials.get('access_token'):
                return False
            
            expires_at_str = credentials.get('expires_at')
            if not expires_at_str:
                return True  # Assume valid if no expiry
            
            expires_at = datetime.fromisoformat(expires_at_str)
            # Add 5 minute buffer
            return datetime.now() < (expires_at - timedelta(minutes=5))
            
        except Exception:
            return False
    
    def _refresh_credentials(self, channel_id: int, credentials: Dict[str, Any], 
                           channel: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Refresh OAuth credentials using refresh token"""
        try:
            refresh_token = credentials.get('refresh_token')
            if not refresh_token:
                self.logger.warning(f"No refresh token for channel {channel_id}")
                return None
            
            client_id = channel.get('client_id')
            client_secret = channel.get('client_secret')
            
            if not client_id or not client_secret:
                self.logger.error(f"Missing OAuth client credentials for channel {channel_id}")
                return None
            
            # Refresh token request
            refresh_data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }
            
            self.logger.info(f"Refreshing OAuth token for channel {channel_id}")
            
            response = requests.post(self.token_uri, data=refresh_data, timeout=30)
            response.raise_for_status()
            
            token_response = response.json()
            
            if 'error' in token_response:
                self.logger.error(f"Token refresh error: {token_response['error_description']}")
                return None
            
            # Update credentials with new token
            new_access_token = token_response.get('access_token')
            expires_in = token_response.get('expires_in', 3600)
            
            if not new_access_token:
                self.logger.error("No access token in refresh response")
                return None
            
            # Update credentials
            credentials.update({
                'access_token': new_access_token,
                'expires_at': (datetime.now() + timedelta(seconds=expires_in)).isoformat(),
                'refreshed_at': datetime.now().isoformat()
            })
            
            # Store updated credentials in database
            if self.db_manager:
                oauth_data = {'oauth_credentials': json.dumps(credentials)}
                self.db_manager.update_channel(channel_id, oauth_data)
            
            self.logger.info(f"OAuth token refreshed successfully for channel {channel_id}")
            
            return credentials
            
        except Exception as e:
            self.logger.error(f"Error refreshing credentials for channel {channel_id}: {e}")
            return None
    
    def revoke_authorization(self, channel_id: int) -> Dict[str, Any]:
        """Revoke OAuth authorization for channel"""
        try:
            credentials = self.get_valid_credentials(channel_id)
            if not credentials:
                return {'success': False, 'error': 'No credentials found'}
            
            access_token = credentials.get('access_token')
            
            # Revoke token with Google
            if access_token:
                revoke_response = requests.post(
                    self.revoke_uri,
                    params={'token': access_token},
                    timeout=10
                )
                # Note: Google returns 200 even for invalid tokens
            
            # Clear from database
            if self.db_manager:
                oauth_data = {
                    'oauth_credentials': None,
                    'oauth_authorized': False
                }
                self.db_manager.update_channel(channel_id, oauth_data)
            
            # Clear from cache
            if channel_id in self.credentials_cache:
                del self.credentials_cache[channel_id]
            
            self.logger.info(f"OAuth authorization revoked for channel {channel_id}")
            
            return {
                'success': True,
                'message': 'Authorization revoked successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Error revoking authorization for channel {channel_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to revoke authorization'
            }
    
    def test_credentials(self, channel_id: int) -> Dict[str, Any]:
        """Test if channel credentials are working"""
        try:
            credentials = self.get_valid_credentials(channel_id)
            if not credentials:
                return {
                    'success': False,
                    'error': 'No valid credentials',
                    'message': 'Channel not authorized or credentials expired'
                }
            
            # Test API call
            youtube_info = self._get_youtube_channel_info(credentials['access_token'])
            
            if 'error' in youtube_info:
                return {
                    'success': False,
                    'error': youtube_info['error'],
                    'message': 'Credentials test failed'
                }
            
            return {
                'success': True,
                'youtube_info': youtube_info,
                'message': f'Credentials working! Connected to "{youtube_info.get("title")}"'
            }
            
        except Exception as e:
            self.logger.error(f"Error testing credentials for channel {channel_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to test credentials'
            }
    
    def get_oauth_session_info(self, state_token: str) -> Optional[Dict[str, Any]]:
        """Get OAuth session information by state token"""
        return self.oauth_sessions.get(state_token)
    
    def cleanup_expired_sessions(self, max_age_hours: int = 1):
        """Clean up expired OAuth sessions"""
        try:
            current_time = datetime.now()
            expired_sessions = []
            
            for state_token, session_data in self.oauth_sessions.items():
                session_time = datetime.fromisoformat(session_data['timestamp'])
                if (current_time - session_time).total_seconds() > (max_age_hours * 3600):
                    expired_sessions.append(state_token)
            
            for state_token in expired_sessions:
                del self.oauth_sessions[state_token]
                
            if expired_sessions:
                self.logger.info(f"Cleaned up {len(expired_sessions)} expired OAuth sessions")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up OAuth sessions: {e}")
    
    def get_authorization_status(self, channel_id: int) -> Dict[str, Any]:
        """Get detailed authorization status for channel"""
        try:
            if not self.db_manager:
                return {'status': 'unknown', 'error': 'No database manager'}
            
            channel = self.db_manager.get_channel(channel_id)
            if not channel:
                return {'status': 'not_found', 'error': 'Channel not found'}
            
            # Check basic credentials
            api_key = channel.get('api_key')
            client_id = channel.get('client_id')
            client_secret = channel.get('client_secret')
            oauth_authorized = channel.get('oauth_authorized', False)
            
            if not api_key:
                return {
                    'status': 'missing_api_key',
                    'error': 'YouTube Data API key not configured',
                    'needs': ['api_key']
                }
            
            if not client_id or not client_secret:
                return {
                    'status': 'missing_oauth_client',
                    'error': 'OAuth client credentials not configured',
                    'needs': ['client_id', 'client_secret']
                }
            
            if not oauth_authorized:
                return {
                    'status': 'not_authorized',
                    'error': 'Channel not authorized for YouTube access',
                    'needs': ['oauth_authorization']
                }
            
            # Check OAuth credentials
            credentials = self.get_valid_credentials(channel_id)
            if not credentials:
                return {
                    'status': 'invalid_credentials',
                    'error': 'OAuth credentials expired or invalid',
                    'needs': ['oauth_authorization']
                }
            
            return {
                'status': 'authorized',
                'message': 'Channel fully authorized and ready',
                'credentials_valid': True,
                'expires_at': credentials.get('expires_at')
            }
            
        except Exception as e:
            self.logger.error(f"Error checking authorization status: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }