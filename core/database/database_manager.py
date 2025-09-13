import os
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
import json

from .models import Base, ContentCreation, YouTubeVideo, PerformanceMetric

class DatabaseManager:
    """Database manager for handling all database operations"""

    def __init__(self):
        # Get database URL from environment
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///database.db')

        # Create engine
        self.engine = create_engine(
            self.database_url,
            echo=False,  # Set to True for debugging
            connect_args={"check_same_thread": False} if self.database_url.startswith('sqlite') else {}
        )

        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Initialize database
        self.init_db()

    def init_db(self):
        """Initialize database and create all tables"""
        try:
            print("🔧 Initializing database...")
            Base.metadata.create_all(bind=self.engine)
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize database: {e}")
            raise

    def get_db(self) -> Session:
        """Get database session"""
        return self.SessionLocal()

    def close_db(self, db: Session):
        """Close database session"""
        db.close()

    # Content Creation CRUD Operations
    def add_content_creation(self, data: Dict[str, Any]) -> ContentCreation:
        """Add new content creation to database"""
        db = self.get_db()
        try:
            content_creation = ContentCreation.from_dict(data)
            db.add(content_creation)
            db.commit()
            db.refresh(content_creation)
            print(f"✅ Content creation added to database: {content_creation.title}")
            return content_creation
        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Failed to add content creation: {e}")
            raise
        finally:
            self.close_db(db)

    def get_creation_by_id(self, creation_id: int) -> Optional[ContentCreation]:
        """Get content creation by ID"""
        db = self.get_db()
        try:
            return db.query(ContentCreation).filter(ContentCreation.id == creation_id).first()
        finally:
            self.close_db(db)

    def get_all_creations(self, limit: int = 50) -> List[ContentCreation]:
        """Get all content creations"""
        db = self.get_db()
        try:
            return db.query(ContentCreation).order_by(ContentCreation.creation_date.desc()).limit(limit).all()
        finally:
            self.close_db(db)

    def update_creation_status(self, creation_id: int, new_status: str) -> bool:
        """Update content creation status"""
        db = self.get_db()
        try:
            creation = db.query(ContentCreation).filter(ContentCreation.id == creation_id).first()
            if creation:
                creation.status = new_status
                db.commit()
                print(f"✅ Content creation {creation_id} status updated to: {new_status}")
                return True
            else:
                print(f"❌ Content creation {creation_id} not found")
                return False
        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Failed to update creation status: {e}")
            return False
        finally:
            self.close_db(db)

    # YouTube Video CRUD Operations
    def add_youtube_video(self, creation_obj: ContentCreation, video_data: Dict[str, Any]) -> YouTubeVideo:
        """Add YouTube video to database"""
        db = self.get_db()
        try:
            # Add content_id to video data
            video_data['content_id'] = creation_obj.id

            youtube_video = YouTubeVideo.from_dict(video_data)
            db.add(youtube_video)
            db.commit()
            db.refresh(youtube_video)
            print(f"✅ YouTube video added to database: {youtube_video.title}")
            return youtube_video
        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Failed to add YouTube video: {e}")
            raise
        finally:
            self.close_db(db)

    def get_video_by_youtube_id(self, youtube_video_id: str) -> Optional[YouTubeVideo]:
        """Get YouTube video by YouTube video ID"""
        db = self.get_db()
        try:
            return db.query(YouTubeVideo).filter(YouTubeVideo.video_id == youtube_video_id).first()
        finally:
            self.close_db(db)

    def get_videos_by_creation_id(self, creation_id: int) -> List[YouTubeVideo]:
        """Get all YouTube videos for a content creation"""
        db = self.get_db()
        try:
            return db.query(YouTubeVideo).filter(YouTubeVideo.content_id == creation_id).all()
        finally:
            self.close_db(db)

    def get_all_videos(self, limit: int = 100) -> List[YouTubeVideo]:
        """Get all YouTube videos"""
        db = self.get_db()
        try:
            return db.query(YouTubeVideo).order_by(YouTubeVideo.upload_date.desc()).limit(limit).all()
        finally:
            self.close_db(db)

    # Performance Metrics CRUD Operations
    def add_performance_metric(self, video_id: int, metrics_data: Dict[str, Any]) -> PerformanceMetric:
        """Add performance metrics for a video"""
        db = self.get_db()
        try:
            # Check if we already have metrics for today
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)

            existing_metric = db.query(PerformanceMetric)\
                               .filter(PerformanceMetric.video_id == video_id)\
                               .filter(PerformanceMetric.check_date >= today_start)\
                               .filter(PerformanceMetric.check_date < today_end)\
                               .first()

            if existing_metric:
                # Update existing metrics
                existing_metric.view_count = metrics_data.get('view_count', existing_metric.view_count)
                existing_metric.like_count = metrics_data.get('like_count', existing_metric.like_count)
                existing_metric.comment_count = metrics_data.get('comment_count', existing_metric.comment_count)
                existing_metric.check_date = datetime.utcnow()
                db.commit()
                db.refresh(existing_metric)
                print(f"✅ Updated existing metrics for video {video_id}")
                return existing_metric
            else:
                # Create new metrics entry
                metrics_data['video_id'] = video_id
                metric = PerformanceMetric.from_dict(metrics_data)
                db.add(metric)
                db.commit()
                db.refresh(metric)
                print(f"✅ Added new performance metrics for video {video_id}")
                return metric

        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Failed to add/update performance metrics: {e}")
            raise
        finally:
            self.close_db(db)

    def get_latest_metrics_for_video(self, video_id: int) -> Optional[PerformanceMetric]:
        """Get latest performance metrics for a video"""
        db = self.get_db()
        try:
            return db.query(PerformanceMetric)\
                    .filter(PerformanceMetric.video_id == video_id)\
                    .order_by(PerformanceMetric.check_date.desc())\
                    .first()
        finally:
            self.close_db(db)

    def get_metrics_history_for_video(self, video_id: int, days: int = 30) -> List[PerformanceMetric]:
        """Get performance metrics history for a video"""
        db = self.get_db()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            return db.query(PerformanceMetric)\
                    .filter(PerformanceMetric.video_id == video_id)\
                    .filter(PerformanceMetric.check_date >= cutoff_date)\
                    .order_by(PerformanceMetric.check_date.desc())\
                    .all()
        finally:
            self.close_db(db)

    # Analytics and Reporting
    def get_content_performance_summary(self) -> Dict[str, Any]:
        """Get overall content performance summary"""
        db = self.get_db()
        try:
            # Get total counts
            total_creations = db.query(ContentCreation).count()
            total_videos = db.query(YouTubeVideo).count()
            total_views = db.query(PerformanceMetric).with_entities(
                func.sum(PerformanceMetric.view_count)
            ).scalar() or 0

            # Get status breakdown
            status_counts = db.query(ContentCreation.status, func.count(ContentCreation.id))\
                             .group_by(ContentCreation.status).all()
            status_breakdown = {status: count for status, count in status_counts}

            # Get recent activity (last 7 days)
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_creations = db.query(ContentCreation)\
                                .filter(ContentCreation.creation_date >= week_ago).count()
            recent_videos = db.query(YouTubeVideo)\
                             .filter(YouTubeVideo.upload_date >= week_ago).count()

            return {
                'total_creations': total_creations,
                'total_videos': total_videos,
                'total_views': total_views,
                'status_breakdown': status_breakdown,
                'recent_creations': recent_creations,
                'recent_videos': recent_videos
            }
        finally:
            self.close_db(db)

    def get_top_performing_videos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing videos by view count"""
        db = self.get_db()
        try:
            # Get latest metrics for each video
            subquery = db.query(
                PerformanceMetric.video_id,
                func.max(PerformanceMetric.check_date).label('latest_date')
            ).group_by(PerformanceMetric.video_id).subquery()

            results = db.query(
                YouTubeVideo,
                PerformanceMetric.view_count,
                PerformanceMetric.like_count,
                PerformanceMetric.comment_count
            ).join(
                PerformanceMetric,
                db.and_(
                    PerformanceMetric.video_id == YouTubeVideo.id,
                    PerformanceMetric.check_date == subquery.c.latest_date
                )
            ).order_by(PerformanceMetric.view_count.desc()).limit(limit).all()

            top_videos = []
            for video, views, likes, comments in results:
                top_videos.append({
                    'video_id': video.video_id,
                    'title': video.title,
                    'youtube_url': video.youtube_url,
                    'views': views,
                    'likes': likes,
                    'comments': comments,
                    'upload_date': video.upload_date.isoformat() if video.upload_date else None
                })

            return top_videos
        finally:
            self.close_db(db)

    def get_genre_performance_analysis(self) -> Dict[str, Any]:
        """Analyze performance by genre"""
        db = self.get_db()
        try:
            results = db.query(
                ContentCreation.genre,
                func.count(ContentCreation.id).label('creation_count'),
                func.avg(PerformanceMetric.view_count).label('avg_views'),
                func.avg(PerformanceMetric.like_count).label('avg_likes')
            ).join(
                YouTubeVideo, ContentCreation.id == YouTubeVideo.content_id
            ).join(
                PerformanceMetric, YouTubeVideo.id == PerformanceMetric.video_id
            ).group_by(ContentCreation.genre).all()

            genre_analysis = {}
            for genre, count, avg_views, avg_likes in results:
                if genre:  # Skip None values
                    genre_analysis[genre] = {
                        'creation_count': count,
                        'avg_views': float(avg_views or 0),
                        'avg_likes': float(avg_likes or 0)
                    }

            return genre_analysis
        finally:
            self.close_db(db)

    # Utility methods
    def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old performance metrics data"""
        db = self.get_db()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            deleted_count = db.query(PerformanceMetric)\
                             .filter(PerformanceMetric.check_date < cutoff_date)\
                             .delete()
            db.commit()
            print(f"✅ Cleaned up {deleted_count} old performance metrics")
            return deleted_count
        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Failed to cleanup old data: {e}")
            return 0
        finally:
            self.close_db(db)

    def export_data_to_json(self, filename: str = "database_export.json"):
        """Export all data to JSON file for backup"""
        db = self.get_db()
        try:
            data = {
                'content_creations': [creation.to_dict() for creation in self.get_all_creations(1000)],
                'youtube_videos': [video.to_dict() for video in self.get_all_videos(1000)],
                'export_date': datetime.utcnow().isoformat()
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Database exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to export data: {e}")
            return False
        finally:
            self.close_db(db)

    def get_performance_summary_for_analysis(self) -> str:
        """
        Get comprehensive performance summary formatted for AI analysis

        Returns:
            Formatted string with all video performance data for analysis
        """
        db = self.get_db()
        try:
            # Get all videos with their latest performance metrics
            results = db.query(
                YouTubeVideo,
                ContentCreation.genre,
                ContentCreation.theme,
                PerformanceMetric.view_count,
                PerformanceMetric.like_count,
                PerformanceMetric.comment_count,
                PerformanceMetric.check_date
            ).join(
                ContentCreation, YouTubeVideo.content_id == ContentCreation.id
            ).join(
                PerformanceMetric, YouTubeVideo.id == PerformanceMetric.video_id
            ).filter(
                PerformanceMetric.check_date == db.query(
                    func.max(PerformanceMetric.check_date)
                ).filter(
                    PerformanceMetric.video_id == YouTubeVideo.id
                ).correlate(YouTubeVideo).as_scalar()
            ).order_by(PerformanceMetric.view_count.desc()).all()

            if not results:
                return "No performance data available for analysis."

            # Format data for AI analysis
            analysis_data = []
            for video, genre, theme, views, likes, comments, check_date in results:
                video_info = {
                    'title': video.title,
                    'genre': genre,
                    'theme': theme,
                    'tags': video.tags if video.tags else [],
                    'views': views,
                    'likes': likes,
                    'comments': comments,
                    'upload_date': video.upload_date.isoformat() if video.upload_date else 'Unknown',
                    'check_date': check_date.isoformat() if check_date else 'Unknown'
                }
                analysis_data.append(video_info)

            # Create formatted text for AI analysis
            formatted_text = "YOUTUBE VIDEO PERFORMANCE ANALYSIS DATA\n"
            formatted_text += "=" * 50 + "\n\n"

            for i, data in enumerate(analysis_data, 1):
                formatted_text += f"Video {i}:\n"
                formatted_text += f"  Title: '{data['title']}'\n"
                formatted_text += f"  Genre: '{data['genre']}'\n"
                formatted_text += f"  Theme: '{data['theme']}'\n"
                formatted_text += f"  Tags: {', '.join([f'\"{tag}\"' for tag in data['tags']])}\n"
                formatted_text += f"  Performance: {data['views']} views, {data['likes']} likes, {data['comments']} comments\n"
                formatted_text += f"  Upload Date: {data['upload_date']}\n"
                formatted_text += f"  Last Checked: {data['check_date']}\n\n"

            # Add summary statistics
            total_videos = len(analysis_data)
            total_views = sum(data['views'] for data in analysis_data)
            total_likes = sum(data['likes'] for data in analysis_data)
            total_comments = sum(data['comments'] for data in analysis_data)

            avg_views = total_views / total_videos if total_videos > 0 else 0
            avg_likes = total_likes / total_videos if total_videos > 0 else 0
            avg_comments = total_comments / total_videos if total_videos > 0 else 0

            formatted_text += "SUMMARY STATISTICS:\n"
            formatted_text += f"  Total Videos: {total_videos}\n"
            formatted_text += f"  Total Views: {total_views:,}\n"
            formatted_text += f"  Total Likes: {total_likes:,}\n"
            formatted_text += f"  Total Comments: {total_comments:,}\n"
            formatted_text += f"  Average Views: {avg_views:.1f}\n"
            formatted_text += f"  Average Likes: {avg_likes:.1f}\n"
            formatted_text += f"  Average Comments: {avg_comments:.1f}\n\n"

            return formatted_text

        except Exception as e:
            print(f"❌ Failed to get performance summary for analysis: {e}")
            return f"Error retrieving performance data: {e}"
        finally:
            self.close_db(db)
