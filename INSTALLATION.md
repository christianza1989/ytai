# 🚀 Autonominis Muzikantas - Detalus Diegimo Vadovas

## 📋 Sistemos Reikalavimai

### **Minimalūs Reikalavimai:**
- **OS:** Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python:** 3.8 ar naujesnė versija
- **RAM:** 4GB (rekomenduojama 8GB+)  
- **Disk:** 10GB laisvos vietos
- **Internet:** Stabilus ryšys API calls

### **Rekomenduojami Reikalavimai:**
- **OS:** Ubuntu 20.04+ / Windows 11 / macOS 12+
- **Python:** 3.10+
- **RAM:** 16GB+ (multi-threading optimization)
- **Disk:** 50GB+ SSD (fast audio processing)
- **CPU:** 4+ cores (concurrent generation)

---

## 🔧 **Žingsnis 1: Sistemos Paruošimas**

### **Windows:**
```powershell
# 1. Atsisiųskite Python 3.10+ iš python.org
# 2. Įdiekite su "Add to PATH" opcija
python --version

# 3. Įdiekite Git
# Atsisiųskite iš git-scm.com
git --version

# 4. Atidarykite PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **macOS:**
```bash
# 1. Įdiekite Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Įdiekite Python ir Git
brew install python@3.10
brew install git

# 3. Patikrinkite versijas
python3 --version
git --version
```

### **Linux (Ubuntu/Debian):**
```bash
# 1. Atnaujinkite sistemą
sudo apt update && sudo apt upgrade -y

# 2. Įdiekite Python ir priklausomybes
sudo apt install python3.10 python3.10-venv python3.10-pip
sudo apt install git curl wget

# 3. Įdiekite papildomas bibliotekas
sudo apt install ffmpeg libmagic1
sudo apt install build-essential python3-dev

# 4. Patikrinkite versijas
python3 --version
git --version
```

---

## 📥 **Žingsnis 2: Projekto Parsisiuntimas**

### **GitHub Clone:**
```bash
# 1. Klonuokite projektą
git clone https://github.com/christianza1989/ytai.git
cd ytai

# 2. Perjunkite į DIAMOND branch (svarbu!)
git checkout genspark_ai_developer

# 3. Patikrinkite branch'ą
git branch
# * genspark_ai_developer ← turėtumėte matyti žvaigždutę

# 4. Patikrinkite ar yra DIAMOND failus
ls -la | grep -E "(voice_cloning|trending|community)"
```

### **Alternative: ZIP Download:**
```bash
# Jei neturite Git, atsisiųskite ZIP:
# 1. Eikite į https://github.com/christianza1989/ytai
# 2. Pasirinkite "genspark_ai_developer" branch
# 3. Spragtelėkite "Code" → "Download ZIP"
# 4. Išpakuokite ir cd į katalogą
```

---

## 🐍 **Žingsnis 3: Python Aplinkos Konfigūracija**

### **Virtual Environment Setup:**
```bash
# 1. Sukurkite virtual environment
python -m venv venv
# arba macOS/Linux:
python3 -m venv venv

# 2. Aktyvuokite environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Patikrinkite aktyvaciją (turėtumėte matyti (venv) prefix)
which python  # macOS/Linux
where python  # Windows

# 4. Atnaujinkite pip
python -m pip install --upgrade pip
```

### **Dependencies Installation:**
```bash
# 1. Patikrinkite ar yra requirements.txt
cat requirements.txt

# 2. Įdiekite visas priklausomybes
pip install -r requirements.txt

# 3. Jei requirements.txt neegzistuoja, įdiekite rankiniu būdu:
pip install flask==2.3.3
pip install requests==2.31.0  
pip install python-dotenv==1.0.0
pip install moviepy==1.0.3
pip install Pillow==10.0.0
pip install werkzeug==2.3.6
pip install gunicorn==20.1.0
pip install supervisor

# 4. Patikrinkite instaliaciją
pip list | grep -E "(flask|requests|moviepy)"
```

---

## 🔑 **Žingsnis 4: API Raktų Konfigūracija**

### **4.1. Environment File Setup:**
```bash
# 1. Nukopijuokite pavyzdinį failą
cp .env.example .env

# 2. Redaguokite .env failą
# Windows:
notepad .env
# macOS:
nano .env
# Linux:
nano .env
```

### **4.2. .env Failo Turinys:**
```env
# ========================================
# CORE API KEYS (BŪTINI)
# ========================================

