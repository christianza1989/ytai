#!/usr/bin/env python3
"""
🤖 24/7 AUTONOMOUS EMPIRE WEB DASHBOARD
Complete control panel for fully automated AI music empire
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autonomous_empire_24_7 import start_empire, stop_empire, get_empire_status, autonomous_empire

app = Flask(__name__)
app.secret_key = "autonomous_empire_secret_key_2024"

@app.route('/')
def dashboard():
    """Main autonomous empire dashboard"""
    try:
        # Get system status
        status = get_empire_status()
        
        # Get recent activity
        recent_beats = get_recent_beats(limit=10)
        
        # Get performance metrics
        metrics = get_performance_metrics()
        
        # Get YouTube accounts status
        youtube_accounts = get_youtube_accounts_status()
        
        return render_template('autonomous_dashboard.html',
                             status=status,
                             recent_beats=recent_beats,
                             metrics=metrics,
                             youtube_accounts=youtube_accounts)
    except Exception as e:
        flash(f"Dashboard error: {e}", 'error')
        return render_template('autonomous_dashboard.html', 
                             status={'system_running': False},
                             recent_beats=[],
                             metrics={},
                             youtube_accounts=[])

@app.route('/start_empire', methods=['POST'])
def start_empire_route():
    """Start the autonomous empire system"""
    try:
        empire = start_empire()
        flash('🚀 Autonomous Empire started! System is now running 24/7', 'success')
    except Exception as e:
        flash(f'❌ Failed to start empire: {e}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/stop_empire', methods=['POST'])  
def stop_empire_route():
    """Stop the autonomous empire system"""
    try:
        stop_empire()
        flash('🛑 Autonomous Empire stopped', 'info')
    except Exception as e:
        flash(f'❌ Failed to stop empire: {e}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/api/status')
def api_status():
    """API endpoint for real-time status"""
    return jsonify(get_empire_status())

@app.route('/api/recent_activity')
def api_recent_activity():
    """API endpoint for recent activity"""
    return jsonify({
        'recent_beats': get_recent_beats(limit=20),
        'recent_uploads': get_recent_uploads(limit=10)
    })

@app.route('/api/performance_metrics')
def api_performance_metrics():
    """API endpoint for performance metrics"""
    return jsonify(get_performance_metrics())

@app.route('/beats_library')
def beats_library():
    """View all generated beats"""
    try:
        conn = sqlite3.connect('autonomous_empire.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT beat_id, genre, prompt, generated_at, upload_status, 
                   youtube_account, views, revenue, performance_score
            FROM generated_beats 
            ORDER BY generated_at DESC 
            LIMIT 100
        ''')
        
        beats = []
        for row in cursor.fetchall():
            beats.append({
                'beat_id': row[0],
                'genre': row[1], 
                'prompt': row[2][:100] + '...' if len(row[2]) > 100 else row[2],
                'generated_at': row[3],
                'upload_status': row[4],
                'youtube_account': row[5],
                'views': row[6] or 0,
                'revenue': row[7] or 0.0,
                'performance_score': row[8] or 0.0
            })
        
        conn.close()
        
        return render_template('beats_library.html', beats=beats)
        
    except Exception as e:
        flash(f'❌ Library error: {e}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/youtube_accounts')
def youtube_accounts_page():
    """Manage YouTube accounts"""
    accounts = get_youtube_accounts_status()
    return render_template('youtube_accounts.html', accounts=accounts)

@app.route('/add_youtube_account', methods=['POST'])
def add_youtube_account():
    """Add new YouTube account"""
    try:
        account_name = request.form.get('account_name')
        specialization = request.form.get('specialization') 
        upload_schedule = request.form.get('upload_schedule')
        
        conn = sqlite3.connect('autonomous_empire.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO youtube_accounts 
            (account_name, specialization, upload_schedule, status)
            VALUES (?, ?, ?, 'active')
        ''', (account_name, specialization, upload_schedule))
        
        conn.commit()
        conn.close()
        
        flash(f'✅ YouTube account "{account_name}" added successfully!', 'success')
        
    except Exception as e:
        flash(f'❌ Failed to add account: {e}', 'error')
    
    return redirect(url_for('youtube_accounts_page'))

@app.route('/analytics')
def analytics_page():
    """Detailed analytics dashboard"""
    try:
        # Get comprehensive analytics
        analytics_data = get_comprehensive_analytics()
        
        return render_template('analytics.html', analytics=analytics_data)
        
    except Exception as e:
        flash(f'❌ Analytics error: {e}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/settings')
def settings_page():
    """Empire settings and configuration"""
    try:
        # Load current configuration
        if os.path.exists('empire_config.json'):
            with open('empire_config.json', 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        return render_template('settings.html', config=config)
        
    except Exception as e:
        flash(f'❌ Settings error: {e}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/update_settings', methods=['POST'])
def update_settings():
    """Update empire settings"""
    try:
        # Get form data
        config = {
            'generation_schedule': {
                'interval_hours': int(request.form.get('interval_hours', 4)),
                'beats_per_session': int(request.form.get('beats_per_session', 3))
            },
            'upload_schedule': {
                'stagger_minutes': int(request.form.get('stagger_minutes', 30)),
                'daily_limit_per_account': int(request.form.get('daily_limit', 5))
            },
            'safety': {
                'max_daily_uploads': int(request.form.get('max_daily_uploads', 50))
            }
        }
        
        # Save configuration
        with open('empire_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        flash('⚙️ Settings updated successfully!', 'success')
        
    except Exception as e:
        flash(f'❌ Failed to update settings: {e}', 'error')
    
    return redirect(url_for('settings_page'))

@app.route('/logs')
def logs_page():
    """View system logs"""
    try:
        log_file = 'autonomous_empire.log'
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()[-100:]  # Last 100 lines
        else:
            logs = ['No logs available yet.']
        
        return render_template('logs.html', logs=logs)
        
    except Exception as e:
        flash(f'❌ Logs error: {e}', 'error')
        return redirect(url_for('dashboard'))

def get_recent_beats(limit=10):
    """Get recent generated beats"""
    try:
        conn = sqlite3.connect('autonomous_empire.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT beat_id, genre, generated_at, upload_status, views, revenue
            FROM generated_beats 
            ORDER BY generated_at DESC 
            LIMIT ?
        ''', (limit,))
        
        beats = []
        for row in cursor.fetchall():
            beats.append({
                'beat_id': row[0],
                'genre': row[1],
                'generated_at': row[2],
                'upload_status': row[3],
                'views': row[4] or 0,
                'revenue': row[5] or 0.0
            })
        
        conn.close()
        return beats
        
    except Exception as e:
        print(f"Error getting recent beats: {e}")
        return []

def get_recent_uploads(limit=10):
    """Get recent uploads"""
    try:
        conn = sqlite3.connect('autonomous_empire.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT beat_id, genre, youtube_account, generated_at, views
            FROM generated_beats 
            WHERE upload_status = 'uploaded'
            ORDER BY generated_at DESC 
            LIMIT ?
        ''', (limit,))
        
        uploads = []
        for row in cursor.fetchall():
            uploads.append({
                'beat_id': row[0],
                'genre': row[1],
                'youtube_account': row[2],
                'uploaded_at': row[3],
                'views': row[4] or 0
            })
        
        conn.close()
        return uploads
        
    except Exception:
        return []

def get_performance_metrics():
    """Get performance metrics"""
    try:
        conn = sqlite3.connect('autonomous_empire.db')
        cursor = conn.cursor()
        
        # Today's stats
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT 
                COUNT(*) as generated_today,
                COUNT(CASE WHEN upload_status = 'uploaded' THEN 1 END) as uploaded_today,
                SUM(views) as views_today,
                SUM(revenue) as revenue_today
            FROM generated_beats 
            WHERE DATE(generated_at) = ?
        ''', (today,))
        
        today_stats = cursor.fetchone()
        
        # Total stats
        cursor.execute('''
            SELECT 
                COUNT(*) as total_beats,
                COUNT(CASE WHEN upload_status = 'uploaded' THEN 1 END) as total_uploaded,
                SUM(views) as total_views,
                SUM(revenue) as total_revenue
            FROM generated_beats
        ''')
        
        total_stats = cursor.fetchone()
        
        # Genre performance
        cursor.execute('''
            SELECT genre, COUNT(*), AVG(views), SUM(revenue)
            FROM generated_beats 
            WHERE upload_status = 'uploaded'
            GROUP BY genre 
            ORDER BY SUM(revenue) DESC
        ''')
        
        genre_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'today': {
                'generated': today_stats[0] or 0,
                'uploaded': today_stats[1] or 0,
                'views': today_stats[2] or 0,
                'revenue': today_stats[3] or 0.0
            },
            'total': {
                'beats': total_stats[0] or 0,
                'uploaded': total_stats[1] or 0,
                'views': total_stats[2] or 0,
                'revenue': total_stats[3] or 0.0
            },
            'top_genres': [
                {
                    'genre': row[0],
                    'beats': row[1],
                    'avg_views': row[2] or 0,
                    'revenue': row[3] or 0.0
                }
                for row in genre_stats[:5]
            ]
        }
        
    except Exception as e:
        print(f"Error getting metrics: {e}")
        return {'today': {}, 'total': {}, 'top_genres': []}

def get_youtube_accounts_status():
    """Get YouTube accounts status"""
    try:
        conn = sqlite3.connect('autonomous_empire.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_name, specialization, upload_schedule, 
                   total_videos, total_views, total_revenue, last_upload, status
            FROM youtube_accounts
        ''')
        
        accounts = []
        for row in cursor.fetchall():
            accounts.append({
                'name': row[0],
                'specialization': row[1], 
                'schedule': row[2],
                'total_videos': row[3] or 0,
                'total_views': row[4] or 0,
                'total_revenue': row[5] or 0.0,
                'last_upload': row[6],
                'status': row[7]
            })
        
        conn.close()
        return accounts
        
    except Exception as e:
        print(f"Error getting YouTube accounts: {e}")
        return []

def get_comprehensive_analytics():
    """Get comprehensive analytics data"""
    try:
        conn = sqlite3.connect('autonomous_empire.db')
        cursor = conn.cursor()
        
        # Daily performance over last 30 days
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT DATE(generated_at) as date, 
                   COUNT(*) as beats_generated,
                   COUNT(CASE WHEN upload_status = 'uploaded' THEN 1 END) as beats_uploaded,
                   SUM(views) as daily_views,
                   SUM(revenue) as daily_revenue
            FROM generated_beats 
            WHERE DATE(generated_at) >= ?
            GROUP BY DATE(generated_at)
            ORDER BY date DESC
        ''', (thirty_days_ago,))
        
        daily_stats = cursor.fetchall()
        
        # Hourly generation pattern
        cursor.execute('''
            SELECT strftime('%H', generated_at) as hour, COUNT(*) as count
            FROM generated_beats
            GROUP BY hour
            ORDER BY hour
        ''')
        
        hourly_pattern = cursor.fetchall()
        
        conn.close()
        
        return {
            'daily_performance': [
                {
                    'date': row[0],
                    'generated': row[1],
                    'uploaded': row[2], 
                    'views': row[3] or 0,
                    'revenue': row[4] or 0.0
                }
                for row in daily_stats
            ],
            'hourly_pattern': [
                {'hour': int(row[0]), 'count': row[1]}
                for row in hourly_pattern
            ]
        }
        
    except Exception as e:
        print(f"Error getting comprehensive analytics: {e}")
        return {'daily_performance': [], 'hourly_pattern': []}

# Create basic HTML templates if they don't exist
def create_templates():
    """Create basic HTML templates"""
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    # Main dashboard template
    dashboard_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Autonomous AI Music Empire 24/7</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .card h3 { margin-top: 0; color: #333; }
        .status-running { color: #28a745; font-weight: bold; }
        .status-stopped { color: #dc3545; font-weight: bold; }
        .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; text-decoration: none; display: inline-block; }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-secondary { background: #6c757d; color: white; }
        .metrics { display: flex; justify-content: space-between; flex-wrap: wrap; }
        .metric { text-align: center; padding: 10px; }
        .metric-value { font-size: 2em; font-weight: bold; color: #007bff; }
        .metric-label { color: #666; font-size: 0.9em; }
        .recent-beats { max-height: 400px; overflow-y: auto; }
        .beat-item { padding: 10px; border-bottom: 1px solid #eee; }
        .flash-messages { margin-bottom: 20px; }
        .alert { padding: 10px; margin-bottom: 10px; border-radius: 5px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .alert-info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .auto-refresh { position: fixed; top: 20px; right: 20px; background: rgba(0,0,0,0.8); color: white; padding: 10px; border-radius: 5px; }
    </style>
    <script>
        // Auto-refresh status every 30 seconds
        setInterval(function() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('system-status').innerHTML = 
                        data.system_running ? '<span class="status-running">🟢 RUNNING 24/7</span>' : '<span class="status-stopped">🔴 STOPPED</span>';
                    document.getElementById('total-beats').textContent = data.total_beats_generated || 0;
                    document.getElementById('total-uploaded').textContent = data.total_beats_uploaded || 0;
                    document.getElementById('total-revenue').textContent = '$' + (data.total_revenue || 0).toFixed(2);
                });
        }, 30000);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AUTONOMOUS AI MUSIC EMPIRE 24/7</h1>
            <p>Fully Automated Beat Generation & YouTube Upload System</p>
            <div id="system-status">
                {% if status.system_running %}
                    <span class="status-running">🟢 RUNNING 24/7</span>
                {% else %}
                    <span class="status-stopped">🔴 STOPPED</span>
                {% endif %}
            </div>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        <div class="cards">
            <div class="card">
                <h3>🎛️ Empire Controls</h3>
                {% if not status.system_running %}
                    <form method="POST" action="/start_empire" style="display: inline;">
                        <button type="submit" class="btn btn-success">🚀 START EMPIRE</button>
                    </form>
                    <p>Start the fully autonomous 24/7 system. Once started, it will:</p>
                    <ul>
                        <li>🎵 Auto-generate beats every 4 hours</li>
                        <li>📺 Auto-upload to YouTube accounts</li>
                        <li>🔧 Auto-optimize based on performance</li>
                        <li>💰 Auto-track revenue and analytics</li>
                    </ul>
                {% else %}
                    <form method="POST" action="/stop_empire" style="display: inline;">
                        <button type="submit" class="btn btn-danger">🛑 STOP EMPIRE</button>
                    </form>
                    <p>✅ System is running autonomously!</p>
                    <p>🤖 No manual intervention required</p>
                {% endif %}
                
                <div style="margin-top: 15px;">
                    <a href="/settings" class="btn btn-secondary">⚙️ Settings</a>
                    <a href="/logs" class="btn btn-secondary">📜 View Logs</a>
                </div>
            </div>
            
            <div class="card">
                <h3>📊 Performance Metrics</h3>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value" id="total-beats">{{ status.total_beats_generated or 0 }}</div>
                        <div class="metric-label">Total Beats</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="total-uploaded">{{ status.total_beats_uploaded or 0 }}</div>
                        <div class="metric-label">Uploaded</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="total-revenue">${{ "%.2f"|format(status.total_revenue or 0) }}</div>
                        <div class="metric-label">Revenue</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{{ status.active_youtube_accounts or 0 }}</div>
                        <div class="metric-label">YT Accounts</div>
                    </div>
                </div>
                
                {% if metrics.today %}
                <h4>Today's Performance:</h4>
                <ul>
                    <li>🎵 Generated: {{ metrics.today.generated }} beats</li>
                    <li>📺 Uploaded: {{ metrics.today.uploaded }} videos</li>
                    <li>👀 Views: {{ metrics.today.views }}</li>
                    <li>💰 Revenue: ${{ "%.2f"|format(metrics.today.revenue) }}</li>
                </ul>
                {% endif %}
                
                <a href="/analytics" class="btn btn-primary">📈 Detailed Analytics</a>
            </div>
            
            <div class="card">
                <h3>📺 YouTube Accounts</h3>
                {% if youtube_accounts %}
                    {% for account in youtube_accounts %}
                    <div style="padding: 5px 0; border-bottom: 1px solid #eee;">
                        <strong>{{ account.name }}</strong><br>
                        <small>{{ account.specialization }} | {{ account.total_videos }} videos | ${{ "%.2f"|format(account.total_revenue) }}</small>
                    </div>
                    {% endfor %}
                {% else %}
                    <p>No accounts configured yet.</p>
                {% endif %}
                <div style="margin-top: 10px;">
                    <a href="/youtube_accounts" class="btn btn-primary">🎬 Manage Accounts</a>
                </div>
            </div>
            
            <div class="card">
                <h3>🎵 Recent Beats</h3>
                <div class="recent-beats">
                    {% if recent_beats %}
                        {% for beat in recent_beats %}
                        <div class="beat-item">
                            <strong>{{ beat.beat_id }}</strong><br>
                            <small>{{ beat.genre }} | {{ beat.upload_status }} | {{ beat.generated_at }}</small>
                        </div>
                        {% endfor %}
                    {% else %}
                        <p>No beats generated yet.</p>
                    {% endif %}
                </div>
                <a href="/beats_library" class="btn btn-primary">🎼 Full Library</a>
            </div>
        </div>
        
        <div class="card">
            <h3>🚀 Quick Start Guide</h3>
            <ol>
                <li><strong>Setup APIs:</strong> Add GEMINI_API_KEY and SUNO_API_KEY to .env file</li>
                <li><strong>Configure Accounts:</strong> Set up YouTube accounts in the accounts section</li>
                <li><strong>Start Empire:</strong> Click "START EMPIRE" button above</li>
                <li><strong>Monitor:</strong> Watch the system work automatically 24/7</li>
                <li><strong>Profit:</strong> Revenue will be tracked automatically</li>
            </ol>
            
            {% if not status.has_real_apis %}
            <div style="background: #fff3cd; padding: 10px; border-radius: 5px; margin-top: 10px;">
                <strong>⚠️ Mock Mode:</strong> Configure real API keys for full automation.
                <br>Current mode generates demo content for testing the workflow.
            </div>
            {% endif %}
        </div>
    </div>
    
    <div class="auto-refresh">
        🔄 Auto-refreshing every 30s
    </div>
</body>
</html>
    '''
    
    with open('templates/autonomous_dashboard.html', 'w') as f:
        f.write(dashboard_html)

if __name__ == '__main__':
    # Create templates
    create_templates()
    
    print("🤖 Starting Autonomous Empire Dashboard...")
    print("🌐 Dashboard will be available at: http://localhost:8002")
    print("📊 Full control of your 24/7 AI Music Empire!")
    
    app.run(host='0.0.0.0', port=8002, debug=False, threaded=True)