# 🚀 VEIKSMU PLANAS PRODUKCIJAI

## ⚡ SKUBIAUSI VEIKSMAI (ŠIANDIEN - 1 DIENA)

### 1. BACKUP IR VERSIJŲ KONTROLĖ
```bash
# Sukurti pilną backup
cp -r /home/user/webapp /home/user/webapp_backup_$(date +%Y%m%d_%H%M%S)

# Inicializuoti Git (jei dar nėra)
cd /home/user/webapp
git init
git add .
git commit -m "Initial backup before production fixes"
```

### 2. PAŠALINTI TESTNIUS FAILUS
```bash
# Sukurti archyvą testiniams failams
mkdir -p /home/user/webapp/archive/tests
mkdir -p /home/user/webapp/archive/backup

# Perkelti visus test failus
mv test_*.py archive/tests/
mv debug_*.py archive/tests/
mv diagnose_*.py archive/tests/
mv direct_*.py archive/tests/
mv check_*.py archive/tests/
mv fix_*.py archive/tests/
mv final_*.py archive/tests/
mv setup_*.py archive/tests/
mv test_*.html archive/tests/

# Perkelti backup failus
mv admin_app_backup.py archive/backup/
mv admin_app_fixed.py archive/backup/
```

### 3. SUKURTI PRODUCTION .ENV
```bash
# Kopijuoti pavyzdį
cp .env.example .env

# Redaguoti .env failą ir įrašyti REALIUS API raktus
nano .env
```

**BŪTINI .ENV PARAMETRAI:**
```env
# PRODUCTION KONFIGŪRACIJA
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<sugeneruotas-32-simbolių-raktas>
ADMIN_PASSWORD=<hash'uotas-slaptažodis>

# API RAKTAI (įrašyti realius)
SUNO_API_KEY=your_real_suno_key_here
GEMINI_API_KEY=your_real_gemini_key_here
YOUTUBE_API_KEY=your_real_youtube_key_here
YOUTUBE_CLIENT_ID=your_real_client_id
YOUTUBE_CLIENT_SECRET=your_real_client_secret
YOUTUBE_CHANNEL_ID=your_real_channel_id

# DUOMENŲ BAZĖ
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

## 🔨 KRITINIAI PATAISYMAI (1-3 DIENOS)

### 4. PAKEISTI MOCK KLASES

**Sukurti naują failą:** `/core/services/implementations.py`
```python
# Laikinai paslėpti neveikiančius funkcionalumus
class DisabledFeature:
    def __init__(self, feature_name):
        self.feature_name = feature_name
    
    def __call__(self, *args, **kwargs):
        return {
            'success': False,
            'error': f'{self.feature_name} temporarily disabled for maintenance',
            'available': False
        }

# Pakeisti Mock klases su DisabledFeature
VoiceEmpire = DisabledFeature("Voice Empire")
TrendingHijacker = DisabledFeature("Trending Hijacker")
ChannelGenerator = DisabledFeature("Channel Generator")
```

### 5. PATAISYTI AUTENTIFIKACIJĄ

**Atnaujinti** `admin_app.py`:
```python
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Generuoti saugų slaptažodį
def generate_secure_password():
    return generate_password_hash(os.getenv('ADMIN_PASSWORD', 'change_me_now'))

# Pataisyti login funkciją (eilutė ~301)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        hashed = generate_secure_password()
        
        if check_password_hash(hashed, password):
            session['authenticated'] = True
            session['csrf_token'] = secrets.token_hex(16)
            return redirect(url_for('dashboard'))
