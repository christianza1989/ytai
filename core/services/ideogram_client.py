#!/usr/bin/env python3
"""
Ideogram 3.0 Image Generation Client
Simple and fast image generation using Ideogram API
"""

import os
import json
import time
import requests
from typing import Dict, Any, Optional

class IdeogramClient:
    """Client for Ideogram 3.0 image generation"""
    
    def __init__(self):
        self.api_key = os.getenv('IDEOGRAM_API_KEY')
        self.base_url = "https://api.ideogram.ai/v1/ideogram-v3/generate"
        
    def generate_image(self, prompt: str, aspect_ratio: str = '16:9', 
                      rendering_speed: str = 'TURBO', style_type: str = 'GENERAL') -> Dict[str, Any]:
        """Generate image using Ideogram 3.0 API"""
        
        try:
            print(f"🎨 Ideogram 3.0: Generating image")
            print(f"📝 Prompt: {prompt}")
            print(f"📐 Aspect: {aspect_ratio}")
            print(f"⚡ Speed: {rendering_speed}")
            
            # Prepare request data
            data = {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "rendering_speed": rendering_speed,
                "style_type": style_type,
                "magic_prompt": "AUTO",
                "num_images": 1
            }
            
            headers = {
                "Api-Key": self.api_key or "test-key-placeholder"
            }
            
            # For now, simulate API call since we don't have real API key
            if not self.api_key or self.api_key == "test-key-placeholder":
                print("⚠️ No real API key - using demo mode")
                return self._generate_demo_response(prompt, aspect_ratio)
            
            # Make API request
            print(f"🌐 Calling Ideogram API...")
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('data') and len(result['data']) > 0:
                    image_data = result['data'][0]
                    
                    return {
                        'success': True,
                        'image_url': image_data.get('url'),
                        'image_id': f"ideogram_{int(time.time())}",
                        'prompt_used': image_data.get('prompt', prompt),
                        'resolution': image_data.get('resolution'),
                        'seed': image_data.get('seed'),
                        'is_safe': image_data.get('is_image_safe', True),
                        'style_type': image_data.get('style_type'),
                        'model': 'ideogram-3.0',
                        'aspect_ratio': aspect_ratio,
                        'rendering_speed': rendering_speed,
                        'created_at': result.get('created'),
                        'message': 'Image generated successfully with Ideogram 3.0'
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No image data in response',
                        'message': 'Ideogram API returned empty data'
                    }
            else:
                return {
                    'success': False,
                    'error': f'API error: {response.status_code}',
                    'message': f'Ideogram API failed: {response.text}'
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout',
                'message': 'Ideogram API request timed out'
            }
            
        except Exception as e:
            print(f"❌ Ideogram generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Ideogram image generation failed'
            }
    
    def _generate_demo_response(self, prompt: str, aspect_ratio: str) -> Dict[str, Any]:
        """Generate demo response when no API key available"""
        
        # Create demo image URL based on prompt content
        demo_images = {
            'electronic': 'https://picsum.photos/1920/1080?random=1&blur=1',
            'cyberpunk': 'https://picsum.photos/1920/1080?random=2&blur=1', 
            'synthwave': 'https://picsum.photos/1920/1080?random=3&blur=1',
            'modern': 'https://picsum.photos/1920/1080?random=4&blur=1',
            'futuristic': 'https://picsum.photos/1920/1080?random=5&blur=1',
            'default': 'https://picsum.photos/1920/1080?random=6&blur=1'
        }
        
        # Determine image based on prompt keywords
        image_url = demo_images['default']
        for keyword, url in demo_images.items():
            if keyword in prompt.lower():
                image_url = url
                break
        
        return {
            'success': True,
            'image_url': image_url,
            'image_id': f"demo_ideogram_{int(time.time())}",
            'prompt_used': prompt,
            'resolution': '1920x1080',
            'seed': 12345,
            'is_safe': True,
            'style_type': 'GENERAL',
            'model': 'ideogram-3.0-demo',
            'aspect_ratio': aspect_ratio,
            'rendering_speed': 'TURBO',
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S+00:00'),
            'message': 'Demo image generated (API key needed for real generation)',
            'demo_mode': True
        }
    
    def get_supported_aspect_ratios(self) -> list:
        """Get list of supported aspect ratios"""
        return [
            '1:1', '16:9', '9:16', '4:3', '3:4', '3:2', '2:3',
            '16:10', '10:16', '5:4', '4:5', '3:1', '1:3', '2:1', '1:2'
        ]
    
    def get_rendering_speeds(self) -> list:
        """Get list of rendering speeds"""
        return ['TURBO', 'DEFAULT', 'QUALITY']
    
    def get_style_types(self) -> list:
        """Get list of style types"""
        return ['AUTO', 'GENERAL', 'REALISTIC', 'DESIGN', 'FICTION']