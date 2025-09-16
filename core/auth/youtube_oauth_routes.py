#!/usr/bin/env python3
"""
YouTube OAuth API Routes
Dedicated routes for YouTube OAuth 2.0 authentication flows
"""

from flask import Blueprint, request, jsonify, redirect, render_template, session
from core.auth.youtube_oauth_manager import YouTubeOAuthManager
from core.database.youtube_channels_db import YouTubeChannelsDB
import logging
import os

# Create Blueprint
youtube_oauth_bp = Blueprint('youtube_oauth', __name__, url_prefix='/oauth/youtube')

# Initialize logger
logger = logging.getLogger(__name__)

def create_oauth_routes(app, require_auth=None):
    """
    Create and register YouTube OAuth routes
    
    Args:
        app: Flask application instance
        require_auth: Authentication decorator function
    """
    
    # Initialize managers
    db_manager = YouTubeChannelsDB()
    oauth_manager = YouTubeOAuthManager(db_manager)
    
    # Create auth decorator helper
    def auth_required(f):
        if require_auth:
            return require_auth(f)
        return f
    
    @youtube_oauth_bp.route('/start/<int:channel_id>')
    def start_oauth_flow(channel_id):
        """Start OAuth authorization flow for a channel"""
        try:
            # Get channel info
            channel = db_manager.get_channel(channel_id)
            if not channel:
                return render_template('error.html', 
                                     error='Channel not found',
                                     message='The specified channel does not exist.')
            
            client_id = channel.get('client_id')
            if not client_id:
                return render_template('error.html',
                                     error='OAuth client not configured',
                                     message='Please configure OAuth Client ID first.')
            
            # Generate OAuth URL
            base_url = os.getenv('BASE_URL', 'http://localhost:3000')
            redirect_uri = f"{base_url}/oauth/youtube/callback"
            
            auth_url, state_token = oauth_manager.generate_oauth_url(
                channel_id=channel_id,
                client_id=client_id,
                redirect_uri=redirect_uri
            )
            
            # Store state in session as backup
            session['oauth_state'] = state_token
            session['oauth_channel_id'] = channel_id
            
            logger.info(f"Starting OAuth flow for channel {channel_id}")
            
            # Redirect to Google OAuth
            return redirect(auth_url)
            
        except Exception as e:
            logger.error(f"Error starting OAuth flow: {e}")
            return render_template('error.html',
                                 error='OAuth Error',
                                 message=f'Failed to start authorization: {str(e)}')
    
    @youtube_oauth_bp.route('/callback')
    def oauth_callback():
        """Handle OAuth callback from Google"""
        try:
            # Get callback parameters
            authorization_code = request.args.get('code')
            state_token = request.args.get('state')
            error = request.args.get('error')
            
            # Handle OAuth errors
            if error:
                error_description = request.args.get('error_description', error)
                logger.warning(f"OAuth error: {error} - {error_description}")
                
                return render_template('oauth_result.html',
                                     success=False,
                                     error=error,
                                     message=f'Authorization denied: {error_description}')
            
            # Validate required parameters
            if not authorization_code or not state_token:
                return render_template('oauth_result.html',
                                     success=False,
                                     error='Missing parameters',
                                     message='Invalid callback - missing authorization code or state.')
            
            # Get OAuth session info
            session_info = oauth_manager.get_oauth_session_info(state_token)
            if not session_info:
                return render_template('oauth_result.html',
                                     success=False,
                                     error='Invalid session',
                                     message='OAuth session expired or invalid. Please try again.')
            
            channel_id = session_info['channel_id']
            
            # Get channel info for client_secret
            channel = db_manager.get_channel(channel_id)
            if not channel:
                return render_template('oauth_result.html',
                                     success=False,
                                     error='Channel not found',
                                     message='The specified channel no longer exists.')
            
            client_secret = channel.get('client_secret')
            if not client_secret:
                return render_template('oauth_result.html',
                                     success=False,
                                     error='Missing client secret',
                                     message='OAuth client secret not configured.')
            
            # Handle OAuth callback
            result = oauth_manager.handle_oauth_callback(
                authorization_code=authorization_code,
                state_token=state_token,
                client_secret=client_secret
            )
            
            # Clean up session
            session.pop('oauth_state', None)
            session.pop('oauth_channel_id', None)
            
            if result['success']:
                youtube_info = result.get('youtube_info', {})
                return render_template('oauth_result.html',
                                     success=True,
                                     channel_name=channel['channel_name'],
                                     youtube_channel=youtube_info.get('title'),
                                     message=result['message'])
            else:
                return render_template('oauth_result.html',
                                     success=False,
                                     error=result.get('error'),
                                     message=result['message'])
                
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            return render_template('oauth_result.html',
                                 success=False,
                                 error='Callback error',
                                 message=f'Failed to process authorization: {str(e)}')
    
    # API Routes
    @youtube_oauth_bp.route('/api/authorize/<int:channel_id>', methods=['POST'])
    @auth_required
    def api_authorize_channel(channel_id):
        """API endpoint to start OAuth authorization"""
        
        try:
            channel = db_manager.get_channel(channel_id)
            if not channel:
                return jsonify({
                    'success': False,
                    'error': 'Channel not found'
                }), 404
            
            client_id = channel.get('client_id')
            if not client_id:
                return jsonify({
                    'success': False,
                    'error': 'OAuth client ID not configured',
                    'message': 'Please configure OAuth Client ID first'
                }), 400
            
            # Generate OAuth URL
            base_url = os.getenv('BASE_URL', 'http://localhost:3000')
            redirect_uri = f"{base_url}/oauth/youtube/callback"
            
            auth_url, state_token = oauth_manager.generate_oauth_url(
                channel_id=channel_id,
                client_id=client_id,
                redirect_uri=redirect_uri
            )
            
            return jsonify({
                'success': True,
                'authorization_url': auth_url,
                'state_token': state_token,
                'message': 'OAuth authorization URL generated'
            })
            
        except Exception as e:
            logger.error(f"API authorize error: {e}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': 'Failed to generate authorization URL'
            }), 500
    
    @youtube_oauth_bp.route('/api/status/<int:channel_id>', methods=['GET'])
    @auth_required
    def api_authorization_status(channel_id):
        """API endpoint to check authorization status"""
        
        try:
            status = oauth_manager.get_authorization_status(channel_id)
            
            return jsonify({
                'success': True,
                'channel_id': channel_id,
                'authorization_status': status
            })
            
        except Exception as e:
            logger.error(f"API status error: {e}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': 'Failed to check authorization status'
            }), 500
    
    @youtube_oauth_bp.route('/api/test/<int:channel_id>', methods=['POST'])
    @auth_required
    def api_test_credentials(channel_id):
        """API endpoint to test channel credentials"""
        
        try:
            result = oauth_manager.test_credentials(channel_id)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"API test error: {e}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': 'Failed to test credentials'
            }), 500
    
    @youtube_oauth_bp.route('/api/revoke/<int:channel_id>', methods=['POST'])
    @auth_required
    def api_revoke_authorization(channel_id):
        """API endpoint to revoke authorization"""
        
        try:
            result = oauth_manager.revoke_authorization(channel_id)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"API revoke error: {e}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': 'Failed to revoke authorization'
            }), 500
    
    @youtube_oauth_bp.route('/api/refresh/<int:channel_id>', methods=['POST'])
    @auth_required
    def api_refresh_credentials(channel_id):
        """API endpoint to refresh credentials"""
        
        try:
            # Force refresh by clearing cache
            if channel_id in oauth_manager.credentials_cache:
                del oauth_manager.credentials_cache[channel_id]
            
            credentials = oauth_manager.get_valid_credentials(channel_id)
            
            if credentials:
                return jsonify({
                    'success': True,
                    'message': 'Credentials refreshed successfully',
                    'expires_at': credentials.get('expires_at')
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No valid credentials',
                    'message': 'Failed to refresh credentials - reauthorization required'
                })
            
        except Exception as e:
            logger.error(f"API refresh error: {e}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': 'Failed to refresh credentials'
            }), 500
    
    # Register cleanup task
    @youtube_oauth_bp.before_app_request
    def cleanup_oauth_sessions():
        """Clean up expired OAuth sessions on each request"""
        try:
            oauth_manager.cleanup_expired_sessions()
        except Exception:
            pass  # Don't let cleanup errors affect requests
    
    # Register blueprint
    app.register_blueprint(youtube_oauth_bp)
    
    return youtube_oauth_bp