# SUNO AI API - Pagrindinis muzikos generavimas
SUNO_API_KEY=your_suno_api_key_here
SUNO_API_BASE=https://api.sunoapi.org/api/v1

# ELEVENLABS API - Voice Cloning (DIAMOND System #3)  
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# GEMINI AI API - AI optimization
GEMINI_API_KEY=your_gemini_api_key_here

# YOUTUBE DATA API - YouTube integration
YOUTUBE_DATA_API_KEY=your_youtube_api_key_here

# ========================================
# FLASK CONFIGURATION
# ========================================
FLASK_SECRET_KEY=your_super_secret_key_here_make_it_random_and_long
FLASK_ENV=production
FLASK_DEBUG=False

# ========================================
# SOCIAL MEDIA APIS (OPTIONAL)
# ========================================

# Discord Bot (Community Empire)
DISCORD_BOT_TOKEN=your_discord_bot_token_here

# Reddit API (Community Empire)
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_secret_here

# Twitter API (Community Empire)
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_secret_here

# Spotify API (Trending Hijacker)
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_secret_here

# Instagram API (Community Empire)
INSTAGRAM_ACCESS_TOKEN=your_instagram_token_here

# TikTok API (Trending Hijacker)
TIKTOK_API_KEY=your_tiktok_api_key_here

# ========================================
# DATABASE CONFIGURATION
# ========================================
DATABASE_URL=sqlite:///autonominis_muzikantas.db

# ========================================
# ADVANCED SETTINGS
# ========================================
MAX_GENERATION_TIME=300
DEFAULT_AUDIO_FORMAT=mp3
LOG_LEVEL=INFO
BACKUP_ENABLED=true
```

### **4.3. API Raktų Gavimo Instrukcijos:**

#### **🎵 SUNO AI API (BŪTINAS):**
```bash
# 1. Registruokitės: https://suno.ai
# 2. Eikite į Account Settings
# 3. API Keys section
# 4. Generate new API key
# 5. Nukopijuokite ir įdėkite į .env

# Test API key:
curl -H "Authorization: Bearer your_api_key" https://api.suno.com/api/v1/credits
```

#### **🎭 ElevenLabs API (Voice Cloning):**
```bash
# 1. Registruokitės: https://elevenlabs.io
# 2. Eikite į Profile → API Key
# 3. Copy API key
# 4. Įdėkite į .env

# Test API key:
curl -H "xi-api-key: your_api_key" https://api.elevenlabs.io/v1/user
```

#### **🤖 YouTube Data API:**
```bash
# 1. Eikite į: https://console.developers.google.com
# 2. Create new project arba select existing
# 3. Enable "YouTube Data API v3"
# 4. Credentials → Create credentials → API Key
# 5. Nukopijuokite API key

# Test API key:
curl "https://www.googleapis.com/youtube/v3/search?part=snippet&q=test&key=YOUR_API_KEY"
```

#### **🧠 Gemini AI API:**
```bash
# 1. Eikite į: https://makersuite.google.com/app/apikey
# 2. Create API key
# 3. Nukopijuokite key

# Test API key:
curl -H "x-goog-api-key: your_api_key" https://generativelanguage.googleapis.com/v1/models
```

---

## 🗄️ **Žingsnis 5: Duomenų Bazės Setup**

### **Database Initialization:**
```bash
# 1. Sukurkite reikalingus katalogus
mkdir -p logs output temp static/css static/js templates

# 2. Nustatykite leidimus
chmod 755 logs output temp static
chmod 644 *.py

# 3. Inicializuokite duomenų bazę
python -c "
import sqlite3
from pathlib import Path

# Create main database
conn = sqlite3.connect('autonominis_muzikantas.db')
conn.execute('CREATE TABLE IF NOT EXISTS init_check (id INTEGER PRIMARY KEY)')
conn.commit()
conn.close()

print('✅ Main database initialized')

# Initialize component databases
Path('voice_empire.db').touch()
Path('trending_hijacker.db').touch()  
Path('community_empire.db').touch()

print('✅ Component databases created')
print('✅ Database setup complete!')
"
```

### **Database Verification:**
```bash
# Patikrinkite ar duomenų bazės egzistuoja
ls -la *.db

