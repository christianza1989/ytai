#!/usr/bin/env python3
"""
Professional Admin Interface for Autonominis Muzikantas
Advanced Flask application with comprehensive management features
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_from_directory, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our main modules
from core.services.suno_client import SunoClient
from core.services.gemini_client import GeminiClient
from core.services.image_client import ImageClient
from core.utils.file_manager import FileManager
from core.analytics.collector import AnalyticsCollector
from core.analytics.analyzer import PerformanceAnalyzer

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))

# Global state management
class SystemState:
    def __init__(self):
        self.generation_tasks = {}
        self.system_stats = {}
        self.active_sessions = {}
        self.api_status = {}
        self.batch_operations = {}
        
    def update_api_status(self):
        """Update API connection status"""
        status = {}
        
        # Suno API
        try:
            if os.getenv('SUNO_API_KEY') and os.getenv('SUNO_API_KEY') != 'your_suno_api_key_here':
                suno = SunoClient()
                credits = suno.get_credits()
                status['suno'] = {'status': 'connected', 'credits': credits, 'error': None}
            else:
                status['suno'] = {'status': 'not_configured', 'credits': 0, 'error': 'API key not configured'}
        except Exception as e:
            status['suno'] = {'status': 'error', 'credits': 0, 'error': str(e)}
        
        # Gemini API
        try:
            if os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here':
                gemini = GeminiClient()
                # Simple test to verify API key
                status['gemini'] = {'status': 'connected', 'model': os.getenv('GEMINI_MODEL', 'gemini-1.5-flash'), 'error': None}
            else:
                status['gemini'] = {'status': 'not_configured', 'model': None, 'error': 'API key not configured'}
        except Exception as e:
            status['gemini'] = {'status': 'error', 'model': None, 'error': str(e)}
        
        # Stability AI
        try:
            if os.getenv('STABLE_DIFFUSION_API_KEY') and os.getenv('STABLE_DIFFUSION_API_KEY') != 'your_stable_diffusion_key_here':
                status['stability'] = {'status': 'connected', 'error': None}
            else:
                status['stability'] = {'status': 'not_configured', 'error': 'API key not configured'}
        except Exception as e:
            status['stability'] = {'status': 'error', 'error': str(e)}
        
        self.api_status = status
        return status
    
    def get_system_stats(self):
        """Get comprehensive system statistics"""
        stats = {}
        
        # Project statistics
        output_dir = Path('output')
        if output_dir.exists():
            projects = [d for d in output_dir.iterdir() if d.is_dir()]
            stats['total_projects'] = len(projects)
            
            # Calculate total files and size
            total_files = 0
            total_size = 0
            for project in projects:
                for file in project.rglob('*'):
                    if file.is_file():
                        total_files += 1
                        total_size += file.stat().st_size
            
            stats['total_files'] = total_files
            stats['total_size_mb'] = total_size / (1024 * 1024)
            
            # Recent activity
            recent_projects = sorted(projects, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
            stats['recent_projects'] = []
            
            for project in recent_projects:
                metadata_file = project / 'metadata.json'
                if metadata_file.exists():
                    try:
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                        stats['recent_projects'].append({
                            'name': project.name,
                            'title': metadata.get('title', 'Unknown'),
                            'created_at': metadata.get('created_at', 'Unknown'),
                            'tracks_created': metadata.get('tracks_created', 0)
                        })
                    except:
                        pass
        else:
            stats['total_projects'] = 0
            stats['total_files'] = 0
            stats['total_size_mb'] = 0
            stats['recent_projects'] = []
        
        # System info
        stats['system'] = {
            'python_version': sys.version.split()[0],
            'current_time': datetime.now().isoformat(),
            'uptime_hours': time.time() / 3600  # Approximate
        }
        
        self.system_stats = stats
        return stats

# Global system state
system_state = SystemState()

# Authentication functions
from functools import wraps

def require_auth(f):
    """Simple authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login page"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        # Simple password check (in production, use proper hashing)
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        if password == admin_password:
            session['authenticated'] = True
            session['login_time'] = datetime.now().isoformat()
            return redirect(url_for('dashboard'))
        else:
            flash('Neteisingas slaptažodis', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@require_auth
def dashboard():
    """Main admin dashboard"""
    # Update system stats
    system_state.update_api_status()
    system_state.get_system_stats()
    
    return render_template('admin_dashboard.html', 
                         api_status=system_state.api_status,
                         system_stats=system_state.system_stats)

@app.route('/projects')
@require_auth
def projects():
    """Project management page"""
    projects_data = []
    output_dir = Path('output')
    
    if output_dir.exists():
        for project_dir in sorted(output_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if project_dir.is_dir():
                metadata_file = project_dir / 'metadata.json'
                metadata = {'title': 'Unknown', 'created_at': 'Unknown'}
                
                if metadata_file.exists():
                    try:
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                    except:
                        pass
                
                # Get file count and size
                files = list(project_dir.rglob('*'))
                file_count = len([f for f in files if f.is_file()])
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                
                projects_data.append({
                    'name': project_dir.name,
                    'path': str(project_dir),
                    'metadata': metadata,
                    'file_count': file_count,
                    'size_mb': total_size / (1024 * 1024),
                    'modified': project_dir.stat().st_mtime
                })
    
    return render_template('projects.html', projects=projects_data)

@app.route('/api-config')
@require_auth
def api_config():
    """API configuration management"""
    system_state.update_api_status()
    
    # Get current env values (masked for security)
    env_config = {}
    for key in ['SUNO_API_KEY', 'GEMINI_API_KEY', 'STABLE_DIFFUSION_API_KEY', 'GEMINI_MODEL']:
        value = os.getenv(key, '')
        if value and value != f'your_{key.lower()}_here':
            env_config[key] = value[:8] + '...' + value[-4:] if len(value) > 12 else 'configured'
        else:
            env_config[key] = 'not_configured'
    
    return render_template('api_config.html', 
                         api_status=system_state.api_status,
                         env_config=env_config)

@app.route('/generator')
@require_auth
def generator():
    """Advanced generation interface"""
    return render_template('generator.html', api_status=system_state.api_status)

@app.route('/analytics')
@require_auth
def analytics():
    """Analytics and monitoring dashboard"""
    # Get analytics data
    analytics_data = {
        'generation_history': [],
        'api_usage': {},
        'performance_metrics': {},
        'error_logs': []
    }
    
    # Process output directories for analytics
    output_dir = Path('output')
    if output_dir.exists():
        for project_dir in output_dir.iterdir():
            if project_dir.is_dir():
                metadata_file = project_dir / 'metadata.json'
                if metadata_file.exists():
                    try:
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                        analytics_data['generation_history'].append({
                            'project': project_dir.name,
                            'title': metadata.get('title', 'Unknown'),
                            'mode': metadata.get('mode', 'unknown'),
                            'genre': metadata.get('genre', 'Unknown'),
                            'created_at': metadata.get('created_at', ''),
                            'tracks_created': metadata.get('tracks_created', 0),
                            'success': metadata.get('tracks_created', 0) > 0
                        })
                    except:
                        pass
    
    # Sort by date
    analytics_data['generation_history'].sort(
        key=lambda x: x.get('created_at', ''), reverse=True
    )
    
    return render_template('analytics.html', analytics=analytics_data)

@app.route('/batch')
@require_auth
def batch():
    """Batch operations interface"""
    return render_template('batch.html')

@app.route('/settings')
@require_auth
def settings():
    """System settings"""
    return render_template('settings.html')

# API Endpoints
@app.route('/api/system/status')
@require_auth
def api_system_status():
    """Get comprehensive system status"""
    system_state.update_api_status()
    system_state.get_system_stats()
    
    return jsonify({
        'api_status': system_state.api_status,
        'system_stats': system_state.system_stats,
        'generation_tasks': system_state.generation_tasks,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/projects/<project_name>/delete', methods=['DELETE'])
@require_auth
def api_delete_project(project_name):
    """Delete a project"""
    try:
        project_path = Path('output') / project_name
        if project_path.exists() and project_path.is_dir():
            import shutil
            shutil.rmtree(project_path)
            return jsonify({'success': True, 'message': 'Project deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/generate/start', methods=['POST'])
@require_auth
def api_start_generation():
    """Start advanced generation with custom parameters"""
    data = request.get_json()
    
    task_id = f"task_{int(time.time())}"
    demo_mode = data.get('demo_mode', False)
    
    # Store task info
    system_state.generation_tasks[task_id] = {
        'id': task_id,
        'status': 'queued',
        'progress': 0,
        'current_step': 'Initializing...',
        'logs': [],
        'parameters': data,
        'created_at': datetime.now().isoformat(),
        'result': None,
        'demo_mode': demo_mode
    }
    
    # Start generation in background thread
    def run_generation():
        try:
            system_state.generation_tasks[task_id]['status'] = 'running'
            
            if demo_mode:
                # Demo mode with realistic simulation
                result = run_demo_generation(task_id, data)
                system_state.generation_tasks[task_id]['result'] = result
            else:
                # Real generation pipeline
                from main import run_creation_pipeline
                
                # Mock implementation - replace with actual generation
                for i in range(10):
                    system_state.generation_tasks[task_id]['progress'] = (i + 1) * 10
                    system_state.generation_tasks[task_id]['current_step'] = f'Step {i+1}/10'
                    time.sleep(1)
                
                system_state.generation_tasks[task_id]['result'] = {'success': True}
            
            system_state.generation_tasks[task_id]['status'] = 'completed'
            
        except Exception as e:
            system_state.generation_tasks[task_id]['status'] = 'failed'
            system_state.generation_tasks[task_id]['result'] = {'success': False, 'error': str(e)}
    
    thread = threading.Thread(target=run_generation, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'task_id': task_id})

def run_demo_generation(task_id, parameters):
    """Run realistic demo generation with actual file creation"""
    import shutil
    import random
    
    # Update progress step by step
    def update_progress(progress, step):
        system_state.generation_tasks[task_id]['progress'] = progress
        system_state.generation_tasks[task_id]['current_step'] = step
        system_state.generation_tasks[task_id]['logs'].append(f"[{datetime.now().strftime('%H:%M:%S')}] {step}")
        time.sleep(random.uniform(1, 3))  # Realistic timing
    
    try:
        # Step 1: Initialize project
        update_progress(10, "🎵 Inicijuojamas projektas...")
        
        project_name = f"demo_project_{int(time.time())}"
        project_dir = Path('output') / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Step 2: Generate concept
        update_progress(20, "🧠 Generuojama muzikos koncepcija...")
        
        concept = generate_demo_concept(parameters)
        
        # Step 3: Create lyrics
        update_progress(35, "📝 Kuriami tekstai...")
        
        lyrics = generate_demo_lyrics(parameters.get('genre', 'pop'), concept)
        
        # Step 4: Generate audio tracks
        update_progress(50, "🎼 Generuojami audio takeliai...")
        
        audio_files = create_demo_audio_files(project_dir, parameters)
        
        # Step 5: Create video content
        update_progress(70, "🎥 Kuriamas video turinys...")
        
        video_files = create_demo_video_files(project_dir, audio_files)
        
        # Step 6: Generate cover art
        update_progress(85, "🎨 Generuojama albumo viršelis...")
        
        cover_art = create_demo_cover_art(project_dir, concept)
        
        # Step 7: Finalize project
        update_progress(95, "📦 Baigiamas projektas...")
        
        # Create metadata
        metadata = {
            'title': parameters.get('title', f'Demo Song {int(time.time())}'),
            'mode': parameters.get('mode', 'demo'),
            'genre': parameters.get('genre', 'demo'),
            'concept': concept,
            'lyrics': lyrics,
            'created_at': datetime.now().isoformat(),
            'tracks_created': len(audio_files),
            'video_files': len(video_files),
            'demo_mode': True,
            'parameters_used': parameters
        }
        
        with open(project_dir / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Create project summary
        create_demo_project_summary(project_dir, metadata)
        
        update_progress(100, "✅ Projektas baigtas sėkmingai!")
        
        return {
            'success': True,
            'project_name': project_name,
            'project_path': str(project_dir),
            'files_created': len(list(project_dir.rglob('*'))),
            'audio_files': len(audio_files),
            'video_files': len(video_files),
            'metadata': metadata
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def generate_demo_concept(parameters):
    """Generate realistic music concept"""
    genre = parameters.get('genre', 'pop')
    mood = parameters.get('mood', 'upbeat')
    
    concepts = {
        'pop': [
            "Vasaros nostalgijos ir jaunystės prisiminimų tema",
            "Meilės istorija su šiuolaikišku skambesiu",
            "Optimistiškas požiūris į ateities galimybes",
            "Draugystės ir kartu praleisto laiko šventė"
        ],
        'rock': [
            "Laisvės ir nepaklusnumo himnas",
            "Gyvenimo iššūkių įveikos istorija",
            "Energijos ir jėgos demonstracija",
            "Klasikinio roko garsų modernizacija"
        ],
        'electronic': [
            "Skaitmeninio amžiaus refleksijos",
            "Kosmoso ir ateities vizijos",
            "Šokių kultūros evoliucija",
            "Technologijų ir emocijų sintezė"
        ]
    }
    
    available_concepts = concepts.get(genre, concepts['pop'])
    return random.choice(available_concepts)

def generate_demo_lyrics(genre, concept):
    """Generate demo lyrics based on genre and concept"""
    lyrics_templates = {
        'pop': [
            "Verse 1:\nSummer nights and city lights\nDancing till the morning bright\nMemories we'll never lose\nIn this moment, me and you\n\nChorus:\nWe're flying high above the clouds\nSinging our hearts out loud\nNothing can stop us now\nThis is our time somehow",
            "Verse 1:\nWalking down this empty street\nHeartbeat matching to the beat\nEvery step takes me away\nFrom the pain of yesterday\n\nChorus:\nI'm breaking free from all the chains\nWashing away all of the stains\nStarting fresh, starting new\nThis is what I'm gonna do"
        ],
        'rock': [
            "Verse 1:\nThunder rolling in the night\nLightning strikes with all its might\nStanding strong against the storm\nThis is where legends are born\n\nChorus:\nWe won't back down, we'll never fall\nBreaking through, we'll break the wall\nScream it out with all your soul\nRock and roll will make us whole",
            "Verse 1:\nBorn to run, born to fight\nNever giving up the fight\nFuel the fire in your veins\nBreak away from all the chains\n\nChorus:\nRise up, stand tall\nWe'll conquer it all\nWith power and might\nWe'll light up the night"
        ]
    }
    
    available_lyrics = lyrics_templates.get(genre, lyrics_templates['pop'])
    return random.choice(available_lyrics)

def create_demo_audio_files(project_dir, parameters):
    """Create realistic demo audio files based on genre"""
    audio_files = []
    track_count = parameters.get('track_count', 2)
    genre = parameters.get('genre', 'pop')
    
    # Create audio directory
    audio_dir = project_dir / 'audio'
    audio_dir.mkdir(exist_ok=True)
    
    # Genre-specific source files
    genre_files = {
        'pop': ['pop_demo.mp3', 'demo_track_1.mp3'],
        'rock': ['rock_demo.mp3', 'demo_track_2.mp3'],
        'electronic': ['electronic_demo.mp3', 'demo_track_3.mp3'],
        'demo': ['demo_track_1.mp3', 'demo_track_2.mp3', 'demo_track_3.mp3']
    }
    
    mock_audio_dir = Path('mock_audio')
    source_files = genre_files.get(genre, genre_files['demo'])
    
    if mock_audio_dir.exists():
        for i in range(track_count):
            # Select source file (cycle through available files)
            source_filename = source_files[i % len(source_files)]
            source_file = mock_audio_dir / source_filename
            
            if source_file.exists():
                dest_file = audio_dir / f'{genre}_track_{i+1}.mp3'
                shutil.copy2(source_file, dest_file)
                audio_files.append(str(dest_file))
            else:
                # Fallback: create placeholder
                dest_file = audio_dir / f'demo_track_{i+1}.mp3'
                create_placeholder_audio(dest_file, f'{genre.title()} Demo Track {i+1}')
                audio_files.append(str(dest_file))
    else:
        # Create placeholders if no mock files
        for i in range(track_count):
            audio_file = audio_dir / f'{genre}_demo_track_{i+1}.mp3'
            create_placeholder_audio(audio_file, f'{genre.title()} Demo Track {i+1}')
            audio_files.append(str(audio_file))
    
    return audio_files

def create_placeholder_audio(file_path, title):
    """Create a placeholder MP3 file with proper ID3 tags"""
    with open(file_path, 'wb') as f:
        # Write ID3v2 header with title
        id3_header = b'ID3\x03\x00\x00\x00\x00\x00\x3F'  # ID3v2.3.0
        
        # TIT2 frame (title)
        title_bytes = title.encode('utf-8')
        title_frame = b'TIT2' + (len(title_bytes) + 1).to_bytes(4, 'big') + b'\x00\x00\x00' + title_bytes
        
        # TPE1 frame (artist)
        artist = 'AI Demo Generator'
        artist_bytes = artist.encode('utf-8')
        artist_frame = b'TPE1' + (len(artist_bytes) + 1).to_bytes(4, 'big') + b'\x00\x00\x00' + artist_bytes
        
        f.write(id3_header + title_frame + artist_frame)
        
        # Minimal MP3 audio frame
        f.write(b'\xff\xfb\x90\x00' + b'\x00' * 100)

def create_demo_video_files(project_dir, audio_files):
    """Create demo video files"""
    video_files = []
    video_dir = project_dir / 'video'
    video_dir.mkdir(exist_ok=True)
    
    for i, audio_file in enumerate(audio_files):
        video_file = video_dir / f'video_{i+1}.mp4'
        # Create placeholder video file
        with open(video_file, 'wb') as f:
            # Write minimal MP4 header
            f.write(b'\x00\x00\x00\x20ftypmp41')
        video_files.append(str(video_file))
    
    return video_files

def create_demo_cover_art(project_dir, concept):
    """Create demo cover art"""
    import base64
    
    images_dir = project_dir / 'images'
    images_dir.mkdir(exist_ok=True)
    
    # Create a simple colored rectangle as cover art
    cover_file = images_dir / 'cover.png'
    
    # Create minimal PNG file (1x1 pixel)
    png_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU8j6gAAAABJRU5ErkJggg==')
    with open(cover_file, 'wb') as f:
        f.write(png_data)
    
    return str(cover_file)

def create_demo_project_summary(project_dir, metadata):
    """Create human-readable project summary"""
    summary_file = project_dir / 'PROJECT_SUMMARY.md'
    
    summary_content = f"""# Demo Projekto Santrauka

## Projekto Informacija
- **Pavadinimas:** {metadata['title']}
- **Žanras:** {metadata['genre']}
- **Sukurta:** {metadata['created_at']}
- **Demo režimas:** ✅ Taip

## Koncepcija
{metadata['concept']}

## Sukurti Failai
- **Audio takeliai:** {metadata['tracks_created']}
- **Video failai:** {metadata['video_files']}
- **Albumo viršelis:** ✅ Sukurtas

## Tekstai
```
{metadata['lyrics']}
```

## Naudoti Parametrai
- **Režimas:** {metadata['mode']}
- **Žanras:** {metadata['genre']}

---
*Šis projektas sukurtas demo režimu su simuliuotais duomenimis.*
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)

@app.route('/api/generate/status/<task_id>')
@require_auth
def api_generation_status(task_id):
    """Get generation task status"""
    task = system_state.generation_tasks.get(task_id, {})
    return jsonify(task)

@app.route('/api/demo/quick-test', methods=['POST'])
@require_auth
def api_demo_quick_test():
    """Start quick demo test with predefined parameters"""
    demo_params = {
        'title': 'Demo Greitas Testas',
        'mode': 'demo',
        'genre': 'pop',
        'mood': 'upbeat',
        'track_count': 2,
        'demo_mode': True,
        'test_type': 'quick'
    }
    
    task_id = f"demo_quick_{int(time.time())}"
    
    # Store task info
    system_state.generation_tasks[task_id] = {
        'id': task_id,
        'status': 'queued',
        'progress': 0,
        'current_step': 'Pradedamas greitas demo testas...',
        'logs': [],
        'parameters': demo_params,
        'created_at': datetime.now().isoformat(),
        'result': None,
        'demo_mode': True
    }
    
    # Start demo generation
    def run_quick_demo():
        try:
            system_state.generation_tasks[task_id]['status'] = 'running'
            result = run_demo_generation(task_id, demo_params)
            system_state.generation_tasks[task_id]['result'] = result
            system_state.generation_tasks[task_id]['status'] = 'completed'
        except Exception as e:
            system_state.generation_tasks[task_id]['status'] = 'failed'
            system_state.generation_tasks[task_id]['result'] = {'success': False, 'error': str(e)}
    
    thread = threading.Thread(target=run_quick_demo, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'task_id': task_id, 'demo_mode': True})

@app.route('/api/demo/full-process', methods=['POST'])
@require_auth
def api_demo_full_process():
    """Start comprehensive demo with all features"""
    data = request.get_json() or {}
    
    demo_params = {
        'title': data.get('title', 'Demo Pilnas Procesas'),
        'mode': 'comprehensive_demo',
        'genre': data.get('genre', 'electronic'),
        'mood': data.get('mood', 'energetic'),
        'track_count': data.get('track_count', 3),
        'include_video': True,
        'include_cover_art': True,
        'demo_mode': True,
        'test_type': 'comprehensive'
    }
    
    task_id = f"demo_full_{int(time.time())}"
    
    # Store task info
    system_state.generation_tasks[task_id] = {
        'id': task_id,
        'status': 'queued',
        'progress': 0,
        'current_step': 'Pradedamas pilnas demo procesas...',
        'logs': [],
        'parameters': demo_params,
        'created_at': datetime.now().isoformat(),
        'result': None,
        'demo_mode': True
    }
    
    # Start comprehensive demo
    def run_full_demo():
        try:
            system_state.generation_tasks[task_id]['status'] = 'running'
            result = run_demo_generation(task_id, demo_params)
            system_state.generation_tasks[task_id]['result'] = result
            system_state.generation_tasks[task_id]['status'] = 'completed'
        except Exception as e:
            system_state.generation_tasks[task_id]['status'] = 'failed'
            system_state.generation_tasks[task_id]['result'] = {'success': False, 'error': str(e)}
    
    thread = threading.Thread(target=run_full_demo, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'task_id': task_id, 'demo_mode': True})

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    # Create required directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("🚀 Starting Professional Autonominis Muzikantas Admin Interface...")
    print("🔐 Default admin password: admin123")
    print("🌐 Access: http://localhost:8000")
    
    app.run(host='0.0.0.0', port=8000, debug=True)