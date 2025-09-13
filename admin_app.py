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
    
    # Store task info
    system_state.generation_tasks[task_id] = {
        'id': task_id,
        'status': 'queued',
        'progress': 0,
        'current_step': 'Initializing...',
        'logs': [],
        'parameters': data,
        'created_at': datetime.now().isoformat(),
        'result': None
    }
    
    # Start generation in background thread
    def run_generation():
        # Import and run the generation pipeline
        from main import run_creation_pipeline
        
        try:
            system_state.generation_tasks[task_id]['status'] = 'running'
            
            # Mock implementation - replace with actual generation
            for i in range(10):
                system_state.generation_tasks[task_id]['progress'] = (i + 1) * 10
                system_state.generation_tasks[task_id]['current_step'] = f'Step {i+1}/10'
                time.sleep(1)
            
            system_state.generation_tasks[task_id]['status'] = 'completed'
            system_state.generation_tasks[task_id]['result'] = {'success': True}
            
        except Exception as e:
            system_state.generation_tasks[task_id]['status'] = 'failed'
            system_state.generation_tasks[task_id]['result'] = {'success': False, 'error': str(e)}
    
    thread = threading.Thread(target=run_generation, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'task_id': task_id})

@app.route('/api/generate/status/<task_id>')
@require_auth
def api_generation_status(task_id):
    """Get generation task status"""
    task = system_state.generation_tasks.get(task_id, {})
    return jsonify(task)

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