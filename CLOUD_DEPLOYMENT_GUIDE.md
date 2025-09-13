# 🌐 CLOUD DEPLOYMENT GUIDE - 24/7 AUTONOMOUS OPERATION

## 🎯 TIKSLAS: 
**Paleisti jūsų AI musik empire serverį cloud'e kad veiktų 24/7 be jūsų kompiuterio**

---

## 🚀 1. DIGITALOCEAN DEPLOYMENT (Rekomenduojama pradžiai)

### 💰 **Kaina:** ~$12/mėnesį
### ⚡ **Setup laikas:** 30-60 minučių

#### **Step 1: Sukurti DigitalOcean paskyrą**
```
🌐 Eiti į: digitalocean.com
💳 Užsiregistruoti (reikia kredito kortelės)
💵 Gauti $200 free credits naujiems vartotojams
```

#### **Step 2: Sukurti Droplet**
```bash
# Pasirinkti:
- Ubuntu 20.04 LTS
- Basic plan: $12/month (1 CPU, 2GB RAM, 50GB SSD)
- Region: Frankfurt arba Amsterdam (arčiau Lietuvos)
- SSH Key: sukurti naują arba import'inti
```

#### **Step 3: Prisijungti prie serverio**
```bash
# Nuo jūsų kompiuterio:
ssh root@YOUR_SERVER_IP

# Atnaujinti sistemą:
apt update && apt upgrade -y

# Įdiegti Python ir reikalingus packages:
apt install python3 python3-pip nginx supervisor git -y
```

#### **Step 4: Upload'inti projektą**
```bash
# 1 būdas: Git clone (rekomenduojama)
git clone https://github.com/christianza1989/ytai.git
cd ytai

# 2 būdas: SCP upload
# Nuo jūsų kompiuterio:
scp -r /path/to/your/webapp/ root@YOUR_SERVER_IP:/home/
```

#### **Step 5: Sukonfigūruoti environment**
```bash
# Serveryje:
cd /home/ytai  # arba /home/webapp
pip3 install -r requirements.txt

# Sukurti .env failą su jūsų API raktais:
nano .env
# Įdėti:
SUNO_API_KEY=your_real_suno_key
GEMINI_API_KEY=your_real_gemini_key
YOUTUBE_CHANNEL_ID=your_channel_id
```

#### **Step 6: Sukonfigūruoti Nginx (web server)**
```bash
# Sukurti nginx config:
nano /etc/nginx/sites-available/musicempire

# Įdėti:
server {
    listen 80;
    server_name YOUR_SERVER_IP;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Aktyvuoti config:
ln -s /etc/nginx/sites-available/musicempire /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

#### **Step 7: Sukonfigūruoti Supervisor (24/7 veikimas)**
```bash
# Sukurti supervisor config:
nano /etc/supervisor/conf.d/musicempire.conf

# Įdėti:
[program:musicempire_web]
command=python3 /home/ytai/web_launch.py
directory=/home/ytai
autostart=true
autorestart=true
user=root
environment=PYTHONPATH="/home/ytai"

[program:musicempire_autonomous]
command=python3 /home/ytai/autonomous_empire_24_7.py
directory=/home/ytai
autostart=true
autorestart=true
user=root
environment=PYTHONPATH="/home/ytai"

# Perkrauti supervisor:
supervisorctl reread
supervisorctl update
supervisorctl start all
```

#### **Step 8: Patikrinti veikimą**
```bash
# Patikrinti ar veikia:
supervisorctl status

# Turėtumėte matyti:
# musicempire_web         RUNNING
# musicempire_autonomous  RUNNING

# Patikrinti web interface:
curl http://localhost:8000
# Arba atidarykite naršyklėje: http://YOUR_SERVER_IP
```

---

## 🛡️ 2. AWS EC2 DEPLOYMENT (Profesionalus sprendimas)

### 💰 **Kaina:** ~$15-25/mėnesį
### 🔒 **Privalumai:** Aukštesnė kokybė, geresnė saugumas

#### **Step 1: AWS Setup**
```bash
# 1. Eiti į aws.amazon.com
# 2. Sukurti paskyrą (12 mėnesių free tier)
# 3. EC2 Dashboard → Launch Instance
```

#### **Step 2: EC2 Configuration**
```bash
# Pasirinkti:
- Amazon Linux 2 AMI arba Ubuntu 20.04
- Instance type: t3.small (2 vCPU, 2GB RAM)
- Storage: 20GB gp3
- Security Group: HTTP (80), HTTPS (443), SSH (22)
- Key Pair: sukurti naują
```

#### **Step 3: Setup procesas**
```bash
# Prisijungti:
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# Analogiškas setup kaip DigitalOcean
# Tik vietoj apt naudoti yum (Amazon Linux)
```

---

## 🔧 3. AUTOMATINIS DEPLOYMENT SCRIPT

### 📝 **Sukurkim deployment script'ą:**

```bash
#!/bin/bash
# auto_deploy.sh - Automatinis serverio setup

