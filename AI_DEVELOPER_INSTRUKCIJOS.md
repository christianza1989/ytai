# 🤖 AI DEVELOPER INSTRUKCIJOS - PROJEKTO TAISYMAS

## 📋 UŽDUOTIES APŽVALGA

Sveiki! Jūs esate AI Developer, kuris turi sutaisyti šį "Autonominis Muzikantas" projektą, kad jis veiktų produkcijai. Projektas šiuo metu turi daug Mock klasių ir saugumo spragų. Jūsų užduotis - padaryti, kad **CORE FUNKCIONALUMAS VEIKTŲ 100%**.

## 🎯 PAGRINDINIS TIKSLAS

Padaryti veikiantį muzikos generavimo ir publikavimo pipeline:
1. **Muzikos generavimas** → Suno API
2. **Saugojimas į Gallery** → Music Gallery
3. **Video kūrimas** → Su cover image
4. **Upload į YouTube** → Per YouTube API

## ⚠️ KĄ PALIKTI KAIP MOCK (kol kas netaisyti)

Šias funkcijas **PALIKITE kaip Mock klases** (jos nėra prioritetas):
- Voice Empire
- Trending Hijacker  
- Channel Generator
- Analytics (palikti demo duomenis)

## 🔧 KĄ BŪTINA SUTAISYTI

### 1. KRITINĖS SAUGUMO SPRAGOS (Pirmas prioritetas!)

#### A. Autentifikacija (admin_app.py ~301 eilutė)
**PROBLEMA:** Slaptažodis tikrinamas plain text
```python
# BLOGAI - dabar yra taip:
if password == admin_password:
```

**SPRENDIMAS:**
```python
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Startup metu:
ADMIN_PASSWORD_HASH = generate_password_hash(os.getenv('ADMIN_PASSWORD', 'change_me_now'))

# Login funkcijoje:
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['authenticated'] = True
            session['csrf_token'] = secrets.token_hex(16)
            session['user_id'] = 'admin'
            return redirect(url_for('dashboard'))
        flash('Invalid password', 'error')
    return render_template('login.html')
```

#### B. CSRF Protection
**Pridėti į visus POST/DELETE endpoints:**
```python
def validate_csrf(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'DELETE', 'PUT']:
            token = request.form.get('csrf_token') or \
                   request.headers.get('X-CSRF-Token') or \
                   request.args.get('csrf_token')
            if not token or token != session.get('csrf_token'):
                return jsonify({'error': 'Invalid CSRF token'}), 403
        return f(*args, **kwargs)
    return decorated_function
```

#### C. Input Validation
**Pridėti validaciją visiems user inputs:**
```python
import re
from flask import abort

def validate_safe_string(value, pattern=r'^[a-zA-Z0-9_\-\s]+$', max_length=100):
    if not value or len(value) > max_length:
        abort(400, 'Invalid input length')
    if not re.match(pattern, value):
        abort(400, 'Invalid characters in input')
    return value

def validate_project_name(name):
    return validate_safe_string(name, r'^[a-zA-Z0-9_\-]+$', 50)
```

### 2. PAŠALINTI/ARCHYVUOTI TEST FAILUS

**Sukurti archive direktoriją ir perkelti:**
```bash
mkdir -p archive/tests archive/backup archive/old_docs

# Perkelti visus test failus
mv test_*.py debug_*.py diagnose_*.py direct_*.py check_*.py fix_*.py final_*.py setup_*.py archive/tests/
mv test_*.html archive/tests/

# Perkelti backup failus  
mv admin_app_backup.py admin_app_fixed.py archive/backup/

# Perkelti senus dokumentus
mv STABLE_V2_README.md MUSIC_QUEUE_SUMMARY.md archive/old_docs/
```

### 3. SUJUNGTI DUBLIUOJANČIUS KOMPONENTUS

