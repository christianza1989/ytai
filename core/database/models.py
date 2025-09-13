from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import json

Base = declarative_base()

class ContentCreation(Base):
    """Model for tracking content creation cycles"""
    __tablename__ = 'content_creations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime, default=datetime.utcnow)
    genre = Column(String(100))
    theme = Column(String(200))
    title = Column(String(200))
    youtube_title = Column(String(100))  # Optimized YouTube title
    brief_json = Column(Text)  # Store full Gemini brief as JSON
    suno_task_id = Column(String(100))
    cover_image_path = Column(String(500))
    status = Column(String(50), default='creating')  # 'creating', 'created', 'uploaded', 'analyzed'

    # Relationship to YouTube videos
    youtube_videos = relationship("YouTubeVideo", back_populates="content_creation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ContentCreation(id={self.id}, title='{self.title}', status='{self.status}')>"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'genre': self.genre,
            'theme': self.theme,
            'title': self.title,
            'youtube_title': self.youtube_title,
            'brief_json': self.brief_json,
            'suno_task_id': self.suno_task_id,
            'cover_image_path': self.cover_image_path,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        """Create instance from dictionary"""
        brief_json = data.get('brief_json')
        if isinstance(brief_json, dict):
            brief_json = json.dumps(brief_json)

        return cls(
            genre=data.get('genre'),
            theme=data.get('theme'),
            title=data.get('title'),
            youtube_title=data.get('youtube_title'),
            brief_json=brief_json,
            suno_task_id=data.get('suno_task_id'),
            cover_image_path=data.get('cover_image_path'),
            status=data.get('status', 'creating')
        )


class YouTubeVideo(Base):
    """Model for tracking uploaded YouTube videos"""
    __tablename__ = 'youtube_videos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(Integer, ForeignKey('content_creations.id'), nullable=False)
    video_id = Column(String(50), unique=True, nullable=False)  # YouTube video ID
    youtube_url = Column(String(200), nullable=False)
    title = Column(String(200))
    description = Column(Text)
    tags = Column(Text)  # Store as JSON string
    category_id = Column(String(10), default='10')  # 10 = Music
    privacy_status = Column(String(20), default='private')
    upload_date = Column(DateTime, default=datetime.utcnow)

    # Relationship to content creation
    content_creation = relationship("ContentCreation", back_populates="youtube_videos")

    # Relationship to performance metrics
    performance_metrics = relationship("PerformanceMetric", back_populates="youtube_video", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<YouTubeVideo(id={self.id}, video_id='{self.video_id}', title='{self.title}')>"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'content_id': self.content_id,
            'video_id': self.video_id,
            'youtube_url': self.youtube_url,
            'title': self.title,
            'description': self.description,
            'tags': self.tags,
            'category_id': self.category_id,
            'privacy_status': self.privacy_status,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None
        }

    @classmethod
    def from_dict(cls, data):
        """Create instance from dictionary"""
        tags = data.get('tags')
        if isinstance(tags, list):
            tags = json.dumps(tags)

        return cls(
            content_id=data['content_id'],
            video_id=data['video_id'],
            youtube_url=data['youtube_url'],
            title=data.get('title'),
            description=data.get('description'),
            tags=tags,
            category_id=data.get('category_id', '10'),
            privacy_status=data.get('privacy_status', 'private')
        )

    def get_tags_list(self):
        """Get tags as a list"""
        if not self.tags:
            return []
        try:
            return json.loads(self.tags)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_tags_list(self, tags_list):
        """Set tags from a list"""
        if isinstance(tags_list, list):
            self.tags = json.dumps(tags_list)
        else:
            self.tags = tags_list


class PerformanceMetric(Base):
    """Model for tracking YouTube video performance metrics"""
    __tablename__ = 'performance_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey('youtube_videos.id'), nullable=False)
    check_date = Column(DateTime, default=datetime.utcnow)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    subscriber_gain = Column(Integer, default=0)  # Subscriber change since last check

    # Additional metrics for future use
    average_view_duration = Column(Float, default=0.0)  # in seconds
    click_through_rate = Column(Float, default=0.0)  # CTR percentage
    traffic_source_breakdown = Column(Text)  # JSON string with traffic sources

    # Relationship to YouTube video
    youtube_video = relationship("YouTubeVideo", back_populates="performance_metrics")

    def __repr__(self):
        return f"<PerformanceMetric(id={self.id}, video_id={self.video_id}, views={self.view_count}, date={self.check_date})>"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'video_id': self.video_id,
            'check_date': self.check_date.isoformat() if self.check_date else None,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'subscriber_gain': self.subscriber_gain,
            'average_view_duration': self.average_view_duration,
            'click_through_rate': self.click_through_rate,
            'traffic_source_breakdown': self.traffic_source_breakdown
        }

    @classmethod
    def from_dict(cls, data):
        """Create instance from dictionary"""
        traffic_sources = data.get('traffic_source_breakdown')
        if isinstance(traffic_sources, dict):
            traffic_sources = json.dumps(traffic_sources)

        return cls(
            video_id=data['video_id'],
            view_count=data.get('view_count', 0),
            like_count=data.get('like_count', 0),
            comment_count=data.get('comment_count', 0),
            subscriber_gain=data.get('subscriber_gain', 0),
            average_view_duration=data.get('average_view_duration', 0.0),
            click_through_rate=data.get('click_through_rate', 0.0),
            traffic_source_breakdown=traffic_sources
        )

    def calculate_engagement_rate(self):
        """Calculate engagement rate (likes + comments) / views"""
        if self.view_count == 0:
            return 0.0
        return ((self.like_count + self.comment_count) / self.view_count) * 100


