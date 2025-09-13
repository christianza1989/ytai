#!/usr/bin/env python3
"""
🤖 24/7 AUTOMATION CONTROLLER
Integrates YouTube Channels Manager with Autonomous Empire
Provides central control for starting/stopping 24/7 automation
"""

import os
import sys
import json
import time
import threading
import schedule
from datetime import datetime, timedelta
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autonomous_empire_24_7 import AutonomousEmpire24_7
from core.database.database_manager import DatabaseManager
from core.database.models import YouTubeChannel

class AutomationController:
    """Central controller for 24/7 YouTube automation"""
    
    def __init__(self):
        self.is_running = False
        self.db_manager = DatabaseManager()
        self.autonomous_empire = None
        self.automation_thread = None
        self.status = "stopped"
        
        # Statistics
        self.start_time = None
        self.total_generated = 0
        self.total_uploaded = 0
        self.active_channels = 0
        
        self.log_file = "automation_controller.log"
        
    def log(self, message):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, "a", encoding='utf-8') as f:
            f.write(log_message + "\n")
    
    def get_active_channels(self):
        """Get all channels ready for 24/7 automation"""
        try:
            channels = self.db_manager.get_active_channels_for_automation()
            self.log(f"📺 Found {len(channels)} channels ready for automation")
            return channels
        except Exception as e:
            self.log(f"❌ Error getting active channels: {e}")
            return []
    
    def start_24_7_automation(self):
        """Start 24/7 automation for all configured channels"""
        if self.is_running:
            self.log("⚠️ Automation already running!")
            return False
            
        try:
            # Get active channels
            active_channels = self.get_active_channels()
            
            if not active_channels:
                self.log("❌ No active channels found for automation!")
                return False
                
            self.active_channels = len(active_channels)
            self.log(f"🚀 Starting 24/7 automation with {self.active_channels} channels")
            
            # Initialize autonomous empire
            self.autonomous_empire = AutonomousEmpire24_7()
            
            # Sync channels with autonomous empire database
            self._sync_channels_to_autonomous_empire(active_channels)
            
            # Start automation thread
            self.is_running = True
            self.status = "running" 
            self.start_time = datetime.now()
            
            self.automation_thread = threading.Thread(target=self._automation_worker, daemon=True)
            self.automation_thread.start()
            
            self.log("✅ 24/7 Automation started successfully!")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to start automation: {e}")
            self.is_running = False
            self.status = "error"
            return False
    
    def stop_24_7_automation(self):
        """Stop 24/7 automation"""
        if not self.is_running:
            self.log("⚠️ Automation not running")
            return False
            
        try:
            self.log("🛑 Stopping 24/7 automation...")
            self.is_running = False
            self.status = "stopped"
            
            if self.autonomous_empire:
                self.autonomous_empire.stop_empire()
                
            # Wait for thread to finish
            if self.automation_thread and self.automation_thread.is_alive():
                self.automation_thread.join(timeout=10)
                
            self.log("✅ Automation stopped successfully")
            return True
            
        except Exception as e:
            self.log(f"❌ Error stopping automation: {e}")
            return False
    
    def _sync_channels_to_autonomous_empire(self, channels):
        """Sync YouTube channels to autonomous empire database"""
        try:
            self.log("🔄 Syncing channels to autonomous empire...")
            
            for channel in channels:
                # Convert YouTubeChannel to autonomous empire format
                account_data = {
                    "account_name": channel.name.replace(" ", "_"),
                    "channel_id": channel.youtube_channel_id,
                    "specialization": channel.primary_genre,
                    "upload_schedule": self._convert_schedule(channel.upload_schedule),
                    "api_credentials": {
                        "api_key": channel.api_key,
                        "client_id": channel.client_id,
                        "client_secret": channel.client_secret
                    } if channel.api_key else None,
                    "status": "active",
                    "auto_upload": channel.auto_upload,
                    "auto_thumbnails": channel.auto_thumbnails,
                    "auto_seo": channel.auto_seo
                }
                
                # Add to autonomous empire
                self.autonomous_empire._add_youtube_account(account_data)
                
            self.log(f"✅ Synced {len(channels)} channels to autonomous empire")
            
        except Exception as e:
            self.log(f"❌ Error syncing channels: {e}")
    
    def _convert_schedule(self, schedule):
        """Convert YouTube channel schedule to autonomous empire format"""
        schedule_mapping = {
            "daily": "daily",
            "every-2-days": "every_48_hours",
            "every-3-days": "every_72_hours", 
            "weekly": "weekly",
            "twice-weekly": "every_84_hours"
        }
        return schedule_mapping.get(schedule, "daily")
    
    def _automation_worker(self):
        """Main automation worker thread"""
        self.log("🔄 Automation worker started")
        
        try:
            while self.is_running:
                # Run one generation cycle
                self._run_generation_cycle()
                
                # Update statistics
                self._update_statistics()
                
                # Wait before next cycle (5 minutes)
                for _ in range(300):  # 5 minutes = 300 seconds
                    if not self.is_running:
                        break
                    time.sleep(1)
                    
        except Exception as e:
            self.log(f"❌ Automation worker error: {e}")
            self.is_running = False
            self.status = "error"
        
        self.log("🛑 Automation worker stopped")
    
    def _run_generation_cycle(self):
        """Run one complete generation cycle"""
        try:
            self.log("🎵 Running generation cycle...")
            
            if self.autonomous_empire:
                # Generate content for all channels
                result = self.autonomous_empire.generate_batch_content(batch_size=3)
                
                if result.get("success"):
                    generated_count = result.get("generated_count", 0)
                    self.total_generated += generated_count
                    self.log(f"✅ Generated {generated_count} tracks this cycle")
                else:
                    self.log(f"⚠️ Generation cycle completed with warnings")
            
        except Exception as e:
            self.log(f"❌ Error in generation cycle: {e}")
    
    def _update_statistics(self):
        """Update automation statistics"""
        try:
            # Update channel metrics in database
            channels = self.get_active_channels()
            
            for channel in channels:
                # Get latest metrics from autonomous empire
                if self.autonomous_empire:
                    metrics = self.autonomous_empire.get_channel_metrics(channel.name)
                    if metrics:
                        self.db_manager.update_channel_metrics(channel.id, metrics)
                        
        except Exception as e:
            self.log(f"❌ Error updating statistics: {e}")
    
    def get_automation_status(self):
        """Get current automation status"""
        uptime = None
        if self.start_time:
            uptime = str(datetime.now() - self.start_time).split('.')[0]
            
        return {
            "is_running": self.is_running,
            "status": self.status,
            "active_channels": self.active_channels,
            "total_generated": self.total_generated,
            "total_uploaded": self.total_uploaded,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "uptime": uptime
        }
    
    def get_channel_performance(self):
        """Get performance data for all channels"""
        try:
            channels = self.get_active_channels()
            performance_data = []
            
            for channel in channels:
                channel_data = channel.to_dict()
                
                # Add real-time metrics from autonomous empire
                if self.autonomous_empire:
                    metrics = self.autonomous_empire.get_channel_metrics(channel.name)
                    if metrics:
                        channel_data.update(metrics)
                        
                performance_data.append(channel_data)
                
            return performance_data
            
        except Exception as e:
            self.log(f"❌ Error getting channel performance: {e}")
            return []

# Global automation controller instance
automation_controller = AutomationController()