#### A. Suno Client (SVARBU!)
**PROBLEMA:** Yra 3 versijos - `suno_client.py`, `suno_client_enhanced.py`, `suno_client_updated.py`

**SPRENDIMAS:** Palikti TIK `suno_client.py` su geriausiais features iš visų:
```python
# core/services/suno_client.py - GALUTINĖ VERSIJA
import os
import requests
import json
import time
from typing import Dict, Optional, List, Any
from datetime import datetime

class SunoClient:
    """Unified Suno API client - PRODUCTION VERSION"""
    
    def __init__(self):
        self.api_key = os.getenv('SUNO_API_KEY')
        if not self.api_key or self.api_key == 'your_suno_api_key_here':
            raise ValueError("Valid SUNO_API_KEY required in .env file")
            
        self.base_url = "https://api.sunoapi.org/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_credits(self) -> int:
        """Get remaining credits"""
        try:
            response = requests.get(
                f"{self.base_url}/generate/credit",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get('data', 0) if data.get('code') == 200 else 0
        except Exception as e:
            print(f"Error getting credits: {e}")
            return 0
    
    def generate_music(self, title: str, style: str, lyrics: str = None, 
                      instrumental: bool = False) -> Dict:
        """Generate music with Suno API"""
        try:
            payload = {
                "model": os.getenv('SUNO_MODEL', 'V4'),
                "prompt": f"{style}. Title: {title}",
                "custom": True,
                "instrumental": instrumental
            }
            
            if lyrics and not instrumental:
                payload["lyrics"] = lyrics
                
            response = requests.post(
                f"{self.base_url}/generate",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_generation_status(self, task_id: str) -> Dict:
        """Check generation status"""
        try:
            response = requests.get(
                f"{self.base_url}/generate/{task_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'success': False, 'error': str(e)}
```

**Pašalinti kitus failus:**
```bash
rm core/services/suno_client_enhanced.py
rm core/services/suno_client_updated.py
```

#### B. Music Generator Templates
**Palikti TIK:** `music_generator_simplified.html`
**Pašalinti:** `music_generator_compact.html`

### 4. IMPLEMENTUOTI CORE FUNKCIONALUMĄ

#### A. Music Generation Pipeline (admin_app.py)
**Pakeisti Mock implementation į realią:**

```python
@app.route('/api/generate/start', methods=['POST'])
@require_auth
@validate_csrf
def api_start_generation():
    """Start REAL music generation"""
    data = request.get_json()
    
    # Validate inputs
    title = validate_safe_string(data.get('title', ''), max_length=100)
    style = validate_safe_string(data.get('style', ''), max_length=200)
    lyrics = data.get('lyrics', '')  # Lyrics can have special chars
    instrumental = data.get('instrumental', False)
    
    task_id = f"task_{int(time.time())}_{secrets.token_hex(4)}"
    
    # Create task
    task_data = {
        'id': task_id,
        'status': 'starting',
        'progress': 0,
        'title': title,
        'style': style,
        'created_at': datetime.now().isoformat(),
        'result': None
    }
    
    system_state.add_generation_task(task_id, task_data)
    
    # Start REAL generation in background
    def run_real_generation():
        try:
            # 1. Update status
            system_state.update_generation_task(task_id, {
                'status': 'generating',
                'progress': 10,
                'current_step': 'Initializing Suno API...'
            })
            
            # 2. Generate with Suno
            suno = SunoClient()
            result = suno.generate_music(
                title=title,
                style=style,
                lyrics=lyrics,
                instrumental=instrumental
            )
            
            if not result.get('success', False):
                raise Exception(result.get('error', 'Generation failed'))
            
            suno_task_id = result.get('task_id')
            
            # 3. Poll for completion
            system_state.update_generation_task(task_id, {
                'progress': 30,
                'current_step': 'Generating music...'
            })
            
            # Wait for generation (poll every 5 seconds, max 5 minutes)
            for i in range(60):
                time.sleep(5)
                status = suno.get_generation_status(suno_task_id)
                
                if status.get('status') == 'completed':
                    # 4. Save to Music Gallery
                    music_data = save_to_gallery(status.get('data'))
                    
                    system_state.update_generation_task(task_id, {
                        'status': 'completed',
                        'progress': 100,
                        'result': music_data
                    })
                    return
                    
                elif status.get('status') == 'failed':
                    raise Exception('Suno generation failed')
                    
                # Update progress
                progress = min(30 + i, 90)
                system_state.update_generation_task(task_id, {
                    'progress': progress
                })
            
            raise Exception('Generation timeout')
            
        except Exception as e:
            system_state.update_generation_task(task_id, {
                'status': 'failed',
                'error': str(e)
            })
    
    # Start thread
    thread = threading.Thread(target=run_real_generation)
    thread.daemon = True
    thread.start()
    
    return jsonify({'task_id': task_id, 'status': 'started'})
```

