#!/usr/bin/env python3
"""
Gemini 2.5 Flash Image Generator (nano-banana)
State-of-the-art image generation and editing with Gemini's world knowledge
"""

import os
import sys
import json
import time
import base64
import secrets
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import requests
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'generated_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

class NanoBananaGenerator:
    """Advanced Gemini 2.5 Flash Image Generator"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = "gemini-2.5-flash-image-preview"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.generation_history = []
        
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def encode_image_to_base64(self, image_path):
        """Convert image to base64 for API"""
        try:
            with open(image_path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None
    
    def generate_image_with_gemini(self, prompt, input_images=None, generation_type="text_to_image"):
        """Generate image using Gemini 2.5 Flash Image API"""
        try:
            if not self.api_key or self.api_key == 'your_gemini_api_key_here':
                return self._mock_generation(prompt, input_images, generation_type)
            
            # Prepare API request
            url = f"{self.base_url}/models/{self.model_name}:generateContent"
            
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': self.api_key
            }
            
            # Build content array
            contents = [{"text": prompt}]
            
            # Add input images if provided
            if input_images:
                for img_path in input_images:
                    img_base64 = self.encode_image_to_base64(img_path)
                    if img_base64:
                        contents.append({
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": img_base64
                            }
                        })
            
            payload = {
                "contents": [{
                    "parts": contents
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return self._process_gemini_response(result, prompt, generation_type)
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._mock_generation(prompt, input_images, generation_type)
                
        except Exception as e:
            print(f"Generation error: {e}")
            return self._mock_generation(prompt, input_images, generation_type)
    
    def _process_gemini_response(self, response, prompt, generation_type):
        """Process API response and extract generated image"""
        try:
            candidates = response.get('candidates', [])
            if not candidates:
                return None
            
            parts = candidates[0].get('content', {}).get('parts', [])
            
            for part in parts:
                if 'inline_data' in part:
                    # Extract generated image data
                    image_data = part['inline_data']['data']
                    
                    # Decode and save image
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(BytesIO(image_bytes))
                    
                    # Generate unique filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"nano_banana_{timestamp}_{secrets.token_hex(4)}.png"
                    output_path = os.path.join(OUTPUT_FOLDER, filename)
                    
                    # Save image
                    image.save(output_path)
                    
                    # Create result object
                    result = {
                        'success': True,
                        'filename': filename,
                        'path': output_path,
                        'prompt': prompt,
                        'generation_type': generation_type,
                        'created_at': datetime.now().isoformat(),
                        'size': f"{image.width}x{image.height}",
                        'model': self.model_name
                    }
                    
                    # Add to history
                    self.generation_history.append(result)
                    
                    return result
            
            return None
            
        except Exception as e:
            print(f"Response processing error: {e}")
            return None
    
    def _mock_generation(self, prompt, input_images, generation_type):
        """Mock generation for testing without API key"""
        try:
            # Create a simple colored rectangle as mock image
            from PIL import Image, ImageDraw, ImageFont
            
            # Create base image
            width, height = 512, 512
            image = Image.new('RGB', (width, height), color=(135, 206, 250))  # Sky blue
            draw = ImageDraw.Draw(image)
            
            # Add some visual elements based on prompt keywords
            if 'cat' in prompt.lower():
                draw.ellipse([200, 200, 300, 280], fill=(255, 165, 0))  # Orange circle for cat
                draw.ellipse([220, 220, 240, 240], fill=(0, 0, 0))      # Eye 1
                draw.ellipse([260, 220, 280, 240], fill=(0, 0, 0))      # Eye 2
            
            if 'nano-banana' in prompt.lower() or 'banana' in prompt.lower():
                draw.ellipse([100, 350, 150, 450], fill=(255, 255, 0))  # Yellow banana shape
            
            if 'restaurant' in prompt.lower():
                draw.rectangle([50, 100, 450, 150], fill=(139, 69, 19))  # Brown table
            
            # Add text overlay
            try:
                draw.text((10, 10), f"MOCK: {prompt[:40]}...", fill=(0, 0, 0))
                draw.text((10, 480), f"Gemini 2.5 Flash Image", fill=(255, 255, 255))
            except:
                pass  # Skip if font issues
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mock_nano_banana_{timestamp}_{secrets.token_hex(4)}.png"
            output_path = os.path.join(OUTPUT_FOLDER, filename)
            
            # Save mock image
            image.save(output_path)
            
            result = {
                'success': True,
                'filename': filename,
                'path': output_path,
                'prompt': prompt,
                'generation_type': generation_type,
                'created_at': datetime.now().isoformat(),
                'size': f"{width}x{height}",
                'model': f"{self.model_name} (MOCK)",
                'mock': True
            }
            
            self.generation_history.append(result)
            return result
            
        except Exception as e:
            print(f"Mock generation error: {e}")
            return None
    
    def edit_image(self, image_path, edit_prompt):
        """Edit existing image with natural language prompt"""
        return self.generate_image_with_gemini(
            prompt=f"Edit this image: {edit_prompt}",
            input_images=[image_path],
            generation_type="image_editing"
        )
    
    def fuse_images(self, image_paths, fusion_prompt):
        """Fuse multiple images into one"""
        return self.generate_image_with_gemini(
            prompt=f"Fuse these images together: {fusion_prompt}",
            input_images=image_paths,
            generation_type="multi_image_fusion"
        )
    
    def maintain_character_consistency(self, reference_image, new_scene_prompt):
        """Generate new image with same character in different scene"""
        return self.generate_image_with_gemini(
            prompt=f"Place this character in a new scene: {new_scene_prompt}. Maintain the exact same character appearance and style.",
            input_images=[reference_image],
            generation_type="character_consistency"
        )

# Initialize generator
generator = NanoBananaGenerator()

@app.route('/')
def index():
    """Main nano-banana generator interface"""
    api_configured = bool(os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here')
    return render_template('nano_banana_index.html', 
                         api_configured=api_configured,
                         recent_generations=generator.generation_history[-5:])

@app.route('/generate', methods=['POST'])
def generate():
    """Generate image from text prompt"""
    try:
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            flash('Please enter a prompt!', 'error')
            return redirect(url_for('index'))
        
        result = generator.generate_image_with_gemini(prompt)
        
        if result and result['success']:
            flash(f'✨ Image generated successfully! ({result.get("model", "Unknown")})', 'success')
            return redirect(url_for('view_result', filename=result['filename']))
        else:
            flash('❌ Image generation failed. Please try again.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit():
    """Edit uploaded image with natural language"""
    try:
        if 'image' not in request.files:
            flash('Please upload an image!', 'error')
            return redirect(url_for('index'))
        
        file = request.files['image']
        edit_prompt = request.form.get('edit_prompt', '').strip()
        
        if file.filename == '' or not edit_prompt:
            flash('Please select an image and enter edit instructions!', 'error')
            return redirect(url_for('index'))
        
        if file and generator.allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(upload_path)
            
            # Edit image
            result = generator.edit_image(upload_path, edit_prompt)
            
            if result and result['success']:
                flash(f'✨ Image edited successfully! ({result.get("model", "Unknown")})', 'success')
                return redirect(url_for('view_result', filename=result['filename']))
            else:
                flash('❌ Image editing failed. Please try again.', 'error')
                return redirect(url_for('index'))
        else:
            flash('Invalid file type! Please use PNG, JPG, JPEG, GIF, or WebP.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/fuse', methods=['POST'])
def fuse():
    """Fuse multiple images together"""
    try:
        fusion_prompt = request.form.get('fusion_prompt', '').strip()
        
        if not fusion_prompt:
            flash('Please enter fusion instructions!', 'error')
            return redirect(url_for('index'))
        
        # Handle multiple file uploads
        uploaded_files = []
        for i in range(1, 5):  # Support up to 4 images
            file_key = f'fusion_image_{i}'
            if file_key in request.files:
                file = request.files[file_key]
                if file.filename != '' and generator.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{timestamp}_{i}_{filename}"
                    upload_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(upload_path)
                    uploaded_files.append(upload_path)
        
        if len(uploaded_files) < 2:
            flash('Please upload at least 2 images for fusion!', 'error')
            return redirect(url_for('index'))
        
        # Fuse images
        result = generator.fuse_images(uploaded_files, fusion_prompt)
        
        if result and result['success']:
            flash(f'✨ Images fused successfully! ({result.get("model", "Unknown")})', 'success')
            return redirect(url_for('view_result', filename=result['filename']))
        else:
            flash('❌ Image fusion failed. Please try again.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/character_consistency', methods=['POST'])
def character_consistency():
    """Maintain character consistency across different scenes"""
    try:
        if 'character_image' not in request.files:
            flash('Please upload a character reference image!', 'error')
            return redirect(url_for('index'))
        
        file = request.files['character_image']
        scene_prompt = request.form.get('scene_prompt', '').strip()
        
        if file.filename == '' or not scene_prompt:
            flash('Please select an image and describe the new scene!', 'error')
            return redirect(url_for('index'))
        
        if file and generator.allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"char_{timestamp}_{filename}"
            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(upload_path)
            
            # Generate consistent character
            result = generator.maintain_character_consistency(upload_path, scene_prompt)
            
            if result and result['success']:
                flash(f'✨ Character consistency maintained! ({result.get("model", "Unknown")})', 'success')
                return redirect(url_for('view_result', filename=result['filename']))
            else:
                flash('❌ Character consistency generation failed. Please try again.', 'error')
                return redirect(url_for('index'))
        else:
            flash('Invalid file type! Please use PNG, JPG, JPEG, GIF, or WebP.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/result/<filename>')
def view_result(filename):
    """View generated image result"""
    # Find result in history
    result = None
    for gen in generator.generation_history:
        if gen['filename'] == filename:
            result = gen
            break
    
    if not result:
        flash('Result not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('nano_banana_result.html', result=result)

@app.route('/gallery')
def gallery():
    """View all generated images"""
    return render_template('nano_banana_gallery.html', 
                         generations=reversed(generator.generation_history))

@app.route('/generated_images/<filename>')
def serve_generated_image(filename):
    """Serve generated images"""
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded images"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for image generation"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400
        
        result = generator.generate_image_with_gemini(prompt)
        
        if result and result['success']:
            return jsonify({
                'success': True,
                'result': result,
                'image_url': url_for('serve_generated_image', filename=result['filename'], _external=True)
            })
        else:
            return jsonify({'success': False, 'error': 'Generation failed'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history')
def api_history():
    """API endpoint for generation history"""
    return jsonify({
        'success': True,
        'history': generator.generation_history,
        'total_generations': len(generator.generation_history)
    })

if __name__ == '__main__':
    print("🍌 Starting Nano-Banana Generator (Gemini 2.5 Flash Image)...")
    print("✨ State-of-the-art image generation and editing")
    print("🎨 Features: Text-to-Image, Image Editing, Multi-Image Fusion, Character Consistency")
    print("🌐 Starting web server on port 8001...")
    
    app.run(host='0.0.0.0', port=8001, debug=False, threaded=True)