```

### 6. PRIDĖTI CSRF APSAUGĄ

```python
# Pridėti CSRF validaciją
def validate_csrf(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            if not token or token != session.get('csrf_token'):
                return jsonify({'error': 'Invalid CSRF token'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Pritaikyti visiems POST/DELETE endpoints
@app.route('/api/generate/start', methods=['POST'])
@require_auth
@validate_csrf
def api_start_generation():
    # ...existing code...
```

### 7. SUJUNGTI DUBLIUOJANČIUS FAILUS

```bash
# Palikti tik vieną Suno Client versiją
mv core/services/suno_client.py core/services/suno_client_main.py
rm core/services/suno_client_enhanced.py
rm core/services/suno_client_updated.py
mv core/services/suno_client_main.py core/services/suno_client.py

# Palikti tik vieną Music Generator template
rm templates/music_generator_compact.html
# Palikti tik music_generator_simplified.html
```

### 8. PASLĖPTI NEVEIKIANČIUS MENIU

**Atnaujinti** `templates/admin_base.html`:
```html
<!-- Užkomentuoti arba pašalinti neveikiančius meniu -->
{% if False %}  <!-- Laikinai paslėpti -->
<li class="nav-item">
    <a class="nav-link" href="/voice-empire">
        <i class="fas fa-microphone"></i> Voice Empire
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" href="/trending-hijacker">
        <i class="fas fa-fire"></i> Trending Hijacker
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" href="/channel-generator">
        <i class="fas fa-tv"></i> Channel Generator
    </a>
</li>
{% endif %}
```

## 📊 DUOMENŲ BAZĖS MIGRACIJA (2-3 DIENOS)

### 9. MIGRUOTI Į POSTGRESQL

```bash
# Įdiegti PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Sukurti duomenų bazę
sudo -u postgres psql
CREATE DATABASE youtube_automation;
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE youtube_automation TO app_user;
\q

# Įdiegti Python dependencies
pip install psycopg2-binary
pip install alembic

# Inicializuoti Alembic migracijas
alembic init migrations
```

### 10. ATNAUJINTI MODELIUS

```python
# core/database/models.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Production database
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/dbname')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sukurti visas lenteles
Base.metadata.create_all(bind=engine)
```

## 🔒 SAUGUMO PATAISYMAI (3-4 DIENOS)

### 11. INPUT VALIDACIJA

```python
from flask import abort
import re

def validate_project_name(name):
    # Leisti tik saugius simbolius
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        abort(400, 'Invalid project name')
    return name

@app.route('/api/projects/<project_name>/delete', methods=['DELETE'])
@require_auth
@validate_csrf
def api_delete_project(project_name):
    project_name = validate_project_name(project_name)
    # ...existing code...
```

### 12. RATE LIMITING

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/generate/start', methods=['POST'])
@limiter.limit("5 per minute")
@require_auth
def api_start_generation():
    # ...existing code...
```

## 📝 LOGGING SISTEMA (2 DIENOS)

### 13. ĮDIEGTI LOGGING

```python
import logging
from logging.handlers import RotatingFileHandler

# Sukurti logs direktoriją
os.makedirs('logs', exist_ok=True)

# Konfigūruoti logging
if app.config['ENV'] == 'production':
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')
```

## 🚀 DEPLOYMENT (5 DIENA)

### 14. PRODUCTION SERVER SETUP

```bash
# Įdiegti Gunicorn
pip install gunicorn

# Sukurti systemd service
sudo nano /etc/systemd/system/webapp.service
```

**webapp.service turinys:**
```ini
[Unit]
Description=YouTube Automation Web App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/user/webapp
Environment="PATH=/home/user/webapp/venv/bin"
ExecStart=/home/user/webapp/venv/bin/gunicorn --workers 3 --bind unix:webapp.sock -m 007 admin_app:app

[Install]
WantedBy=multi-user.target
```

### 15. NGINX KONFIGŪRACIJA

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/webapp/webapp.sock;
    }

    location /static {
        alias /home/user/webapp/static;
    }
}
```

## ✅ CHECKLIST PRIEŠ PRODUKCIJĄ

- [ ] Visi test failai pašalinti
- [ ] Mock klasės pakeistos arba paslėptos
- [ ] .env failas su realiais API raktais
- [ ] Autentifikacija su password hashing
- [ ] CSRF apsauga įdiegta
- [ ] Input validacija visuose endpoints
- [ ] PostgreSQL duomenų bazė
- [ ] Rate limiting įdiegtas
- [ ] Logging sistema veikia
- [ ] SSL sertifikatas (Let's Encrypt)
- [ ] Backup strategija
- [ ] Monitoring (Sentry/NewRelic)
- [ ] Load testing atliktas
- [ ] Security audit atliktas
- [ ] Dokumentacija atnaujinta

## ⚠️ SVARBŪS PERSPĖJIMAI

1. **NIEKADA nepaleiskite produkcijos su:**
   - DEBUG=True
   - Default slaptažodžiais
   - SQLite duomenų baze
   - Mock klasėmis
   - Test failais

2. **VISADA turėkite:**
   - Backup prieš kiekvieną pakeitimą
   - Staging aplinką testavimui
   - Rollback planą
   - Monitoring ir alertus
   - Incident response planą

## 📞 PAGALBA

Jei reikia profesionalios pagalbos:
1. Pasamdyti Python/Flask developerį
2. Security auditoriaus konsultacija
3. DevOps specialisto pagalba deployment
4. Database administratoriaus pagalba migracijai

---
**SVARBU:** Šis planas yra MINIMALUS. Rekomenduoju rimtai apsvarstyti aplikacijos perrašymą nuo nulio su tinkama architektūra.

*Planas sudarytas: 2025-01-15*
*Numatoma trukmė: 2-3 savaitės intensyvaus darbo*