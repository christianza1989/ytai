"""
Database Manager for AI Music Empire
Handles all database operations for YouTube channels, content creation, and analytics
"""

import json
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
import logging

from .models import Base, YouTubeChannel, ContentCreation, YouTubeVideo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Centralized database management for the AI Music Empire system"""
    
    def __init__(self, db_path: str = "database.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        
        # Create all tables
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        
        logger.info(f"Database initialized: {db_path}")
    
    def get_session(self):
        """Get a database session"""
        return self.Session()
    
    def close_session(self):
        """Close the session"""
        self.Session.remove()
    
    # =================== YouTube Channel Management ===================
    
    def create_youtube_channel(self, channel_data: Dict[str, Any]) -> Optional[int]:
        """Create a new YouTube channel record"""
        session = self.get_session()
        try:
            # Ensure JSON fields are properly serialized
            if isinstance(channel_data.get('upload_schedule'), dict):
                channel_data['upload_schedule'] = json.dumps(channel_data['upload_schedule'])
            if isinstance(channel_data.get('secondary_genres'), list):
                channel_data['secondary_genres'] = json.dumps(channel_data['secondary_genres'])
            if isinstance(channel_data.get('style_preferences'), dict):
                channel_data['style_preferences'] = json.dumps(channel_data['style_preferences'])
            if isinstance(channel_data.get('privacy_settings'), dict):
                channel_data['privacy_settings'] = json.dumps(channel_data['privacy_settings'])
            
            # Set timestamps
            now = datetime.now(timezone.utc)
            channel_data['created_at'] = now
            channel_data['updated_at'] = now
            
            # Set default values for required fields
            channel_data.setdefault('secondary_genres', '[]')
            channel_data.setdefault('upload_schedule', '{}')
            channel_data.setdefault('preferred_upload_time', '14:00')
            channel_data.setdefault('timezone', 'Europe/Vilnius')
            channel_data.setdefault('auto_upload', False)
            channel_data.setdefault('auto_thumbnails', False)
            channel_data.setdefault('auto_seo', False)
            channel_data.setdefault('enable_analytics', False)
            channel_data.setdefault('enable_monetization', False)
            channel_data.setdefault('privacy_settings', 'private')
            channel_data.setdefault('comments_enabled', True)
            channel_data.setdefault('ratings_enabled', True)
            channel_data.setdefault('notify_subscribers', False)
            channel_data.setdefault('status', 'needs_setup')
            channel_data.setdefault('subscribers', 0)
            channel_data.setdefault('total_views', 0)
            channel_data.setdefault('total_videos', 0)
            channel_data.setdefault('monthly_revenue', 0.0)
            channel_data.setdefault('error_count', 0)
            
            channel = YouTubeChannel(**channel_data)
            session.add(channel)
            session.commit()
            
            channel_id = channel.id
            logger.info(f"Created YouTube channel: {channel_id}")
            return channel_id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating YouTube channel: {e}")
            return None
        finally:
            session.close()
    
    def get_youtube_channel(self, channel_id: int) -> Optional[Dict[str, Any]]:
        """Get YouTube channel by ID"""
        session = self.get_session()
        try:
            channel = session.query(YouTubeChannel).filter_by(id=channel_id).first()
            if channel:
                return self._youtube_channel_to_dict(channel)
            return None
        except Exception as e:
            logger.error(f"Error getting YouTube channel {channel_id}: {e}")
            return None
        finally:
            session.close()
    
    def get_all_youtube_channels(self) -> List[Dict[str, Any]]:
        """Get all YouTube channels"""
        session = self.get_session()
        try:
            channels = session.query(YouTubeChannel).all()
            return [self._youtube_channel_to_dict(channel) for channel in channels]
        except Exception as e:
            logger.error(f"Error getting YouTube channels: {e}")
            return []
        finally:
            session.close()
    
    def update_youtube_channel(self, channel_id: int, updates: Dict[str, Any]) -> bool:
        """Update YouTube channel"""
        session = self.get_session()
        try:
            # Ensure JSON fields are properly serialized
            if isinstance(updates.get('upload_schedule'), dict):
                updates['upload_schedule'] = json.dumps(updates['upload_schedule'])
            if isinstance(updates.get('secondary_genres'), list):
                updates['secondary_genres'] = json.dumps(updates['secondary_genres'])
            if isinstance(updates.get('style_preferences'), dict):
                updates['style_preferences'] = json.dumps(updates['style_preferences'])
            if isinstance(updates.get('privacy_settings'), dict):
                updates['privacy_settings'] = json.dumps(updates['privacy_settings'])
            
            updates['updated_at'] = datetime.now(timezone.utc)
            
            result = session.query(YouTubeChannel).filter_by(id=channel_id).update(updates)
            session.commit()
            
            if result > 0:
                logger.info(f"Updated YouTube channel: {channel_id}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating YouTube channel {channel_id}: {e}")
            return False
        finally:
            session.close()
    
    def delete_youtube_channel(self, channel_id: int) -> bool:
        """Delete YouTube channel"""
        session = self.get_session()
        try:
            result = session.query(YouTubeChannel).filter_by(id=channel_id).delete()
            session.commit()
            
            if result > 0:
                logger.info(f"Deleted YouTube channel: {channel_id}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting YouTube channel {channel_id}: {e}")
            return False
        finally:
            session.close()
    
    def get_youtube_channels_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get YouTube channels by status"""
        session = self.get_session()
        try:
            channels = session.query(YouTubeChannel).filter_by(status=status).all()
            return [self._youtube_channel_to_dict(channel) for channel in channels]
        except Exception as e:
            logger.error(f"Error getting YouTube channels by status {status}: {e}")
            return []
        finally:
            session.close()
    
    def get_youtube_channels_statistics(self) -> Dict[str, Any]:
        """Get YouTube channels statistics"""
        session = self.get_session()
        try:
            total_channels = session.query(YouTubeChannel).count()
            active_channels = session.query(YouTubeChannel).filter_by(status='active').count()
            needs_setup = session.query(YouTubeChannel).filter_by(status='needs_setup').count()
            
            # Calculate total metrics
            channels = session.query(YouTubeChannel).all()
            total_subscribers = sum(ch.subscribers or 0 for ch in channels)
            total_views = sum(ch.total_views or 0 for ch in channels)
            total_videos = sum(ch.total_videos or 0 for ch in channels)
            total_revenue = sum(ch.monthly_revenue or 0 for ch in channels)
            
            return {
                'total_channels': total_channels,
                'active_channels': active_channels,
                'needs_setup': needs_setup,
                'total_subscribers': total_subscribers,
                'total_views': total_views,
                'total_videos': total_videos,
                'total_monthly_revenue': total_revenue
            }
        except Exception as e:
            logger.error(f"Error getting YouTube channels statistics: {e}")
            return {}
        finally:
            session.close()
    
    def _youtube_channel_to_dict(self, channel: YouTubeChannel) -> Dict[str, Any]:
        """Convert YouTubeChannel object to dictionary"""
        try:
            return {
                'id': channel.id,
                'name': channel.name,
                'url': channel.url,
                'youtube_channel_id': channel.youtube_channel_id,
                'description': channel.description,
                'api_key': channel.api_key,
                'client_id': channel.client_id,
                'client_secret': channel.client_secret,
                'refresh_token': channel.refresh_token,
                'primary_genre': channel.primary_genre,
                'secondary_genres': json.loads(channel.secondary_genres or '[]'),
                'target_audience': channel.target_audience,
                'style_preferences': json.loads(channel.style_preferences or '{}'),
                'upload_schedule': json.loads(channel.upload_schedule or '{}'),
                'preferred_upload_time': channel.preferred_upload_time,
                'timezone': channel.timezone,
                'auto_upload': channel.auto_upload,
                'auto_thumbnails': channel.auto_thumbnails,
                'auto_seo': channel.auto_seo,
                'enable_analytics': channel.enable_analytics,
                'enable_monetization': channel.enable_monetization,
                'privacy_settings': channel.privacy_settings,
                'comments_enabled': channel.comments_enabled,
                'ratings_enabled': channel.ratings_enabled,
                'notify_subscribers': channel.notify_subscribers,
                'status': channel.status,
                'subscribers': channel.subscribers,
                'total_views': channel.total_views,
                'total_videos': channel.total_videos,
                'monthly_revenue': channel.monthly_revenue,
                'created_at': channel.created_at.isoformat() if channel.created_at else None,
                'updated_at': channel.updated_at.isoformat() if channel.updated_at else None,
                'last_upload': channel.last_upload.isoformat() if channel.last_upload else None,
                'last_sync': channel.last_sync.isoformat() if channel.last_sync else None,
                'last_error': channel.last_error,
                'error_count': channel.error_count
            }
        except Exception as e:
            logger.error(f"Error converting YouTube channel to dict: {e}")
            return {}
    
    # =================== Content Creation Management ===================
    
    def create_content_creation(self, content_data: Dict[str, Any]) -> Optional[int]:
        """Create a new content creation record"""
        session = self.get_session()
        try:
            # Ensure JSON fields are properly serialized
            if isinstance(content_data.get('brief_json'), dict):
                content_data['brief_json'] = json.dumps(content_data['brief_json'])
            
            content = ContentCreation(**content_data)
            session.add(content)
            session.commit()
            
            content_id = content.id
            logger.info(f"Created content creation: {content_id}")
            return content_id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating content creation: {e}")
            return None
        finally:
            session.close()
    
    def get_content_creation(self, content_id: int) -> Optional[Dict[str, Any]]:
        """Get content creation by ID"""
        session = self.get_session()
        try:
            content = session.query(ContentCreation).filter_by(id=content_id).first()
            if content:
                return content.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error getting content creation {content_id}: {e}")
            return None
        finally:
            session.close()
    
    def get_recent_content_creations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent content creations"""
        session = self.get_session()
        try:
            contents = session.query(ContentCreation)\
                           .order_by(ContentCreation.creation_date.desc())\
                           .limit(limit).all()
            return [content.to_dict() for content in contents]
        except Exception as e:
            logger.error(f"Error getting recent content creations: {e}")
            return []
        finally:
            session.close()
    
    def update_content_creation_status(self, content_id: int, status: str) -> bool:
        """Update content creation status"""
        session = self.get_session()
        try:
            result = session.query(ContentCreation)\
                          .filter_by(id=content_id)\
                          .update({'status': status})
            session.commit()
            
            if result > 0:
                logger.info(f"Updated content creation status: {content_id} -> {status}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating content creation status {content_id}: {e}")
            return False
        finally:
            session.close()
    
    # =================== System Statistics ===================
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        session = self.get_session()
        try:
            # Content creation stats
            total_content = session.query(ContentCreation).count()
            completed_content = session.query(ContentCreation).filter_by(status='created').count()
            uploaded_content = session.query(ContentCreation).filter_by(status='uploaded').count()
            
            # Recent projects
            recent_contents = session.query(ContentCreation)\
                                  .order_by(ContentCreation.creation_date.desc())\
                                  .limit(5).all()
            
            return {
                'total_content_created': total_content,
                'completed_content': completed_content,
                'uploaded_content': uploaded_content,
                'recent_projects': [content.to_dict() for content in recent_contents],
                'youtube_stats': self.get_youtube_channels_statistics()
            }
        except Exception as e:
            logger.error(f"Error getting system statistics: {e}")
            return {}
        finally:
            session.close()
    
    # =================== Utility Methods ===================
    
    def execute_raw_sql(self, sql: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute raw SQL query (use with caution)"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql), params or {})
                return [dict(row) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Error executing raw SQL: {e}")
            return []
    
    def backup_database(self, backup_path: str) -> bool:
        """Create a backup of the database"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            return False
    
    def get_active_channels_for_automation(self) -> List[Dict[str, Any]]:
        """Get channels that are ready for 24/7 automation"""
        session = self.get_session()
        try:
            # Get channels that have active status (have API keys set up)
            channels = session.query(YouTubeChannel).filter_by(status='active').all()
            return [self._youtube_channel_to_dict(channel) for channel in channels]
        except Exception as e:
            logger.error(f"Error getting active channels for automation: {e}")
            return []
        finally:
            session.close()
    
    def cleanup_old_records(self, days_old: int = 30) -> int:
        """Clean up old records (placeholder for future implementation)"""
        # This would clean up old content creation records, logs, etc.
        # Implementation depends on specific cleanup requirements
        return 0