class YouTubeChannel(Base):
    """Model for managing YouTube channels with their credentials and settings"""
    __tablename__ = 'youtube_channels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic Information
    name = Column(String(200), nullable=False)
    url = Column(String(500))
    youtube_channel_id = Column(String(100), unique=True)
    description = Column(Text)
    
    # API Credentials (encrypted in production)
    api_key = Column(Text)  # YouTube Data API key
    client_id = Column(Text)  # OAuth Client ID
    client_secret = Column(Text)  # OAuth Client Secret
    refresh_token = Column(Text)  # OAuth Refresh Token
    
    # Music Style and Preferences
    primary_genre = Column(String(100), nullable=False)
    secondary_genres = Column(Text)  # JSON array of secondary genres
    target_audience = Column(String(100))
    style_preferences = Column(Text)  # JSON object with style preferences
    
    # Upload and Scheduling Settings
    upload_schedule = Column(String(50), default='daily')  # daily, weekly, etc.
    preferred_upload_time = Column(String(10), default='14:00')  # HH:MM format
    timezone = Column(String(50), default='Europe/Vilnius')
    
    # Automation Settings
    auto_upload = Column(Boolean, default=True)
    auto_thumbnails = Column(Boolean, default=True)
    auto_seo = Column(Boolean, default=True)
    enable_analytics = Column(Boolean, default=True)
    enable_monetization = Column(Boolean, default=False)
    
    # Privacy and Safety Settings
    privacy_settings = Column(String(20), default='private')  # private, unlisted, public
    comments_enabled = Column(Boolean, default=True)
    ratings_enabled = Column(Boolean, default=True)
    notify_subscribers = Column(Boolean, default=False)  # Safe default for bulk uploads
    
    # Channel Status and Metrics
    status = Column(String(50), default='needs_setup')  # active, inactive, needs_setup, error
    subscribers = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_videos = Column(Integer, default=0)
    monthly_revenue = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_upload = Column(DateTime)
    last_sync = Column(DateTime)  # Last time we synced with YouTube API
    
    # Error tracking
    last_error = Column(Text)
    error_count = Column(Integer, default=0)

    def __repr__(self):
        return f"<YouTubeChannel(id={self.id}, name='{self.name}', status='{self.status}')>"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'youtube_channel_id': self.youtube_channel_id,
            'description': self.description,
            'primary_genre': self.primary_genre,
            'secondary_genres': self.get_secondary_genres_list(),
            'target_audience': self.target_audience,
            'style_preferences': self.get_style_preferences_dict(),
            'upload_schedule': self.upload_schedule,
            'preferred_upload_time': self.preferred_upload_time,
            'timezone': self.timezone,
            'auto_upload': self.auto_upload,
            'auto_thumbnails': self.auto_thumbnails,
            'auto_seo': self.auto_seo,
            'enable_analytics': self.enable_analytics,
            'enable_monetization': self.enable_monetization,
            'privacy_settings': self.privacy_settings,
            'comments_enabled': self.comments_enabled,
            'ratings_enabled': self.ratings_enabled,
            'notify_subscribers': self.notify_subscribers,
            'status': self.status,
            'subscribers': self.subscribers,
            'total_views': self.total_views,
            'total_videos': self.total_videos,
            'monthly_revenue': self.monthly_revenue,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_upload': self.last_upload.isoformat() if self.last_upload else None,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'has_credentials': bool(self.api_key and self.client_id)
        }

    @classmethod
    def from_dict(cls, data):
        """Create instance from dictionary"""
        secondary_genres = data.get('secondary_genres')
        if isinstance(secondary_genres, list):
            secondary_genres = json.dumps(secondary_genres)

        style_preferences = data.get('style_preferences')
        if isinstance(style_preferences, dict):
            style_preferences = json.dumps(style_preferences)

        return cls(
            name=data['name'],
            url=data.get('url'),
            youtube_channel_id=data.get('youtube_channel_id'),
            description=data.get('description'),
            api_key=data.get('api_key'),
            client_id=data.get('client_id'),
            client_secret=data.get('client_secret'),
            primary_genre=data['primary_genre'],
            secondary_genres=secondary_genres,
            target_audience=data.get('target_audience'),
            style_preferences=style_preferences,
            upload_schedule=data.get('upload_schedule', 'daily'),
            preferred_upload_time=data.get('preferred_upload_time', '14:00'),
            timezone=data.get('timezone', 'Europe/Vilnius'),
            auto_upload=data.get('auto_upload', True),
            auto_thumbnails=data.get('auto_thumbnails', True),
            auto_seo=data.get('auto_seo', True),
            enable_analytics=data.get('enable_analytics', True),
            enable_monetization=data.get('enable_monetization', False),
            privacy_settings=data.get('privacy_settings', 'private'),
            comments_enabled=data.get('comments_enabled', True),
            ratings_enabled=data.get('ratings_enabled', True),
            notify_subscribers=data.get('notify_subscribers', False),
            status=data.get('status', 'needs_setup')
        )

    def get_secondary_genres_list(self):
        """Get secondary genres as a list"""
        if not self.secondary_genres:
            return []
        try:
            return json.loads(self.secondary_genres)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_secondary_genres_list(self, genres_list):
        """Set secondary genres from a list"""
        if isinstance(genres_list, list):
            self.secondary_genres = json.dumps(genres_list)
        else:
            self.secondary_genres = genres_list

    def get_style_preferences_dict(self):
        """Get style preferences as a dictionary"""
        if not self.style_preferences:
            return {}
        try:
            return json.loads(self.style_preferences)
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_style_preferences_dict(self, preferences_dict):
        """Set style preferences from a dictionary"""
        if isinstance(preferences_dict, dict):
            self.style_preferences = json.dumps(preferences_dict)
        else:
            self.style_preferences = preferences_dict

    def update_metrics(self, subscribers=None, total_views=None, total_videos=None, monthly_revenue=None):
        """Update channel metrics"""
        if subscribers is not None:
            self.subscribers = subscribers
        if total_views is not None:
            self.total_views = total_views
        if total_videos is not None:
            self.total_videos = total_videos
        if monthly_revenue is not None:
            self.monthly_revenue = monthly_revenue
        self.updated_at = datetime.utcnow()

    def record_error(self, error_message):
        """Record an error for this channel"""
        self.last_error = error_message
        self.error_count += 1
        self.status = 'error'
        self.updated_at = datetime.utcnow()

    def clear_error(self):
        """Clear error status"""
        self.last_error = None
        self.error_count = 0
        if self.status == 'error':
            self.status = 'active'
        self.updated_at = datetime.utcnow()

    def is_ready_for_automation(self):
        """Check if channel is ready for automated operations"""
        return (
            self.status == 'active' and
            self.api_key and
            self.client_id and
            self.primary_genre and
            not self.last_error
        )

    def get_traffic_sources(self):
        """Get traffic sources as a dictionary"""
        if not self.traffic_source_breakdown:
            return {}
        try:
            return json.loads(self.traffic_source_breakdown)
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_traffic_sources(self, sources_dict):
        """Set traffic sources from a dictionary"""
        if isinstance(sources_dict, dict):
            self.traffic_source_breakdown = json.dumps(sources_dict)
        else:
            self.traffic_source_breakdown = sources_dict
