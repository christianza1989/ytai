#!/usr/bin/env python3
"""
YouTube Channels Database Manager
Comprehensive database management for YouTube automation system
"""

import sqlite3
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging

class YouTubeChannelsDB:
    """Advanced database manager for YouTube channels with automation features"""
    
    def __init__(self, db_path: str = "data/youtube_channels.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self._init_database()
        
    def _init_database(self):
        """Initialize database with comprehensive schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Main channels table with all automation features
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS youtube_channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_uuid TEXT UNIQUE NOT NULL,
                    channel_name TEXT NOT NULL,
                    channel_url TEXT,
                    youtube_channel_id TEXT,
                    description TEXT,
                    
                    -- API Credentials (encrypted in production)
                    api_key TEXT,
                    client_id TEXT,
                    client_secret TEXT,
                    oauth_token TEXT,
                    
                    -- Music Genre Selection (JSON array)
                    selected_genres TEXT NOT NULL DEFAULT '[]',
                    primary_genre TEXT,
                    target_audience TEXT,
                    
                    -- Automation Configuration
                    auto_upload BOOLEAN DEFAULT 1,
                    auto_thumbnails BOOLEAN DEFAULT 1,
                    auto_seo BOOLEAN DEFAULT 1,
                    enable_analytics BOOLEAN DEFAULT 1,
                    enable_monetization BOOLEAN DEFAULT 0,
                    
                    -- Daily Upload Configuration
                    daily_upload_count INTEGER DEFAULT 1,
                    upload_schedule TEXT DEFAULT 'daily',
                    
                    -- Hour-specific scheduling (JSON array of time slots)
                    upload_hours TEXT DEFAULT '[{"hour": 14, "vocal_probability": 0.8}]',
                    
                    -- AI Vocal Configuration
                    vocal_probability REAL DEFAULT 0.8,  -- 80% vocal, 20% instrumental
                    ai_decision_enabled BOOLEAN DEFAULT 1,
                    
                    -- Privacy and Settings
                    privacy_settings TEXT DEFAULT 'private',
                    default_video_title_template TEXT DEFAULT '[GENRE] - Relaxing Music #[NUMBER]',
                    default_description_template TEXT,
                    
                    -- Performance Tracking
                    total_subscribers INTEGER DEFAULT 0,
                    monthly_revenue REAL DEFAULT 0.0,
                    total_videos INTEGER DEFAULT 0,
                    total_views INTEGER DEFAULT 0,
                    last_upload_date TEXT,
                    
                    -- Status and Metadata
                    status TEXT DEFAULT 'active',  -- active, inactive, needs_setup, error
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    
                    -- 24/7 Automation Status
                    automation_enabled BOOLEAN DEFAULT 0,
                    automation_start_date TEXT,
                    automation_last_run TEXT,
                    automation_next_run TEXT,
                    
                    -- Advanced Settings (JSON)
                    advanced_settings TEXT DEFAULT '{}',
                    error_log TEXT DEFAULT '[]'
                )
            ''')
            
            # Video generation queue for scheduling
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS video_generation_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    queue_uuid TEXT UNIQUE NOT NULL,
                    channel_id INTEGER NOT NULL,
                    
                    -- Generation Parameters
                    genre TEXT NOT NULL,
                    vocal_type TEXT NOT NULL,  -- vocal, instrumental
                    scheduled_time TEXT NOT NULL,
                    
                    -- Generation Status
                    status TEXT DEFAULT 'queued',  -- queued, generating, completed, failed, uploaded
                    progress INTEGER DEFAULT 0,
                    
                    -- Generated Content
                    music_url TEXT,
                    thumbnail_url TEXT,
                    video_title TEXT,
                    video_description TEXT,
                    video_tags TEXT,  -- JSON array
                    
                    -- Upload Information
                    youtube_video_id TEXT,
                    upload_status TEXT,
                    upload_response TEXT,  -- JSON response from YouTube API
                    
                    -- Metadata
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    generated_at TEXT,
                    uploaded_at TEXT,
                    
                    -- Error Handling
                    error_message TEXT,
                    retry_count INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3,
                    
                    FOREIGN KEY (channel_id) REFERENCES youtube_channels (id) ON DELETE CASCADE
                )
            ''')
            
            # Automation logs for monitoring
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS automation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id INTEGER NOT NULL,
                    log_type TEXT NOT NULL,  -- generation, upload, error, status
                    message TEXT NOT NULL,
                    details TEXT,  -- JSON details
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (channel_id) REFERENCES youtube_channels (id) ON DELETE CASCADE
                )
            ''')
            
            # Performance analytics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS channel_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    
                    -- Daily Metrics
                    videos_generated INTEGER DEFAULT 0,
                    videos_uploaded INTEGER DEFAULT 0,
                    new_subscribers INTEGER DEFAULT 0,
                    total_views INTEGER DEFAULT 0,
                    estimated_revenue REAL DEFAULT 0.0,
                    
                    -- Vocal vs Instrumental Performance
                    vocal_videos INTEGER DEFAULT 0,
                    instrumental_videos INTEGER DEFAULT 0,
                    vocal_avg_views INTEGER DEFAULT 0,
                    instrumental_avg_views INTEGER DEFAULT 0,
                    
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (channel_id) REFERENCES youtube_channels (id) ON DELETE CASCADE,
                    UNIQUE(channel_id, date)
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_channels_status ON youtube_channels (status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_channels_automation ON youtube_channels (automation_enabled)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_queue_status ON video_generation_queue (status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_queue_scheduled ON video_generation_queue (scheduled_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_type ON automation_logs (log_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_date ON channel_analytics (date)')
            
            conn.commit()
            self.logger.info("YouTube Channels database initialized successfully")
    
    def add_channel(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new YouTube channel with comprehensive configuration"""
        try:
            channel_uuid = str(uuid.uuid4())
            
            # Process genre selection
            selected_genres = channel_data.get('selected_genres', [])
            if isinstance(selected_genres, list):
                selected_genres_json = json.dumps(selected_genres)
            else:
                selected_genres_json = json.dumps([selected_genres] if selected_genres else [])
            
            # Process upload hours with AI vocal probability
            upload_hours = channel_data.get('upload_hours', [])
            if not upload_hours:
                # Default: single upload at 2 PM with 80% vocal probability
                upload_hours = [{"hour": 14, "vocal_probability": 0.8}]
            upload_hours_json = json.dumps(upload_hours)
            
            # Advanced settings
            advanced_settings = {
                'thumbnail_style': channel_data.get('thumbnail_style', '16:9_modern'),
                'seo_optimization_level': channel_data.get('seo_optimization', 'high'),
                'content_diversity': channel_data.get('content_diversity', True),
                'trending_keywords_enabled': channel_data.get('trending_keywords', True),
                'ai_title_generation': channel_data.get('ai_titles', True),
                'automated_descriptions': channel_data.get('auto_descriptions', True)
            }
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO youtube_channels (
                        channel_uuid, channel_name, channel_url, youtube_channel_id, description,
                        api_key, client_id, client_secret,
                        selected_genres, primary_genre, target_audience,
                        auto_upload, auto_thumbnails, auto_seo, enable_analytics, enable_monetization,
                        daily_upload_count, upload_schedule, upload_hours,
                        vocal_probability, ai_decision_enabled,
                        privacy_settings, default_video_title_template, default_description_template,
                        advanced_settings
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    channel_uuid,
                    channel_data.get('channel_name'),
                    channel_data.get('channel_url'),
                    channel_data.get('youtube_channel_id'),
                    channel_data.get('description'),
                    channel_data.get('api_key'),
                    channel_data.get('client_id'),
                    channel_data.get('client_secret'),
                    selected_genres_json,
                    channel_data.get('primary_genre'),
                    channel_data.get('target_audience'),
                    channel_data.get('auto_upload', True),
                    channel_data.get('auto_thumbnails', True),
                    channel_data.get('auto_seo', True),
                    channel_data.get('enable_analytics', True),
                    channel_data.get('enable_monetization', False),
                    channel_data.get('daily_upload_count', 1),
                    channel_data.get('upload_schedule', 'daily'),
                    upload_hours_json,
                    channel_data.get('vocal_probability', 0.8),
                    channel_data.get('ai_decision_enabled', True),
                    channel_data.get('privacy_settings', 'private'),
                    channel_data.get('title_template', '[GENRE] - Relaxing Music #[NUMBER]'),
                    channel_data.get('description_template'),
                    json.dumps(advanced_settings)
                ))
                
                channel_id = cursor.lastrowid
                conn.commit()
                
                # Log channel creation
                self._log_event(channel_id, 'channel_created', f'Channel {channel_data.get("channel_name")} created successfully')
                
                # Get the created channel
                created_channel = self.get_channel(channel_id)
                
                self.logger.info(f"Channel created successfully: {channel_data.get('channel_name')} (ID: {channel_id})")
                
                return {
                    'success': True,
                    'channel_id': channel_id,
                    'channel_uuid': channel_uuid,
                    'channel': created_channel,
                    'message': 'Channel created successfully'
                }
                
        except Exception as e:
            self.logger.error(f"Error creating channel: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to create channel'
            }
    
    def update_channel(self, channel_id: int, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing YouTube channel configuration"""
        try:
            # Process genre selection
            selected_genres = channel_data.get('selected_genres', [])
            if isinstance(selected_genres, list):
                selected_genres_json = json.dumps(selected_genres)
            else:
                selected_genres_json = json.dumps([selected_genres] if selected_genres else [])
            
            # Process upload hours
            upload_hours = channel_data.get('upload_hours', [])
            if not upload_hours:
                upload_hours = [{"hour": 14, "vocal_probability": 0.8}]
            upload_hours_json = json.dumps(upload_hours)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Update channel
                cursor.execute('''
                    UPDATE youtube_channels SET
                        channel_name = ?, channel_url = ?, youtube_channel_id = ?, description = ?,
                        api_key = ?, client_id = ?, client_secret = ?,
                        selected_genres = ?, primary_genre = ?, target_audience = ?,
                        auto_upload = ?, auto_thumbnails = ?, auto_seo = ?, enable_analytics = ?, enable_monetization = ?,
                        daily_upload_count = ?, upload_schedule = ?, upload_hours = ?,
                        vocal_probability = ?, ai_decision_enabled = ?,
                        privacy_settings = ?, default_video_title_template = ?, default_description_template = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    channel_data.get('channel_name'),
                    channel_data.get('channel_url'),
                    channel_data.get('youtube_channel_id'),
                    channel_data.get('description'),
                    channel_data.get('api_key'),
                    channel_data.get('client_id'),
                    channel_data.get('client_secret'),
                    selected_genres_json,
                    channel_data.get('primary_genre'),
                    channel_data.get('target_audience'),
                    channel_data.get('auto_upload', True),
                    channel_data.get('auto_thumbnails', True),
                    channel_data.get('auto_seo', True),
                    channel_data.get('enable_analytics', True),
                    channel_data.get('enable_monetization', False),
                    channel_data.get('daily_upload_count', 1),
                    channel_data.get('upload_schedule', 'daily'),
                    upload_hours_json,
                    channel_data.get('vocal_probability', 0.8),
                    channel_data.get('ai_decision_enabled', True),
                    channel_data.get('privacy_settings', 'private'),
                    channel_data.get('title_template', '[GENRE] - Relaxing Music #[NUMBER]'),
                    channel_data.get('description_template'),
                    channel_id
                ))
                
                if cursor.rowcount == 0:
                    return {
                        'success': False,
                        'message': 'Channel not found'
                    }
                
                conn.commit()
                
                # Log update
                self._log_event(channel_id, 'channel_updated', f'Channel configuration updated')
                
                # Get updated channel
                updated_channel = self.get_channel(channel_id)
                
                return {
                    'success': True,
                    'channel': updated_channel,
                    'message': 'Channel updated successfully'
                }
                
        except Exception as e:
            self.logger.error(f"Error updating channel {channel_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to update channel'
            }
    
    def get_channel(self, channel_id: int) -> Optional[Dict[str, Any]]:
        """Get channel by ID with parsed JSON fields"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM youtube_channels WHERE id = ?', (channel_id,))
                row = cursor.fetchone()
                
                if not row:
                    return None
                
                channel = dict(row)
                
                # Parse JSON fields
                channel['selected_genres'] = json.loads(channel['selected_genres']) if channel['selected_genres'] else []
                channel['upload_hours'] = json.loads(channel['upload_hours']) if channel['upload_hours'] else []
                channel['advanced_settings'] = json.loads(channel['advanced_settings']) if channel['advanced_settings'] else {}
                channel['error_log'] = json.loads(channel['error_log']) if channel['error_log'] else []
                
                return channel
                
        except Exception as e:
            self.logger.error(f"Error getting channel {channel_id}: {e}")
            return None
    
    def list_channels(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all channels with optional status filter"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if status:
                    cursor.execute('SELECT * FROM youtube_channels WHERE status = ? ORDER BY created_at DESC', (status,))
                else:
                    cursor.execute('SELECT * FROM youtube_channels ORDER BY created_at DESC')
                
                rows = cursor.fetchall()
                
                channels = []
                for row in rows:
                    channel = dict(row)
                    
                    # Parse JSON fields
                    channel['selected_genres'] = json.loads(channel['selected_genres']) if channel['selected_genres'] else []
                    channel['upload_hours'] = json.loads(channel['upload_hours']) if channel['upload_hours'] else []
                    channel['advanced_settings'] = json.loads(channel['advanced_settings']) if channel['advanced_settings'] else {}
                    
                    channels.append(channel)
                
                return channels
                
        except Exception as e:
            self.logger.error(f"Error listing channels: {e}")
            return []
    
    def delete_channel(self, channel_id: int) -> Dict[str, Any]:
        """Delete channel and all related data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if channel exists
                cursor.execute('SELECT channel_name FROM youtube_channels WHERE id = ?', (channel_id,))
                channel = cursor.fetchone()
                
                if not channel:
                    return {
                        'success': False,
                        'message': 'Channel not found'
                    }
                
                channel_name = channel[0]
                
                # Delete channel (CASCADE will handle related records)
                cursor.execute('DELETE FROM youtube_channels WHERE id = ?', (channel_id,))
                
                conn.commit()
                
                self.logger.info(f"Channel deleted: {channel_name} (ID: {channel_id})")
                
                return {
                    'success': True,
                    'message': f'Channel "{channel_name}" deleted successfully'
                }
                
        except Exception as e:
            self.logger.error(f"Error deleting channel {channel_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to delete channel'
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive channel statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Basic counts
                cursor.execute('SELECT COUNT(*) FROM youtube_channels')
                total_channels = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM youtube_channels WHERE status = "active"')
                active_channels = cursor.fetchone()[0]
                
                cursor.execute('SELECT SUM(total_subscribers) FROM youtube_channels')
                total_subscribers = cursor.fetchone()[0] or 0
                
                cursor.execute('SELECT SUM(monthly_revenue) FROM youtube_channels')
                total_revenue = cursor.fetchone()[0] or 0.0
                
                cursor.execute('SELECT SUM(total_videos) FROM youtube_channels')
                total_videos = cursor.fetchone()[0] or 0
                
                cursor.execute('SELECT SUM(total_views) FROM youtube_channels')
                total_views = cursor.fetchone()[0] or 0
                
                # Status breakdown
                cursor.execute('SELECT status, COUNT(*) FROM youtube_channels GROUP BY status')
                status_breakdown = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Genre breakdown
                cursor.execute('SELECT primary_genre, COUNT(*) FROM youtube_channels WHERE primary_genre IS NOT NULL GROUP BY primary_genre')
                genre_breakdown = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Automation stats
                cursor.execute('SELECT COUNT(*) FROM youtube_channels WHERE automation_enabled = 1')
                automated_channels = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM video_generation_queue WHERE status = "queued"')
                queued_videos = cursor.fetchone()[0]
                
                return {
                    'total_channels': total_channels,
                    'active_channels': active_channels,
                    'automated_channels': automated_channels,
                    'total_subscribers': total_subscribers,
                    'total_revenue': total_revenue,
                    'total_videos': total_videos,
                    'total_views': total_views,
                    'queued_videos': queued_videos,
                    'status_breakdown': status_breakdown,
                    'genre_breakdown': genre_breakdown
                }
                
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {
                'total_channels': 0,
                'active_channels': 0,
                'automated_channels': 0,
                'total_subscribers': 0,
                'total_revenue': 0.0,
                'total_videos': 0,
                'total_views': 0,
                'queued_videos': 0,
                'status_breakdown': {},
                'genre_breakdown': {}
            }
    
    def enable_automation(self, channel_id: int) -> Dict[str, Any]:
        """Enable 24/7 automation for a channel"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate next run time based on upload schedule
                next_run = self._calculate_next_run_time(channel_id)
                
                cursor.execute('''
                    UPDATE youtube_channels SET 
                        automation_enabled = 1,
                        automation_start_date = CURRENT_TIMESTAMP,
                        automation_next_run = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (next_run, channel_id))
                
                if cursor.rowcount == 0:
                    return {'success': False, 'message': 'Channel not found'}
                
                conn.commit()
                
                self._log_event(channel_id, 'automation_enabled', f'24/7 automation enabled, next run: {next_run}')
                
                return {
                    'success': True,
                    'message': '24/7 automation enabled',
                    'next_run': next_run
                }
                
        except Exception as e:
            self.logger.error(f"Error enabling automation for channel {channel_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    def _calculate_next_run_time(self, channel_id: int) -> str:
        """Calculate next automation run time based on channel schedule"""
        try:
            channel = self.get_channel(channel_id)
            if not channel:
                return (datetime.now() + timedelta(hours=1)).isoformat()
            
            upload_hours = channel.get('upload_hours', [])
            if not upload_hours:
                upload_hours = [{"hour": 14, "vocal_probability": 0.8}]
            
            # Find next upload time
            now = datetime.now()
            today = now.date()
            
            # Get all today's upload times
            today_uploads = []
            for hour_config in upload_hours:
                upload_time = datetime.combine(today, datetime.min.time().replace(hour=hour_config['hour']))
                if upload_time > now:
                    today_uploads.append(upload_time)
            
            if today_uploads:
                return min(today_uploads).isoformat()
            else:
                # No more uploads today, schedule for tomorrow's first upload
                tomorrow = today + timedelta(days=1)
                first_hour = min(hour_config['hour'] for hour_config in upload_hours)
                next_upload = datetime.combine(tomorrow, datetime.min.time().replace(hour=first_hour))
                return next_upload.isoformat()
                
        except Exception as e:
            self.logger.error(f"Error calculating next run time: {e}")
            return (datetime.now() + timedelta(hours=1)).isoformat()
    
    def _log_event(self, channel_id: int, log_type: str, message: str, details: Dict[str, Any] = None):
        """Log automation event"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO automation_logs (channel_id, log_type, message, details)
                    VALUES (?, ?, ?, ?)
                ''', (channel_id, log_type, message, json.dumps(details) if details else None))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Error logging event: {e}")