# Patikrinkite struktūrą
sqlite3 autonominis_muzikantas.db ".schema"
```

---

## 🚀 **Žingsnis 6: Sistemos Paleidimas**

### **6.1. Development Mode (Testing):**
```bash
# 1. Aktyvuokite virtual environment
source venv/bin/activate  # macOS/Linux
# arba: venv\Scripts\activate  # Windows

# 2. Test basic functionality
python -c "
from main import app
print('✅ Main app imports successfully')

from admin_app import app as admin_app  
print('✅ Admin app imports successfully')

from voice_cloning_empire import VoiceCloningEmpire
ve = VoiceCloningEmpire()
print('✅ Voice Empire initializes successfully')
"

# 3. Paleiskite main server (Terminal 1)
python main.py
# Turėtumėte matyti: "Running on http://127.0.0.1:3000"

# 4. Atidarykite naują terminal ir paleiskite admin (Terminal 2)
source venv/bin/activate  # Aktyvuokite environment
python admin_app.py
# Turėtumėte matyti: "Running on http://127.0.0.1:8000"
```

### **6.2. Production Mode (Recommended):**
```bash
# 1. Įdiekite supervisor (jei dar neįdiegta)
pip install supervisor

# 2. Sukurkite supervisor config
cat > supervisord.conf << 'EOF'
[supervisord]
nodaemon=false
logfile=./supervisord.log
pidfile=./supervisord.pid
childlogdir=./logs

[unix_http_server]
file=./supervisor.sock
chmod=0700

[supervisorctl]
serverurl=unix://./supervisor.sock

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[program:webserver]
command=python main.py
directory=./
autostart=true
autorestart=true
stdout_logfile=./logs/webserver.log
stderr_logfile=./logs/webserver_error.log
environment=PATH="./venv/bin:%(ENV_PATH)s"

[program:admin_server]  
command=python admin_app.py
directory=./
autostart=true
autorestart=true
stdout_logfile=./logs/admin_server.log
stderr_logfile=./logs/admin_server_error.log
environment=PATH="./venv/bin:%(ENV_PATH)s"
EOF

# 3. Paleiskite supervisor
supervisord -c supervisord.conf

# 4. Patikrinkite statusą
supervisorctl -c supervisord.conf status

# 5. Valdykite services
supervisorctl -c supervisord.conf restart webserver
supervisorctl -c supervisord.conf restart admin_server
supervisorctl -c supervisord.conf stop all
```

---

## ✅ **Žingsnis 7: Sistemos Patikrinimas**

### **7.1. Health Check:**
```bash
# 1. Patikrinkite ar serveriai veikia
curl -I http://localhost:3000
curl -I http://localhost:8000

# 2. Patikrinkite API endpoints
curl http://localhost:8000/api/system/status

# 3. Patikrinkite logus
tail -f logs/webserver.log
tail -f logs/admin_server.log
tail -f supervisord.log
```

### **7.2. Admin Interface Test:**
```bash
# 1. Atidarykite browser: http://localhost:8000
# 2. Login credentials:
#    Username: admin
#    Password: admin123
# 3. Turėtumėte matyti dashboard su:
#    - ✅ API Status indicators
#    - ✅ Navigation menu su DIAMOND systems
#    - ✅ System metrics
```

### **7.3. Functionality Test:**
```bash
# 1. Test music generation
# Eikite į Admin → Generator
# Užpildykite:
# - Prompt: "Relaxing lo-fi hip hop for studying"
# - Style: "lo-fi hip hop"
# - Duration: 60
# Spragtelėkite "Generate"

# 2. Test Voice Empire  
# Eikite į Admin → Voice Cloning Empire
# Spragtelėkite "Initialize Voice Empire"
# Turėtumėte matyti 8 characters created

# 3. Test Trending Hijacker
# Eikite į Admin → Trending Hijacker  
# Spragtelėkite "Start Live Monitoring"
# Turėtumėte matyti real-time trends
```

---

## 🔧 **Žingsnis 8: Optimizacija ir Tuning**

### **8.1. Performance Optimization:**
```bash
# 1. Increase worker processes (production)
# Redaguokite supervisord.conf:
[program:webserver]
command=gunicorn -w 4 -b 0.0.0.0:3000 main:app
numprocs=1

[program:admin_server]
command=gunicorn -w 2 -b 0.0.0.0:8000 admin_app:app
numprocs=1