echo "🚀 AI Music Empire - Cloud Deployment"
echo "=================================="

# Update system
echo "📦 Updating system..."
apt update && apt upgrade -y

# Install dependencies
echo "🔧 Installing dependencies..."
apt install python3 python3-pip nginx supervisor git ffmpeg -y

# Clone project
echo "📥 Downloading project..."
git clone https://github.com/christianza1989/ytai.git /home/musicempire
cd /home/musicempire

# Install Python packages
echo "🐍 Installing Python packages..."
pip3 install -r requirements.txt

# Setup environment
echo "⚙️ Setting up environment..."
cp .env.example .env
echo "✏️  Edit /home/musicempire/.env with your API keys!"

# Setup Nginx
echo "🌐 Configuring Nginx..."
cat > /etc/nginx/sites-available/musicempire << EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

ln -s /etc/nginx/sites-available/musicempire /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# Setup Supervisor
echo "🔄 Setting up 24/7 service..."
cat > /etc/supervisor/conf.d/musicempire.conf << EOF
[program:musicempire_web]
command=python3 /home/musicempire/web_launch.py
directory=/home/musicempire
autostart=true
autorestart=true
user=root
environment=PYTHONPATH="/home/musicempire"
stdout_logfile=/var/log/musicempire_web.log
stderr_logfile=/var/log/musicempire_web_error.log

[program:musicempire_autonomous]
command=python3 /home/musicempire/autonomous_empire_24_7.py
directory=/home/musicempire
autostart=true
autorestart=true
user=root
environment=PYTHONPATH="/home/musicempire"
stdout_logfile=/var/log/musicempire_auto.log
stderr_logfile=/var/log/musicempire_auto_error.log
EOF

supervisorctl reread && supervisorctl update

echo "✅ Deployment completed!"
echo "🌐 Access your empire at: http://$(curl -s ifconfig.me)"
echo "🔑 Login: admin123"
echo "⚙️ Don't forget to edit /home/musicempire/.env with your API keys!"
echo "📊 Check status: supervisorctl status"
```

---

## 💡 4. PAPILDOMI PATARIMAI

### 🔐 **SSL Sertifikatas (HTTPS):**
```bash
# Let's Encrypt (nemokamas SSL):
apt install certbot python3-certbot-nginx
certbot --nginx -d yourdomain.com
```

### 📊 **Monitoring:**
```bash
# Patikrinti sistemos statusą:
supervisorctl status
top
df -h
free -m

# Logų peržiūra:
tail -f /var/log/musicempire_web.log
tail -f /var/log/musicempire_auto.log
```

### 💾 **Backup strategija:**
```bash
# Automatinis backup script:
#!/bin/bash
tar -czf backup_$(date +%Y%m%d).tar.gz /home/musicempire
# Upload to cloud storage
```

### 🚨 **Troubleshooting:**
```bash
# Jei kažkas neveikia:
systemctl status nginx
supervisorctl status
journalctl -f

# Restart visų:
systemctl restart nginx
supervisorctl restart all
```

---

## 📋 5. QUICKSTART CHECKLIST

### ✅ **Prieš deployment:**
- [ ] Turėti API raktus (Suno, Gemini)
- [ ] Sukurti cloud paskyrą
- [ ] Turėti SSH raktus
- [ ] Backup'inti lokalius duomenis

### ✅ **Po deployment:**
- [ ] Sukonfigūruoti .env failą
- [ ] Patikrinti web interface veikimą
- [ ] Sukonfigūruoti 10 YouTube kanalų
- [ ] Paleisti autonomous režimą
- [ ] Nustatyti monitoring

### ✅ **Reguliari priežiūra:**
- [ ] Tikrinti logs kas savaitę
- [ ] Backup'inti duomenis
- [ ] Atnaujinti API raktus jei reikia
- [ ] Stebėti server resources

---

## 🎯 REZULTATAS:

**Po šio setup jūsų AI Music Empire veiks 24/7:**
- ✅ Automatiškai generuos muziką
- ✅ Kels video į YouTube kanalus  
- ✅ Optimizuos performance
- ✅ Generuos pajamas net miegant
- ✅ Veiks be jūsų kompiuterio

**💰 Investicija:** $10-25/mėnesį  
**💎 Rezultatas:** $1000-20000+/mėnesį passive income!

---

**🚀 AR NORITE PRADĖTI DEPLOYMENT DABAR?**