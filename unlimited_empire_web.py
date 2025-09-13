#!/usr/bin/env python3
"""
🌐 UNLIMITED EMPIRE WEB INTERFACE
Web interface for AI Channel Generator and unlimited empire scaling
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_channel_generator import AIChannelGenerator, EmpireScaler

app = Flask(__name__)
app.secret_key = 'unlimited_empire_secret'

# Global instances
generator = AIChannelGenerator()
scaler = EmpireScaler()

@app.route('/unlimited')
def unlimited_dashboard():
    """Main dashboard for unlimited empire"""
    try:
        # Get empire statistics
        stats = generator.get_empire_stats()
        
        # Get recent concepts
        recent_concepts = generator.get_all_concepts()[:10]
        
        # Get suggestions for next channels
        suggestions = generator.suggest_next_channels(stats['active_channels'])
        
        return render_template('unlimited_dashboard.html', 
                             stats=stats, 
                             recent_concepts=recent_concepts,
                             suggestions=suggestions)
    except Exception as e:
        flash(f'Error loading dashboard: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/unlimited/generate', methods=['GET', 'POST'])
def generate_channel():
    """Generate new channel concept"""
    if request.method == 'POST':
        try:
            category = request.form.get('category', None)
            
            # Generate concept
            result = generator.generate_channel_concept(category)
            
            if result['success']:
                flash(f'Generated concept: {result["concept"]["channel_name"]}', 'success')
                return redirect(url_for('view_concept', concept_id=result['concept']['id']))
            else:
                flash(f'Generation failed: {result["error"]}', 'error')
                
        except Exception as e:
            flash(f'Error generating concept: {e}', 'error')
    
    # GET request - show generation form
    categories = list(generator.genre_categories.keys())
    return render_template('generate_channel.html', categories=categories)

@app.route('/unlimited/concept/<int:concept_id>')
def view_concept(concept_id):
    """View detailed concept"""
    try:
        concepts = generator.get_all_concepts()
        concept = next((c for c in concepts if c['id'] == concept_id), None)
        
        if not concept:
            flash('Concept not found', 'error')
            return redirect(url_for('unlimited_dashboard'))
            
        return render_template('concept_details.html', concept=concept)
        
    except Exception as e:
        flash(f'Error loading concept: {e}', 'error')
        return redirect(url_for('unlimited_dashboard'))

@app.route('/unlimited/batch_generate', methods=['GET', 'POST'])
def batch_generate():
    """Generate multiple concepts at once"""
    if request.method == 'POST':
        try:
            count = int(request.form.get('count', 5))
            categories = request.form.getlist('categories')
            
            if not categories:
                categories = None
            
            # Generate batch
            concepts = generator.generate_batch_concepts(count, categories)
            
            flash(f'Generated {len(concepts)} channel concepts', 'success')
            return redirect(url_for('unlimited_dashboard'))
            
        except Exception as e:
            flash(f'Batch generation failed: {e}', 'error')
    
    categories = list(generator.genre_categories.keys())
    return render_template('batch_generate.html', categories=categories)

@app.route('/unlimited/expansion_plan')
def expansion_plan():
    """Generate expansion plan for unlimited empire"""
    try:
        target_channels = int(request.args.get('target', 50))
        target_revenue = float(request.args.get('revenue', 50000))
        
        # Generate expansion plan
        plan_result = scaler.auto_generate_expansion_plan(target_channels, target_revenue)
        
        if plan_result['success']:
            plan = plan_result['expansion_plan']
            return render_template('expansion_plan.html', plan=plan)
        else:
            flash('Failed to generate expansion plan', 'error')
            return redirect(url_for('unlimited_dashboard'))
            
    except Exception as e:
        flash(f'Error generating expansion plan: {e}', 'error')
        return redirect(url_for('unlimited_dashboard'))

@app.route('/unlimited/api/approve_concept', methods=['POST'])
def api_approve_concept():
    """API endpoint to approve concept"""
    try:
        data = request.get_json()
        concept_id = data.get('concept_id')
        
        result = generator.approve_concept(concept_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/unlimited/api/register_channel', methods=['POST'])
def api_register_channel():
    """API endpoint to register created channel"""
    try:
        data = request.get_json()
        concept_id = data.get('concept_id')
        youtube_channel_id = data.get('youtube_channel_id')
        
        result = generator.register_created_channel(concept_id, youtube_channel_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/unlimited/api/generate_single', methods=['POST'])
def api_generate_single():
    """API endpoint for single concept generation"""
    try:
        data = request.get_json()
        category = data.get('category', None)
        
        result = generator.generate_channel_concept(category)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/unlimited/api/empire_stats')
def api_empire_stats():
    """API endpoint for empire statistics"""
    try:
        stats = generator.get_empire_stats()
        return jsonify({'success': True, 'stats': stats})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/unlimited/channel_setup/<int:concept_id>')
def channel_setup_guide(concept_id):
    """Step-by-step channel setup guide"""
    try:
        concepts = generator.get_all_concepts()
        concept = next((c for c in concepts if c['id'] == concept_id), None)
        
        if not concept:
            flash('Concept not found', 'error')
            return redirect(url_for('unlimited_dashboard'))
        
        # Generate detailed setup instructions
        setup_guide = {
            'channel_name': concept['channel_name'],
            'description': concept['channel_description'],
            'branding': {
                'colors': concept['branding_colors'],
                'tags': concept['suggested_tags']
            },
            'content_strategy': concept['content_strategy'],
            'monetization': {
                'expected_cpm': concept['expected_cpm'],
                'potential': concept['monetization_potential']
            },
            'steps': [
                {
                    'step': 1,
                    'title': 'Create YouTube Channel',
                    'description': f'Go to YouTube Studio and create channel: "{concept["channel_name"]}"',
                    'estimated_time': '10 minutes'
                },
                {
                    'step': 2, 
                    'title': 'Channel Branding',
                    'description': f'Set up channel art with colors: {", ".join(concept["branding_colors"])}',
                    'estimated_time': '20 minutes'
                },
                {
                    'step': 3,
                    'title': 'Channel Description',
                    'description': concept['channel_description'],
                    'estimated_time': '5 minutes'
                },
                {
                    'step': 4,
                    'title': 'Add to System',
                    'description': 'Copy Channel ID and register in unlimited empire system',
                    'estimated_time': '5 minutes'
                },
                {
                    'step': 5,
                    'title': 'Configure Upload Schedule', 
                    'description': f'Set upload frequency: every {concept["suggested_upload_frequency"]} hours',
                    'estimated_time': '5 minutes'
                }
            ]
        }
        
        return render_template('channel_setup_guide.html', 
                             concept=concept, 
                             guide=setup_guide)
        
    except Exception as e:
        flash(f'Error loading setup guide: {e}', 'error')
        return redirect(url_for('unlimited_dashboard'))

# HTML Templates (inline for now - should be in templates/ folder)
def create_templates():
    """Create HTML templates"""
    templates = {
        'unlimited_dashboard.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>Unlimited Empire Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; }
        .btn { padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }
        .btn:hover { background: #0056b3; }
        .concept-item { border-bottom: 1px solid #eee; padding: 10px 0; }
        .concept-item:last-child { border-bottom: none; }
        .badge { padding: 3px 8px; border-radius: 15px; font-size: 12px; }
        .badge-concept { background: #ffc107; color: black; }
        .badge-approved { background: #28a745; color: white; }
        .badge-created { background: #007bff; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏰 Unlimited Empire Dashboard</h1>
        
        <div class="stats-grid">
            <div class="card stat-card">
                <h3>Active Channels</h3>
                <h2>{{ stats.active_channels }}</h2>
                <p>Unlimited Scaling</p>
            </div>
            <div class="card stat-card">
                <h3>Monthly Revenue</h3>
                <h2>${{ "{:,.0f}".format(stats.total_monthly_revenue) }}</h2>
                <p>Growing Empire</p>
            </div>
            <div class="card stat-card">
                <h3>AI Concepts</h3>
                <h2>{{ stats.concepts|length }}</h2>
                <p>Generated Ideas</p>
            </div>
            <div class="card stat-card">
                <h3>Avg Engagement</h3>
                <h2>{{ "{:.1%}".format(stats.average_engagement) }}</h2>
                <p>Performance</p>
            </div>
        </div>
        
        <div class="card">
            <h3>🤖 AI Actions</h3>
            <a href="{{ url_for('generate_channel') }}" class="btn">🎯 Generate Single Channel</a>
            <a href="{{ url_for('batch_generate') }}" class="btn">🚀 Batch Generate (5x)</a>
            <a href="{{ url_for('expansion_plan') }}" class="btn">📈 Create Expansion Plan</a>
        </div>
        
        <div class="card">
            <h3>📋 Recent Channel Concepts</h3>
            {% for concept in recent_concepts %}
            <div class="concept-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{{ concept.channel_name }}</strong>
                        <span class="badge badge-{{ concept.status }}">{{ concept.status }}</span>
                        <br>
                        <small>{{ concept.specific_genre }} • {{ concept.target_audience }}</small>
                    </div>
                    <div>
                        <span>${{ concept.expected_cpm }}</span>
                        <a href="{{ url_for('view_concept', concept_id=concept.id) }}" class="btn" style="padding: 5px 10px; font-size: 12px;">View</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        {% if suggestions %}
        <div class="card">
            <h3>💡 AI Suggestions for Next Channels</h3>
            {% for suggestion in suggestions %}
            <div class="concept-item">
                <strong>{{ suggestion.channel_name }}</strong>
                <br>
                <small>{{ suggestion.specific_genre }} • Expected CPM: ${{ suggestion.expected_cpm }}</small>
                <br>
                <small>🎯 {{ suggestion.suggestion_reason }}</small>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>''',
        
        'generate_channel.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>Generate AI Channel Concept</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        select, input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .btn { padding: 12px 30px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .btn:hover { background: #0056b3; }
        .category-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin: 10px 0; }
        .category-item { padding: 10px; background: #f8f9fa; border-radius: 5px; text-align: center; cursor: pointer; border: 2px solid transparent; }
        .category-item:hover { border-color: #007bff; }
        .category-item.selected { background: #007bff; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🤖 Generate AI Channel Concept</h1>
            
            <form method="POST">
                <div class="form-group">
                    <label>Select Category (or leave blank for random):</label>
                    <div class="category-grid">
                        <div class="category-item" onclick="selectCategory('')">
                            🎲 Random
                        </div>
                        {% for category in categories %}
                        <div class="category-item" onclick="selectCategory('{{ category }}')">
                            {{ category }}
                        </div>
                        {% endfor %}
                    </div>
                    <input type="hidden" name="category" id="selectedCategory">
                </div>
                
                <button type="submit" class="btn">🎯 Generate Channel Concept</button>
            </form>
            
            <div style="margin-top: 30px;">
                <h3>What happens next:</h3>
                <ol>
                    <li>AI analyzes market gaps and trends</li>
                    <li>Generates unique channel name and concept</li>
                    <li>Creates branding suggestions and strategy</li>
                    <li>Provides setup instructions</li>
                    <li>You create the actual YouTube channel</li>
                    <li>Register channel in unlimited empire system</li>
                </ol>
            </div>
        </div>
    </div>
    
    <script>
        function selectCategory(category) {
            document.getElementById('selectedCategory').value = category;
            
            // Update visual selection
            document.querySelectorAll('.category-item').forEach(item => {
                item.classList.remove('selected');
            });
            event.target.classList.add('selected');
        }
    </script>
</body>
</html>'''
    }
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Write templates to files
    for filename, content in templates.items():
        with open(f'templates/{filename}', 'w') as f:
            f.write(content)

if __name__ == '__main__':
    # Create templates
    create_templates()
    
    # Run the app
    print("🌐 Starting Unlimited Empire Web Interface...")
    print("🔗 Access at: http://localhost:5001/unlimited")
    
    app.run(host='0.0.0.0', port=5001, debug=True)