# 2. Setup nginx reverse proxy (optional)
sudo apt install nginx
# Configure nginx proxy to supervisor processes
```

### **8.2. Memory Optimization:**
```bash
# 1. Configure Python memory management
export PYTHONMALLOC=malloc
export MALLOC_ARENA_MAX=2

# 2. Limit MoviePy memory usage
# Add to .env:
MOVIEPY_TEMP_DIR=./temp
IMAGEIO_FFMPEG_EXE=/usr/bin/ffmpeg
```

### **8.3. Security Hardening:**
```bash
# 1. Generate secure secret key
python -c "
import secrets
print('FLASK_SECRET_KEY=' + secrets.token_hex(32))
"
# Copy output į .env file

# 2. Set restrictive file permissions
chmod 600 .env
chmod 700 logs/
chmod 755 static/

# 3. Configure firewall (Linux)
sudo ufw allow 3000
sudo ufw allow 8000
sudo ufw enable
```

---

## 📊 **Žingsnis 9: Monitoring Setup**

### **9.1. Log Monitoring:**
```bash
# 1. Install log monitoring tools
pip install loguru

# 2. Setup log rotation
cat > /etc/logrotate.d/autonominis-muzikantas << 'EOF'
/path/to/your/project/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 user user
}
EOF

# 3. Real-time log monitoring
tail -f logs/*.log | grep -E "(ERROR|WARNING|CRITICAL)"
```

### **9.2. System Monitoring:**
```bash
# 1. Create monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash
echo "=== Autonominis Muzikantas Health Check ==="
echo "Timestamp: $(date)"
echo ""

# Check processes
echo "🔍 Process Status:"
supervisorctl -c supervisord.conf status

# Check disk usage
echo ""
echo "💾 Disk Usage:"
df -h | grep -E "(Filesystem|/$)"

# Check memory
echo ""  
echo "🧠 Memory Usage:"
free -h

# Check API connectivity
echo ""
echo "🌐 API Status:"
curl -s http://localhost:8000/api/system/status | head -n 1

echo ""
echo "==============================================="
EOF

chmod +x monitor.sh

# 2. Setup monitoring cron
(crontab -l 2>/dev/null; echo "*/5 * * * * /path/to/monitor.sh >> /var/log/autonominis-monitor.log") | crontab -
```

---

## 🚨 **Troubleshooting Guide**

### **Common Issues & Solutions:**

#### **1. Import Errors:**
```bash
# Problem: ModuleNotFoundError
# Solution:
source venv/bin/activate  # Ensure venv is activated
pip install -r requirements.txt
pip list | grep flask  # Verify installation
```

#### **2. API Key Errors:**
```bash
# Problem: Invalid API key responses
# Solution:
cat .env | grep -E "API_KEY"  # Check keys exist
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('SUNO_API_KEY:', os.getenv('SUNO_API_KEY')[:10] + '...')
"  # Test key loading
```

#### **3. Port Already in Use:**
```bash
# Problem: Port 3000/8000 already in use
# Solution:
# Linux/Mac:
lsof -i :3000
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

#### **4. Permission Errors:**
```bash
# Problem: Permission denied
# Solution:
chmod +x main.py admin_app.py
chmod 755 logs/ output/ temp/
chmod 644 *.py *.md
```

#### **5. Database Locked:**
```bash
# Problem: SQLite database locked
# Solution:
supervisorctl -c supervisord.conf stop all
rm -f *.db-lock
sqlite3 autonominis_muzikantas.db "PRAGMA integrity_check;"
supervisorctl -c supervisord.conf start all
```

#### **6. Memory Issues:**
```bash
# Problem: Out of memory during generation
# Solution:
# Increase swap space:
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Or reduce concurrent operations:
# Edit .env:
MAX_CONCURRENT_GENERATIONS=1
MOVIEPY_MEMORY_LIMIT=1GB
```

---

## 🔄 **Backup & Recovery**

### **Backup Setup:**
```bash
# 1. Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Database backup
cp *.db $BACKUP_DIR/

# Configuration backup  
cp .env $BACKUP_DIR/
cp supervisord.conf $BACKUP_DIR/

# Generated content backup
tar -czf $BACKUP_DIR/output.tar.gz output/

# Logs backup (last 7 days)
find logs/ -name "*.log" -mtime -7 -exec cp {} $BACKUP_DIR/ \;

echo "✅ Backup completed: $BACKUP_DIR"
EOF

chmod +x backup.sh

# 2. Setup automatic backups
(crontab -l 2>/dev/null; echo "0 2 * * * /path/to/backup.sh") | crontab -
```

