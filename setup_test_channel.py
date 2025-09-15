#!/usr/bin/env python3
"""
Setup test YouTube channel directly in database
"""

import sqlite3
import json
import uuid
from datetime import datetime, timedelta

def setup_test_channel():
    """Setup test YouTube channel in database"""
    
    db_path = "data/youtube_channels.db"
    
    # Channel data matching actual schema
    channel_data = {
        "channel_uuid": str(uuid.uuid4()),
        "channel_name": "AI Music Studio Test",
        "channel_url": "https://youtube.com/channel/test",
        "youtube_channel_id": "UCTestChannelId123",
        "description": "Test channel for AI-generated music content",
        "api_key": "test_youtube_api_key_12345",
        "client_id": "test_client_id.apps.googleusercontent.com", 
        "client_secret": "test_client_secret_abc123",
        "selected_genres": json.dumps(["electronic", "lo-fi", "ambient", "chill"]),
        "primary_genre": "chill-electronic",
        "target_audience": "study-relaxation", 
        "auto_upload": 1,
        "auto_thumbnails": 1,
        "auto_seo": 1,
        "enable_analytics": 1,
        "enable_monetization": 0,
        "daily_upload_count": 3,
        "upload_schedule": "daily",
        "upload_hours": json.dumps([
            {"hour": 14, "minute": 0, "vocal_probability": 0.8},
            {"hour": 18, "minute": 30, "vocal_probability": 0.6},
            {"hour": 20, "minute": 0, "vocal_probability": 0.7}
        ]),
        "vocal_probability": 0.7,
        "ai_decision_enabled": 1,
        "privacy_settings": "public",
        "default_video_title_template": "{title} - {genre} Music",
        "default_description_template": "🎵 {title}\n\nGenre: {genre}\nMood: {mood}\n\n#music #{genre_tag} #{mood_tag}",
        "total_subscribers": 1250,
        "monthly_revenue": 89.50,
        "total_videos": 45,
        "total_views": 38250,
        "last_upload_date": datetime.now().isoformat(),
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "automation_enabled": 1,
        "automation_start_date": datetime.now().isoformat(),
        "automation_last_run": datetime.now().isoformat(),
        "automation_next_run": (datetime.now() + timedelta(hours=6)).isoformat(),
        "advanced_settings": json.dumps({
            "batch_size": 5,
            "content_strategy": "consistent-quality",
            "branding_style": "minimal-modern"
        }),
        "error_log": ""
    }
    
    try:
        # Connect to database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check if channel already exists
            cursor.execute("SELECT COUNT(*) FROM youtube_channels WHERE channel_name = ?", 
                         (channel_data["channel_name"],))
            if cursor.fetchone()[0] > 0:
                print("📺 Test channel already exists, updating...")
                # Update existing channel
                cursor.execute("""
                    UPDATE youtube_channels SET
                        selected_genres = ?,
                        upload_schedule = ?,
                        upload_hours = ?,
                        total_subscribers = ?,
                        updated_at = ?
                    WHERE channel_name = ?
                """, (
                    channel_data["selected_genres"],
                    channel_data["upload_schedule"], 
                    channel_data["upload_hours"],
                    channel_data["total_subscribers"],
                    channel_data["updated_at"],
                    channel_data["channel_name"]
                ))
            else:
                # Insert new channel
                columns = ', '.join(channel_data.keys())
                placeholders = ', '.join(['?' for _ in channel_data])
                
                cursor.execute(f"""
                    INSERT INTO youtube_channels ({columns})
                    VALUES ({placeholders})
                """, list(channel_data.values()))
                
            conn.commit()
            
            # Verify insertion
            cursor.execute("SELECT id, channel_name, primary_genre, total_subscribers FROM youtube_channels WHERE channel_name = ?",
                         (channel_data["channel_name"],))
            result = cursor.fetchone()
            
            if result:
                print("✅ Test YouTube channel setup successful!")
                print(f"📺 ID: {result[0]}")
                print(f"📺 Name: {result[1]}")
                print(f"🎯 Primary Genre: {result[2]}")
                print(f"👥 Subscribers: {result[3]}")
                print(f"🎵 Genres: {', '.join(json.loads(channel_data['selected_genres']))}")
                return True
            else:
                print("❌ Failed to setup channel")
                return False
                
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False

if __name__ == "__main__":
    setup_test_channel()