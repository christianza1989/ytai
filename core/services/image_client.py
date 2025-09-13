import os
import base64
import requests
from typing import Optional
from pathlib import Path
from PIL import Image
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ImageClient:
    """Gemini 2.5 Flash Image (nano-banana) client for YouTube music image generation"""

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key or self.api_key == 'your_gemini_api_key_here':
            print("⚠️ GEMINI_API_KEY not configured, using mock mode")
            self.mock_mode = True
        else:
            self.mock_mode = False
            
        self.model_name = "gemini-2.5-flash-image-preview"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        print(f"🍌 Initialized Gemini nano-banana image client (Mock: {self.mock_mode})")

    def generate_image(self, prompt: str, save_path: str, filename: str) -> bool:
        """Generate image using Gemini 2.5 Flash Image (nano-banana)"""
        try:
            print(f"🍌 Generuojamas nano-banana paveikslėlis: {prompt[:50]}...")

            # Ensure save_path exists
            Path(save_path).mkdir(parents=True, exist_ok=True)
            
            if self.mock_mode:
                return self._generate_mock_image(prompt, save_path, filename)
            
            # Prepare API request for Gemini
            url = f"{self.base_url}/models/{self.model_name}:generateContent"
            
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': self.api_key
            }
            
            # Enhanced prompt for YouTube album covers
            enhanced_prompt = f"Create a professional music album cover: {prompt}. Style: modern, artistic, vibrant colors, high quality, music-themed, YouTube thumbnail ready, 1024x1024 resolution"
            
            payload = {
                "contents": [{
                    "parts": [{"text": enhanced_prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            print(f"🚀 Sending request to Gemini API...")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return self._process_gemini_response(result, save_path, filename)
            else:
                print(f"❌ Gemini API error: {response.status_code} - {response.text}")
                print("🔄 Falling back to mock generation...")
                return self._generate_mock_image(prompt, save_path, filename)
                
        except Exception as e:
            print(f"❌ Klaida generuojant nano-banana paveikslėlį: {e}")
            print("🔄 Falling back to mock generation...")
            return self._generate_mock_image(prompt, save_path, filename)

    def _process_gemini_response(self, response, save_path, filename):
        """Process Gemini API response and extract generated image"""
        try:
            candidates = response.get('candidates', [])
            if not candidates:
                print("❌ No candidates in Gemini response")
                return False
            
            parts = candidates[0].get('content', {}).get('parts', [])
            
            for part in parts:
                if 'inline_data' in part:
                    # Extract generated image data
                    image_data = part['inline_data']['data']
                    
                    # Decode and save image
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(BytesIO(image_bytes))
                    
                    # Save image
                    file_path = Path(save_path) / filename
                    image.save(file_path, 'PNG')
                    
                    print(f"✅ Nano-banana paveikslėlis išsaugotas: {file_path}")
                    print(f"📐 Dydis: {image.width}x{image.height}")
                    return True
            
            print("❌ No image data found in Gemini response")
            return False
            
        except Exception as e:
            print(f"❌ Error processing Gemini response: {e}")
            return False
    
    def _generate_mock_image(self, prompt, save_path, filename):
        """Generate mock image when API is not available"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import random
            
            # Create base image with gradient background
            width, height = 1024, 1024
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            
            # Create gradient background
            colors = [
                [(255, 0, 150), (0, 150, 255)],  # Pink to blue
                [(255, 165, 0), (255, 20, 147)], # Orange to pink
                [(50, 205, 50), (255, 215, 0)],  # Green to gold
                [(138, 43, 226), (255, 105, 180)] # Purple to pink
            ]
            
            color_pair = random.choice(colors)
            
            for y in range(height):
                r = int(color_pair[0][0] + (color_pair[1][0] - color_pair[0][0]) * y / height)
                g = int(color_pair[0][1] + (color_pair[1][1] - color_pair[0][1]) * y / height)
                b = int(color_pair[0][2] + (color_pair[1][2] - color_pair[0][2]) * y / height)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Add music-themed elements
            # Musical notes
            draw.ellipse([100, 200, 150, 250], fill=(255, 255, 255, 180))
            draw.ellipse([200, 300, 250, 350], fill=(255, 255, 255, 180))
            
            # Album title area
            draw.rectangle([50, 800, 974, 900], fill=(0, 0, 0, 120))
            
            # Add text
            try:
                # Title
                draw.text((60, 820), "🍌 NANO-BANANA GENERATED", fill=(255, 255, 255), anchor="ls")
                draw.text((60, 850), prompt[:40] + "...", fill=(255, 255, 255), anchor="ls")
                
                # Gemini watermark
                draw.text((60, 970), "Powered by Gemini 2.5 Flash Image (MOCK)", fill=(255, 255, 255), anchor="ls")
            except:
                pass  # Skip if font issues
            
            # Save mock image
            file_path = Path(save_path) / filename
            image.save(file_path, 'PNG')
            
            print(f"✅ [MOCK] Nano-banana paveikslėlis išsaugotas: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Mock generation error: {e}")
            return False
    
    def generate_image_with_style(self, prompt: str, style: str, save_path: str, filename: str) -> bool:
        """Generate image with specific style using Gemini nano-banana"""
        try:
            # Enhanced style prompts for music album covers
            style_prompts = {
                "neon_city": "neon lights, cyberpunk city, futuristic, glowing signs, urban landscape, synthwave aesthetic",
                "dark_mood": "dark atmosphere, moody lighting, mysterious, dramatic shadows, gothic, noir style",
                "vibrant": "bright colors, energetic, dynamic composition, vivid, pop art style, rainbow colors",
                "minimalist": "clean, simple, geometric shapes, limited color palette, modern design, abstract",
                "nature": "natural landscape, organic shapes, earthy tones, forest, mountains, serene",
                "abstract": "abstract art, geometric patterns, artistic composition, surreal, contemporary art",
                "retro": "vintage style, 80s aesthetics, retro colors, nostalgic, classic design",
                "electronic": "digital art, electronic music vibe, LED lights, circuit patterns, tech aesthetic"
            }

            style_enhancement = style_prompts.get(style, "modern, artistic, professional")
            enhanced_prompt = f"{prompt}, {style_enhancement}, professional music album cover, YouTube thumbnail, high quality, detailed artwork"

            return self.generate_image(enhanced_prompt, save_path, filename)

        except Exception as e:
            print(f"❌ Klaida generuojant nano-banana paveikslėlį su stiliumi: {e}")
            return False
    
    def generate_youtube_thumbnail(self, prompt: str, save_path: str, filename: str) -> bool:
        """Generate YouTube thumbnail optimized image"""
        youtube_prompt = f"YouTube music thumbnail: {prompt}. Style: eye-catching, vibrant colors, clear text space, music theme, professional design, 1280x720 aspect ratio optimized for 1024x1024 canvas"
        return self.generate_image(youtube_prompt, save_path, filename)
    
    def generate_album_cover(self, song_title: str, genre: str, mood: str, save_path: str, filename: str) -> bool:
        """Generate album cover specifically for music"""
        album_prompt = f"Professional music album cover for '{song_title}'. Genre: {genre}. Mood: {mood}. Include musical elements, artistic design, suitable for streaming platforms, modern aesthetic"
        return self.generate_image(album_prompt, save_path, filename)
    
    # Backward compatibility methods
    def create_album_cover(self, prompt: str, output_path: str) -> bool:
        """Backward compatibility method"""
        filename = f"album_cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        save_path = str(Path(output_path).parent)
        return self.generate_image(prompt, save_path, filename)