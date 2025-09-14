#!/usr/bin/env python3
"""
YouTube Data Scheduler
Automatic YouTube channel statistics synchronization
"""

import os
import sys
import time
import schedule
import logging
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path

# Add the parent directory to sys.path to import our modules
sys.path.append(str(Path(__file__).parent.parent))

from core.youtube_api_client import youtube_client

class YouTubeDataScheduler:
    """Automatic YouTube data synchronization scheduler"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Database path
        self.db_path = os.path.join(os.path.dirname(__file__), "../data/youtube_channels.db")
        
    def sync_all_channels(self):
        """Sync all YouTube channels data"""
        try:
            self.logger.info("🔄 Starting scheduled YouTube data synchronization...")
            
            # Get all channels with YouTube IDs
            channels = self._get_channels_to_sync()
            
            if not channels:
                self.logger.info("No channels found to sync")
                return
                
            self.logger.info(f"Found {len(channels)} channels to sync")
            
            # Extract YouTube channel IDs
            db_ids = [ch[0] for ch in channels]
            youtube_ids = [ch[1] for ch in channels]
            
            # Get fresh data from YouTube API
            api_result = youtube_client.get_multiple_channels_statistics(youtube_ids)
            
            if not api_result['success']:
                self.logger.error(f"❌ YouTube API call failed: {api_result['error']}")
                return
                
            # Update database
            updated_count = self._update_database(db_ids, youtube_ids, api_result['results'])
            
            self.logger.info(f"✅ Scheduled sync completed: {updated_count}/{len(channels)} channels updated")
            self.logger.info(f"📊 API quota used: {api_result.get('quota_used', 0)}")
            
        except Exception as e:
            self.logger.error(f"❌ Scheduled sync failed: {e}")
    
    def _get_channels_to_sync(self):
        """Get channels that need syncing"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, youtube_channel_id 
                    FROM youtube_channels 
                    WHERE youtube_channel_id IS NOT NULL 
                    AND youtube_channel_id != ''
                ''')
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error getting channels: {e}")
            return []
    
    def _update_database(self, db_ids, youtube_ids, api_results):
        """Update database with fresh YouTube data"""
        updated_count = 0
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for i, youtube_id in enumerate(youtube_ids):
                    db_id = db_ids[i]
                    
                    if youtube_id in api_results:
                        stats = api_results[youtube_id]
                        
                        if stats.get('success'):
                            # Update with fresh data
                            cursor.execute('''
                                UPDATE youtube_channels 
                                SET total_subscribers = ?, 
                                    total_videos = ?,
                                    total_views = ?,
                                    updated_at = ?
                                WHERE id = ?
                            ''', (
                                stats['subscriber_count'],
                                stats['video_count'], 
                                stats['view_count'],
                                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                db_id
                            ))
                            updated_count += 1
                            
                            self.logger.info(f"✅ Updated channel {db_id}: {stats['subscriber_count']} subs, {stats['video_count']} videos")
                        else:
                            self.logger.warning(f"⚠️ Failed to get data for channel {db_id}: {stats.get('error', 'Unknown error')}")
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error updating database: {e}")
            
        return updated_count
    
    def start_scheduler(self):
        """Start the background scheduler"""
        self.logger.info("🚀 Starting YouTube Data Scheduler...")
        
        # Schedule daily sync at 2 AM
        schedule.every().day.at("02:00").do(self.sync_all_channels)
        
        # Schedule hourly light sync during business hours (9 AM - 6 PM)
        for hour in range(9, 18):
            schedule.every().day.at(f"{hour:02d}:00").do(self.sync_all_channels)
        
        self.logger.info("📅 Scheduled tasks:")
        self.logger.info("  - Daily full sync: 2:00 AM")
        self.logger.info("  - Hourly sync: 9:00 AM - 6:00 PM")
        
        # Run initial sync
        self.logger.info("🔄 Running initial synchronization...")
        self.sync_all_channels()
        
        # Keep scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def run_scheduler():
    """Entry point for running the scheduler"""
    scheduler = YouTubeDataScheduler()
    try:
        scheduler.start_scheduler()
    except KeyboardInterrupt:
        logging.info("🛑 YouTube Data Scheduler stopped by user")
    except Exception as e:
        logging.error(f"❌ Scheduler crashed: {e}")

if __name__ == "__main__":
    run_scheduler()