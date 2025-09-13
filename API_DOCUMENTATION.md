# 📚 Autonominis Muzikantas - API Dokumentacija

[![API Status](https://img.shields.io/badge/API%20Status-Active-green.svg)](#)
[![Version](https://img.shields.io/badge/Version-3.0.0-blue.svg)](#)
[![Endpoints](https://img.shields.io/badge/Endpoints-45+-orange.svg)](#)

**Išsami API dokumentacija visiems Autonominis Muzikantas sistemos endpoints.**

---

## 📋 **Turinys**

1. [API Apžvalga](#api-apžvalga)
2. [Autentifikacija](#autentifikacija)
3. [Core Music Generation API](#core-music-generation-api)
4. [Voice Cloning Empire API](#voice-cloning-empire-api)
5. [Live Trending Hijacker API](#live-trending-hijacker-api)
6. [Automated Community Empire API](#automated-community-empire-api)
7. [Analytics & Reporting API](#analytics--reporting-api)
8. [System Management API](#system-management-api)
9. [Error Handling](#error-handling)
10. [Rate Limiting](#rate-limiting)
11. [WebSocket Events](#websocket-events)

---

## 🚀 **API Apžvalga**

### **Base URLs:**
```
Main Server:  http://localhost:3000/api/
Admin Server: http://localhost:8000/api/
```

### **Supported Formats:**
- **Request:** JSON, Form-Data
- **Response:** JSON, Binary (audio/video files)
- **Authentication:** Session-based, API Keys

### **API Statistics:**
```
📊 Total Endpoints: 45+
🎵 Music Generation: 8 endpoints
🎭 Voice Cloning: 12 endpoints
🚀 Trending Hijacker: 10 endpoints
🤖 Community Empire: 8 endpoints
📊 Analytics: 7 endpoints
⚙️ System Management: 6 endpoints
```

---

## 🔐 **Autentifikacija**

### **Session Authentication (Admin Interface):**
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

Response:
{
  "status": "success",
  "message": "Login successful",
  "session_id": "abc123...",
  "expires_in": 3600
}
```

### **API Key Authentication (Programming Access):**
```bash
# Header-based authentication
GET /api/music/generate
Authorization: Bearer YOUR_API_KEY
X-API-Key: YOUR_API_KEY

# Query parameter authentication  
GET /api/music/generate?api_key=YOUR_API_KEY
```

---

## 🎵 **Core Music Generation API**

### **Generate Music**
```bash
POST /api/music/generate
Content-Type: application/json

{
  "prompt": "Relaxing lo-fi hip hop beat for studying",
  "style": "lo-fi hip hop",
  "duration": 60,
  "mode": "custom",
  "lyrics": "Optional lyrics here",
  "instrumental": false,
  "tags": ["chill", "study", "lofi"]
}

Response:
{
  "status": "success",
  "generation_id": "gen_123456789",
  "estimated_time": 120,
  "credits_used": 10,
  "queue_position": 1,
  "webhook_url": "/api/music/status/gen_123456789"
}
```

### **Check Generation Status**
```bash
GET /api/music/status/{generation_id}

Response:
{
  "status": "completed",
  "generation_id": "gen_123456789",
  "progress": 100,
  "audio_url": "/api/music/download/gen_123456789.mp3",
  "video_url": "/api/music/download/gen_123456789.mp4",
  "duration": 62.5,
  "file_size": 2456789,
  "metadata": {
    "title": "Relaxing Study Session",
    "artist": "AI Composer",
    "genre": "Lo-Fi Hip Hop",
    "bpm": 85
  }
}
```

### **Download Generated Content**
```bash
GET /api/music/download/{file_id}
Accept: audio/mpeg, video/mp4

Response: Binary file download
```

### **List Generations**
```bash
GET /api/music/list?page=1&limit=20&status=completed

Response:
{
  "status": "success",
  "total": 150,
  "page": 1,
  "limit": 20,
  "generations": [
    {
      "id": "gen_123456789",
      "prompt": "Relaxing lo-fi hip hop",
      "status": "completed",
      "created_at": "2024-01-15T14:30:00Z",
      "duration": 62.5,
      "download_url": "/api/music/download/gen_123456789.mp3"
    }
  ]
}
```

### **Extend Audio**
```bash
POST /api/music/extend
Content-Type: application/json

{
  "audio_id": "gen_123456789",
  "additional_duration": 30,
  "continue_style": true
}

Response:
{
  "status": "processing",
  "extend_id": "ext_987654321",
  "estimated_time": 60
}
```

### **Batch Generation**
```bash
POST /api/music/batch
Content-Type: application/json

{
  "generations": [
    {
      "prompt": "Energetic workout music",
      "style": "electronic",
      "duration": 120
    },
    {
      "prompt": "Calm meditation sounds", 
      "style": "ambient",
      "duration": 300
    }
  ]
}

Response:
{
  "status": "processing",
  "batch_id": "batch_555666777",
  "total_generations": 2,
  "estimated_time": 300
}
```

### **Get Account Credits**
```bash
GET /api/music/credits

Response:
{
  "status": "success",
  "credits": 250,
  "credits_used_today": 45,
  "subscription_type": "pro",
  "renewal_date": "2024-02-15T00:00:00Z"
}
```

### **Music Analytics**
```bash
GET /api/music/analytics?period=30d

Response:
{
  "status": "success",
  "period": "30d",
  "total_generations": 125,
  "successful_generations": 118,
  "success_rate": 94.4,
  "total_duration_minutes": 7850,
  "credits_used": 1250,
  "top_styles": [
    {"style": "lo-fi hip hop", "count": 35},
    {"style": "electronic", "count": 28}
  ]
}
```

---

## 🎭 **Voice Cloning Empire API**

### **Initialize Voice Empire**
```bash
POST /api/voice/initialize

Response:
{
  "status": "success",
  "message": "Voice Empire initialized successfully",
  "characters_created": 8,
  "total_setup_time": 45.2,
  "characters": [
    {
      "id": "luna_lofi",
      "name": "Luna",
      "genre": "Lo-Fi",
      "personality": "Dreamy meditation guide",
      "voice_id": "elevenlabs_voice_123"
    }
  ]
}
```

### **List Voice Characters**
```bash
GET /api/voice/characters

Response:
{
  "status": "success",
  "total_characters": 8,
  "characters": [
    {
      "id": "luna_lofi",
      "name": "Luna",
      "genre": "Lo-Fi",
      "personality": "Dreamy meditation guide",
      "backstory": "Luna is a ethereal being who guides souls through peaceful soundscapes...",
      "voice_quality": "dreamy_female",
      "revenue_multiplier": 3.2,
      "monthly_potential": 5420,
      "total_content": 12,
      "last_active": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### **Generate Character Content**
```bash
POST /api/voice/characters/{character_id}/generate
Content-Type: application/json

{
  "content_type": "introduction",
  "duration": 60,
  "topic": "New album release",
  "mood": "excited",
  "include_music": true
}

Response:
{
  "status": "processing",
  "content_id": "content_789123456",
  "character": "luna_lofi",
  "estimated_time": 90,
  "script_preview": "Hey beautiful souls, it's Luna here with something magical to share..."
}
```

### **Get Character Script**
```bash
GET /api/voice/characters/{character_id}/script

Response:
{
  "status": "success",
  "character": "luna_lofi",
  "script": "Welcome to another dreamy journey with Luna. Today we're exploring the ethereal sounds of...",
  "duration_estimate": 45,
  "word_count": 150,
  "emotion_tags": ["dreamy", "calm", "inspiring"]
}
```

### **Synthesize Character Voice**
```bash
POST /api/voice/characters/{character_id}/synthesize
Content-Type: application/json

{
  "text": "Welcome to another dreamy journey with Luna...",
  "emotion": "calm",
  "speed": 0.9,
  "pitch": 0.1
}

Response:
{
  "status": "processing",
  "synthesis_id": "synth_456789123",
  "estimated_time": 30,
  "character": "luna_lofi"
}
```

### **Character Performance Analytics**
```bash
GET /api/voice/characters/{character_id}/analytics

Response:
{
  "status": "success",
  "character": "luna_lofi",
  "performance": {
    "total_content": 25,
    "total_views": 125000,
    "average_engagement": 8.7,
    "revenue_generated": 1250.50,
    "growth_rate": 15.6,
    "top_performing_content": [
      {
        "title": "Midnight Study Session",
        "views": 15000,
        "engagement": 9.2
      }
    ]
  }
}
```

### **Batch Character Operations**
```bash
POST /api/voice/characters/batch
Content-Type: application/json

{
  "operation": "generate_weekly_content",
  "characters": ["luna_lofi", "kai_lofi", "zara_trap"],
  "content_types": ["intro", "outro", "track_commentary"]
}

Response:
{
  "status": "processing",
  "batch_id": "voice_batch_789456123",
  "total_operations": 9,
  "estimated_time": 450
}
```

### **Voice Cloning (Custom Voice)**
```bash
POST /api/voice/clone
Content-Type: multipart/form-data

audio_samples: [file1.wav, file2.wav, file3.wav]
voice_name: "Custom Character"
voice_description: "Energetic gaming narrator"

Response:
{
  "status": "processing",
  "clone_id": "clone_123789456",
  "estimated_time": 300,
  "samples_uploaded": 3,
  "total_duration": 180
}
```

### **Voice Empire Dashboard Data**
```bash
GET /api/voice/dashboard

Response:
{
  "status": "success",
  "summary": {
    "total_characters": 8,
    "active_characters": 7,
    "total_content": 156,
    "monthly_revenue": 12450.75,
    "growth_rate": 23.5
  },
  "top_performers": [
    {
      "character": "zara_trap",
      "revenue": 3200.25,
      "growth": 35.2
    }
  ]
}
```

### **Update Character Settings**
```bash
PUT /api/voice/characters/{character_id}
Content-Type: application/json

{
  "personality_update": "More energetic and upbeat",
  "voice_settings": {
    "pitch": 0.2,
    "speed": 1.1,
    "emotion": "excited"
  },
  "content_schedule": "daily"
}

Response:
{
  "status": "success",
  "character": "luna_lofi",
  "updated_fields": ["personality", "voice_settings", "schedule"],
  "effective_immediately": true
}
```

### **Character Content History**
```bash
GET /api/voice/characters/{character_id}/content?page=1&limit=10

Response:
{
  "status": "success",
  "character": "luna_lofi",
  "total_content": 25,
  "content": [
    {
      "id": "content_789123",
      "type": "introduction",
      "title": "Dreamy Night Session",
      "duration": 45,
      "created_at": "2024-01-15T20:00:00Z",
      "views": 5000,
      "engagement": 8.9,
      "download_url": "/api/voice/content/download/content_789123"
    }
  ]
}
```

---

## 🚀 **Live Trending Hijacker API**

### **Start Live Monitoring**
```bash
POST /api/trending/start

Response:
{
  "status": "success",
  "message": "Live trending monitoring started",
  "monitoring_platforms": 6,
  "scan_interval": 30,
  "next_scan": "2024-01-15T14:35:00Z"
}
```

### **Get Current Trends**
```bash
GET /api/trending/current?platform=all&limit=20

Response:
{
  "status": "success",
  "scan_time": "2024-01-15T14:30:00Z",
  "total_trends": 847,
  "filtered_trends": 20,
  "trends": [
    {
      "id": "trend_456789123",
      "title": "Chill Beats for Studying",
      "platform": "youtube_music",
      "viral_score": 94.7,
      "growth_rate": 156.3,
      "opportunity_level": "HIGH",
      "suggested_response": "Lo-Fi study beats with rain sounds",
      "estimated_revenue": 1250,
      "time_sensitive": true,
      "expires_at": "2024-01-15T16:30:00Z"
    }
  ]
}
```

### **Hijack Trend (Generate Response)**
```bash
POST /api/trending/hijack/{trend_id}
Content-Type: application/json

{
  "response_strategy": "fast_follower",
  "customizations": {
    "style_variation": "add_trap_elements",
    "duration": 90,
    "target_audience": "study_community"
  },
  "schedule_upload": true
}

Response:
{
  "status": "processing",
  "hijack_id": "hijack_789456123",
  "trend_id": "trend_456789123",
  "estimated_completion": "2024-01-15T15:30:00Z",
  "generation_steps": [
    "analyzing_trend_patterns",
    "generating_music_response",
    "creating_video_content",
    "scheduling_upload"
  ]
}
```

### **Trending Analytics**
```bash
GET /api/trending/analytics?period=7d

Response:
{
  "status": "success",
  "period": "7d",
  "trends_detected": 324,
  "hijacks_attempted": 28,
  "successful_hijacks": 18,
  "success_rate": 64.3,
  "revenue_generated": 3450.75,
  "top_platforms": [
    {"platform": "tiktok", "opportunities": 125},
    {"platform": "youtube_music", "opportunities": 89}
  ]
}
```

### **Platform Monitoring Status**
```bash
GET /api/trending/platforms

Response:
{
  "status": "success",
  "platforms": [
    {
      "name": "youtube_music",
      "status": "active",
      "last_scan": "2024-01-15T14:28:00Z",
      "trends_found": 156,
      "api_quota_remaining": 8450,
      "error_rate": 0.2
    },
    {
      "name": "tiktok_sounds",
      "status": "active", 
      "last_scan": "2024-01-15T14:29:00Z",
      "trends_found": 203,
      "api_quota_remaining": 7230,
      "error_rate": 0.1
    }
  ]
}
```

### **Trend Pattern Analysis**
```bash
GET /api/trending/patterns?genre=lofi&timeframe=30d

Response:
{
  "status": "success",
  "genre": "lofi",
  "analysis_period": "30d",
  "patterns": {
    "peak_hours": ["14:00-16:00", "20:00-23:00"],
    "best_days": ["Sunday", "Monday", "Wednesday"],
    "trending_keywords": ["study", "chill", "rain", "focus"],
    "optimal_duration": "60-90 seconds",
    "success_factors": [
      "rain_sound_integration",
      "nostalgic_melody_patterns",
      "consistent_tempo_85_95_bpm"
    ]
  }
}
```

### **Schedule Trend Monitoring**
```bash
POST /api/trending/schedule
Content-Type: application/json

{
  "schedule_type": "custom",
  "intervals": {
    "peak_hours": 15,
    "normal_hours": 30,
    "overnight": 60
  },
  "priority_platforms": ["tiktok", "youtube_music"],
  "auto_hijack": {
    "enabled": true,
    "min_viral_score": 85,
    "max_daily_hijacks": 5
  }
}

Response:
{
  "status": "success",
  "schedule_id": "schedule_456123789",
  "next_scan": "2024-01-15T14:45:00Z",
  "estimated_daily_scans": 48
}
```

### **Hijack Performance Tracking**
```bash
GET /api/trending/hijacks/{hijack_id}/performance

Response:
{
  "status": "success",
  "hijack_id": "hijack_789456123",
  "original_trend": {
    "title": "Chill Beats for Studying",
    "viral_score": 94.7
  },
  "our_response": {
    "title": "Ultra Chill Study Beats with Rain",
    "upload_time": "2024-01-15T15:45:00Z",
    "current_views": 2500,
    "engagement_rate": 8.3,
    "revenue_generated": 125.75,
    "trending_position": "#23"
  },
  "success_metrics": {
    "hijack_speed": "90 minutes",
    "viral_capture": 32.5,
    "roi_percentage": 615
  }
}
```

### **Stop Monitoring**
```bash
POST /api/trending/stop

Response:
{
  "status": "success",
  "message": "Trending monitoring stopped",
  "final_stats": {
    "uptime": "6 hours 23 minutes",
    "trends_processed": 156,
    "hijacks_generated": 4
  }
}
```

---

## 🤖 **Automated Community Empire API**

### **Initialize Community Management**
```bash
POST /api/community/initialize

Response:
{
  "status": "success",
  "message": "Community Empire initialized",
  "platforms_connected": 6,
  "automation_level": 90,
  "estimated_daily_interactions": 450
}
```

### **Community Analytics Overview**
```bash
GET /api/community/analytics

Response:
{
  "status": "success",
  "overview": {
    "total_members": 15420,
    "daily_interactions": 1250,
    "automation_percentage": 92.3,
    "sentiment_score": 8.7,
    "growth_rate": 15.6,
    "engagement_improvement": 23.4
  },
  "platform_breakdown": [
    {
      "platform": "discord",
      "members": 5200,
      "daily_messages": 450,
      "ai_responses": 380,
      "sentiment": 9.1
    }
  ]
}
```

### **Generate AI Response**
```bash
POST /api/community/respond
Content-Type: application/json

{
  "platform": "discord",
  "message_content": "Hey, can you recommend some good lo-fi tracks for coding?",
  "user_context": {
    "username": "DevCoder99",
    "join_date": "2024-01-10",
    "activity_level": "high",
    "preferences": ["programming", "lofi", "productivity"]
  },
  "response_type": "helpful_recommendation"
}

Response:
{
  "status": "success",
  "response": {
    "content": "Hey @DevCoder99! 🎧 Perfect timing! For coding sessions, I'd recommend our 'Deep Focus' collection - especially the 90-minute uninterrupted tracks. Luna's 'Midnight Code' and Kai's 'Binary Dreams' are fan favorites among developers. They have minimal vocals and consistent beats that won't break your flow. Want me to create a custom coding playlist for you? 💻✨",
    "tone": "friendly_helpful",
    "personalization_score": 94.2,
    "estimated_engagement": 8.5
  }
}
```

### **Monitor Community Sentiment**
```bash
GET /api/community/sentiment?platform=all&period=24h

Response:
{
  "status": "success",
  "period": "24h",
  "overall_sentiment": {
    "score": 8.7,
    "trend": "improving",
    "change": "+1.2"
  },
  "platform_sentiment": [
    {
      "platform": "discord",
      "score": 9.1,
      "positive_mentions": 156,
      "negative_mentions": 8,
      "neutral_mentions": 245
    }
  ],
  "trending_topics": [
    {"topic": "new_release", "sentiment": 9.4, "mentions": 89},
    {"topic": "voice_characters", "sentiment": 8.8, "mentions": 67}
  ]
}
```

### **Manage Community Members**
```bash
GET /api/community/members?platform=discord&status=active&limit=50

Response:
{
  "status": "success",
  "total_members": 5200,
  "active_members": 3450,
  "members": [
    {
      "id": "member_789456123",
      "username": "LoFiLover92",
      "platform": "discord",
      "join_date": "2024-01-05T12:00:00Z",
      "activity_level": "high",
      "total_messages": 156,
      "favorite_genres": ["lofi", "chillhop"],
      "engagement_score": 9.2,
      "vip_status": true
    }
  ]
}
```

### **Automated Response Configuration**
```bash
PUT /api/community/config
Content-Type: application/json

{
  "automation_level": 95,
  "response_delay": {
    "min_seconds": 30,
    "max_seconds": 300
  },
  "personalization": {
    "enabled": true,
    "use_member_history": true,
    "mention_preferences": true
  },
  "content_promotion": {
    "frequency": "daily",
    "max_per_day": 3,
    "target_engagement": 8.0
  }
}

Response:
{
  "status": "success",
  "config_updated": true,
  "effective_immediately": true,
  "estimated_daily_responses": 420
}
```

### **Platform Connection Status**
```bash
GET /api/community/platforms

Response:
{
  "status": "success",
  "platforms": [
    {
      "name": "discord",
      "status": "connected",
      "bot_online": true,
      "members": 5200,
      "daily_messages": 450,
      "last_response": "2024-01-15T14:25:00Z"
    },
    {
      "name": "reddit",
      "status": "connected", 
      "subreddits_monitored": 12,
      "daily_comments": 85,
      "karma_score": 2450
    }
  ]
}
```

### **Content Engagement Tracking**
```bash
GET /api/community/engagement?content_id=gen_123456789

Response:
{
  "status": "success",
  "content_id": "gen_123456789",
  "title": "Midnight Study Session",
  "engagement": {
    "total_interactions": 1250,
    "likes": 890,
    "comments": 245,
    "shares": 115,
    "saves": 340,
    "engagement_rate": 8.7
  },
  "platform_breakdown": [
    {
      "platform": "discord",
      "reactions": 156,
      "comments": 45,
      "shares": 23
    }
  ]
}
```

### **AI Training Data Export**
```bash
GET /api/community/training-data?format=json&period=30d

Response:
{
  "status": "success",
  "period": "30d",
  "total_interactions": 12500,
  "successful_responses": 11250,
  "training_samples": [
    {
      "input": "Can you recommend relaxing music?",
      "response": "I'd love to help! For relaxation, try our 'Evening Calm' series...",
      "engagement": 9.1,
      "platform": "discord"
    }
  ]
}
```

---

## 📊 **Analytics & Reporting API**

### **System Performance Dashboard**
```bash
GET /api/analytics/dashboard

Response:
{
  "status": "success",
  "timestamp": "2024-01-15T14:30:00Z",
  "system_health": {
    "overall_status": "excellent",
    "uptime": "99.8%",
    "response_time_avg": 245,
    "error_rate": 0.2
  },
  "revenue_metrics": {
    "daily_revenue": 1250.75,
    "monthly_projection": 22750,
    "growth_rate": 23.5,
    "diamond_systems_contribution": 68.5
  },
  "content_metrics": {
    "total_generated": 1456,
    "successful_generations": 1398,
    "total_duration_hours": 84.2,
    "average_quality_score": 8.9
  }
}
```

### **Revenue Analytics**
```bash
GET /api/analytics/revenue?period=30d&breakdown=daily

Response:
{
  "status": "success",
  "period": "30d",
  "total_revenue": 18450.25,
  "breakdown": {
    "music_generation": 8750.00,
    "voice_empire": 4500.75,
    "trending_hijacker": 3200.50,
    "community_empire": 1999.00
  },
  "daily_data": [
    {
      "date": "2024-01-15",
      "revenue": 925.50,
      "generations": 45,
      "voice_content": 12,
      "hijacks": 3
    }
  ],
  "projections": {
    "next_30d": 25600.00,
    "confidence": 87.3
  }
}
```

### **Content Performance Analytics**
```bash
GET /api/analytics/content?sort=performance&limit=20

Response:
{
  "status": "success",
  "top_performing": [
    {
      "content_id": "gen_123456789",
      "title": "Midnight Study Vibes",
      "type": "music_generation",
      "views": 25600,
      "engagement": 9.2,
      "revenue": 450.75,
      "created_at": "2024-01-10T20:00:00Z"
    }
  ],
  "performance_insights": {
    "best_genres": ["lofi", "chillhop", "ambient"],
    "optimal_duration": "60-90 seconds",
    "peak_upload_times": ["14:00", "20:00"],
    "engagement_factors": ["voice_character", "trend_timing", "community_promotion"]
  }
}
```

### **API Usage Statistics**
```bash
GET /api/analytics/api-usage?period=7d

Response:
{
  "status": "success",
  "period": "7d",
  "total_requests": 15420,
  "successful_requests": 14856,
  "error_rate": 3.7,
  "endpoint_usage": [
    {
      "endpoint": "/api/music/generate",
      "requests": 2450,
      "avg_response_time": 1250,
      "error_rate": 2.1
    }
  ],
  "quota_usage": {
    "suno_credits": 450,
    "elevenlabs_characters": 125000,
    "youtube_quota": 8500
  }
}
```

### **User Engagement Analytics**
```bash
GET /api/analytics/engagement?platform=all&period=30d

Response:
{
  "status": "success",
  "engagement_overview": {
    "total_users": 12500,
    "active_users": 8750,
    "engagement_rate": 8.7,
    "retention_rate": 76.3
  },
  "platform_engagement": [
    {
      "platform": "youtube",
      "subscribers": 5600,
      "avg_watch_time": 145,
      "likes_per_video": 234,
      "comments_per_video": 45
    }
  ]
}
```

### **Export Analytics Report**
```bash
POST /api/analytics/export
Content-Type: application/json

{
  "report_type": "comprehensive",
  "period": "30d",
  "format": "pdf",
  "include_sections": [
    "revenue_analysis",
    "content_performance", 
    "system_health",
    "growth_projections"
  ]
}

Response:
{
  "status": "processing",
  "report_id": "report_789456123",
  "estimated_time": 120,
  "download_url": "/api/analytics/reports/report_789456123.pdf"
}
```

---

## ⚙️ **System Management API**

### **System Status Check**
```bash
GET /api/system/status

Response:
{
  "status": "operational",
  "timestamp": "2024-01-15T14:30:00Z",
  "uptime": "5 days, 14 hours, 23 minutes",
  "system_health": {
    "cpu_usage": 45.2,
    "memory_usage": 62.8,
    "disk_usage": 34.1,
    "network_latency": 28
  },
  "services": [
    {
      "name": "music_generator",
      "status": "running",
      "last_activity": "2024-01-15T14:28:00Z"
    },
    {
      "name": "voice_empire",
      "status": "running", 
      "last_activity": "2024-01-15T14:29:00Z"
    }
  ],
  "api_connections": {
    "suno_ai": "connected",
    "elevenlabs": "connected",
    "youtube_api": "connected",
    "gemini_ai": "connected"
  }
}
```

### **Configuration Management**
```bash
GET /api/system/config

Response:
{
  "status": "success",
  "configuration": {
    "generation_settings": {
      "max_concurrent": 5,
      "default_timeout": 300,
      "quality_threshold": 7.5
    },
    "api_limits": {
      "suno_daily_limit": 500,
      "elevenlabs_monthly_chars": 100000,
      "youtube_daily_quota": 10000
    },
    "automation": {
      "trending_monitoring": true,
      "community_responses": true,
      "auto_upload": false
    }
  }
}

PUT /api/system/config
Content-Type: application/json

{
  "generation_settings": {
    "max_concurrent": 8,
    "default_timeout": 600
  }
}

Response:
{
  "status": "success",
  "updated_settings": ["max_concurrent", "default_timeout"],
  "restart_required": false
}
```

### **Service Control**
```bash
POST /api/system/services/{service_name}/restart

Response:
{
  "status": "success",
  "service": "voice_empire",
  "action": "restart",
  "previous_uptime": "2 days, 5 hours",
  "restart_time": "2024-01-15T14:30:15Z"
}

POST /api/system/services/{service_name}/stop

Response:
{
  "status": "success",
  "service": "trending_hijacker",
  "action": "stop",
  "final_uptime": "1 day, 8 hours",
  "stop_time": "2024-01-15T14:30:30Z"
}
```

### **Backup Management**
```bash
POST /api/system/backup

Response:
{
  "status": "processing",
  "backup_id": "backup_456789123",
  "estimated_time": 180,
  "backup_size_estimate": "2.4 GB",
  "includes": ["databases", "generated_content", "configurations"]
}

GET /api/system/backups

Response:
{
  "status": "success",
  "backups": [
    {
      "id": "backup_456789123",
      "created_at": "2024-01-15T12:00:00Z",
      "size": "2.1 GB",
      "status": "completed",
      "download_url": "/api/system/backups/download/backup_456789123"
    }
  ]
}
```

### **Log Management**
```bash
GET /api/system/logs?service=all&level=error&limit=100

Response:
{
  "status": "success",
  "logs": [
    {
      "timestamp": "2024-01-15T14:25:00Z",
      "service": "music_generator",
      "level": "error",
      "message": "API rate limit exceeded",
      "details": {
        "endpoint": "/api/music/generate",
        "user_ip": "192.168.1.100"
      }
    }
  ]
}
```

### **Database Maintenance**
```bash
POST /api/system/maintenance

Response:
{
  "status": "processing",
  "maintenance_id": "maint_789456123",
  "operations": [
    "database_cleanup",
    "index_optimization",
    "cache_clearing",
    "log_rotation"
  ],
  "estimated_time": 300
}
```

---

## 🚨 **Error Handling**

### **Standard Error Response Format:**
```bash
{
  "status": "error",
  "error": {
    "code": "INVALID_API_KEY",
    "message": "The provided API key is invalid or expired",
    "details": {
      "received_key": "sk-1234...",
      "key_type": "suno_ai",
      "suggestion": "Please verify your API key in the .env file"
    },
    "timestamp": "2024-01-15T14:30:00Z",
    "request_id": "req_789456123"
  }
}
```

### **Common Error Codes:**
```bash
# Authentication Errors
401 - UNAUTHORIZED: "Invalid or missing authentication"
403 - FORBIDDEN: "Insufficient permissions"
429 - RATE_LIMITED: "Too many requests"

# API Errors  
400 - INVALID_REQUEST: "Missing or invalid parameters"
404 - NOT_FOUND: "Resource not found"
422 - VALIDATION_ERROR: "Request validation failed"

# Service Errors
500 - INTERNAL_ERROR: "Internal server error"
502 - SERVICE_UNAVAILABLE: "External service unavailable"
503 - MAINTENANCE_MODE: "System under maintenance"

# Custom Errors
1001 - INSUFFICIENT_CREDITS: "Not enough API credits"
1002 - GENERATION_FAILED: "Music generation failed"
1003 - VOICE_SYNTHESIS_ERROR: "Voice synthesis failed"
1004 - TREND_DETECTION_ERROR: "Trending analysis failed"
```

---

## 🔒 **Rate Limiting**

### **Rate Limit Headers:**
```bash
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1642234800
X-RateLimit-Window: 3600

Response when limit exceeded:
HTTP 429 Too Many Requests
{
  "status": "error",
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded",
    "retry_after": 1800,
    "limits": {
      "current": "100 requests per hour",
      "next_tier": "500 requests per hour with Pro plan"
    }
  }
}
```

### **Rate Limits by Endpoint:**
```bash
# Music Generation
/api/music/generate: 10 requests/hour (Free), 100 requests/hour (Pro)
/api/music/batch: 2 requests/hour (Free), 20 requests/hour (Pro)

# Voice Cloning
/api/voice/synthesize: 50 requests/hour (Free), 500 requests/hour (Pro)
/api/voice/clone: 1 request/day (Free), 10 requests/day (Pro)

# Trending & Community
/api/trending/*: 100 requests/hour
/api/community/*: 200 requests/hour

# Analytics & System
/api/analytics/*: 500 requests/hour
/api/system/*: 50 requests/hour
```

---

## 🔌 **WebSocket Events**

### **Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

// Authentication
ws.send(JSON.stringify({
  type: 'auth',
  token: 'your_session_token'
}));
```

### **Real-time Events:**

#### **Music Generation Progress:**
```javascript
{
  "event": "generation_progress",
  "data": {
    "generation_id": "gen_123456789",
    "progress": 45,
    "stage": "audio_synthesis",
    "estimated_remaining": 75
  }
}
```

#### **New Trend Detected:**
```javascript
{
  "event": "trend_detected",
  "data": {
    "trend_id": "trend_456789123",
    "title": "Viral Study Beats",
    "viral_score": 92.5,
    "platform": "tiktok",
    "opportunity_level": "HIGH",
    "expires_in": 7200
  }
}
```

#### **Community Interaction:**
```javascript
{
  "event": "community_mention", 
  "data": {
    "platform": "discord",
    "user": "MusicLover99",
    "message": "@AutonominisMuzikantas can you make some chill beats?",
    "sentiment": "positive",
    "requires_response": true
  }
}
```

#### **System Alert:**
```javascript
{
  "event": "system_alert",
  "data": {
    "severity": "warning",
    "service": "suno_ai",
    "message": "API quota at 85% usage",
    "action_required": false,
    "estimated_reset": "2024-01-16T00:00:00Z"
  }
}
```

---

## 🧪 **API Testing**

### **Test Environment:**
```bash
# Use test endpoints for development
BASE_URL_TEST=http://localhost:3001/api/
API_KEY_TEST=test_key_123456789

# Test data generation
curl -X POST http://localhost:3001/api/test/generate-sample-data
```

### **Health Check Endpoint:**
```bash
GET /api/health

Response:
{
  "status": "healthy",
  "version": "3.0.0",
  "timestamp": "2024-01-15T14:30:00Z",
  "checks": {
    "database": "ok",
    "apis": "ok", 
    "disk_space": "ok",
    "memory": "ok"
  }
}
```

---

## 📞 **API Support**

### **Getting Help:**
- **Documentation Issues:** GitHub Issues with label 'documentation'
- **API Bugs:** GitHub Issues with label 'api-bug'
- **Feature Requests:** GitHub Issues with label 'api-enhancement'
- **Rate Limit Increases:** Contact support with usage justification

### **Response Times:**
- **Critical Issues:** 2-4 hours
- **Bug Reports:** 24-48 hours  
- **Feature Requests:** 1-2 weeks
- **Documentation Updates:** 48-72 hours

---

**🚀 Happy Coding with Autonominis Muzikantas API!**

*API Version: 3.0.0 | Last Updated: 2024-01-15 | Next Update: 2024-02-01*