#### B. Music Gallery Storage
**Implementuoti `save_to_gallery` funkciją:**

```python
def save_to_gallery(music_data: Dict) -> Dict:
    """Save generated music to gallery"""
    try:
        # Create output directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_name = f"music_{timestamp}"
        output_dir = Path('output') / project_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Download audio files
        audio_urls = music_data.get('audio_urls', [])
        saved_files = []
        
        for i, url in enumerate(audio_urls):
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            file_path = output_dir / f"track_{i+1}.mp3"
            with open(file_path, 'wb') as f:
                f.write(response.content)
            saved_files.append(str(file_path))
        
        # Save metadata
        metadata = {
            'id': project_name,
            'title': music_data.get('title'),
            'style': music_data.get('style'),
            'created_at': datetime.now().isoformat(),
            'files': saved_files,
            'suno_data': music_data
        }
        
        with open(output_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update gallery database
        update_gallery_database(metadata)
        
        return metadata
        
    except Exception as e:
        print(f"Error saving to gallery: {e}")
        raise

def update_gallery_database(metadata: Dict):
    """Update music gallery database"""
    gallery_file = Path('data/music_gallery.json')
    gallery_file.parent.mkdir(exist_ok=True)
    
    # Load existing
    gallery = []
    if gallery_file.exists():
        try:
            with open(gallery_file) as f:
                gallery = json.load(f)
        except:
            gallery = []
    
    # Add new entry
    gallery.append({
        'id': metadata['id'],
        'title': metadata['title'],
        'style': metadata['style'],
        'created_at': metadata['created_at'],
        'files': metadata['files']
    })
    
    # Save (keep last 100 entries)
    gallery = gallery[-100:]
    with open(gallery_file, 'w') as f:
        json.dump(gallery, f, indent=2)
```

#### C. Video Creation from Music
**Implementuoti video kūrimą su cover image:**

```python
@app.route('/api/create-video', methods=['POST'])
@require_auth
@validate_csrf
def api_create_video():
    """Create video from music with cover image"""
    data = request.get_json()
    
    music_id = validate_safe_string(data.get('music_id'))
    
    # Load music metadata
    metadata_path = Path('output') / music_id / 'metadata.json'
    if not metadata_path.exists():
        return jsonify({'error': 'Music not found'}), 404
    
    with open(metadata_path) as f:
        metadata = json.load(f)
    
    # Generate cover image
    from core.services.image_client import ImageClient
    image_client = ImageClient()
    
    cover_prompt = f"Album cover for {metadata['title']}, style: {metadata['style']}"
    cover_result = image_client.generate_image(cover_prompt)
    
    if cover_result.get('success'):
        cover_path = Path('output') / music_id / 'cover.jpg'
        # Download and save cover
        response = requests.get(cover_result['url'])
        with open(cover_path, 'wb') as f:
            f.write(response.content)
        
        # Create simple video (static image + audio)
        create_music_video(
            audio_path=metadata['files'][0],
            image_path=str(cover_path),
            output_path=str(Path('output') / music_id / 'video.mp4')
        )
        
        return jsonify({
            'success': True,
            'video_path': f"output/{music_id}/video.mp4"
        })
    
    return jsonify({'error': 'Cover generation failed'}), 500

def create_music_video(audio_path: str, image_path: str, output_path: str):
    """Create video from audio and image using ffmpeg"""
    import subprocess
    
    cmd = [
        'ffmpeg', '-loop', '1',
        '-i', image_path,
        '-i', audio_path,
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        output_path
    ]
    
    subprocess.run(cmd, check=True)
```

