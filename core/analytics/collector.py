import os
from typing import List, Dict, Any
from datetime import datetime, timedelta
import time

from core.database.database_manager import DatabaseManager
from core.services.youtube_client import YouTubeClient

class AnalyticsCollector:
    """Collects YouTube video performance metrics and stores them in database"""

    def __init__(self, db_manager: DatabaseManager, youtube_client: YouTubeClient):
        self.db_manager = db_manager
        self.youtube_client = youtube_client
        self.batch_size = 50  # YouTube API limit for statistics requests

    def run_collection_cycle(self) -> str:
        """
        Main collection cycle - gathers statistics for all uploaded videos

        Returns:
            Summary string of collection results
        """
        print("📊 Starting YouTube analytics collection cycle...")
        print("=" * 60)

        try:
            # Get all uploaded videos from database
            uploaded_videos = self.db_manager.get_all_videos()
            if not uploaded_videos:
                return "ℹ️  No uploaded videos found in database"

            print(f"🎬 Found {len(uploaded_videos)} uploaded videos to analyze")

            # Extract video IDs
            video_ids = [video.video_id for video in uploaded_videos]
            print(f"📋 Processing video IDs: {video_ids}")

            # Split into batches (YouTube API limit: 50 videos per request)
            batches = self._split_into_batches(video_ids, self.batch_size)
            print(f"📦 Split into {len(batches)} batches (max {self.batch_size} per batch)")

            total_processed = 0
            total_new_metrics = 0

            # Process each batch
            for i, batch in enumerate(batches, 1):
                print(f"\n🔄 Processing batch {i}/{len(batches)} ({len(batch)} videos)")

                # Get statistics for this batch
                batch_stats = self.youtube_client.get_videos_statistics(batch)

                if batch_stats:
                    # Process each video's statistics
                    for video_id, stats in batch_stats.items():
                        try:
                            # Find corresponding database video object
                            db_video = self.db_manager.get_video_by_youtube_id(video_id)
                            if db_video:
                                # Check if we already have today's metrics
                                today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                                existing_metrics = self.db_manager.get_latest_metrics_for_video(db_video.id)

                                # Only add new metrics if we don't have today's data
                                if not existing_metrics or existing_metrics.check_date < today_start:
                                    self.db_manager.add_performance_metric(db_video.id, stats)
                                    total_new_metrics += 1
                                    print(f"✅ Added metrics for video {video_id}")
                                else:
                                    print(f"⏭️  Skipped {video_id} - already have today's metrics")
                            else:
                                print(f"⚠️  Video {video_id} not found in database")

                        except Exception as e:
                            print(f"❌ Failed to process video {video_id}: {e}")
                            continue

                    total_processed += len(batch_stats)
                else:
                    print(f"❌ Failed to get statistics for batch {i}")

                # Small delay between batches to be respectful to API
                if i < len(batches):
                    time.sleep(1)

            # Generate summary
            summary = self._generate_collection_summary(
                total_videos=len(uploaded_videos),
                total_processed=total_processed,
                total_new_metrics=total_new_metrics
            )

            print("\n" + "=" * 60)
            print("✅ Analytics collection cycle completed!")
            print(summary)
            print("=" * 60)

            return summary

        except Exception as e:
            error_msg = f"❌ Analytics collection failed: {e}"
            print(error_msg)
            return error_msg

    def _split_into_batches(self, items: List[str], batch_size: int) -> List[List[str]]:
        """Split a list into smaller batches"""
        return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

    def _generate_collection_summary(self, total_videos: int, total_processed: int,
                                   total_new_metrics: int) -> str:
        """Generate a summary of the collection results"""
        success_rate = (total_processed / total_videos * 100) if total_videos > 0 else 0

        summary_lines = [
            "📊 ANALYTICS COLLECTION SUMMARY",
            "=" * 40,
            f"Total videos in database: {total_videos}",
            f"Successfully processed: {total_processed}",
            f"New metrics added: {total_new_metrics}",
            ".1f",
            f"Collection timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        ]

        return "\n".join(summary_lines)

    def collect_single_video_metrics(self, video_id: str) -> bool:
        """
        Collect metrics for a single video

        Args:
            video_id: YouTube video ID

        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"📊 Collecting metrics for single video: {video_id}")

            # Get video statistics
            stats_result = self.youtube_client.get_videos_statistics([video_id])

            if not stats_result or video_id not in stats_result:
                print(f"❌ Failed to get statistics for video {video_id}")
                return False

            # Find video in database
            db_video = self.db_manager.get_video_by_youtube_id(video_id)
            if not db_video:
                print(f"❌ Video {video_id} not found in database")
                return False

            # Add metrics to database
            stats = stats_result[video_id]
            self.db_manager.add_performance_metric(db_video.id, stats)

            print(f"✅ Successfully collected metrics for video {video_id}")
            return True

        except Exception as e:
            print(f"❌ Failed to collect metrics for video {video_id}: {e}")
            return False

    def get_collection_status(self) -> Dict[str, Any]:
        """
        Get status of analytics collection

        Returns:
            Dictionary with collection status information
        """
        try:
            # Get database summary
            summary = self.db_manager.get_content_performance_summary()

            # Get recent metrics (last 24 hours)
            yesterday = datetime.utcnow() - timedelta(hours=24)

            # Count videos with recent metrics
            recent_metrics_count = 0
            all_videos = self.db_manager.get_all_videos()

            for video in all_videos:
                latest_metrics = self.db_manager.get_latest_metrics_for_video(video.id)
                if latest_metrics and latest_metrics.check_date >= yesterday:
                    recent_metrics_count += 1

            status = {
                'total_videos': summary.get('total_videos', 0),
                'total_views': summary.get('total_views', 0),
                'videos_with_recent_metrics': recent_metrics_count,
                'recent_metrics_percentage': (recent_metrics_count / len(all_videos) * 100) if all_videos else 0,
                'last_collection_time': datetime.utcnow().isoformat(),
                'database_status': 'healthy' if summary else 'error'
            }

            return status

        except Exception as e:
            print(f"❌ Failed to get collection status: {e}")
            return {
                'error': str(e),
                'database_status': 'error'
            }

    def cleanup_old_metrics(self, days_to_keep: int = 90) -> int:
        """
        Clean up old performance metrics

        Args:
            days_to_keep: Number of days of metrics to keep

        Returns:
            Number of records deleted
        """
        try:
            print(f"🧹 Cleaning up metrics older than {days_to_keep} days...")
            deleted_count = self.db_manager.cleanup_old_data(days_to_keep)
            print(f"✅ Cleaned up {deleted_count} old metric records")
            return deleted_count
        except Exception as e:
            print(f"❌ Failed to cleanup old metrics: {e}")
            return 0

    def export_analytics_report(self, filename: str = None) -> str:
        """
        Export comprehensive analytics report

        Args:
            filename: Optional filename for the report

        Returns:
            Path to the generated report file
        """
        if not filename:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"analytics_report_{timestamp}.txt"

        try:
            print("📊 Generating analytics report...")

            # Get various analytics data
            summary = self.db_manager.get_content_performance_summary()
            top_videos = self.db_manager.get_top_performing_videos(limit=10)
            genre_analysis = self.db_manager.get_genre_performance_analysis()
            collection_status = self.get_collection_status()

            # Generate report content
            report_lines = [
                "=" * 60,
                "🎯 YOUTUBE ANALYTICS REPORT",
                "=" * 60,
                f"Report generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
                "",
                "📈 OVERALL PERFORMANCE SUMMARY",
                "-" * 30,
                f"Total videos: {summary.get('total_videos', 0)}",
                f"Total views: {summary.get('total_views', 0):,}",
                f"Recent creations (7 days): {summary.get('recent_creations', 0)}",
                f"Recent uploads (7 days): {summary.get('recent_videos', 0)}",
                "",
                "🎬 TOP PERFORMING VIDEOS",
                "-" * 30
            ]

            if top_videos:
                for i, video in enumerate(top_videos, 1):
                    report_lines.extend([
                        f"{i}. {video['title']}",
                        f"   Views: {video['views']:,} | Likes: {video['likes']:,} | Comments: {video['comments']:,}",
                        f"   URL: {video['youtube_url']}",
                        ""
                    ])
            else:
                report_lines.append("No performance data available yet")
                report_lines.append("")

            # Add genre analysis
            if genre_analysis:
                report_lines.extend([
                    "🎵 GENRE PERFORMANCE ANALYSIS",
                    "-" * 30
                ])
                for genre, stats in genre_analysis.items():
                    report_lines.extend([
                        f"{genre}:",
                        f"   Creations: {stats['creation_count']}",
                        f"   Avg Views: {stats['avg_views']:.0f}",
                        f"   Avg Likes: {stats['avg_likes']:.0f}",
                        ""
                    ])

            # Add collection status
            report_lines.extend([
                "📊 COLLECTION STATUS",
                "-" * 30,
                f"Videos with recent metrics: {collection_status.get('videos_with_recent_metrics', 0)}",
                ".1f",
                f"Database status: {collection_status.get('database_status', 'unknown')}",
                "",
                "=" * 60
            ])

            # Write report to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))

            print(f"✅ Analytics report saved to: {filename}")
            return filename

        except Exception as e:
            error_msg = f"❌ Failed to generate analytics report: {e}"
            print(error_msg)
            return error_msg
