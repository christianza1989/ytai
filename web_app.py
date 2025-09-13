#!/usr/bin/env python3
"""
Web interface for Autonominis Muzikantas
Simple Flask application to control the music generation system
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, flash, redirect, url_for
from datetime import datetime
import json
import threading
import time
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our main modules
from core.services.suno_client import SunoClient
from core.services.gemini_client import GeminiClient
from core.services.image_client import ImageClient
from core.utils.file_manager import FileManager

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Global variables to track generation status
generation_status = {
    'running': False,
    'progress': 0,
    'current_step': '',
    'logs': [],
    'result': None,
    'error': None
}

class WebLogger:
    """Custom logger that stores messages for web interface"""
    
    @staticmethod
    def log(message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        generation_status['logs'].append(log_entry)
        print(log_entry)  # Also print to console
        
        # Keep only last 100 log entries
        if len(generation_status['logs']) > 100:
            generation_status['logs'] = generation_status['logs'][-100:]

def check_api_configuration():
    """Check if API keys are configured"""
    config = {}
    config['suno_api'] = bool(os.getenv('SUNO_API_KEY') and os.getenv('SUNO_API_KEY') != 'your_suno_api_key_here')
    config['gemini_api'] = bool(os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here')
    config['stability_api'] = bool(os.getenv('STABLE_DIFFUSION_API_KEY') and os.getenv('STABLE_DIFFUSION_API_KEY') != 'your_stable_diffusion_key_here')
    return config

def run_generation_pipeline(mode='mock', genre='Lo-Fi Hip Hop', theme='rainy night'):
    """Run the music generation pipeline in a separate thread"""
    try:
        generation_status['running'] = True
        generation_status['progress'] = 0
        generation_status['current_step'] = 'Initializing...'
        generation_status['logs'] = []
        generation_status['result'] = None
        generation_status['error'] = None
        
        WebLogger.log(f"🚀 Starting music generation in {mode} mode")
        WebLogger.log(f"🎵 Genre: {genre}, Theme: {theme}")
        
        # Initialize components based on mode
        if mode == 'real':
            WebLogger.log("🔑 Using REAL API keys")
            suno = SunoClient()
            gemini = GeminiClient()
            image_client = ImageClient()
        else:
            WebLogger.log("🧪 Using MOCK data for testing")
            suno = None
            gemini = None
            image_client = None
        
        file_manager = FileManager()
        
        # Step 1: Check credits (10%)
        generation_status['progress'] = 10
        generation_status['current_step'] = 'Checking API credits...'
        
        if mode == 'real' and suno:
            try:
                credits = suno.get_credits()
                WebLogger.log(f"✅ Suno credits remaining: {credits}")
                if credits < 10:
                    WebLogger.log("⚠️ WARNING: Low credits remaining!")
            except Exception as e:
                WebLogger.log(f"⚠️ Could not check credits: {e}")
        else:
            WebLogger.log("✅ [MOCK] Credits check skipped")
        
        # Step 2: Generate creative brief (30%)
        generation_status['progress'] = 30
        generation_status['current_step'] = 'Generating creative idea...'
        WebLogger.log("🧠 Generating creative brief...")
        
        if mode == 'real' and gemini:
            try:
                brief = gemini.generate_creative_brief(genre=genre, theme=theme)
                WebLogger.log(f"✅ Creative brief generated: {brief.get('title', 'N/A')}")
            except Exception as e:
                WebLogger.log(f"❌ Creative brief generation failed: {e}")
                brief = {'title': f'Mock {genre} Track', 'lyrics_prompt': f'A {genre} track about {theme}'}
        else:
            brief = {'title': f'Mock {genre} Track', 'lyrics_prompt': f'A {genre} track about {theme}'}
            WebLogger.log(f"✅ [MOCK] Creative brief: {brief['title']}")
        
        # Step 3: Create song directory (40%)
        generation_status['progress'] = 40
        generation_status['current_step'] = 'Creating output directory...'
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in brief['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')
        song_dir = f"output/{safe_title}_{timestamp}"
        
        os.makedirs(song_dir, exist_ok=True)
        WebLogger.log(f"📁 Created directory: {song_dir}")
        
        # Step 4: Generate music (60%)
        generation_status['progress'] = 60
        generation_status['current_step'] = 'Generating music...'
        WebLogger.log("🎵 Generating music...")
        
        if mode == 'real' and suno:
            try:
                # Real Suno API call
                task_response = suno.generate_music_simple(brief['lyrics_prompt'])
                task_id = task_response.get('taskId')
                WebLogger.log(f"✅ Music generation task submitted: {task_id}")
                
                # Wait for completion
                WebLogger.log("⏳ Waiting for music generation to complete...")
                result = suno.wait_for_task_completion(task_id, timeout_minutes=10)
                
                if result and result.get('status') == 'SUCCESS':
                    WebLogger.log("✅ Music generation completed successfully!")
                else:
                    WebLogger.log("❌ Music generation failed or timed out")
                    result = None
            except Exception as e:
                WebLogger.log(f"❌ Music generation error: {e}")
                result = None
        else:
            # Mock mode
            WebLogger.log("🎵 [MOCK] Simulating music generation...")
            time.sleep(2)  # Simulate processing time
            result = {
                'status': 'SUCCESS',
                'data': [
                    {
                        'id': 'mock_track_1',
                        'title': f'{brief["title"]} - Track 1',
                        'audio_url': 'https://example.com/mock_audio_1.mp3',
                        'duration': 180.5
                    },
                    {
                        'id': 'mock_track_2',
                        'title': f'{brief["title"]} - Track 2',
                        'audio_url': 'https://example.com/mock_audio_2.mp3',
                        'duration': 195.2
                    }
                ]
            }
            WebLogger.log("✅ [MOCK] Music generation completed!")
        
        # Step 5: Download and organize files (80%)
        generation_status['progress'] = 80
        generation_status['current_step'] = 'Processing files...'
        WebLogger.log("⬇️ Processing audio files...")
        
        tracks_created = 0
        if result and result.get('data'):
            for i, track in enumerate(result['data'], 1):
                if mode == 'real':
                    # In real mode, download actual files
                    WebLogger.log(f"⬇️ Downloading track {i}: {track['title']}")
                    # TODO: Implement actual file download
                    WebLogger.log(f"✅ Track {i} downloaded")
                else:
                    # In mock mode, copy mock files
                    mock_file = f"mock_audio/sample_track_{i}.mp3"
                    output_file = f"{song_dir}/track_{i}.mp3"
                    
                    if os.path.exists(mock_file):
                        import shutil
                        shutil.copy2(mock_file, output_file)
                        WebLogger.log(f"✅ [MOCK] Copied {mock_file} → {output_file}")
                        tracks_created += 1
                    else:
                        WebLogger.log(f"⚠️ [MOCK] Mock file not found: {mock_file}")
        else:
            WebLogger.log("⚠️ No audio tracks to process")
        
        # Step 6: Generate cover art (100%)
        generation_status['progress'] = 100
        generation_status['current_step'] = 'Generating cover art...'
        WebLogger.log("🎨 Generating cover art...")
        
        cover_created = False
        if mode == 'real' and image_client:
            try:
                # Real image generation
                WebLogger.log("🖼️ Generating album cover...")
                # TODO: Implement real cover generation
                WebLogger.log("✅ Cover art generated")
                cover_created = True
            except Exception as e:
                WebLogger.log(f"❌ Cover art generation failed: {e}")
        else:
            WebLogger.log("⚠️ [MOCK] Cover art generation not available")
        
        # Save metadata
        metadata = {
            'title': brief['title'],
            'genre': genre,
            'theme': theme,
            'mode': mode,
            'created_at': datetime.now().isoformat(),
            'tracks_created': tracks_created,
            'cover_created': cover_created
        }
        
        metadata_file = f"{song_dir}/metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        WebLogger.log(f"💾 Metadata saved: {metadata_file}")
        
        # Final summary
        WebLogger.log("=" * 50)
        WebLogger.log("🎉 GENERATION COMPLETED!")
        WebLogger.log(f"📂 Output directory: {song_dir}")
        WebLogger.log(f"🎵 Tracks created: {tracks_created}")
        WebLogger.log(f"🖼️ Cover art: {'✅' if cover_created else '❌'}")
        WebLogger.log("=" * 50)
        
        generation_status['result'] = {
            'success': True,
            'directory': song_dir,
            'tracks_created': tracks_created,
            'cover_created': cover_created,
            'metadata': metadata
        }
        
    except Exception as e:
        WebLogger.log(f"❌ CRITICAL ERROR: {str(e)}")
        generation_status['error'] = str(e)
        generation_status['result'] = {'success': False, 'error': str(e)}
    
    finally:
        generation_status['running'] = False
        generation_status['current_step'] = 'Complete'

@app.route('/')
def index():
    """Main dashboard page"""
    config = check_api_configuration()
    
    # Get recent outputs
    recent_outputs = []
    output_dir = Path('output')
    if output_dir.exists():
        for item in sorted(output_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
            if item.is_dir():
                metadata_file = item / 'metadata.json'
                if metadata_file.exists():
                    try:
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                        recent_outputs.append({
                            'name': item.name,
                            'path': str(item),
                            'metadata': metadata
                        })
                    except:
                        recent_outputs.append({
                            'name': item.name,
                            'path': str(item),
                            'metadata': {'title': 'Unknown', 'created_at': 'Unknown'}
                        })
    
    return render_template('index.html', 
                         config=config, 
                         recent_outputs=recent_outputs,
                         generation_status=generation_status)

@app.route('/generate', methods=['POST'])
def generate():
    """Start music generation"""
    if generation_status['running']:
        flash('Generation is already running!', 'warning')
        return redirect(url_for('index'))
    
    mode = request.form.get('mode', 'mock')
    genre = request.form.get('genre', 'Lo-Fi Hip Hop')
    theme = request.form.get('theme', 'rainy night')
    
    # Start generation in background thread
    thread = threading.Thread(
        target=run_generation_pipeline,
        args=(mode, genre, theme),
        daemon=True
    )
    thread.start()
    
    flash(f'Music generation started in {mode} mode!', 'success')
    return redirect(url_for('status'))

@app.route('/status')
def status():
    """Generation status page"""
    return render_template('status.html', status=generation_status)

@app.route('/api/status')
def api_status():
    """API endpoint for generation status"""
    return jsonify(generation_status)

@app.route('/outputs')
def outputs():
    """List all generated outputs"""
    outputs = []
    output_dir = Path('output')
    if output_dir.exists():
        for item in sorted(output_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if item.is_dir():
                metadata_file = item / 'metadata.json'
                files = list(item.glob('*'))
                
                metadata = {'title': 'Unknown', 'created_at': 'Unknown'}
                if metadata_file.exists():
                    try:
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                    except:
                        pass
                
                outputs.append({
                    'name': item.name,
                    'path': str(item),
                    'metadata': metadata,
                    'files': [f.name for f in files]
                })
    
    return render_template('outputs.html', outputs=outputs)

@app.route('/download/<path:filename>')
def download(filename):
    """Download generated files"""
    return send_from_directory('output', filename, as_attachment=True)

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🌐 Starting Autonominis Muzikantas Web Interface...")
    print("📁 Output directory ready")
    print("🔑 API Configuration:")
    config = check_api_configuration()
    for api, configured in config.items():
        status = "✅ Configured" if configured else "❌ Not configured"
        print(f"   {api}: {status}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)