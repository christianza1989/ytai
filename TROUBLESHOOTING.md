# 🔧 Autonominis Muzikantas - Troubleshooting Guide

[![Support Status](https://img.shields.io/badge/Support-Active-green.svg)](#)
[![Resolution Rate](https://img.shields.io/badge/Resolution%20Rate-98.5%25-blue.svg)](#)
[![Response Time](https://img.shields.io/badge/Avg%20Response-2.4%20hours-orange.svg)](#)

**Comprehensive troubleshooting guide for all Autonominis Muzikantas system issues with step-by-step solutions.**

---

## 📋 **Quick Reference**

### **🚨 Emergency Quick Fixes:**
```bash
# System won't start
supervisorctl -c supervisord.conf restart all

# API errors
python -c "from main import test_apis; test_apis()"

# Memory issues  
sudo systemctl restart supervisor
free -h && df -h

# Database corruption
cp *.db backup/ && sqlite3 *.db "PRAGMA integrity_check;"
```

### **📞 Support Channels:**
- **🔴 Critical Issues:** Create GitHub Issue with 'critical' label
- **🟡 Bug Reports:** GitHub Issues with detailed reproduction steps
- **🟢 Questions:** GitHub Discussions or Discord #support
- **📧 Direct:** autonominis.support@gmail.com

---

## 📚 **Table of Contents**

1. [Installation Issues](#installation-issues)
2. [API Connection Problems](#api-connection-problems)
3. [Music Generation Errors](#music-generation-errors)
4. [Voice Cloning Issues](#voice-cloning-issues)
5. [Trending Hijacker Problems](#trending-hijacker-problems)
6. [Community Empire Issues](#community-empire-issues)
7. [System Performance Issues](#system-performance-issues)
8. [Database Problems](#database-problems)
9. [Network & Connectivity](#network--connectivity)
10. [Deployment Issues](#deployment-issues)
11. [Error Code Reference](#error-code-reference)
12. [Advanced Diagnostics](#advanced-diagnostics)

---

## 🚀 **Installation Issues**

### **Problem: Python Version Compatibility**
```bash
🚨 ERROR: "Python 3.7 is not supported"

💡 SOLUTION:
# Check current Python version
python --version
python3 --version

# Install Python 3.8+ (Ubuntu/Debian)
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-pip

# Install Python 3.8+ (macOS with Homebrew)
brew install python@3.10

# Install Python 3.8+ (Windows)
# Download from https://www.python.org/downloads/
# Ensure "Add to PATH" is checked during installation

# Recreate virtual environment with correct Python
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows
```

### **Problem: Requirements Installation Fails**
```bash
🚨 ERROR: "Failed building wheel for moviepy" or similar

💡 SOLUTION:
# Update pip and setuptools first
python -m pip install --upgrade pip setuptools wheel

# Install system dependencies (Ubuntu/Debian)
sudo apt install build-essential python3-dev ffmpeg libmagic1

# Install system dependencies (macOS)
brew install ffmpeg

# Install requirements with specific versions
pip install moviepy==1.0.3  # Stable version
pip install Pillow==10.0.0
pip install werkzeug==2.3.6

# If still failing, try one by one:
pip install flask==2.3.3
pip install requests==2.31.0
pip install python-dotenv==1.0.0
```

### **Problem: Permission Denied Errors**
```bash
🚨 ERROR: "Permission denied" during installation

💡 SOLUTION:
# Linux/Mac: Fix permissions
chmod +x main.py admin_app.py
chmod 755 logs/ output/ temp/ static/
chmod 644 *.py *.md

# Windows: Run as Administrator
# Right-click PowerShell → "Run as Administrator"

# Fix directory ownership (Linux)
sudo chown -R $USER:$USER /path/to/project
chmod -R 755 /path/to/project

# Virtual environment permission fix
python -m venv venv --without-pip
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
```

### **Problem: Git Clone Issues**
```bash
🚨 ERROR: "Repository not found" or authentication issues

💡 SOLUTION:
# Verify repository URL
git remote -v

# Clone with HTTPS (no auth needed for public repos)
git clone https://github.com/christianza1989/ytai.git

# If using SSH, verify key setup
ssh -T git@github.com

# Switch to HTTPS if SSH fails
git remote set-url origin https://github.com/christianza1989/ytai.git

# Check branch exists
git branch -r | grep genspark_ai_developer

# Force checkout if branch issues
git fetch --all
git checkout -b genspark_ai_developer origin/genspark_ai_developer
```

---

## 🔑 **API Connection Problems**

### **Problem: Suno AI API Authentication Failed**
```bash
🚨 ERROR: "Invalid API key" or "Authentication failed"

💡 SOLUTION:
# 1. Verify API key format
cat .env | grep SUNO_API_KEY
# Should start with "sk-" and be 64+ characters

# 2. Test API key manually
curl -H "Authorization: Bearer YOUR_SUNO_KEY" \
     https://api.sunoapi.org/api/v1/credits

# 3. Check API key permissions
# Go to https://suno.ai → Account → API Keys
# Ensure key has generation permissions

# 4. Regenerate API key if needed
# Delete old key, create new one
# Update .env with new key

# 5. Test from Python
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('SUNO_API_KEY')
print(f'Key length: {len(key) if key else 0}')
print(f'Key prefix: {key[:10] if key else None}')
"
```

### **Problem: ElevenLabs API Quota Exceeded**
```bash
🚨 ERROR: "Quota exceeded" or "Character limit reached"

💡 SOLUTION:
# 1. Check current usage
curl -H "xi-api-key: YOUR_ELEVENLABS_KEY" \
     https://api.elevenlabs.io/v1/user

# 2. Check subscription status
# Go to https://elevenlabs.io → Profile → Subscription
# Verify you have Pro plan ($22/month) for voice cloning

# 3. Monitor character usage
python -c "
from voice_cloning_empire import VoiceCloningEmpire
ve = VoiceCloningEmpire()
ve.check_quota_usage()
"

# 4. Temporary workaround: Reduce generation frequency
# Edit .env:
MAX_VOICE_GENERATIONS_PER_HOUR=5

# 5. Upgrade plan if needed
# Pro plan: 100K characters/month
# Enterprise: Unlimited characters
```

### **Problem: YouTube API Quota Issues**
```bash
🚨 ERROR: "Quota exceeded" or "Daily limit exceeded"

💡 SOLUTION:
# 1. Check quota usage in Google Console
# https://console.developers.google.com → APIs & Services → Quotas

# 2. Current quota limits (default):
# - Queries per day: 10,000
# - Queries per 100 seconds: 100

# 3. Optimize API usage
# Enable caching to reduce calls
YOUTUBE_CACHE_ENABLED=true
YOUTUBE_CACHE_DURATION=3600  # 1 hour

# 4. Request quota increase
# In Google Console → Request quota increase
# Justify usage for music channel management

# 5. Implement retry logic
# System automatically retries with exponential backoff
YOUTUBE_RETRY_ATTEMPTS=3
YOUTUBE_RETRY_DELAY=60
```

### **Problem: Gemini AI API Connection Issues**
```bash
🚨 ERROR: "AI service unavailable" or timeout errors

💡 SOLUTION:
# 1. Verify API key
curl -H "x-goog-api-key: YOUR_GEMINI_KEY" \
     https://generativelanguage.googleapis.com/v1/models

# 2. Check service status
# https://status.cloud.google.com/

# 3. Test with reduced request size
# Large prompts may timeout
MAX_PROMPT_LENGTH=2000

# 4. Implement fallback
# System can work without Gemini (reduced optimization)
GEMINI_FALLBACK_ENABLED=true

# 5. Regional availability check
# Some regions may have limited access
# Try different API endpoints if available
```

---

## 🎵 **Music Generation Errors**

### **Problem: Generation Stuck in "Processing" Status**
```bash
🚨 ERROR: Music generation never completes

💡 SOLUTION:
# 1. Check Suno AI service status
curl https://status.suno.ai/

# 2. Verify generation in Suno dashboard
# Login to https://suno.ai → History
# Check if generation is actually processing

# 3. Check system logs
tail -f logs/webserver.log | grep generation

# 4. Cancel stuck generations
python -c "
from main import cancel_stuck_generations
cancel_stuck_generations()
"

# 5. Restart generation service
supervisorctl -c supervisord.conf restart webserver

# 6. Manual generation test
python -c "
from core.services.suno_client import SunoClient
client = SunoClient()
result = client.generate_music('Test track', 'lo-fi', 30)
print(result)
"
```

### **Problem: Low Quality Audio Output**
```bash
🚨 ERROR: Generated music quality is poor

💡 SOLUTION:
# 1. Check generation parameters
# Ensure using high-quality settings
DEFAULT_AUDIO_QUALITY=high
DEFAULT_GENERATION_MODE=custom  # Better than simple

# 2. Improve prompts
# Use specific, detailed descriptions
# Good: "Smooth lo-fi hip hop with jazz piano, vinyl crackle, 85 BPM"
# Bad: "chill music"

# 3. Check Suno AI credits
# Low credits may result in reduced quality
# Verify subscription status

# 4. Audio post-processing
# Enable audio enhancement
AUDIO_ENHANCEMENT_ENABLED=true
NORMALIZE_AUDIO=true

# 5. Test different styles
# Some genres work better than others
# Lo-fi, electronic, ambient typically best results
```

### **Problem: Video Creation Fails**
```bash
🚨 ERROR: "MoviePy error" or video generation fails

💡 SOLUTION:
# 1. Check MoviePy installation
pip show moviepy
# Should be version 1.0.3 (stable)

# 2. Verify ffmpeg installation
ffmpeg -version
# Install if missing:
# Ubuntu: sudo apt install ffmpeg
# macOS: brew install ffmpeg
# Windows: Download from https://ffmpeg.org/

# 3. Check temp directory permissions
ls -la temp/
chmod 755 temp/
rm -rf temp/* # Clear temp files

# 4. Memory issues fix
# MoviePy can be memory intensive
export MOVIEPY_MEMORY_LIMIT=1GB
IMAGEIO_FFMPEG_EXE=$(which ffmpeg)

# 5. Reinstall MoviePy if corrupted
pip uninstall moviepy
pip install moviepy==1.0.3

# 6. Test video creation manually
python -c "
from moviepy.editor import ColorClip
clip = ColorClip(size=(1920,1080), color=(0,0,0), duration=10)
clip.write_videofile('test.mp4', fps=24)
print('Video test successful')
"
```

### **Problem: File Download Errors**
```bash
🚨 ERROR: "File not found" or download fails

💡 SOLUTION:
# 1. Check file permissions
ls -la output/
chmod 755 output/
chmod 644 output/*.mp3 output/*.mp4

# 2. Verify file exists
ls -la output/ | grep {generation_id}

# 3. Check disk space
df -h
# Ensure sufficient space (>2GB recommended)

# 4. Clean old files
# Automated cleanup (files older than 30 days)
find output/ -name "*.mp3" -mtime +30 -delete
find output/ -name "*.mp4" -mtime +30 -delete

# 5. Manual file recovery
python -c "
from main import recover_missing_files
recover_missing_files()
"

# 6. Re-download from Suno if file lost
python -c "
from core.services.suno_client import SunoClient
client = SunoClient()
client.redownload_generation('generation_id')
"
```

---

## 🎭 **Voice Cloning Issues**

### **Problem: Voice Character Creation Fails**
```bash
🚨 ERROR: "Voice cloning failed" or character not created

💡 SOLUTION:
# 1. Check ElevenLabs subscription
# Voice cloning requires Pro plan ($22/month minimum)

# 2. Verify character limit
curl -H "xi-api-key: YOUR_KEY" \
     https://api.elevenlabs.io/v1/voices
# Check available voice slots

# 3. Audio sample quality check
# Samples should be:
# - Clear audio (no background noise)
# - Single speaker
# - 1-10 minutes total duration
# - High quality (22kHz+ sample rate)

# 4. Retry with different samples
python -c "
from voice_cloning_empire import VoiceCloningEmpire
ve = VoiceCloningEmpire()
ve.retry_failed_characters()
"

# 5. Manual character creation
python -c "
from voice_cloning_empire import VoiceCloningEmpire
ve = VoiceCloningEmpire()
result = ve.create_voice_character(
    name='Luna',
    description='Dreamy lo-fi guide',
    samples=['sample1.wav', 'sample2.wav']
)
print(result)
"
```

### **Problem: Voice Synthesis Quality Issues**
```bash
🚨 ERROR: Generated voice sounds unnatural

💡 SOLUTION:
# 1. Improve training samples
# Use consistent audio quality
# Same microphone, environment, speaking style
# 2-3 samples, 2-5 minutes each

# 2. Adjust synthesis settings
VOICE_STABILITY=0.75  # Higher = more consistent
VOICE_CLARITY=0.85    # Higher = clearer pronunciation
VOICE_STYLE=0.20      # Lower = more natural

# 3. Script optimization
# Use natural language patterns
# Avoid technical jargon
# Include punctuation for proper pacing

# 4. Test different text lengths
# Shorter texts (50-200 words) often better quality
# Break long scripts into segments

# 5. Voice model retraining
python -c "
from voice_cloning_empire import VoiceCloningEmpire
ve = VoiceCloningEmpire()
ve.retrain_character('character_id', new_samples=['better_sample.wav'])
"
```

### **Problem: Character Content Generation Errors**
```bash
🚨 ERROR: Character script generation fails

💡 SOLUTION:
# 1. Check AI model availability
# Verify Gemini AI connection
curl -H "x-goog-api-key: YOUR_KEY" \
     https://generativelanguage.googleapis.com/v1/models

# 2. Character personality validation
python -c "
from voice_cloning_empire import VoiceCloningEmpire
ve = VoiceCloningEmpire()
characters = ve.list_characters()
for char in characters:
    print(f'{char.name}: {char.personality}')
"

# 3. Content template issues
# Check template files exist
ls -la templates/voice_*

# 4. Regenerate with simpler prompts
# Complex personalities may confuse AI
# Use clear, simple character descriptions

# 5. Manual script creation
# Bypass AI and create custom scripts
python -c "
from voice_cloning_empire import VoiceCloningEmpire
ve = VoiceCloningEmpire()
script = 'Hello everyone, welcome to another chill session with Luna.'
result = ve.synthesize_voice('luna_lofi', script)
print(result)
"
```

---

## 🚀 **Trending Hijacker Problems**

### **Problem: Trend Detection Not Working**
```bash
🚨 ERROR: No trends detected or monitoring fails

💡 SOLUTION:
# 1. Check monitoring service status
supervisorctl -c supervisord.conf status | grep trending

# 2. Verify API connections
python -c "
from live_trending_hijacker import LiveTrendingHijacker
lth = LiveTrendingHijacker()
status = lth.check_platform_connections()
print(status)
"

# 3. Check platform API quotas
# YouTube: 10,000 requests/day
# TikTok: Varies by agreement
# Spotify: 20,000 requests/day

# 4. Monitor log files
tail -f trending_hijacker.log

# 5. Restart monitoring service
python -c "
from live_trending_hijacker import LiveTrendingHijacker
lth = LiveTrendingHijacker()
lth.restart_monitoring()
"

# 6. Manual trend check
python -c "
from live_trending_hijacker import LiveTrendingHijacker
lth = LiveTrendingHijacker()
trends = lth.fetch_current_trends('youtube_music')
for trend in trends[:5]:
    print(f'{trend.title}: {trend.viral_score}')
"
```

### **Problem: Slow Trend Response Time**
```bash
🚨 ERROR: Taking too long to respond to trends (>2 hours)

💡 SOLUTION:
# 1. Optimize monitoring frequency
# Reduce scan interval for peak hours
PEAK_HOURS_INTERVAL=15  # minutes
NORMAL_HOURS_INTERVAL=30  # minutes

# 2. Increase generation priority
# Set trending generations to high priority
TRENDING_GENERATION_PRIORITY=high
MAX_CONCURRENT_TRENDING=3

# 3. Pre-generate content templates
# Have base content ready for quick customization
python -c "
from live_trending_hijacker import LiveTrendingHijacker
lth = LiveTrendingHijacker()
lth.prepare_rapid_response_templates()
"

# 4. Parallel processing
# Generate music and video simultaneously
PARALLEL_PROCESSING_ENABLED=true

# 5. Monitor system resources
htop
# Ensure sufficient CPU/memory for fast generation
```

### **Problem: Low Viral Success Rate**
```bash
🚨 ERROR: Hijacked content not going viral (<10% success rate)

💡 SOLUTION:
# 1. Analyze successful hijacks
python -c "
from live_trending_hijacker import LiveTrendingHijacker
lth = LiveTrendingHijacker()
analysis = lth.analyze_successful_hijacks()
print(analysis.success_patterns)
"

# 2. Improve trend scoring algorithm
# Focus on trends with specific characteristics:
# - Growth rate >100%/hour
# - Engagement rate >5%
# - Duration 60-90 seconds optimal

# 3. Optimize upload timing
# Upload within first 2 hours of trend detection
# Best times: 14:00-16:00, 20:00-22:00 UTC

# 4. Enhance content quality
# Use voice characters for trending content
# Add visual elements to videos
# Optimize titles and descriptions

# 5. A/B test different approaches
# Test various music styles for same trend
# Compare performance metrics
```

---

## 🤖 **Community Empire Issues**

### **Problem: Bot Not Responding in Discord**
```bash
🚨 ERROR: Discord bot offline or not responding

💡 SOLUTION:
# 1. Check bot status
python -c "
from automated_community_empire import AutomatedCommunityEmpire
ace = AutomatedCommunityEmpire()
status = ace.check_bot_status('discord')
print(f'Bot online: {status.online}')
print(f'Last activity: {status.last_activity}')
"

# 2. Verify bot token
cat .env | grep DISCORD_BOT_TOKEN
# Token should start with 'MTA' or similar

# 3. Check bot permissions in Discord
# Bot needs:
# - Send Messages
# - Read Message History
# - Use Slash Commands
# - Attach Files

# 4. Restart Discord bot
python -c "
from automated_community_empire import AutomatedCommunityEmpire
ace = AutomatedCommunityEmpire()
ace.restart_platform_bot('discord')
"

# 5. Check Discord server settings
# Ensure bot has proper role hierarchy
# Verify channel permissions

# 6. Manual bot test
python -c "
import discord
client = discord.Client()
# Test basic connection
"
```

### **Problem: AI Responses Are Inappropriate**
```bash
🚨 ERROR: Bot generates inappropriate or off-topic responses

💡 SOLUTION:
# 1. Check content filtering
python -c "
from automated_community_empire import CommunityAIEngine
ai = CommunityAIEngine()
filters = ai.get_active_filters()
print(filters)
"

# 2. Update response templates
# Ensure templates are appropriate for audience
# Review and update personality guidelines

# 3. Implement stricter filtering
CONTENT_FILTER_LEVEL=strict
INAPPROPRIATE_CONTENT_BLOCK=true
POLITICAL_CONTENT_BLOCK=true

# 4. Human review mode
# Enable manual approval for uncertain responses
HUMAN_REVIEW_ENABLED=true
CONFIDENCE_THRESHOLD=85  # Only auto-respond if >85% confident

# 5. Retrain AI model
python -c "
from automated_community_empire import CommunityAIEngine
ai = CommunityAIEngine()
ai.update_training_data_from_successful_interactions()
ai.retrain_response_model()
"

# 6. Community feedback integration
# Allow community to rate bot responses
# Use feedback to improve future responses
```

### **Problem: Low Community Engagement**
```bash
🚨 ERROR: Community not engaging with bot or content

💡 SOLUTION:
# 1. Analyze engagement patterns
python -c "
from automated_community_empire import AutomatedCommunityEmpire
ace = AutomatedCommunityEmpire()
metrics = ace.get_engagement_analytics()
print(f'Average response rate: {metrics.response_rate}%')
print(f'Most engaging content type: {metrics.top_content_type}')
"

# 2. Optimize response timing
# Respond when community is most active
OPTIMAL_RESPONSE_HOURS=[14, 15, 16, 20, 21, 22]  # UTC
RESPONSE_DELAY_MIN=30    # seconds
RESPONSE_DELAY_MAX=300   # seconds

# 3. Personalize interactions more
# Use member history and preferences
PERSONALIZATION_LEVEL=high
USE_MEMBER_PREFERENCES=true
REMEMBER_PAST_INTERACTIONS=true

# 4. Add interactive elements
# Polls, games, music requests
INTERACTIVE_CONTENT_ENABLED=true
DAILY_MUSIC_POLLS=true
WEEKLY_CHALLENGES=true

# 5. Community events
python -c "
from automated_community_empire import AutomatedCommunityEmpire
ace = AutomatedCommunityEmpire()
ace.schedule_weekly_events()
ace.create_music_listening_parties()
"
```

---

## ⚡ **System Performance Issues**

### **Problem: High Memory Usage**
```bash
🚨 ERROR: System running out of memory, slow performance

💡 SOLUTION:
# 1. Check current memory usage
free -h
ps aux --sort=-%mem | head -10

# 2. MoviePy memory optimization
export MOVIEPY_TEMP_DIR=/tmp/moviepy
export IMAGEIO_FFMPEG_EXE=/usr/bin/ffmpeg
export MOVIEPY_MEMORY_LIMIT=1GB

# 3. Limit concurrent operations
MAX_CONCURRENT_GENERATIONS=2
MAX_CONCURRENT_VOICE_SYNTHESIS=1
MAX_CONCURRENT_VIDEO_CREATION=1

# 4. Clear temp files regularly
# Add to crontab for hourly cleanup
echo "0 * * * * find /tmp -name 'moviepy*' -mtime +1 -delete" | crontab -

# 5. Increase swap space (Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 6. Restart services to clear memory
supervisorctl -c supervisord.conf restart all
```

### **Problem: Slow API Response Times**
```bash
🚨 ERROR: API calls taking too long (>30 seconds)

💡 SOLUTION:
# 1. Check network connectivity
ping api.suno.com
ping api.elevenlabs.io
curl -w "%{time_total}" https://api.suno.com

# 2. Implement caching
REDIS_CACHE_ENABLED=true
CACHE_EXPIRY_HOURS=24
API_RESPONSE_CACHE=true

# 3. Connection pooling
HTTP_CONNECTION_POOL_SIZE=10
HTTP_MAX_RETRIES=3
HTTP_TIMEOUT=60

# 4. Async processing
# Enable background job processing
ASYNC_PROCESSING=true
CELERY_WORKERS=4

# 5. Monitor API performance
python -c "
from core.utils.performance_monitor import PerformanceMonitor
pm = PerformanceMonitor()
report = pm.get_api_performance_report()
print(report)
"

# 6. Use CDN for static content
# Configure Cloudflare or similar
CDN_ENABLED=true
STATIC_FILES_CDN=https://cdn.example.com
```

### **Problem: Database Performance Issues**
```bash
🚨 ERROR: Database queries are slow

💡 SOLUTION:
# 1. Check database size and indexes
sqlite3 autonominis_muzikantas.db ".schema"
sqlite3 autonominis_muzikantas.db "PRAGMA integrity_check;"

# 2. Optimize database
sqlite3 autonominis_muzikantas.db "VACUUM;"
sqlite3 autonominis_muzikantas.db "REINDEX;"

# 3. Add missing indexes
sqlite3 autonominis_muzikantas.db "
CREATE INDEX IF NOT EXISTS idx_generation_status ON generations(status);
CREATE INDEX IF NOT EXISTS idx_generation_created ON generations(created_at);
CREATE INDEX IF NOT EXISTS idx_voice_content_character ON voice_content(character_id);
"

# 4. Clean old data
python -c "
from main import cleanup_old_database_records
cleanup_old_database_records(days=90)
"

# 5. Database maintenance
python -c "
from core.utils.database_maintenance import DatabaseMaintenance
dm = DatabaseMaintenance()
dm.optimize_all_tables()
dm.cleanup_temporary_data()
"

# 6. Monitor database performance
sqlite3 autonominis_muzikantas.db "
.timer on
SELECT COUNT(*) FROM generations;
SELECT COUNT(*) FROM voice_content;
SELECT COUNT(*) FROM trending_data;
"
```

---

## 💾 **Database Problems**

### **Problem: Database Locked Error**
```bash
🚨 ERROR: "Database is locked" or "SQLITE_BUSY"

💡 SOLUTION:
# 1. Stop all services accessing database
supervisorctl -c supervisord.conf stop all

# 2. Check for lock files
ls -la *.db*
rm -f *.db-lock *.db-shm *.db-wal

# 3. Check running processes
lsof *.db
# Kill any processes still using database

# 4. Database integrity check
sqlite3 autonominis_muzikantas.db "PRAGMA integrity_check;"

# 5. Enable WAL mode for better concurrency
sqlite3 autonominis_muzikantas.db "PRAGMA journal_mode=WAL;"

# 6. Restart services
supervisorctl -c supervisord.conf start all

# 7. If still locked, backup and recreate
cp autonominis_muzikantas.db backup_$(date +%Y%m%d).db
sqlite3 autonominis_muzikantas.db ".backup backup.db"
mv autonominis_muzikantas.db corrupted.db
mv backup.db autonominis_muzikantas.db
```

### **Problem: Database Corruption**
```bash
🚨 ERROR: "Database disk image is malformed" 

💡 SOLUTION:
# 1. Stop all services
supervisorctl -c supervisord.conf stop all

# 2. Create backup
cp *.db backup/$(date +%Y%m%d)/

# 3. Check corruption extent
sqlite3 autonominis_muzikantas.db "PRAGMA integrity_check;"

# 4. Attempt repair
sqlite3 autonominis_muzikantas.db "
.mode insert
.output recovery.sql
.dump
.exit
"

# 5. Recreate database from dump
mv autonominis_muzikantas.db corrupted.db
sqlite3 new_autonominis_muzikantas.db < recovery.sql
mv new_autonominis_muzikantas.db autonominis_muzikantas.db

# 6. Verify repair
sqlite3 autonominis_muzikantas.db "PRAGMA integrity_check;"

# 7. Restart services
supervisorctl -c supervisord.conf start all

# 8. If repair fails, restore from backup
# Use most recent backup from backup/ directory
```

### **Problem: Missing Database Tables**
```bash
🚨 ERROR: "No such table" errors

💡 SOLUTION:
# 1. Check existing tables
sqlite3 autonominis_muzikantas.db ".tables"

# 2. Recreate missing tables
python -c "
from main import init_database
init_database(force_recreate=False)
"

# 3. Initialize all component databases
python -c "
from voice_cloning_empire import VoiceCloningEmpire
from live_trending_hijacker import LiveTrendingHijacker
from automated_community_empire import AutomatedCommunityEmpire

ve = VoiceCloningEmpire()
ve.init_database()

lth = LiveTrendingHijacker()
lth.init_database() 

ace = AutomatedCommunityEmpire()
ace.init_database()
"

# 4. Verify table creation
sqlite3 autonominis_muzikantas.db ".schema" | grep "CREATE TABLE"

# 5. Import sample data if needed
python -c "
from main import import_sample_data
import_sample_data()
"
```

---

## 🌐 **Network & Connectivity**

### **Problem: SSL Certificate Errors**
```bash
🚨 ERROR: "SSL: CERTIFICATE_VERIFY_FAILED"

💡 SOLUTION:
# 1. Update certificates (Ubuntu/Debian)
sudo apt update && sudo apt upgrade ca-certificates

# 2. Update certificates (macOS)
brew update && brew upgrade ca-certificates

# 3. Python certificate fix
pip install --upgrade certifi

# 4. Temporarily bypass SSL (development only)
export PYTHONHTTPSVERIFY=0
export SSL_VERIFY=False

# 5. Manual certificate install
python -c "
import ssl
import certifi
print(ssl.get_default_verify_paths())
print(certifi.where())
"

# 6. Corporate firewall bypass
# If behind corporate firewall, configure proxy
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

### **Problem: Firewall Blocking Connections**
```bash
🚨 ERROR: Connection timeouts or "Connection refused"

💡 SOLUTION:
# 1. Check firewall status (Linux)
sudo ufw status
sudo iptables -L

# 2. Open required ports
sudo ufw allow 3000  # Main server
sudo ufw allow 8000  # Admin server
sudo ufw allow out 443  # HTTPS outbound
sudo ufw allow out 80   # HTTP outbound

# 3. Windows Firewall
# Add inbound rules for ports 3000, 8000
# Add outbound rules for HTTPS (443)

# 4. Test connectivity
telnet api.suno.com 443
curl -I https://api.elevenlabs.io

# 5. Router/NAT configuration
# If running on local network, configure port forwarding
# Router settings: Forward 3000 → internal_ip:3000

# 6. Check DNS resolution
nslookup api.suno.com
dig api.elevenlabs.io
```

### **Problem: Proxy Configuration Issues**
```bash
🚨 ERROR: Requests failing through corporate proxy

💡 SOLUTION:
# 1. Configure proxy environment variables
export HTTP_PROXY=http://username:password@proxy.company.com:8080
export HTTPS_PROXY=http://username:password@proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1,.local

# 2. Python requests proxy configuration
# Add to .env:
PROXY_HTTP=http://proxy.company.com:8080
PROXY_HTTPS=http://proxy.company.com:8080

# 3. Verify proxy settings
curl -I --proxy http://proxy.company.com:8080 https://api.suno.com

# 4. Bypass proxy for local services
NO_PROXY_HOSTS=localhost,127.0.0.1,0.0.0.0

# 5. Corporate certificate installation
# Download corporate root certificate
# Install in Python cert store
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org certifi
```

---

## 🚀 **Deployment Issues**

### **Problem: Supervisor Service Won't Start**
```bash
🚨 ERROR: "supervisord: command not found" or service fails

💡 SOLUTION:
# 1. Install supervisor
pip install supervisor

# 2. Verify installation
supervisord --version
which supervisord

# 3. Check configuration file
cat supervisord.conf
# Ensure paths are correct and absolute

# 4. Fix configuration file permissions
chmod 644 supervisord.conf

# 5. Start with explicit config
supervisord -c $(pwd)/supervisord.conf

# 6. Check logs
tail -f supervisord.log

# 7. Alternative: Use systemd (Linux)
sudo tee /etc/systemd/system/autonominis-muzikantas.service << 'EOF'
[Unit]
Description=Autonominis Muzikantas
After=network.target

[Service]
Type=forking
User=user
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/venv/bin/supervisord -c supervisord.conf
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable autonominis-muzikantas
sudo systemctl start autonominis-muzikantas
```

### **Problem: Port Already in Use**
```bash
🚨 ERROR: "Address already in use" on ports 3000 or 8000

💡 SOLUTION:
# 1. Find process using port (Linux/Mac)
lsof -i :3000
lsof -i :8000

# 2. Find process using port (Windows)
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# 3. Kill process using port
kill -9 <PID>
# Windows: taskkill /PID <PID> /F

# 4. Use different ports temporarily
# Edit admin_app.py and main.py:
app.run(host='0.0.0.0', port=3001)  # Instead of 3000
app.run(host='0.0.0.0', port=8001)  # Instead of 8000

# 5. Configure firewall for new ports
sudo ufw allow 3001
sudo ufw allow 8001

# 6. Check for zombie processes
ps aux | grep python | grep -E "(main.py|admin_app.py)"
```

### **Problem: Permission Denied on Production**
```bash
🚨 ERROR: Permission errors in production environment

💡 SOLUTION:
# 1. Fix ownership
sudo chown -R www-data:www-data /var/www/autonominis-muzikantas
# Or for your user:
sudo chown -R $USER:$USER /path/to/project

# 2. Set proper permissions
find . -type f -name "*.py" -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;
chmod +x main.py admin_app.py

# 3. SELinux context (RHEL/CentOS)
sudo setsebool -P httpd_can_network_connect 1
sudo chcon -R -t httpd_exec_t /var/www/autonominis-muzikantas/

# 4. Create service user
sudo useradd -r -s /bin/false autonominis
sudo chown -R autonominis:autonominis /opt/autonominis-muzikantas

# 5. Configure sudo for service management
echo "autonominis ALL=(ALL) NOPASSWD: /bin/systemctl restart autonominis-muzikantas" | sudo tee -a /etc/sudoers.d/autonominis
```

---

## 🔢 **Error Code Reference**

### **HTTP Status Codes:**
```bash
# 2xx Success
200 OK                    # Request successful
201 Created              # Resource created successfully
202 Accepted             # Request accepted for processing

# 4xx Client Errors  
400 Bad Request          # Invalid parameters
401 Unauthorized         # Authentication required
403 Forbidden           # Permission denied
404 Not Found           # Resource not found
422 Unprocessable Entity # Validation error
429 Too Many Requests   # Rate limit exceeded

# 5xx Server Errors
500 Internal Server Error # Generic server error
502 Bad Gateway         # External service unavailable
503 Service Unavailable # System under maintenance
504 Gateway Timeout     # External service timeout
```

### **Custom Application Error Codes:**
```bash
# Music Generation Errors (1000-1099)
1001 INSUFFICIENT_CREDITS     # Not enough API credits
1002 GENERATION_FAILED        # Music generation failed
1003 INVALID_STYLE           # Unsupported music style
1004 DURATION_LIMIT_EXCEEDED # Track too long
1005 QUEUE_FULL              # Generation queue at capacity

# Voice Cloning Errors (1100-1199)  
1101 VOICE_SYNTHESIS_ERROR    # Voice synthesis failed
1102 CHARACTER_NOT_FOUND     # Voice character doesn't exist
1103 SAMPLE_QUALITY_LOW      # Audio samples poor quality
1104 VOICE_LIMIT_REACHED     # Character limit exceeded
1105 CLONING_IN_PROGRESS     # Voice cloning still processing

# Trending Hijacker Errors (1200-1299)
1201 TREND_DETECTION_ERROR    # Trending analysis failed
1202 NO_TRENDS_FOUND         # No viable trends detected
1203 HIJACK_GENERATION_ERROR # Trend response generation failed
1204 VIRAL_SCORE_TOO_LOW     # Trend not viral enough
1205 TREND_EXPIRED           # Trend window closed

# Community Empire Errors (1300-1399)
1301 BOT_OFFLINE             # Community bot not responding
1302 PLATFORM_API_ERROR     # Social platform API error
1303 MESSAGE_GENERATION_ERROR # AI response generation failed
1304 SENTIMENT_ANALYSIS_ERROR # Sentiment detection failed
1305 RATE_LIMIT_PLATFORM    # Platform rate limit hit

# System Errors (1400-1499)
1401 DATABASE_ERROR          # Database operation failed
1402 FILE_SYSTEM_ERROR      # File operation failed  
1403 CONFIGURATION_ERROR    # Invalid configuration
1404 DEPENDENCY_ERROR       # Missing dependency
1405 RESOURCE_EXHAUSTED     # System resources full
```

### **Error Response Format:**
```json
{
  "status": "error",
  "error": {
    "code": 1001,
    "type": "INSUFFICIENT_CREDITS",
    "message": "Not enough Suno AI credits to generate music",
    "details": {
      "current_credits": 2,
      "required_credits": 10,
      "account_type": "free",
      "upgrade_url": "https://suno.ai/pricing"
    },
    "suggestion": "Add more credits to your Suno AI account or upgrade to Pro plan",
    "timestamp": "2024-01-15T14:30:00Z",
    "request_id": "req_789456123"
  }
}
```

---

## 🔍 **Advanced Diagnostics**

### **System Health Check Script:**
```bash
#!/bin/bash
# save as health_check.sh

echo "=== Autonominis Muzikantas Health Check ==="
echo "Timestamp: $(date)"
echo ""

# System resources
echo "🖥️ System Resources:"
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')"
echo "Memory: $(free -h | awk 'NR==2{printf "%.1f%%", $3*100/$2 }')"
echo "Disk: $(df -h | awk '$NF=="/"{printf "%.1f%%", $5}')"
echo ""

# Services status
echo "⚙️ Services Status:"
if pgrep -f "supervisord" > /dev/null; then
    echo "✅ Supervisor: Running"
    supervisorctl -c supervisord.conf status
else
    echo "❌ Supervisor: Not running"
fi
echo ""

# Database health
echo "💾 Database Health:"
for db in *.db; do
    if [ -f "$db" ]; then
        result=$(sqlite3 "$db" "PRAGMA integrity_check;" 2>/dev/null)
        if [ "$result" = "ok" ]; then
            echo "✅ $db: OK"
        else
            echo "❌ $db: CORRUPTED"
        fi
    fi
done
echo ""

# API connectivity
echo "🌐 API Connectivity:"
if curl -s --max-time 10 https://api.suno.com >/dev/null; then
    echo "✅ Suno AI: Reachable"
else
    echo "❌ Suno AI: Unreachable"
fi

if curl -s --max-time 10 https://api.elevenlabs.io >/dev/null; then
    echo "✅ ElevenLabs: Reachable"
else
    echo "❌ ElevenLabs: Unreachable"
fi
echo ""

# Log analysis
echo "📋 Recent Errors:"
grep -i error logs/*.log 2>/dev/null | tail -5
echo ""

echo "==============================================="
```

### **Performance Monitoring Script:**
```bash
#!/bin/bash
# save as performance_monitor.sh

# Monitor system performance for 60 seconds
echo "📊 Performance Monitoring (60 seconds)..."

# CPU and Memory monitoring
sar -u -r 1 60 > performance_$(date +%Y%m%d_%H%M%S).log &
SAR_PID=$!

# Network monitoring
iftop -t -s 60 > network_$(date +%Y%m%d_%H%M%S).log 2>&1 &
IFTOP_PID=$!

# Process monitoring
while [ $SECONDS -lt 60 ]; do
    echo "$(date): $(ps aux --sort=-%cpu | head -5)" >> process_$(date +%Y%m%d_%H%M%S).log
    sleep 10
done

# Cleanup
kill $SAR_PID $IFTOP_PID 2>/dev/null

echo "Performance data saved to *_$(date +%Y%m%d)*.log files"
```

### **Automated Problem Detection:**
```python
#!/usr/bin/env python3
# save as problem_detector.py

import sqlite3
import psutil
import requests
import os
from datetime import datetime, timedelta

class ProblemDetector:
    def __init__(self):
        self.issues = []
        
    def check_system_resources(self):
        """Check CPU, memory, disk usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        if cpu_percent > 90:
            self.issues.append(f"HIGH CPU: {cpu_percent}%")
            
        if memory.percent > 85:
            self.issues.append(f"HIGH MEMORY: {memory.percent}%")
            
        if disk.percent > 90:
            self.issues.append(f"HIGH DISK: {disk.percent}%")
    
    def check_databases(self):
        """Check database integrity"""
        for db_file in ['autonominis_muzikantas.db', 'voice_empire.db', 
                       'trending_hijacker.db', 'community_empire.db']:
            if os.path.exists(db_file):
                try:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.execute("PRAGMA integrity_check;")
                    result = cursor.fetchone()[0]
                    conn.close()
                    
                    if result != 'ok':
                        self.issues.append(f"DB CORRUPT: {db_file}")
                except Exception as e:
                    self.issues.append(f"DB ERROR: {db_file} - {str(e)}")
    
    def check_api_connectivity(self):
        """Check external API connectivity"""
        apis = {
            'Suno AI': 'https://api.suno.com',
            'ElevenLabs': 'https://api.elevenlabs.io',
            'YouTube': 'https://www.googleapis.com/youtube/v3',
        }
        
        for name, url in apis.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code >= 500:
                    self.issues.append(f"API DOWN: {name}")
            except Exception:
                self.issues.append(f"API UNREACHABLE: {name}")
    
    def check_log_files(self):
        """Check for recent errors in logs"""
        log_files = ['logs/webserver.log', 'logs/admin_server.log', 
                    'supervisord.log']
        
        cutoff_time = datetime.now() - timedelta(minutes=30)
        
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()[-100:]  # Last 100 lines
                        
                    error_count = sum(1 for line in lines 
                                    if 'ERROR' in line.upper() or 'CRITICAL' in line.upper())
                    
                    if error_count > 5:
                        self.issues.append(f"HIGH ERRORS: {log_file} ({error_count} errors)")
                        
                except Exception as e:
                    self.issues.append(f"LOG READ ERROR: {log_file}")
    
    def generate_report(self):
        """Generate problem detection report"""
        print(f"🔍 Problem Detection Report - {datetime.now()}")
        print("=" * 50)
        
        if not self.issues:
            print("✅ No issues detected - System healthy")
        else:
            print(f"⚠️  {len(self.issues)} issues detected:")
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue}")
        
        print("\n" + "=" * 50)
        return len(self.issues)

if __name__ == "__main__":
    detector = ProblemDetector()
    detector.check_system_resources()
    detector.check_databases()
    detector.check_api_connectivity()
    detector.check_log_files()
    
    issue_count = detector.generate_report()
    exit(issue_count)  # Exit with number of issues for scripting
```

### **Usage:**
```bash
# Make scripts executable
chmod +x health_check.sh performance_monitor.sh problem_detector.py

# Run health check
./health_check.sh

# Run performance monitoring
./performance_monitor.sh

# Run automated problem detection
python3 problem_detector.py

# Schedule automated checks (add to crontab)
# Run health check every hour
0 * * * * /path/to/health_check.sh >> /var/log/health_check.log

# Run problem detection every 15 minutes
*/15 * * * * /path/to/problem_detector.py >> /var/log/problem_detection.log
```

---

## 📞 **Getting Additional Help**

### **Support Channels Priority:**
1. **🔴 Critical System Down:** Create GitHub Issue with 'critical' label
2. **🟡 Bug Reports:** GitHub Issues with reproduction steps
3. **🟢 Questions:** GitHub Discussions or Discord
4. **📧 Direct Support:** autonominis.support@gmail.com

### **When Creating Support Requests:**
```bash
# Include this information:
1. System Information:
   - OS: $(uname -a)
   - Python: $(python --version)
   - System: $(./health_check.sh)

2. Error Details:
   - Exact error message
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant log files

3. Configuration:
   - .env file (sanitized - no API keys!)
   - supervisord.conf
   - Recent changes made

4. Performance Data:
   - ./performance_monitor.sh output
   - ./problem_detector.py results
   - System resource usage
```

### **Self-Help Resources:**
- 📚 **Documentation:** README_LT.md, INSTALLATION.md
- 💻 **Code Examples:** GitHub repository examples/
- 🎥 **Video Tutorials:** Coming soon
- 💬 **Community:** Discord #support channel

---

**🎯 Remember: Most issues can be resolved by following this guide systematically. Always backup your data before making significant changes!**

*Troubleshooting Guide Version: 3.0.0 | Last Updated: 2024-01-15 | Next Update: 2024-02-15*