#### D. YouTube Upload
**Implementuoti YouTube upload funkciją:**

```python
@app.route('/api/upload-youtube', methods=['POST'])
@require_auth
@validate_csrf
def api_upload_youtube():
    """Upload video to YouTube"""
    data = request.get_json()
    
    music_id = validate_safe_string(data.get('music_id'))
    video_path = Path('output') / music_id / 'video.mp4'
    
    if not video_path.exists():
        return jsonify({'error': 'Video not found'}), 404
    
    # Load metadata
    with open(Path('output') / music_id / 'metadata.json') as f:
        metadata = json.load(f)
    
    # Upload to YouTube
    from core.youtube_api_client import YouTubeAPIClient
    youtube = YouTubeAPIClient()
    
    result = youtube.upload_video(
        video_path=str(video_path),
        title=metadata['title'],
        description=f"Generated music: {metadata['style']}",
        tags=['ai-music', 'generated'],
        category='10'  # Music category
    )
    
    if result.get('success'):
        # Save YouTube URL
        metadata['youtube_url'] = result['url']
        metadata['youtube_id'] = result['video_id']
        with open(Path('output') / music_id / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return jsonify(result)
    
    return jsonify({'error': result.get('error')}), 500
```

### 5. ENVIRONMENT KONFIGŪRACIJA

**.env failas (BŪTINA užpildyti realiais raktais):**
```env
# SECURITY
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-generated-32-char-secret-key-here
ADMIN_PASSWORD=your-secure-admin-password

# SUNO API (BŪTINA!)
SUNO_API_KEY=your-real-suno-api-key
SUNO_MODEL=V4

# GEMINI API (BŪTINA!)
GEMINI_API_KEY=your-real-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash-exp

# YOUTUBE API (BŪTINA!)
YOUTUBE_API_KEY=your-real-youtube-api-key
YOUTUBE_CLIENT_ID=your-oauth-client-id
YOUTUBE_CLIENT_SECRET=your-oauth-client-secret
YOUTUBE_CHANNEL_ID=your-channel-id

# IMAGE API (Optional)
IDEOGRAM_API_KEY=your-ideogram-key

# DATABASE
DATABASE_URL=sqlite:///youtube_automation.db
```

### 6. DEPENDENCIES ATNAUJINIMAS

**requirements.txt:**
```txt
Flask==2.3.3
Flask-Session==0.5.0
Flask-Limiter==3.5.0
python-dotenv==1.0.0
requests==2.31.0
Pillow==10.0.0
werkzeug==2.3.7
SQLAlchemy==2.0.21
psycopg2-binary==2.9.7
gunicorn==21.2.0
google-api-python-client==2.100.0
google-auth==2.23.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
ffmpeg-python==0.2.0
```

### 7. FRONTEND PATAISYMAI

