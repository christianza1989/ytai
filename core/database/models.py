from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Float
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
