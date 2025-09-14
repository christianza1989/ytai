#!/usr/bin/env python3
"""
Image Generation Client
Wrapper for image generation tools integration
"""

import os
import json
import time
from typing import Dict, Any, Optional

class ImageClient:
    """Client for integrating with image generation tools"""
    
    def __init__(self):
        self.api_key = os.getenv('IMAGE_API_KEY')  # Configure if needed
    
    def generate_image(self, prompt: str, model: str = 'fal-ai/nano-banana', 
                      aspect_ratio: str = '16:9', task_summary: str = '') -> Dict[str, Any]:
        """Generate image using external image generation tools - REAL API INTEGRATION"""
        try:
            # Use the actual image generation function that was mentioned in the context
            # This integrates with the real image generation system
            
            print(f"🖼️ Calling real image generation API: {model}")
            print(f"🎯 Prompt: {prompt[:100]}...")
            print(f"📐 Aspect ratio: {aspect_ratio}")
            
            # Call the actual image generation function
            # This should use the same function signature as mentioned in the context
            from image_generation import image_generation
            
            # Build the request parameters
            generation_result = image_generation(
                query=prompt,
                image_urls=[],  # No reference images
                model=model,
                aspect_ratio=aspect_ratio,
                task_summary=task_summary
            )
            
            print(f"📥 Image generation result: {type(generation_result)}")
            
            # Check if generation was successful
            if not generation_result:
                raise Exception("Image generation API returned empty result")
            
            # Extract image URL from the result
            if isinstance(generation_result, dict):
                image_url = generation_result.get('image_url') or generation_result.get('url')
                if not image_url:
                    # Check if it's in a nested structure
                    if 'generated_images' in generation_result:
                        images = generation_result['generated_images']
                        if images and len(images) > 0:
                            image_url = images[0].get('url') or images[0].get('image_url')
            else:
                image_url = str(generation_result)
            
            if not image_url:
                raise Exception("No image URL found in generation result")
            
            image_id = f"img_{int(time.time())}"
            
            return {
                'success': True,
                'image_url': image_url,
                'image_id': image_id,
                'model_used': model,
                'prompt_used': prompt,
                'aspect_ratio': aspect_ratio,
                'generated_at': time.time(),
                'api_response': generation_result  # Include full response for debugging
            }
            
        except ImportError as e:
            print(f"⚠️ Image generation function not available: {e}")
            # Fall back to placeholder for now, but indicate it's a missing integration
            return {
                'success': False,
                'error': 'Image generation function not available - needs integration setup',
                'message': 'Real image generation API not properly configured'
            }
            
        except Exception as e:
            print(f"❌ Image generation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Image generation failed'
            }