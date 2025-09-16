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
                    oauth_credentials TEXT,  -- JSON storage for OAuth credentials
                    oauth_authorized BOOLEAN DEFAULT 0,  -- OAuth authorization status
                    
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
            
            # Background task tracking for batch operations monitoring
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS background_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE NOT NULL,
                    task_type TEXT NOT NULL,  -- full_video, music_only, thumbnail_only, batch_generation
                    channel_id INTEGER,
                    
                    -- Task Configuration
                    title TEXT,
                    description TEXT,
                    genre TEXT,
                    vocal_type TEXT,  -- vocal, instrumental
                    
                    -- Progress Tracking
                    status TEXT DEFAULT 'queued',  -- queued, running, completed, failed, cancelled
                    progress INTEGER DEFAULT 0,  -- 0-100
                    current_step TEXT,
                    current_step_detail TEXT,
                    
                    -- Results
                    music_url TEXT,
                    thumbnail_path TEXT,
                    video_path TEXT,
                    seo_metadata TEXT,  -- JSON
                    
                    -- Timing
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    started_at TEXT,
                    completed_at TEXT,
                    estimated_duration INTEGER,  -- seconds
                    
                    -- Error Handling
                    error_message TEXT,
                    retry_count INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3,
                    
                    -- Upload Scheduling
                    scheduled_upload_time TEXT,
                    upload_status TEXT DEFAULT 'pending',  -- pending, scheduled, uploaded, failed
                    
                    FOREIGN KEY (channel_id) REFERENCES youtube_channels (id) ON DELETE CASCADE
                )
            ''')
            
            # Music Queue - Store unused tracks from Suno API (2 tracks per generation)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS music_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    queue_uuid TEXT UNIQUE NOT NULL,
                    
                    -- Source Information
                    suno_task_id TEXT NOT NULL,
                    suno_clip_id TEXT NOT NULL,
                    original_task_id TEXT,  -- Background task that generated this
                    
                    -- Channel Association
                    channel_id INTEGER NOT NULL,
                    genre TEXT NOT NULL,
                    
                    -- Track Details
                    title TEXT NOT NULL,
                    audio_url TEXT NOT NULL,
                    video_url TEXT,  -- Suno's image/video URL
                    duration TEXT,  -- duration format like 3:45
                    duration_seconds REAL,  -- For calculations
                    
                    -- Music Properties
                    vocal_type TEXT NOT NULL,  -- 'vocal' or 'instrumental'
                    tags TEXT,  -- Suno tags as JSON array
                    prompt TEXT,  -- Original generation prompt
                    model_name TEXT,  -- Suno model used (V4, etc.)
                    
                    -- Queue Status
                    status TEXT DEFAULT 'available',  -- available, reserved, used, expired
                    priority INTEGER DEFAULT 0,  -- Higher = more important
                    reserved_for_channel INTEGER,  -- Channel ID if reserved
                    reserved_at TEXT,  -- When reserved
                    
                    -- Usage Tracking
                    used_at TEXT,
                    used_for_task TEXT,  -- Task ID that used this track
                    expiry_date TEXT,  -- When this track expires (30 days from creation)
                    
                    -- Quality Metrics
                    quality_score REAL DEFAULT 0.0,  -- 0-1 based on tags, title quality
                    match_score REAL DEFAULT 0.0,  -- How well it matches requested genre
                    
                    -- Metadata
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (channel_id) REFERENCES youtube_channels (id) ON DELETE CASCADE,
                    FOREIGN KEY (reserved_for_channel) REFERENCES youtube_channels (id) ON DELETE SET NULL
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_channels_status ON youtube_channels (status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_channels_automation ON youtube_channels (automation_enabled)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_queue_status ON video_generation_queue (status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_queue_scheduled ON video_generation_queue (scheduled_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_type ON automation_logs (log_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON background_tasks (status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_type ON background_tasks (task_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_channel ON background_tasks (channel_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_date ON channel_analytics (date)')
            
            # Music Queue indexes for fast searching
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_music_queue_status ON music_queue (status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_music_queue_channel_genre ON music_queue (channel_id, genre, status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_music_queue_vocal_type ON music_queue (vocal_type, status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_music_queue_priority ON music_queue (priority DESC, created_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_music_queue_expiry ON music_queue (expiry_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_music_queue_suno_clip ON music_queue (suno_clip_id)')
            
            # Video Gallery - Store all generated videos for reuse and upload management
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS video_gallery (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_uuid TEXT UNIQUE NOT NULL,
                    
                    -- Video File Information
                    title TEXT NOT NULL,
                    description TEXT,
                    file_path TEXT NOT NULL,  -- Local path to video file
                    thumbnail_path TEXT,      -- Path to thumbnail image
                    duration REAL,            -- Duration in seconds
                    file_size INTEGER,        -- File size in bytes
                    file_format TEXT DEFAULT 'mp4',
                    
                    -- Generation Details
                    original_task_id TEXT,    -- Background task that created this
                    generation_source TEXT DEFAULT 'suno',  -- suno, manual, other
                    music_track_id TEXT,      -- Reference to music queue entry
                    
                    -- Music Information
                    genre TEXT,
                    vocal_type TEXT,          -- vocal, instrumental
                    music_url TEXT,           -- Original music URL from Suno
                    music_title TEXT,
                    music_tags TEXT,          -- JSON array of music tags
                    
                    -- Video Metadata
                    video_title TEXT,         -- Generated/custom video title
                    video_description TEXT,   -- Generated/custom description
                    video_tags TEXT,          -- JSON array of video tags
                    seo_metadata TEXT,        -- JSON with SEO data
                    
                    -- Upload Status
                    upload_status TEXT DEFAULT 'ready',  -- ready, uploading, uploaded, failed
                    youtube_video_id TEXT,    -- YouTube video ID if uploaded
                    upload_channel_id INTEGER, -- Which channel it was uploaded to
                    uploaded_at TEXT,
                    upload_response TEXT,     -- JSON response from YouTube
                    
                    -- Quality and Performance
                    video_quality TEXT DEFAULT 'HD',  -- SD, HD, FHD
                    processing_time INTEGER,  -- Generation time in seconds
                    
                    -- Status and Metadata
                    status TEXT DEFAULT 'available',  -- available, archived, deleted
                    visibility TEXT DEFAULT 'private', -- public, private, unlisted
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    
                    -- Statistics (filled after upload)
                    view_count INTEGER DEFAULT 0,
                    like_count INTEGER DEFAULT 0,
                    comment_count INTEGER DEFAULT 0,
                    last_stats_update TEXT,
                    
                    -- Notes and Custom Fields
                    notes TEXT,               -- User notes
                    custom_fields TEXT,       -- JSON for additional data
                    
                    FOREIGN KEY (upload_channel_id) REFERENCES youtube_channels (id) ON DELETE SET NULL
                )
            ''')
            
            # Video Gallery indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_video_gallery_status ON video_gallery (status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_video_gallery_upload_status ON video_gallery (upload_status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_video_gallery_genre ON video_gallery (genre)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_video_gallery_created ON video_gallery (created_at DESC)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_video_gallery_channel ON video_gallery (upload_channel_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_video_gallery_youtube_id ON video_gallery (youtube_video_id)')
            
            # Add missing columns if they don't exist (migrations)
            try:
                cursor.execute('ALTER TABLE youtube_channels ADD COLUMN oauth_credentials TEXT')
                print("Added oauth_credentials column")
            except sqlite3.OperationalError:
                pass  # Column already exists
            
            try:
                cursor.execute('ALTER TABLE youtube_channels ADD COLUMN oauth_authorized BOOLEAN DEFAULT 0')
                print("Added oauth_authorized column")
            except sqlite3.OperationalError:
                pass  # Column already exists
            
            conn.commit()
            self.logger.info("YouTube Channels database initialized successfully")
    
    def add_channel(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new YouTube channel with comprehensive configuration"""
        try:
            # Debug: Log API credentials being saved to database
            print(f"🗄️ DB add_channel - API credentials being saved:", {
                'api_key': '***set***' if channel_data.get('api_key') else 'empty/missing',
                'client_id': '***set***' if channel_data.get('client_id') else 'empty/missing',
                'client_secret': '***set***' if channel_data.get('client_secret') else 'empty/missing'
            })
            
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
                        api_key, client_id, client_secret, oauth_credentials, oauth_authorized,
                        selected_genres, primary_genre, target_audience,
                        auto_upload, auto_thumbnails, auto_seo, enable_analytics, enable_monetization,
                        daily_upload_count, upload_schedule, upload_hours,
                        vocal_probability, ai_decision_enabled,
                        privacy_settings, default_video_title_template, default_description_template,
                        advanced_settings
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    channel_uuid,
                    channel_data.get('channel_name'),
                    channel_data.get('channel_url'),
                    channel_data.get('youtube_channel_id'),
                    channel_data.get('description'),
                    channel_data.get('api_key'),
                    channel_data.get('client_id'),
                    channel_data.get('client_secret'),
                    channel_data.get('oauth_credentials'),
                    channel_data.get('oauth_authorized', False),
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
            # Debug: Log API credentials being updated in database
            print(f"🗄️ DB update_channel (ID: {channel_id}) - API credentials being updated:", {
                'api_key': '***set***' if channel_data.get('api_key') else 'empty/missing',
                'client_id': '***set***' if channel_data.get('client_id') else 'empty/missing',
                'client_secret': '***set***' if channel_data.get('client_secret') else 'empty/missing'
            })
            
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
                        api_key = ?, client_id = ?, client_secret = ?, oauth_credentials = ?, oauth_authorized = ?,
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
                    channel_data.get('oauth_credentials'),
                    channel_data.get('oauth_authorized', False),
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
                
                # Debug: Log API credentials being retrieved from database
                print(f"🗄️ DB get_channel (ID: {channel_id}) - API credentials retrieved:", {
                    'api_key': '***set***' if channel.get('api_key') else 'empty/missing',
                    'client_id': '***set***' if channel.get('client_id') else 'empty/missing',
                    'client_secret': '***set***' if channel.get('client_secret') else 'empty/missing'
                })
                
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
                    
                    # Debug: Log API credentials being retrieved for each channel
                    print(f"🗄️ DB list_channels - Channel {channel.get('id')}: API credentials = {
                        'api_key: ***set***' if channel.get('api_key') else 'api_key: empty'
                    }, {
                        'client_id: ***set***' if channel.get('client_id') else 'client_id: empty'  
                    }, {
                        'client_secret: ***set***' if channel.get('client_secret') else 'client_secret: empty'
                    }")
                    
                    # Parse JSON fields
                    channel['selected_genres'] = json.loads(channel['selected_genres']) if channel['selected_genres'] else []
                    channel['upload_hours'] = json.loads(channel['upload_hours']) if channel['upload_hours'] else []
                    channel['advanced_settings'] = json.loads(channel['advanced_settings']) if channel['advanced_settings'] else {}
                    
                    channels.append(channel)
                
                return channels
                
        except Exception as e:
            self.logger.error(f"Error listing channels: {e}")
            return []
    
    def add_background_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new background task"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO background_tasks (
                        task_id, task_type, channel_id, title, description,
                        genre, vocal_type, current_step, estimated_duration
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    task_data.get('task_id'),
                    task_data.get('task_type'),
                    task_data.get('channel_id'),
                    task_data.get('title'),
                    task_data.get('description'),
                    task_data.get('genre'),
                    task_data.get('vocal_type'),
                    task_data.get('current_step', 'Initializing'),
                    task_data.get('estimated_duration', 600)  # 10 minutes default
                ))
                
                return {'success': True, 'task_id': task_data.get('task_id')}
                
        except Exception as e:
            self.logger.error(f"Error adding background task: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_task_progress(self, task_id: str, progress: int, step: str = None, detail: str = None, status: str = None) -> bool:
        """Update task progress"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                updates = ['progress = ?']
                params = [progress]
                
                if step:
                    updates.append('current_step = ?')
                    params.append(step)
                
                if detail:
                    updates.append('current_step_detail = ?')
                    params.append(detail)
                
                if status:
                    updates.append('status = ?')
                    params.append(status)
                    if status == 'running' and not cursor.execute('SELECT started_at FROM background_tasks WHERE task_id = ?', (task_id,)).fetchone()[0]:
                        updates.append('started_at = CURRENT_TIMESTAMP')
                    elif status in ['completed', 'failed', 'cancelled']:
                        updates.append('completed_at = CURRENT_TIMESTAMP')
                
                params.append(task_id)
                
                cursor.execute(f'''
                    UPDATE background_tasks 
                    SET {', '.join(updates)}
                    WHERE task_id = ?
                ''', params)
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error updating task progress: {e}")
            return False
    
    def get_background_tasks(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get background tasks with optional status filter"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if status:
                    cursor.execute('''
                        SELECT t.*, c.channel_name 
                        FROM background_tasks t 
                        LEFT JOIN youtube_channels c ON t.channel_id = c.id 
                        WHERE t.status = ? 
                        ORDER BY t.created_at DESC 
                        LIMIT ?
                    ''', (status, limit))
                else:
                    cursor.execute('''
                        SELECT t.*, c.channel_name 
                        FROM background_tasks t 
                        LEFT JOIN youtube_channels c ON t.channel_id = c.id 
                        ORDER BY t.created_at DESC 
                        LIMIT ?
                    ''', (limit,))
                
                rows = cursor.fetchall()
                
                tasks = []
                for row in rows:
                    task = dict(row)
                    
                    # Parse JSON fields
                    if task.get('seo_metadata'):
                        try:
                            task['seo_metadata'] = json.loads(task['seo_metadata'])
                        except:
                            task['seo_metadata'] = {}
                    
                    tasks.append(task)
                
                return tasks
                
        except Exception as e:
            self.logger.error(f"Error getting background tasks: {e}")
            return []
    
    def get_task_statistics(self) -> Dict[str, int]:
        """Get task statistics for dashboard"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get counts by status
                cursor.execute('''
                    SELECT status, COUNT(*) as count 
                    FROM background_tasks 
                    WHERE created_at >= datetime('now', '-24 hours')
                    GROUP BY status
                ''')
                
                stats = {'total': 0, 'queued': 0, 'running': 0, 'completed': 0, 'failed': 0}
                
                for row in cursor.fetchall():
                    status, count = row
                    stats[status] = count
                    stats['total'] += count
                
                return stats
                
        except Exception as e:
            self.logger.error(f"Error getting task statistics: {e}")
            return {'total': 0, 'queued': 0, 'running': 0, 'completed': 0, 'failed': 0}
    
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
    
    # === MUSIC QUEUE MANAGEMENT ===
    
    def add_to_music_queue(self, tracks_data: list, original_task_id: str = None) -> int:
        """Add multiple tracks to music queue (from Suno API response)
        
        Args:
            tracks_data: List of track dictionaries with Suno API data
            original_task_id: Background task ID that generated these tracks
            
        Returns:
            Number of tracks added to queue
        """
        try:
            added_count = 0
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for track in tracks_data:
                    # Generate unique queue UUID
                    import uuid
                    from datetime import datetime, timedelta
                    
                    queue_uuid = str(uuid.uuid4())
                    
                    # Calculate expiry date (30 days from now)
                    expiry_date = (datetime.now() + timedelta(days=30)).isoformat()
                    
                    # Parse duration to seconds for calculations
                    duration_seconds = self._parse_duration_to_seconds(track.get('duration', '0:00'))
                    
                    # Calculate quality score based on title and tags
                    quality_score = self._calculate_quality_score(track)
                    
                    cursor.execute('''
                        INSERT INTO music_queue (
                            queue_uuid, suno_task_id, suno_clip_id, original_task_id,
                            channel_id, genre, title, audio_url, video_url, 
                            duration, duration_seconds, vocal_type, tags, prompt, model_name,
                            quality_score, expiry_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        queue_uuid,
                        track.get('suno_task_id'),
                        track.get('suno_clip_id'),
                        original_task_id,
                        track.get('channel_id'),
                        track.get('genre'),
                        track.get('title'),
                        track.get('audio_url'),
                        track.get('video_url'),
                        track.get('duration'),
                        duration_seconds,
                        track.get('vocal_type'),
                        json.dumps(track.get('tags', [])),
                        track.get('prompt'),
                        track.get('model_name'),
                        quality_score,
                        expiry_date
                    ))
                    
                    added_count += 1
                    print(f"🎵 ➕ Added to queue: {track.get('title')} ({track.get('genre')})")
                
                conn.commit()
                self.logger.info(f"Added {added_count} tracks to music queue")
                return added_count
                
        except Exception as e:
            self.logger.error(f"Error adding tracks to music queue: {e}")
            return 0
    
    def get_queued_track(self, channel_id: int, genre: str = None, vocal_type: str = None) -> Dict[str, Any]:
        """Get best matching track from queue for immediate use
        
        Args:
            channel_id: Channel ID requesting track
            genre: Preferred genre (optional)
            vocal_type: 'vocal' or 'instrumental' (optional)
            
        Returns:
            Track data dict or None if no suitable track found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build query with flexible matching
                base_query = '''
                    SELECT * FROM music_queue 
                    WHERE status = 'available' 
                    AND expiry_date > datetime('now')
                '''
                params = []
                
                # Add filters if specified
                if channel_id:
                    base_query += ' AND channel_id = ?'
                    params.append(channel_id)
                    
                if genre:
                    base_query += ' AND genre = ?'
                    params.append(genre)
                    
                if vocal_type:
                    base_query += ' AND vocal_type = ?'
                    params.append(vocal_type)
                
                # Order by priority and quality
                base_query += ' ORDER BY priority DESC, quality_score DESC, created_at ASC LIMIT 1'
                
                cursor.execute(base_query, params)
                row = cursor.fetchone()
                
                if row:
                    # Convert row to dict
                    columns = [desc[0] for desc in cursor.description]
                    track = dict(zip(columns, row))
                    
                    # Mark as used
                    self._mark_track_as_used(track['queue_uuid'])
                    
                    print(f"🎵 🎯 Using queued track: {track['title']} ({track['genre']})")
                    return track
                else:
                    print(f"🎵 ⚠️ No suitable queued track found for channel {channel_id}, genre: {genre}, vocal: {vocal_type}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error getting queued track: {e}")
            return None
    
    def _mark_track_as_used(self, queue_uuid: str, task_id: str = None):
        """Mark track as used in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE music_queue 
                    SET status = 'used', used_at = datetime('now'), used_for_task = ?
                    WHERE queue_uuid = ?
                ''', (task_id, queue_uuid))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Error marking track as used: {e}")
    
    def get_music_queue_stats(self, channel_id: int = None) -> Dict[str, Any]:
        """Get music queue statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                base_where = "WHERE expiry_date > datetime('now')"
                params = []
                
                if channel_id:
                    base_where += " AND channel_id = ?"
                    params.append(channel_id)
                
                # Count by status
                cursor.execute(f"SELECT status, COUNT(*) FROM music_queue {base_where} GROUP BY status", params)
                status_counts = dict(cursor.fetchall())
                
                # Count by genre
                cursor.execute(f"SELECT genre, COUNT(*) FROM music_queue {base_where} AND status = 'available' GROUP BY genre", params)
                genre_counts = dict(cursor.fetchall())
                
                # Count by vocal type
                cursor.execute(f"SELECT vocal_type, COUNT(*) FROM music_queue {base_where} AND status = 'available' GROUP BY vocal_type", params)
                vocal_counts = dict(cursor.fetchall())
                
                return {
                    'status_counts': status_counts,
                    'genre_counts': genre_counts,
                    'vocal_counts': vocal_counts,
                    'total_available': status_counts.get('available', 0)
                }
                
        except Exception as e:
            self.logger.error(f"Error getting queue stats: {e}")
            return {}
    
    def cleanup_expired_tracks(self) -> int:
        """Remove expired tracks from queue"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM music_queue WHERE expiry_date <= datetime('now')")
                deleted_count = cursor.rowcount
                conn.commit()
                
                if deleted_count > 0:
                    print(f"🎵 🗑️ Cleaned up {deleted_count} expired tracks from queue")
                
                return deleted_count
                
        except Exception as e:
            self.logger.error(f"Error cleaning up expired tracks: {e}")
            return 0
    
    def _parse_duration_to_seconds(self, duration_str: str) -> float:
        """Convert duration string like '3:45' to seconds"""
        try:
            if ':' in duration_str:
                parts = duration_str.split(':')
                if len(parts) == 2:
                    minutes, seconds = parts
                    return float(minutes) * 60 + float(seconds)
                elif len(parts) == 3:
                    hours, minutes, seconds = parts
                    return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
            return float(duration_str)
        except:
            return 180.0  # Default 3 minutes
    
    def _calculate_quality_score(self, track: Dict[str, Any]) -> float:
        """Calculate quality score based on track properties"""
        score = 0.5  # Base score
        
        # Title quality
        title = track.get('title', '')
        if len(title) > 10:
            score += 0.2
        if any(word in title.lower() for word in ['music', 'song', 'track', 'beat']):
            score += 0.1
            
        # Tags quality
        tags = track.get('tags', [])
        if isinstance(tags, list) and len(tags) > 3:
            score += 0.2
            
        return min(1.0, score)  # Cap at 1.0
    
    def update_channel_credentials(self, channel_id: int, credentials_data: Dict[str, str]) -> bool:
        """Update OAuth credentials for a channel"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Update credentials
                cursor.execute('''
                    UPDATE youtube_channels SET
                        oauth_credentials = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    json.dumps(credentials_data),
                    channel_id
                ))
                
                success = cursor.rowcount > 0
                if success:
                    conn.commit()
                    self.logger.info(f"Updated OAuth credentials for channel {channel_id}")
                
                return success
                
        except Exception as e:
            self.logger.error(f"Error updating channel credentials: {e}")
            return False

    def save_channel(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save channel (add new or update existing based on channel_id)"""
        try:
            channel_id = channel_data.get('channel_id') or channel_data.get('id')
            
            if channel_id:
                # Update existing channel
                return self.update_channel(int(channel_id), channel_data)
            else:
                # Add new channel
                return self.add_channel(channel_data)
                
        except Exception as e:
            self.logger.error(f"Error saving channel: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to save channel'
            }
    
    # === VIDEO GALLERY MANAGEMENT ===
    
    def add_to_video_gallery(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add generated video to gallery"""
        try:
            import uuid
            from datetime import datetime
            from pathlib import Path
            
            video_uuid = str(uuid.uuid4())
            
            # Get file information
            file_path = video_data.get('file_path')
            file_size = 0
            if file_path and Path(file_path).exists():
                file_size = Path(file_path).stat().st_size
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO video_gallery (
                        video_uuid, title, description, file_path, thumbnail_path,
                        duration, file_size, file_format, original_task_id, generation_source,
                        music_track_id, genre, vocal_type, music_url, music_title, music_tags,
                        video_title, video_description, video_tags, seo_metadata,
                        video_quality, processing_time, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    video_uuid,
                    video_data.get('title'),
                    video_data.get('description'),
                    video_data.get('file_path'),
                    video_data.get('thumbnail_path'),
                    video_data.get('duration'),
                    file_size,
                    video_data.get('file_format', 'mp4'),
                    video_data.get('original_task_id'),
                    video_data.get('generation_source', 'suno'),
                    video_data.get('music_track_id'),
                    video_data.get('genre'),
                    video_data.get('vocal_type'),
                    video_data.get('music_url'),
                    video_data.get('music_title'),
                    json.dumps(video_data.get('music_tags', [])),
                    video_data.get('video_title'),
                    video_data.get('video_description'),
                    json.dumps(video_data.get('video_tags', [])),
                    json.dumps(video_data.get('seo_metadata', {})),
                    video_data.get('video_quality', 'HD'),
                    video_data.get('processing_time'),
                    video_data.get('notes')
                ))
                
                video_id = cursor.lastrowid
                conn.commit()
                
                self.logger.info(f"Video added to gallery: {video_data.get('title')} (ID: {video_id})")
                
                return {
                    'success': True,
                    'video_id': video_id,
                    'video_uuid': video_uuid,
                    'message': 'Video added to gallery successfully'
                }
                
        except Exception as e:
            self.logger.error(f"Error adding video to gallery: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to add video to gallery'
            }
    
    def get_video_gallery(self, status: str = None, upload_status: str = None, 
                         genre: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get videos from gallery with optional filters"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Build query
                query = '''
                    SELECT v.*, c.channel_name 
                    FROM video_gallery v 
                    LEFT JOIN youtube_channels c ON v.upload_channel_id = c.id 
                    WHERE 1=1
                '''
                params = []
                
                if status:
                    query += ' AND v.status = ?'
                    params.append(status)
                    
                if upload_status:
                    query += ' AND v.upload_status = ?'
                    params.append(upload_status)
                    
                if genre:
                    query += ' AND v.genre = ?'
                    params.append(genre)
                
                query += ' ORDER BY v.created_at DESC LIMIT ?'
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                videos = []
                for row in rows:
                    video = dict(row)
                    
                    # Parse JSON fields
                    video['music_tags'] = json.loads(video['music_tags']) if video['music_tags'] else []
                    video['video_tags'] = json.loads(video['video_tags']) if video['video_tags'] else []
                    video['seo_metadata'] = json.loads(video['seo_metadata']) if video['seo_metadata'] else {}
                    video['custom_fields'] = json.loads(video['custom_fields']) if video['custom_fields'] else {}
                    
                    # Check if file still exists
                    file_path = video.get('file_path')
                    video['file_exists'] = bool(file_path and Path(file_path).exists()) if file_path else False
                    
                    # Format file size
                    if video.get('file_size'):
                        size_mb = video['file_size'] / (1024 * 1024)
                        video['file_size_mb'] = round(size_mb, 1)
                    
                    videos.append(video)
                
                return videos
                
        except Exception as e:
            self.logger.error(f"Error getting video gallery: {e}")
            return []
    
    def get_video_from_gallery(self, video_id: int) -> Optional[Dict[str, Any]]:
        """Get single video from gallery by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT v.*, c.channel_name 
                    FROM video_gallery v 
                    LEFT JOIN youtube_channels c ON v.upload_channel_id = c.id 
                    WHERE v.id = ?
                ''', (video_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                video = dict(row)
                
                # Parse JSON fields
                video['music_tags'] = json.loads(video['music_tags']) if video['music_tags'] else []
                video['video_tags'] = json.loads(video['video_tags']) if video['video_tags'] else []
                video['seo_metadata'] = json.loads(video['seo_metadata']) if video['seo_metadata'] else {}
                
                return video
                
        except Exception as e:
            self.logger.error(f"Error getting video from gallery: {e}")
            return None
    
    def update_video_upload_status(self, video_id: int, upload_data: Dict[str, Any]) -> bool:
        """Update video upload status in gallery"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE video_gallery SET
                        upload_status = ?,
                        youtube_video_id = ?,
                        upload_channel_id = ?,
                        uploaded_at = ?,
                        upload_response = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    upload_data.get('upload_status'),
                    upload_data.get('youtube_video_id'),
                    upload_data.get('upload_channel_id'),
                    upload_data.get('uploaded_at'),
                    json.dumps(upload_data.get('upload_response', {})),
                    video_id
                ))
                
                success = cursor.rowcount > 0
                if success:
                    conn.commit()
                    self.logger.info(f"Updated upload status for video {video_id}")
                
                return success
                
        except Exception as e:
            self.logger.error(f"Error updating video upload status: {e}")
            return False
    
    def delete_video_from_gallery(self, video_id: int, delete_file: bool = False) -> Dict[str, Any]:
        """Delete video from gallery (optionally delete file too)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get video info first
                cursor.execute('SELECT title, file_path FROM video_gallery WHERE id = ?', (video_id,))
                video = cursor.fetchone()
                
                if not video:
                    return {'success': False, 'message': 'Video not found'}
                
                title, file_path = video
                
                # Delete from database
                cursor.execute('DELETE FROM video_gallery WHERE id = ?', (video_id,))
                
                # Optionally delete file
                if delete_file and file_path and Path(file_path).exists():
                    try:
                        Path(file_path).unlink()
                        self.logger.info(f"Deleted video file: {file_path}")
                    except Exception as e:
                        self.logger.warning(f"Could not delete video file: {e}")
                
                conn.commit()
                
                return {
                    'success': True,
                    'message': f'Video "{title}" deleted from gallery'
                }
                
        except Exception as e:
            self.logger.error(f"Error deleting video from gallery: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to delete video'
            }
    
    def get_video_gallery_stats(self) -> Dict[str, Any]:
        """Get video gallery statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Basic counts
                cursor.execute('SELECT COUNT(*) FROM video_gallery WHERE status = "available"')
                total_videos = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM video_gallery WHERE upload_status = "ready"')
                ready_to_upload = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM video_gallery WHERE upload_status = "uploaded"')
                uploaded_videos = cursor.fetchone()[0]
                
                cursor.execute('SELECT SUM(file_size) FROM video_gallery WHERE status = "available"')
                total_size = cursor.fetchone()[0] or 0
                
                # Upload status breakdown
                cursor.execute('SELECT upload_status, COUNT(*) FROM video_gallery GROUP BY upload_status')
                upload_status_breakdown = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Genre breakdown
                cursor.execute('SELECT genre, COUNT(*) FROM video_gallery WHERE genre IS NOT NULL GROUP BY genre')
                genre_breakdown = {row[0]: row[1] for row in cursor.fetchall()}
                
                return {
                    'total_videos': total_videos,
                    'ready_to_upload': ready_to_upload,
                    'uploaded_videos': uploaded_videos,
                    'total_size_mb': round((total_size / (1024 * 1024)), 1) if total_size else 0,
                    'upload_status_breakdown': upload_status_breakdown,
                    'genre_breakdown': genre_breakdown
                }
                
        except Exception as e:
            self.logger.error(f"Error getting video gallery stats: {e}")
            return {}