#### A. Music Gallery (templates/music_gallery.html)
**Pridėti REALŲ gallery load:**
```javascript
async function loadGallery() {
    try {
        const response = await fetch('/api/gallery/list');
        const data = await response.json();
        
        const container = document.getElementById('gallery-container');
        container.innerHTML = '';
        
        data.items.forEach(item => {
            const card = createMusicCard(item);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading gallery:', error);
    }
}

function createMusicCard(item) {
    const card = document.createElement('div');
    card.className = 'col-md-4 mb-4';
    card.innerHTML = `
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">${item.title}</h5>
                <p class="card-text">Style: ${item.style}</p>
                <p class="text-muted">${item.created_at}</p>
                <audio controls class="w-100 mb-2">
                    <source src="${item.files[0]}" type="audio/mpeg">
                </audio>
                <button class="btn btn-primary btn-sm" onclick="createVideo('${item.id}')">
                    Create Video
                </button>
                <button class="btn btn-success btn-sm" onclick="uploadYouTube('${item.id}')">
                    Upload to YouTube
                </button>
            </div>
        </div>
    `;
    return card;
}
```

#### B. Paslėpti Mock meniu (templates/admin_base.html)
```html
<!-- Užkomentuoti šiuos meniu punktus -->
<!-- 
<li class="nav-item">
    <a class="nav-link" href="/voice-empire">Voice Empire</a>
</li>
<li class="nav-item">
    <a class="nav-link" href="/trending-hijacker">Trending Hijacker</a>
</li>
<li class="nav-item">
    <a class="nav-link" href="/channel-generator">Channel Generator</a>
</li>
-->
```

### 8. TESTAVIMO PLANAS

#### Step 1: Test Suno API
```python
# test_suno.py
from core.services.suno_client import SunoClient

client = SunoClient()
print(f"Credits: {client.get_credits()}")

result = client.generate_music(
    title="Test Song",
    style="Electronic ambient",
    instrumental=True
)
print(f"Generation result: {result}")
```

#### Step 2: Test Full Pipeline
1. Login į admin panel
2. Eiti į Music Generator
3. Sugeneruoti muziką
4. Patikrinti ar atsiranda Music Gallery
5. Sukurti video
6. Upload į YouTube

### 9. PRODUCTION DEPLOYMENT

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations (if using PostgreSQL)
alembic upgrade head

# Test locally
python admin_app.py

# Production with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 admin_app:app
```

## ✅ CHECKLIST

- [ ] Pašalinti visus test failus į archive/
- [ ] Sutaisyti autentifikaciją (password hashing)
- [ ] Pridėti CSRF protection
- [ ] Pridėti input validation
- [ ] Sujungti Suno Client versijas į vieną
- [ ] Pašalinti dubliuojančius templates
- [ ] Implementuoti REAL music generation
- [ ] Implementuoti save_to_gallery
- [ ] Implementuoti video creation
- [ ] Implementuoti YouTube upload
- [ ] Užpildyti .env su realiais API keys
- [ ] Paslėpti Mock meniu punktus
- [ ] Testuoti pilną pipeline
- [ ] Deployment į production serverį

## 🎯 REZULTATAS

Po šių pakeitimų turėsite:
1. ✅ Veikiantį muzikos generavimą per Suno API
2. ✅ Music Gallery su realiais failais
3. ✅ Video kūrimą iš muzikos
4. ✅ YouTube upload funkcionalumą
5. ✅ Saugią autentifikaciją
6. ✅ CSRF apsaugą
7. ✅ Input validaciją

## ⚠️ SVARBU

1. **TESTUOKITE lokaliai** prieš deployment
2. **Darykite BACKUP** prieš kiekvieną pakeitimą
3. **Naudokite Git** versijavimui
4. **Dokumentuokite** pakeitimus
5. **Monitoruokite** logs produkcijai

## 📞 PAGALBOS KONTAKTAI

Jei kažkas neaišku:
1. Peržiūrėkite `PILNAS_AUDITO_ATASKAITA.md` - ten visos problemos
2. Sekite `VEIKSMU_PLANAS_PRODUKCIJAI.md` - ten žingsnis po žingsnio
3. Testuokite mažais žingsniais
4. Commit'inkite dažnai į Git

---
**SĖKMĖS!** 🚀

*Instrukcijos parengtos: 2025-01-15*
*Numatoma trukmė: 3-5 dienos intensyvaus darbo*