### **Recovery Process:**
```bash
# 1. Stop services
supervisorctl -c supervisord.conf stop all

# 2. Restore from backup
BACKUP_DATE="20250913_140000"  # Replace with actual backup
cp backups/$BACKUP_DATE/*.db ./
cp backups/$BACKUP_DATE/.env ./
tar -xzf backups/$BACKUP_DATE/output.tar.gz

# 3. Restart services
supervisorctl -c supervisord.conf start all

# 4. Verify recovery
curl http://localhost:8000/api/system/status
```

---

## 🌐 **Network Configuration**

### **External Access Setup:**
```bash
# 1. Find your IP address
# Linux/Mac:
ip addr show | grep 'inet ' | grep -v 127.0.0.1
# Windows:
ipconfig | findstr IPv4

# 2. Configure firewall
# Linux (ufw):
sudo ufw allow from 192.168.1.0/24 to any port 3000
sudo ufw allow from 192.168.1.0/24 to any port 8000

# Windows Firewall:
# Add inbound rules for ports 3000, 8000

# 3. Update supervisor config for external access
# Edit supervisord.conf:
[program:webserver]
command=python main.py --host=0.0.0.0 --port=3000

[program:admin_server]
command=python admin_app.py --host=0.0.0.0 --port=8000
```

### **Reverse Proxy Setup (Optional):**
```bash
# 1. Install nginx
sudo apt install nginx  # Ubuntu/Debian
brew install nginx      # macOS

# 2. Configure nginx
sudo tee /etc/nginx/sites-available/autonominis-muzikantas << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /admin {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# 3. Enable site
sudo ln -s /etc/nginx/sites-available/autonominis-muzikantas /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## ✅ **Installation Verification Checklist**

### **Pre-Launch Checklist:**
```bash
# ✅ System Requirements
python --version  # >= 3.8
pip --version
git --version

# ✅ Project Files
ls -la | grep -E "(main.py|admin_app.py)"
ls -la | grep -E "(voice_cloning|trending|community)"

# ✅ Environment Configuration  
cat .env | grep -c "API_KEY"  # Should be >= 4
cat .env | grep FLASK_SECRET_KEY | wc -l  # Should be 1

# ✅ Dependencies
pip list | grep -E "(flask|requests|moviepy)" | wc -l  # Should be >= 3

# ✅ Database Setup
ls -la *.db | wc -l  # Should be >= 1

# ✅ Directory Structure
ls -la logs/ output/ temp/ static/  # All should exist

# ✅ Permissions
ls -la *.py | grep -E "rwxr--r--"  # Python files executable

# ✅ Services Running
curl -I http://localhost:3000  # Should return 200
curl -I http://localhost:8000  # Should return 200

# ✅ API Connectivity
curl http://localhost:8000/api/system/status  # Should return JSON

# ✅ Admin Access
# Login to http://localhost:8000 with admin/admin123

# ✅ Core Functionality
# Test music generation in admin interface
# Test voice character initialization
# Test trending monitoring activation
```

### **Success Indicators:**
- ✅ **Servers Running:** Both ports 3000 & 8000 responsive
- ✅ **Admin Login:** Successful login to dashboard
- ✅ **API Status:** All APIs showing "Connected" status
- ✅ **Music Generation:** Successful test generation
- ✅ **Diamond Systems:** All 3 systems initializing properly
- ✅ **No Critical Errors:** Clean logs without critical failures

---

## 🎉 **Post-Installation Steps**

### **1. API Credits Setup:**
- Suno AI: Add credits to account
- ElevenLabs: Upgrade to Pro plan ($22/month) for voice cloning
- YouTube API: Monitor quota usage

### **2. System Optimization:**
- Run first music generation test
- Initialize all voice characters
- Activate trending monitoring
- Configure community management

### **3. Production Deployment:**
- Setup SSL certificates (Let's Encrypt)
- Configure domain name
- Setup monitoring alerts
- Configure automatic backups

### **4. Scaling Preparation:**
- Monitor resource usage patterns
- Plan for increased API costs
- Setup analytics tracking
- Prepare for multi-channel expansion

---

**🚀 Installation Complete! Your AI Music Empire is ready to generate revenue!**

*For support, check the troubleshooting section or create a GitHub issue.*