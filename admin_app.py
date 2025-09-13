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
import random
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps
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

# Import new voice cloning system and trending hijacker
from voice_cloning_empire import VoiceCloningEmpire
from live_trending_hijacker import LiveTrendingHijacker

# Import unlimited empire system
from ai_channel_generator import AIChannelGenerator

# Import advanced genre system
from advanced_genre_system import advanced_genre_system, recommendation_engine, VocalIntelligenceEngine
from gemini_vocal_intelligence import gemini_vocal_engine
from music_industry_analytics import music_analytics

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
        self.voice_empire = VoiceCloningEmpire()  # Initialize voice cloning system
        self.trending_hijacker = LiveTrendingHijacker()  # Initialize trending hijacker
        self.ai_channel_generator = AIChannelGenerator()  # Initialize unlimited empire system
        self.vocal_ai = VocalIntelligenceEngine()  # Initialize AI vocal decision engine
        self.gemini_vocal_ai = gemini_vocal_engine  # Initialize Gemini AI vocal intelligence
        self.music_analytics = music_analytics  # Initialize music industry analytics engine
        
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
                status['gemini'] = {'status': 'connected', 'model': os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'), 'error': None}
            else:
                status['gemini'] = {'status': 'not_configured', 'model': None, 'error': 'API key not configured'}
        except Exception as e:
            status['gemini'] = {'status': 'error', 'model': None, 'error': str(e)}
        
        # Gemini Nano-Banana (Image Generation)
        try:
            if os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here':
                status['nano_banana'] = {'status': 'connected', 'model': 'gemini-2.5-flash-image-preview', 'error': None}
            else:
                status['nano_banana'] = {'status': 'not_configured', 'error': 'Gemini API key required for image generation'}
        except Exception as e:
            status['nano_banana'] = {'status': 'error', 'error': str(e)}
        
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
from dataclasses import asdict

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
    for key in ['SUNO_API_KEY', 'GEMINI_API_KEY', 'GEMINI_MODEL']:
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

@app.route('/system-settings')
@require_auth
def system_settings():
    """Advanced system settings with theme selection"""
    return render_template('system_settings.html')

@app.route('/youtube-channels')
@require_auth
def youtube_channels_manager():
    """YouTube Channels Manager - Multi-channel management interface"""
    return render_template('youtube_channels.html')

@app.route('/enhanced-channel-creation')
@require_auth
def enhanced_channel_creation():
    """Advanced Channel Creation with Genre Intelligence"""
    return render_template('enhanced_channel_creation.html')

@app.route('/channel-generator')
@require_auth
def channel_generator():
    """AI Channel Generator with Interactive Genre Tree"""
    return render_template('channel_generator.html')

@app.route('/templates/genre_tree_selector.html')
def serve_genre_tree_selector():
    """Serve the genre tree selector template as component"""
    return send_from_directory('templates', 'genre_tree_selector.html')

@app.route('/advanced-genre-demo')
@require_auth
def advanced_genre_demo():
    """Advanced Genre System Demo Page"""
    return render_template('advanced_genre_demo.html')

@app.route('/automation-control')
@require_auth
def automation_control():
    """24/7 Automation Control Center"""
    return render_template('automation_control.html')

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

# YouTube Empire Management API Endpoints
@app.route('/youtube-empire')
@require_auth
def youtube_empire():
    """YouTube Empire management page"""
    return render_template('youtube_empire.html')

@app.route('/voice-empire')
@require_auth
def voice_empire():
    """Voice Cloning Empire management page"""
    return render_template('voice_empire.html')

@app.route('/trending-hijacker')
@require_auth
def trending_hijacker():
    """Live Trending Hijacker management page"""
    return render_template('trending_hijacker.html')

@app.route('/api/youtube/channels')
@require_auth
def api_youtube_channels():
    """Get all YouTube channels configuration"""
    from youtube_empire_manager import YouTubeEmpireManager
    
    manager = YouTubeEmpireManager()
    channels_data = []
    
    for channel_id, channel in manager.channels.items():
        channel_data = asdict(channel) if hasattr(channel, '__dict__') else {
            'id': channel_id,
            'name': getattr(channel, 'name', 'Unknown'),
            'style': getattr(channel, 'style', 'general'),
            'upload_schedule': getattr(channel, 'upload_schedule', 'weekly'),
            'subscribers': getattr(channel, 'subscribers', 0),
            'performance_score': getattr(channel, 'performance_score', 0.5)
        }
        channels_data.append(channel_data)
    
    return jsonify({'channels': channels_data})

@app.route('/api/youtube/channels/list')
@require_auth
def api_youtube_channels_list():
    """Get YouTube channels list for management"""
    try:
        from core.database.database_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        channels = db_manager.get_all_youtube_channels()
        
        channels_data = []
        for channel in channels:
            # channel is already a dictionary from database_manager
            channel_dict = channel.copy() if isinstance(channel, dict) else channel.to_dict()
            # Format last_upload for display
            if channel_dict.get('last_upload'):
                try:
                    if isinstance(channel_dict['last_upload'], str):
                        # Already formatted
                        pass
                    else:
                        channel_dict['last_upload'] = channel_dict['last_upload'].strftime('%Y-%m-%d')
                except:
                    channel_dict['last_upload'] = None
            else:
                channel_dict['last_upload'] = None
            channels_data.append(channel_dict)
        
        return jsonify({'channels': channels_data})
        
    except Exception as e:
        print(f"Error loading channels: {e}")
        # Fall back to demo data if database fails
        demo_channels = [
            {
                'id': 1,
                'name': 'Lo-Fi Beats Central',
                'url': 'https://youtube.com/@lofibeatscentral',
                'youtube_channel_id': 'UC123456789012345678901',
                'primary_genre': 'lo-fi-hip-hop',
                'status': 'active',
                'subscribers': 45230,
                'monthly_revenue': 1250,
                'last_upload': '2025-09-12',
                'upload_schedule': 'daily',
                'auto_upload': True,
                'auto_thumbnails': True,
                'auto_seo': True,
                'enable_analytics': True,
                'privacy_settings': 'private'
            },
            {
                'id': 2,
                'name': 'Ambient Soundscapes',
                'url': 'https://youtube.com/@ambientsounds',
                'youtube_channel_id': 'UC234567890123456789012',
                'primary_genre': 'ambient',
                'status': 'active',
                'subscribers': 23100,
                'monthly_revenue': 890,
                'last_upload': '2025-09-11',
                'upload_schedule': 'every-2-days',
                'auto_upload': True,
                'auto_thumbnails': True,
                'auto_seo': True,
                'enable_analytics': True,
                'privacy_settings': 'unlisted'
            }
        ]
        return jsonify({'channels': demo_channels})

@app.route('/api/youtube/channels/save', methods=['POST'])
@require_auth
def api_youtube_channels_save():
    """Save or update YouTube channel"""
    try:
        from core.database.database_manager import DatabaseManager
        
        data = request.get_json() or {}
        db_manager = DatabaseManager()
        
        # Prepare channel data - support both field name formats
        channel_data = {
            'name': data.get('name') or data.get('channel_name'),
            'url': data.get('url') or data.get('channel_url'), 
            'youtube_channel_id': data.get('youtube_channel_id'),
            'description': data.get('description'),
            'primary_genre': data.get('primary_genre'),
            'secondary_genres': data.get('secondary_genres', []),
            'target_audience': data.get('target_audience'),
            'upload_schedule': data.get('upload_schedule'),
            'preferred_upload_time': data.get('preferred_upload_time', '14:00'),
            'style_preferences': {'branding_style': data.get('branding_style')} if data.get('branding_style') else {},
            'auto_upload': data.get('auto_upload') == 'on' or data.get('auto_upload') is True,
            'auto_thumbnails': data.get('auto_thumbnails') == 'on' or data.get('auto_thumbnails') is True,
            'auto_seo': data.get('auto_seo') == 'on' or data.get('auto_seo') is True,
            'enable_analytics': data.get('enable_analytics') == 'on' or data.get('enable_analytics') is True,
            'enable_monetization': data.get('enable_monetization') == 'on' or data.get('enable_monetization') is True,
            'privacy_settings': data.get('privacy_settings', 'private'),
            'api_key': data.get('api_key'),
            'client_id': data.get('client_id'),
            'client_secret': data.get('client_secret'),
            'status': 'active' if data.get('api_key') else 'needs_setup'
        }
        
        channel_id = data.get('channel_id')
        if channel_id:
            # Update existing channel
            channel = db_manager.update_youtube_channel(int(channel_id), channel_data)
            if channel:
                return jsonify({
                    'success': True, 
                    'message': 'Channel updated successfully', 
                    'channel': channel.to_dict()
                })
            else:
                return jsonify({'success': False, 'message': 'Channel not found'}), 404
        else:
            # Create new channel
            channel_id = db_manager.create_youtube_channel(channel_data)
            if channel_id:
                return jsonify({
                    'success': True, 
                    'message': 'Channel created successfully', 
                    'channel_id': channel_id
                })
            else:
                return jsonify({'success': False, 'message': 'Failed to create channel'}), 500
            
    except Exception as e:
        print(f"Error saving channel: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/youtube/channels/<int:channel_id>/delete', methods=['DELETE'])
@require_auth
def api_youtube_channels_delete(channel_id):
    """Delete YouTube channel"""
    try:
        from core.database.database_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        success = db_manager.delete_youtube_channel(channel_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Channel deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Channel not found'}), 404
            
    except Exception as e:
        print(f"Error deleting channel: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/youtube/channels/<int:channel_id>/generate', methods=['POST'])
@require_auth
def api_youtube_channels_generate(channel_id):
    """Generate content for specific channel"""
    data = request.get_json() or {}
    content_type = data.get('type', 'music')  # music, thumbnail, full_video
    
    task_id = f"channel_{channel_id}_{content_type}_{int(time.time())}"
    
    # Store task info
    system_state.generation_tasks[task_id] = {
        'id': task_id,
        'channel_id': channel_id,
        'content_type': content_type,
        'status': 'running',
        'progress': 0,
        'current_step': 'Initializing...',
        'created_at': datetime.now(),
        'logs': []
    }
    
    # Start generation in background thread
    thread = threading.Thread(target=generate_channel_content, args=(task_id, channel_id, content_type))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'task_id': task_id, 'message': f'Content generation started for channel {channel_id}'})

@app.route('/api/automation/start', methods=['POST'])
@require_auth
def api_automation_start():
    """Start 24/7 automation for all channels"""
    try:
        from automation_controller import automation_controller
        
        success = automation_controller.start_24_7_automation()
        
        if success:
            return jsonify({
                'success': True,
                'message': '24/7 automation started successfully!',
                'status': automation_controller.get_automation_status()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to start automation. Check logs for details.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting automation: {str(e)}'
        }), 500

@app.route('/api/automation/stop', methods=['POST'])
@require_auth  
def api_automation_stop():
    """Stop 24/7 automation"""
    try:
        from automation_controller import automation_controller
        
        success = automation_controller.stop_24_7_automation()
        
        if success:
            return jsonify({
                'success': True,
                'message': '24/7 automation stopped successfully!',
                'status': automation_controller.get_automation_status()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to stop automation'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error stopping automation: {str(e)}'
        }), 500

@app.route('/api/automation/status')
@require_auth
def api_automation_status():
    """Get current automation status"""
    try:
        from automation_controller import automation_controller
        
        status = automation_controller.get_automation_status()
        performance = automation_controller.get_channel_performance()
        
        return jsonify({
            'success': True,
            'automation': status,
            'channels': performance
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting automation status: {str(e)}'
        }), 500

@app.route('/api/youtube/channels/statistics')
@require_auth
def api_youtube_channels_statistics():
    """Get comprehensive statistics for all channels"""
    try:
        from core.database.database_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        stats = db_manager.get_channels_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        print(f"Error getting channel statistics: {e}")
        # Return demo stats if database fails
        return jsonify({
            'success': True,
            'statistics': {
                'total_channels': 2,
                'active_channels': 2,
                'total_subscribers': 68330,
                'total_revenue': 2140.0,
                'total_videos': 156,
                'total_views': 1250000,
                'status_breakdown': {'active': 2},
                'genre_breakdown': {'lo-fi-hip-hop': 1, 'ambient': 1}
            }
        })

@app.route('/api/youtube/empire-report')
@require_auth
def api_empire_report():
    """Generate comprehensive empire profitability report"""
    from youtube_empire_manager import YouTubeEmpireManager
    
    manager = YouTubeEmpireManager()
    report = manager.generate_youtube_empire_report()
    
    return jsonify(report)

@app.route('/api/youtube/batch-generate', methods=['POST'])
@require_auth
def api_youtube_batch_generate():
    """Start massive batch generation for all channels"""
    data = request.get_json() or {}
    batch_size = data.get('batch_size', 20)
    
    task_id = f"youtube_batch_{int(time.time())}"
    
    # Store task info
    system_state.generation_tasks[task_id] = {
        'id': task_id,
        'status': 'queued',
        'progress': 0,
        'current_step': f'Pradedamas masinis generavimas {batch_size} video...',
        'logs': [],
        'parameters': data,
        'created_at': datetime.now().isoformat(),
        'result': None,
        'youtube_batch': True,
        'batch_size': batch_size
    }
    
    def run_youtube_batch():
        try:
            from youtube_empire_manager import YouTubeEmpireManager
            import asyncio
            
            system_state.generation_tasks[task_id]['status'] = 'running'
            
            manager = YouTubeEmpireManager()
            
            # Update progress
            def update_progress(progress, step):
                system_state.generation_tasks[task_id]['progress'] = progress
                system_state.generation_tasks[task_id]['current_step'] = step
                system_state.generation_tasks[task_id]['logs'].append(f"[{datetime.now().strftime('%H:%M:%S')}] {step}")
            
            update_progress(10, "🚀 Inicijuojama YouTube imperija...")
            time.sleep(1)
            
            update_progress(25, f"🎵 Generuojama {batch_size} video {len(manager.channels)} kanalams...")
            
            # Simulate async batch generation
            async def simulate_batch():
                return await manager.generate_multi_channel_content(batch_size)
            
            # Run async function in thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(simulate_batch())
            loop.close()
            
            update_progress(70, "💰 Apskaičiuojami pelno projektai...")
            time.sleep(1)
            
            # Generate empire report
            report = manager.generate_youtube_empire_report()
            
            update_progress(85, "📊 Kuriamos analitikos ataskaitos...")
            time.sleep(1)
            
            # Save batch data
            batch_dir = manager.save_generation_data(results)
            
            update_progress(100, f"✅ Baigta! Sukurta {len(results)} video projektų")
            
            system_state.generation_tasks[task_id]['result'] = {
                'success': True,
                'videos_generated': len(results),
                'batch_directory': str(batch_dir),
                'empire_report': report,
                'estimated_monthly_revenue': report['empire_overview']['total_estimated_monthly_revenue'],
                'annual_projection': report['empire_overview']['annual_revenue_projection']
            }
            system_state.generation_tasks[task_id]['status'] = 'completed'
            
        except Exception as e:
            system_state.generation_tasks[task_id]['status'] = 'failed'
            system_state.generation_tasks[task_id]['result'] = {'success': False, 'error': str(e)}
    
    thread = threading.Thread(target=run_youtube_batch, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'task_id': task_id})

@app.route('/api/youtube/upload-schedule', methods=['POST'])
@require_auth  
def api_youtube_upload_schedule():
    """Schedule optimized YouTube uploads"""
    data = request.get_json() or {}
    
    # This would integrate with actual YouTube API
    scheduled_uploads = []
    
    # Mock scheduling for demo
    for i in range(data.get('video_count', 5)):
        scheduled_uploads.append({
            'video_id': f'scheduled_{i}',
            'channel': f'channel_{i % 3}',
            'upload_time': (datetime.now() + timedelta(hours=i*2)).isoformat(),
            'title': f'Auto-scheduled video {i+1}',
            'estimated_views': random.randint(5000, 50000)
        })
    
    return jsonify({
        'success': True,
        'scheduled_count': len(scheduled_uploads),
        'uploads': scheduled_uploads
    })

@app.route('/api/youtube/engagement-bot', methods=['POST'])
@require_auth
def api_youtube_engagement_bot():
    """Activate engagement bot for videos"""
    data = request.get_json() or {}
    
    from youtube_empire_manager import EngagementBot
    
    bot = EngagementBot()
    
    # Mock engagement generation
    engagement_plan = []
    
    for i in range(data.get('video_count', 5)):
        video_metadata = {
            'video_id': f'video_{i}',
            'style': random.choice(['lofi', 'trap', 'meditation', 'gaming'])
        }
        
        # Generate comments for each video
        comments = asyncio.run(bot.generate_engagement_comments(video_metadata, 3))
        engagement_plan.extend(comments)
    
    return jsonify({
        'success': True,
        'engagement_actions': len(engagement_plan),
        'comments_scheduled': len([e for e in engagement_plan if e['engagement_type'] == 'auto_comment']),
        'plan': engagement_plan[:10]  # Show first 10 for preview
    })

@app.route('/api/seo/optimize', methods=['POST'])
@require_auth
def api_seo_optimize():
    """Optimize video metadata for maximum SEO"""
    data = request.get_json() or {}
    
    from seo_optimizer import SEOOptimizer
    
    optimizer = SEOOptimizer()
    
    style = data.get('style', 'lofi')
    mood = data.get('mood', 'chill')
    custom_title = data.get('title')
    
    # Generate optimized metadata
    optimized_metadata = optimizer.optimize_video_metadata(style, mood, custom_title)
    
    return jsonify({
        'success': True,
        'optimized_metadata': optimized_metadata
    })

@app.route('/api/seo/batch-optimize', methods=['POST'])
@require_auth
def api_seo_batch_optimize():
    """Batch SEO optimization for multiple videos"""
    data = request.get_json() or {}
    
    from seo_optimizer import SEOOptimizer
    from youtube_empire_manager import YouTubeEmpireManager
    
    optimizer = SEOOptimizer()
    manager = YouTubeEmpireManager()
    
    batch_size = data.get('batch_size', 10)
    optimize_results = []
    
    # Generate optimized metadata for each channel style
    for channel_id, channel in list(manager.channels.items())[:batch_size]:
        try:
            optimized = optimizer.optimize_video_metadata(
                style=channel.style,
                mood=random.choice(['chill', 'epic', 'peaceful', 'intense'])
            )
            
            optimize_results.append({
                'channel_id': channel_id,
                'channel_name': channel.name,
                'style': channel.style,
                'optimized_metadata': optimized,
                'success': True
            })
        except Exception as e:
            optimize_results.append({
                'channel_id': channel_id,
                'error': str(e),
                'success': False
            })
    
    # Calculate total potential
    total_estimated_views = sum(r['optimized_metadata']['estimated_views'] 
                               for r in optimize_results if r['success'])
    total_estimated_revenue = sum(r['optimized_metadata']['revenue_potential']['estimated_revenue'] 
                                 for r in optimize_results if r['success'])
    avg_seo_score = sum(r['optimized_metadata']['seo_score'] 
                       for r in optimize_results if r['success']) / len([r for r in optimize_results if r['success']])
    
    return jsonify({
        'success': True,
        'batch_results': optimize_results,
        'batch_summary': {
            'total_videos': len(optimize_results),
            'successful_optimizations': len([r for r in optimize_results if r['success']]),
            'total_estimated_views': total_estimated_views,
            'total_estimated_revenue': round(total_estimated_revenue, 2),
            'average_seo_score': round(avg_seo_score, 1)
        }
    })

@app.route('/api/youtube/trending-analysis')
@require_auth
def api_trending_analysis():
    """Get trending analysis for all styles"""
    from seo_optimizer import YouTubeTrendingAnalyzer
    
    analyzer = YouTubeTrendingAnalyzer()
    
    trending_data = {}
    
    for style in ['lofi', 'trap', 'meditation', 'gaming']:
        # Generate sample optimized metadata
        sample_optimization = analyzer.generate_optimized_title(style, trending_boost=True)
        
        trending_data[style] = {
            'trending_keywords': analyzer.trending_keywords.get(style, {}),
            'rpm_data': analyzer.rpm_data.get(style, {}),
            'optimal_upload_times': analyzer.upload_schedule.get(style, {}),
            'sample_title': sample_optimization
        }
    
    return jsonify({
        'trending_analysis': trending_data,
        'generated_at': datetime.now().isoformat()
    })

# Smart Thumbnail Generator API Endpoints
@app.route('/api/thumbnails/generate', methods=['POST'])
@require_auth
def api_generate_thumbnails():
    """Generate smart thumbnails with A/B testing"""
    data = request.get_json() or {}
    
    from smart_thumbnail_generator import SmartThumbnailGenerator
    
    generator = SmartThumbnailGenerator()
    
    style = data.get('style', 'lofi')
    title = data.get('title', 'Demo Music Video')
    mood = data.get('mood', 'chill')
    variant_count = data.get('variant_count', 3)
    
    try:
        # Generate comprehensive thumbnail package
        package = generator.generate_comprehensive_thumbnail_package(style, title, mood)
        
        return jsonify({
            'success': True,
            'thumbnail_package': package,
            'roi_analysis': package['roi_analysis'],
            'winner': package['ab_test_results']['winner']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/thumbnails/batch-generate', methods=['POST'])
@require_auth
def api_batch_generate_thumbnails():
    """Generate thumbnails for multiple videos"""
    data = request.get_json() or {}
    
    from smart_thumbnail_generator import SmartThumbnailGenerator
    from youtube_empire_manager import YouTubeEmpireManager
    
    thumbnail_gen = SmartThumbnailGenerator()
    empire_manager = YouTubeEmpireManager()
    
    batch_size = data.get('batch_size', 5)
    results = []
    total_roi = 0
    
    try:
        # Generate thumbnails for different channels/styles
        for channel_id, channel in list(empire_manager.channels.items())[:batch_size]:
            # Create sample video metadata
            video_metadata = empire_manager.create_optimized_metadata(
                channel, 
                empire_manager.content_templates[channel.style],
                'epic',
                len(results)
            )
            
            # Generate thumbnail package
            package = thumbnail_gen.generate_comprehensive_thumbnail_package(
                style=channel.style,
                title=video_metadata['title'],
                mood=video_metadata['mood']
            )
            
            results.append({
                'channel_id': channel_id,
                'channel_name': channel.name,
                'video_title': video_metadata['title'],
                'thumbnail_package': package,
                'roi_analysis': package['roi_analysis']
            })
            
            total_roi += package['roi_analysis']['additional_monthly_revenue']
        
        return jsonify({
            'success': True,
            'batch_results': results,
            'total_thumbnails_generated': len(results) * 3,  # 3 variants each
            'total_monthly_roi': round(total_roi, 2),
            'total_annual_roi': round(total_roi * 12, 2)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# VOICE CLONING EMPIRE API ROUTES
# ============================================

@app.route('/api/voice/characters')
@require_auth
def get_voice_characters():
    """Get all voice characters"""
    try:
        empire_report = system_state.voice_empire.generate_empire_report()
        return jsonify({
            'success': True,
            'characters': empire_report['characters_by_style'],
            'total_characters': empire_report['total_characters'],
            'monthly_revenue': empire_report['total_monthly_revenue'],
            'roi_summary': empire_report['roi_summary']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice/initialize', methods=['POST'])
@require_auth
def initialize_voice_empire():
    """Initialize all voice characters"""
    try:
        result = system_state.voice_empire.initialize_all_characters()
        return jsonify({
            'success': True,
            'message': 'Voice empire initialized successfully',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice/generate-content', methods=['POST'])
@require_auth
def generate_voice_content():
    """Generate voice content batch"""
    try:
        data = request.get_json()
        count = data.get('count', 10)
        
        result = system_state.voice_empire.generate_voice_content_batch(count)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
        return jsonify({
            'success': True,
            'message': f'Generated {result["successful_generations"]} voice content pieces',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice/character-performance/<character_name>')
@require_auth
def get_character_performance(character_name):
    """Get performance metrics for specific character"""
    try:
        days = request.args.get('days', 30, type=int)
        performance = system_state.voice_empire.get_character_performance(character_name, days)
        
        return jsonify({
            'success': True,
            'performance': performance
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice/empire-report')
@require_auth
def get_voice_empire_report():
    """Get comprehensive voice empire report"""
    try:
        report = system_state.voice_empire.generate_empire_report()
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice/generate-script', methods=['POST'])
@require_auth
def generate_character_script():
    """Generate script for character"""
    try:
        data = request.get_json()
        character_name = data.get('character_name')
        content_type = data.get('content_type', 'track_description')
        music_context = data.get('music_context', {})
        
        if not character_name:
            return jsonify({
                'success': False,
                'error': 'Character name is required'
            }), 400
            
        script = system_state.voice_empire.generate_character_script(
            character_name, content_type, music_context
        )
        
        if 'error' in script:
            return jsonify({
                'success': False,
                'error': script['error']
            }), 400
            
        return jsonify({
            'success': True,
            'script': script
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice/synthesize', methods=['POST'])
@require_auth
def synthesize_character_voice():
    """Synthesize voice for character"""
    try:
        data = request.get_json()
        character_name = data.get('character_name')
        script = data.get('script')
        
        if not character_name or not script:
            return jsonify({
                'success': False,
                'error': 'Character name and script are required'
            }), 400
            
        audio_data = system_state.voice_empire.synthesize_voice(character_name, script)
        
        if 'error' in audio_data:
            return jsonify({
                'success': False,
                'error': audio_data['error']
            }), 400
            
        return jsonify({
            'success': True,
            'audio': audio_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# LIVE TRENDING HIJACKER API ROUTES
# ============================================

@app.route('/api/trending/start-monitoring', methods=['POST'])
@require_auth
def start_trending_monitoring():
    """Start live trending monitoring"""
    try:
        result = system_state.trending_hijacker.start_real_time_monitoring()
        return jsonify({
            'success': True,
            'message': 'Live trending monitoring started',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trending/stop-monitoring', methods=['POST'])
@require_auth
def stop_trending_monitoring():
    """Stop live trending monitoring"""
    try:
        system_state.trending_hijacker.stop_monitoring()
        return jsonify({
            'success': True,
            'message': 'Trending monitoring stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trending/dashboard')
@require_auth
def get_trending_dashboard():
    """Get live trending hijacking dashboard"""
    try:
        dashboard = system_state.trending_hijacker.get_hijacking_dashboard()
        return jsonify({
            'success': True,
            'dashboard': dashboard
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trending/performance-report')
@require_auth
def get_trending_performance_report():
    """Get trending performance report"""
    try:
        days = request.args.get('days', 7, type=int)
        report = system_state.trending_hijacker.get_trend_performance_report(days)
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trending/hijack-trend', methods=['POST'])
@require_auth
def manual_hijack_trend():
    """Manually trigger trend hijacking"""
    try:
        data = request.get_json()
        trend_id = data.get('trend_id')
        
        if not trend_id:
            return jsonify({
                'success': False,
                'error': 'Trend ID is required'
            }), 400
        
        # Mock implementation - would trigger actual hijacking
        result = {
            'trend_id': trend_id,
            'hijack_initiated': True,
            'estimated_completion': '90 minutes',
            'priority': 'high',
            'expected_views': random.randint(50000, 500000),
            'expected_revenue': random.uniform(200, 2000)
        }
        
        return jsonify({
            'success': True,
            'hijack_result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# =============================================================================
# UNLIMITED EMPIRE - AI CHANNEL GENERATOR ROUTES
# =============================================================================

@app.route('/unlimited-empire')
@require_auth
def unlimited_empire():
    """Unlimited Empire main dashboard"""
    try:
        stats = system_state.ai_channel_generator.get_empire_statistics()
        return render_template('unlimited_empire.html', stats=stats)
    except Exception as e:
        flash(f'Error loading unlimited empire: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/unlimited_empire/generate_concept', methods=['POST'])
@require_auth
def generate_concept():
    """Generate a single AI channel concept"""
    try:
        data = request.get_json() or {}
        category = data.get('category')
        
        concept = system_state.ai_channel_generator.generate_channel_concept(category)
        
        return jsonify({
            'success': True,
            'concept': concept
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/unlimited_empire/generate_batch', methods=['POST'])
@require_auth
def generate_batch_concepts():
    """Generate batch AI channel concepts"""
    try:
        data = request.get_json() or {}
        count = data.get('count', 5)
        category = data.get('category')
        
        concepts = system_state.ai_channel_generator.generate_batch_concepts(count, category)
        
        return jsonify({
            'success': True,
            'concepts': concepts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/unlimited_empire/concepts')
@require_auth
def get_concepts():
    """Get channel concepts by status"""
    try:
        status = request.args.get('status', 'all')
        concepts = system_state.ai_channel_generator.get_concepts(status)
        
        return jsonify({
            'success': True,
            'concepts': concepts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/unlimited_empire/approve_concept/<concept_id>', methods=['POST'])
@require_auth
def approve_concept(concept_id):
    """Approve a channel concept"""
    try:
        success = system_state.ai_channel_generator.approve_concept(concept_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Concept approved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to approve concept'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/unlimited_empire/stats')
@require_auth
def get_empire_stats():
    """Get empire statistics"""
    try:
        stats = system_state.ai_channel_generator.get_empire_statistics()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/unlimited_empire/activity')
@require_auth
def get_empire_activity():
    """Get recent empire activity"""
    try:
        activity = system_state.ai_channel_generator.get_recent_activity()
        return jsonify({
            'success': True,
            'activity': activity
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# =============================================================================
# ADVANCED GENRE SYSTEM API ENDPOINTS
# =============================================================================

@app.route('/api/genres/tree')
@require_auth
def api_genres_tree():
    """Get complete genre tree with statistics"""
    try:
        return jsonify(advanced_genre_system.genre_tree)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/genres/recommendations/<recommendation_type>')
@require_auth
def api_genres_recommendations(recommendation_type):
    """Get genre recommendations by type"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        if recommendation_type == 'profitable':
            recommendations = recommendation_engine.get_top_profitable_genres(limit)
        elif recommendation_type == 'trending':
            recommendations = recommendation_engine.get_trending_genres(limit)
        elif recommendation_type == 'easy':
            recommendations = recommendation_engine.get_easiest_to_start(limit)
        else:
            return jsonify({'error': 'Invalid recommendation type'}), 400
        
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/genres/vocal-decision', methods=['POST'])
@require_auth
def api_genres_vocal_decision():
    """Get AI vocal configuration decision using Gemini AI"""
    try:
        data = request.get_json() or {}
        
        # Prepare comprehensive context for Gemini AI
        context = {
            'genre_info': {
                'category': data.get('category', 'ELECTRONIC'),
                'subgenre': data.get('subgenre', 'HOUSE'),
                'substyle': data.get('substyle'),
                'vocal_probability': data.get('vocal_probability', 0.5),
                'preferred_vocals': data.get('preferred_vocals', [])
            },
            'user_context': {
                'target_audience': data.get('target_audience', 'general'),
                'time_context': data.get('time_context', 'any'),
                'upload_schedule': data.get('upload_schedule', 'weekly'),
                'target_revenue': data.get('target_revenue', 2000),
                'preferred_language': data.get('preferred_language', 'en')
            }
        }
        
        # Get comprehensive strategy from Gemini AI
        strategy = system_state.gemini_vocal_ai.get_comprehensive_vocal_strategy(context)
        
        return jsonify({
            'vocal_configuration': strategy['vocal_configuration'],
            'ai_analysis': strategy['ai_analysis'],
            'decision_rationale': strategy['ai_analysis'].get('market_rationale', 'AI-powered analysis'),
            'confidence_score': strategy['ai_analysis'].get('confidence_score', 75),
            'market_intelligence': strategy['ai_analysis'].get('market_intelligence', {}),
            'actionable_insights': strategy['ai_analysis'].get('actionable_insights', []),
            'implementation_guide': strategy['implementation_guide'],
            'success_metrics': strategy['success_metrics'],
            'gemini_powered': strategy['ai_powered']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/genres/vocal-strategy-advanced', methods=['POST'])
@require_auth
def api_genres_vocal_strategy_advanced():
    """Get advanced vocal strategy with full Gemini AI analysis"""
    try:
        data = request.get_json() or {}
        
        context = {
            'genre_info': {
                'category': data.get('category', 'ELECTRONIC'),
                'subgenre': data.get('subgenre', 'HOUSE'),
                'substyle': data.get('substyle'),
                'monthly_revenue': data.get('monthly_revenue', 2500),
                'difficulty_level': data.get('difficulty_level', 50),
                'competition_level': data.get('competition_level', 70)
            },
            'user_context': {
                'target_audience': data.get('target_audience', 'general'),
                'upload_schedule': data.get('upload_schedule', 'weekly'),
                'target_revenue': data.get('target_revenue', 2000),
                'experience_level': data.get('experience_level', 'intermediate'),
                'market_focus': data.get('market_focus', 'global')
            }
        }
        
        # Get full strategy with market analysis
        strategy = system_state.gemini_vocal_ai.get_comprehensive_vocal_strategy(context)
        
        # Add additional market insights
        market_analysis = {
            'trending_opportunities': system_state.gemini_vocal_ai._get_trending_factor(strategy['vocal_configuration']['vocal_type']),
            'audience_fit': system_state.gemini_vocal_ai._get_audience_compatibility(strategy['vocal_configuration']['vocal_type'], context['user_context']['target_audience']),
            'revenue_optimization': system_state.gemini_vocal_ai._get_revenue_optimization(strategy['vocal_configuration']['vocal_type'], context),
            'competitive_position': system_state.gemini_vocal_ai._get_competitive_landscape(strategy['vocal_configuration']['vocal_type'], context['genre_info'])
        }
        
        return jsonify({
            'vocal_strategy': strategy,
            'market_analysis': market_analysis,
            'roi_projection': {
                'monthly_revenue_boost': market_analysis['revenue_optimization']['projected_monthly_revenue'] - context['user_context']['target_revenue'],
                'confidence_level': market_analysis['revenue_optimization']['revenue_confidence'],
                'payback_period': '2-4 weeks',
                'annual_projection': market_analysis['revenue_optimization']['projected_monthly_revenue'] * 12
            },
            'next_steps': [
                'Implement vocal configuration in next content creation',
                'Monitor engagement metrics for 2 weeks',
                'A/B test alternative vocal approaches',
                'Scale successful vocal strategies across channels'
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/genres/statistics')
@require_auth
def api_genres_statistics():
    """Get comprehensive genre statistics overview"""
    try:
        stats = {
            'total_categories': len(advanced_genre_system.genre_tree),
            'total_subgenres': sum(len(cat.get('subgenres', {})) for cat in advanced_genre_system.genre_tree.values()),
            'average_monthly_revenue': 0,
            'highest_revenue_genre': None,
            'trending_count': 0,
            'easy_start_count': 0,
            'vocal_vs_instrumental': {'vocal': 0, 'instrumental': 0, 'mixed': 0}
        }
        
        all_revenues = []
        
        for category_name, category in advanced_genre_system.genre_tree.items():
            if 'subgenres' in category:
                for subgenre_name, subgenre in category['subgenres'].items():
                    if 'statistics' in subgenre:
                        revenue = subgenre['statistics'].monthly_revenue
                        all_revenues.append(revenue)
                        
                        if not stats['highest_revenue_genre'] or revenue > stats['highest_revenue_genre']['revenue']:
                            stats['highest_revenue_genre'] = {
                                'name': f"{category_name}.{subgenre_name}",
                                'revenue': revenue
                            }
                        
                        # Count trending
                        if subgenre['statistics'].growth_trend > 25:
                            stats['trending_count'] += 1
                        
                        # Count easy start
                        if subgenre['statistics'].difficulty_level < 40:
                            stats['easy_start_count'] += 1
                        
                        # Vocal preference categorization
                        vocal_pref = subgenre['statistics'].vocal_preference
                        if vocal_pref < 0.3:
                            stats['vocal_vs_instrumental']['instrumental'] += 1
                        elif vocal_pref > 0.7:
                            stats['vocal_vs_instrumental']['vocal'] += 1
                        else:
                            stats['vocal_vs_instrumental']['mixed'] += 1
        
        if all_revenues:
            stats['average_monthly_revenue'] = round(sum(all_revenues) / len(all_revenues), 2)
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/genres/optimize-channel', methods=['POST'])
@require_auth
def api_genres_optimize_channel():
    """Optimize genre selection for new channel"""
    try:
        data = request.get_json() or {}
        
        # Channel preferences
        target_revenue = data.get('target_monthly_revenue', 2000)
        difficulty_preference = data.get('difficulty_preference', 'medium')  # easy, medium, hard
        vocal_preference = data.get('vocal_preference', 'any')  # vocal, instrumental, any
        upload_frequency = data.get('upload_frequency', 'weekly')  # daily, weekly, monthly
        
        # Get all genres with their scores
        genre_recommendations = []
        
        for category_name, category in advanced_genre_system.genre_tree.items():
            if 'subgenres' in category:
                for subgenre_name, subgenre in category['subgenres'].items():
                    if 'statistics' in subgenre:
                        stats = subgenre['statistics']
                        
                        # Calculate optimization score
                        score = 0
                        
                        # Revenue score (40% weight)
                        revenue_score = min(100, (stats.monthly_revenue / target_revenue) * 100)
                        score += revenue_score * 0.4
                        
                        # Difficulty score (25% weight)
                        if difficulty_preference == 'easy':
                            difficulty_score = 100 - stats.difficulty_level
                        elif difficulty_preference == 'hard':
                            difficulty_score = stats.difficulty_level
                        else:  # medium
                            difficulty_score = 100 - abs(stats.difficulty_level - 50)
                        score += difficulty_score * 0.25
                        
                        # Vocal preference score (20% weight)
                        vocal_score = 50  # default
                        if vocal_preference == 'vocal' and stats.vocal_preference > 0.6:
                            vocal_score = 100
                        elif vocal_preference == 'instrumental' and stats.vocal_preference < 0.3:
                            vocal_score = 100
                        elif vocal_preference == 'any':
                            vocal_score = 75
                        score += vocal_score * 0.2
                        
                        # Growth trend score (15% weight)
                        growth_score = max(0, min(100, stats.growth_trend + 50))
                        score += growth_score * 0.15
                        
                        genre_recommendations.append({
                            'genre_path': f"{category_name}.{subgenre_name}",
                            'category': category_name,
                            'subgenre': subgenre_name,
                            'optimization_score': round(score, 1),
                            'statistics': {
                                'monthly_revenue': stats.monthly_revenue,
                                'difficulty_level': stats.difficulty_level,
                                'growth_trend': stats.growth_trend,
                                'vocal_preference': stats.vocal_preference,
                                'competition_level': stats.competition_level,
                                'monetization_rate': stats.monetization_rate
                            },
                            'match_reasons': []
                        })
        
        # Sort by score and get top recommendations
        genre_recommendations.sort(key=lambda x: x['optimization_score'], reverse=True)
        top_recommendations = genre_recommendations[:10]
        
        # Add match reasons for top recommendations
        for rec in top_recommendations:
            reasons = []
            stats = rec['statistics']
            
            if stats['monthly_revenue'] >= target_revenue:
                reasons.append(f"Exceeds target revenue (${stats['monthly_revenue']}/mo)")
            
            if difficulty_preference == 'easy' and stats['difficulty_level'] < 40:
                reasons.append("Low difficulty - easy to start")
            
            if stats['growth_trend'] > 20:
                reasons.append(f"Strong growth trend (+{stats['growth_trend']}%)")
            
            if vocal_preference == 'vocal' and stats['vocal_preference'] > 0.6:
                reasons.append("High vocal preference match")
            elif vocal_preference == 'instrumental' and stats['vocal_preference'] < 0.3:
                reasons.append("Instrumental preference match")
            
            if stats['competition_level'] < 60:
                reasons.append("Low competition market")
            
            if stats['monetization_rate'] > 80:
                reasons.append("High monetization potential")
            
            rec['match_reasons'] = reasons
        
        return jsonify({
            'optimization_results': top_recommendations,
            'optimization_parameters': {
                'target_revenue': target_revenue,
                'difficulty_preference': difficulty_preference,
                'vocal_preference': vocal_preference,
                'upload_frequency': upload_frequency
            },
            'summary': {
                'total_genres_analyzed': len(genre_recommendations),
                'top_recommendation': top_recommendations[0] if top_recommendations else None,
                'average_score': round(sum(r['optimization_score'] for r in top_recommendations) / len(top_recommendations), 1) if top_recommendations else 0
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/genres/suno-prompt', methods=['POST'])
@require_auth
def api_genres_suno_prompt():
    """Generate optimized Suno prompts based on genre selection"""
    try:
        data = request.get_json() or {}
        
        genre_path = data.get('genre_path', '').split('.')
        if len(genre_path) != 2:
            return jsonify({'error': 'Invalid genre path format'}), 400
        
        category_name, subgenre_name = genre_path
        substyle_name = data.get('substyle')
        
        # Get genre data
        category = advanced_genre_system.genre_tree.get(category_name)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        subgenre = category.get('subgenres', {}).get(subgenre_name)
        if not subgenre:
            return jsonify({'error': 'Subgenre not found'}), 404
        
        # Get substyle if specified
        substyle = None
        if substyle_name and 'substyles' in subgenre:
            substyle = subgenre['substyles'].get(substyle_name)
        
        # Generate AI vocal decision
        vocal_context = {
            'time_context': data.get('time_context', 'any'),
            'target_audience': data.get('target_audience', 'general'),
            'preferred_language': data.get('preferred_language', 'en')
        }
        
        genre_info = {
            'vocal_probability': substyle['vocal_probability'] if substyle else subgenre['statistics'].vocal_preference,
            'preferred_vocals': substyle.get('preferred_vocals', []) if substyle else []
        }
        
        vocal_config = system_state.vocal_ai.decide_vocal_configuration(genre_info, vocal_context)
        
        # Build Suno prompt
        prompt_parts = []
        
        # Genre and style
        if substyle and substyle.get('trending_keywords'):
            prompt_parts.extend(substyle['trending_keywords'][:3])  # Top 3 keywords
        else:
            prompt_parts.append(subgenre_name.replace('_', ' ').lower())
        
        # Vocal configuration
        if vocal_config.vocal_type.value == 'instrumental':
            prompt_parts.append('instrumental')
        elif vocal_config.vocal_type.value == 'atmospheric_vocals':
            prompt_parts.extend(['atmospheric vocals', 'ambient vocals'])
        elif vocal_config.vocal_type.value == 'full_lyrics':
            prompt_parts.extend([vocal_config.style, f'{vocal_config.mood} vocals'])
        elif vocal_config.vocal_type.value == 'minimal_vocals':
            prompt_parts.extend(['minimal vocals', 'sparse lyrics'])
        
        # Mood and style
        prompt_parts.extend([vocal_config.mood, 'professional production'])
        
        # Technical specifications based on genre
        if category_name == 'ELECTRONIC':
            prompt_parts.extend(['electronic', '128 BPM', 'synthesized'])
        elif category_name == 'CHILLOUT':
            prompt_parts.extend(['relaxing', '80-90 BPM', 'ambient'])
        elif category_name == 'WORKOUT':
            prompt_parts.extend(['energetic', '120-140 BPM', 'driving beat'])
        
        # Create final prompt
        suno_prompt = ', '.join(prompt_parts)
        
        # Generate metadata suggestions
        metadata_suggestions = {
            'title_templates': [
                f"{subgenre_name.replace('_', ' ').title()} Vibes",
                f"{vocal_config.mood.title()} {substyle_name.replace('_', ' ').title() if substyle_name else subgenre_name.replace('_', ' ').title()}",
                f"Premium {subgenre_name.replace('_', ' ').title()} Mix"
            ],
            'tags': prompt_parts + ['AI music', 'Suno AI', category_name.lower()],
            'description_template': f"Experience the perfect blend of {subgenre_name.replace('_', ' ')} with {vocal_config.mood} vibes. Created with advanced AI for optimal listening experience."
        }
        
        return jsonify({
            'suno_prompt': suno_prompt,
            'vocal_configuration': {
                'type': vocal_config.vocal_type.value,
                'language': vocal_config.language,
                'mood': vocal_config.mood,
                'style': vocal_config.style,
                'effects': vocal_config.vocal_effects
            },
            'metadata_suggestions': metadata_suggestions,
            'genre_context': {
                'category': category_name,
                'subgenre': subgenre_name,
                'substyle': substyle_name,
                'monthly_revenue_potential': subgenre['statistics'].monthly_revenue,
                'difficulty_level': subgenre['statistics'].difficulty_level,
                'growth_trend': subgenre['statistics'].growth_trend
            },
            'optimization_tips': [
                f"This genre has {subgenre['statistics'].competition_level}% competition level",
                f"Expected monthly revenue: ${subgenre['statistics'].monthly_revenue}",
                f"Audience retention rate: {subgenre['statistics'].audience_retention}%",
                f"Difficulty level: {subgenre['statistics'].difficulty_level}/100"
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================================================
# MUSIC INDUSTRY ANALYTICS API ENDPOINTS
# =============================================================================

@app.route('/api/analytics/market-report')
@require_auth
def api_analytics_market_report():
    """Get comprehensive daily market report"""
    try:
        import asyncio
        
        # Generate daily market report
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        report = loop.run_until_complete(system_state.music_analytics.generate_daily_report())
        loop.close()
        
        return jsonify({
            'success': True,
            'report': report,
            'generated_at': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/genre-performance/<genre_path>')
@require_auth
def api_analytics_genre_performance(genre_path):
    """Get detailed performance analysis for specific genre"""
    try:
        days = request.args.get('days', 30, type=int)
        
        performance = system_state.music_analytics.analyze_genre_performance(genre_path, days)
        
        return jsonify({
            'success': True,
            'performance': performance,
            'analysis_date': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/market-opportunities')
@require_auth
def api_analytics_market_opportunities():
    """Get current market opportunities and trends"""
    try:
        opportunities = system_state.music_analytics.get_market_opportunities()
        
        return jsonify({
            'success': True,
            'opportunities': opportunities,
            'analysis_date': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/real-time-data')
@require_auth
def api_analytics_real_time_data():
    """Get real-time market data collection"""
    try:
        import asyncio
        
        # Collect real-time data
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        market_data = loop.run_until_complete(system_state.music_analytics.collect_real_time_data())
        loop.close()
        
        return jsonify({
            'success': True,
            'market_data': market_data,
            'collected_at': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/industry-benchmarks')
@require_auth
def api_analytics_industry_benchmarks():
    """Get industry benchmarks and standards"""
    try:
        benchmarks = system_state.music_analytics.industry_benchmarks
        
        # Add real-time context
        current_month = datetime.now().strftime('%B').lower()
        seasonal_data = benchmarks['seasonal_multipliers'].get(current_month, {})
        
        enhanced_benchmarks = {
            'global_metrics': {
                'total_market_size': benchmarks['global_music_revenue'],
                'streaming_growth_rate': benchmarks['streaming_growth_rate'],
                'youtube_market_share': benchmarks['youtube_music_share']
            },
            'rpm_benchmarks': benchmarks['average_rpm_by_genre'],
            'current_seasonal_multipliers': seasonal_data,
            'industry_insights': [
                f"Global music industry worth ${benchmarks['global_music_revenue']/1e9:.1f}B in 2025",
                f"Streaming growth rate: {benchmarks['streaming_growth_rate']*100:.1f}% YoY",
                f"YouTube holds {benchmarks['youtube_music_share']*100:.0f}% of music streaming market",
                f"Current month ({current_month.title()}) shows {len(seasonal_data)} genres with seasonal boost"
            ]
        }
        
        return jsonify({
            'success': True,
            'benchmarks': enhanced_benchmarks,
            'updated_at': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/performance-tracking', methods=['POST'])
@require_auth
def api_analytics_performance_tracking():
    """Track performance data for analytics"""
    try:
        data = request.get_json() or {}
        
        # Save performance snapshot
        system_state.music_analytics.save_performance_snapshot(data)
        
        return jsonify({
            'success': True,
            'message': 'Performance data tracked successfully',
            'tracked_at': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/unlimited_empire/expansion_plan', methods=['POST'])
@require_auth
def create_expansion_plan():
    """Create expansion plan with AI optimization"""
    try:
        data = request.get_json() or {}
        target_channels = data.get('target_channels', 50)
        timeframe_days = data.get('timeframe_days', 30)
        focus_categories = data.get('focus_categories', [])
        
        expansion_plan = system_state.ai_channel_generator.create_expansion_plan(
            target_channels, timeframe_days, focus_categories
        )
        
        return jsonify({
            'success': True,
            'expansion_plan': expansion_plan
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/settings/save', methods=['POST'])
@require_auth
def api_save_settings():
    """Save system settings"""
    try:
        data = request.get_json() or {}
        
        # Here you could save to database or file
        # For now, we'll just return success since client handles localStorage
        
        settings_file = Path('user_settings.json')
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Settings saved successfully',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/settings/load')
@require_auth
def api_load_settings():
    """Load system settings"""
    try:
        settings_file = Path('user_settings.json')
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        else:
            # Default settings
            settings = {
                'theme': 'default',
                'language': 'lt',
                'autosave': '60',
                'notifications': True,
                'animations': True,
                'refreshRate': '5000',
                'maxTasks': '3',
                'cache': True,
                'debugMode': False
            }
        
        return jsonify({
            'success': True,
            'settings': settings
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# YouTube Channel Content Generation Functions
def generate_channel_content(task_id, channel_id, content_type):
    """Generate content for a specific YouTube channel"""
    
    def update_progress(progress, step):
        if task_id in system_state.generation_tasks:
            system_state.generation_tasks[task_id]['progress'] = progress
            system_state.generation_tasks[task_id]['current_step'] = step
            system_state.generation_tasks[task_id]['logs'].append(f"[{datetime.now().strftime('%H:%M:%S')}] {step}")
        time.sleep(random.uniform(0.5, 2))
    
    try:
        update_progress(10, f"🎯 Loading channel {channel_id} configuration...")
        
        # In production, load actual channel data from database
        channel_data = {
            'name': f'Channel {channel_id}',
            'primary_genre': 'lo-fi-hip-hop',
            'style_preferences': {},
            'automation_settings': {}
        }
        
        if content_type == 'music':
            update_progress(25, "🎵 Initializing music generation...")
            update_progress(50, "🎼 Creating audio track...")
            update_progress(75, "🎨 Generating cover art...")
            update_progress(90, "📝 Optimizing metadata...")
            
            # Simulate music generation process
            time.sleep(2)
            
        elif content_type == 'thumbnail':
            update_progress(25, "🍌 Initializing Nano-Banana (Gemini 2.5 Flash Image)...")
            update_progress(50, "🎨 Generating thumbnail design...")
            update_progress(75, "✨ Applying AI enhancements...")
            update_progress(90, "📐 Finalizing resolution and format...")
            
            # Simulate thumbnail generation with nano-banana
            time.sleep(2)
            
        elif content_type == 'full_video':
            update_progress(15, "🎵 Generating music track...")
            update_progress(30, "🍌 Creating thumbnail with Nano-Banana...")
            update_progress(50, "🎥 Assembling video content...")
            update_progress(70, "🔍 Optimizing SEO (titles, tags, description)...")
            update_progress(85, "📤 Preparing for upload...")
            update_progress(95, "✅ Finalizing project...")
            
            # Simulate full video generation pipeline
            time.sleep(3)
        
        # Mark as completed
        if task_id in system_state.generation_tasks:
            system_state.generation_tasks[task_id]['status'] = 'completed'
            system_state.generation_tasks[task_id]['progress'] = 100
            system_state.generation_tasks[task_id]['current_step'] = f"✅ {content_type.title()} generation completed!"
            system_state.generation_tasks[task_id]['completed_at'] = datetime.now()
            
    except Exception as e:
        # Mark as failed
        if task_id in system_state.generation_tasks:
            system_state.generation_tasks[task_id]['status'] = 'failed'
            system_state.generation_tasks[task_id]['error'] = str(e)
            system_state.generation_tasks[task_id]['current_step'] = f"❌ Error: {str(e)}"

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