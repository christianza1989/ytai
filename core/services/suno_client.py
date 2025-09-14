import os
import requests
import json
from typing import Dict, Optional, Any
from datetime import datetime

class SunoClient:
    """Suno API client for music generation"""

    def __init__(self):
        self.api_key = os.getenv('SUNO_API_KEY')
        self.base_url = "https://api.sunoapi.org/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        if not self.api_key:
            raise ValueError("SUNO_API_KEY environment variable is required")

    def get_credits(self) -> int:
        """Get remaining credits"""
        try:
            url = f"{self.base_url}/generate/credit"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            if data.get('code') == 200:
                return data.get('data', 0)
            elif data.get('code') == 401:
                print(f"🔑 Suno API Authentication Error: {data.get('msg')}")
                print("💡 This usually means:")
                print("   - API key has expired or been revoked")
                print("   - Account access has been suspended")
                print("   - API key needs to be renewed")
                return 0
            else:
                print(f"⚠️ Suno API Error ({data.get('code')}): {data.get('msg')}")
                return 0
        except Exception as e:
            print(f"❌ Failed to connect to Suno API: {e}")
            return 0

    def generate_music_simple(self, prompt: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Generate music with simple parameters"""
        try:
            url = f"{self.base_url}/generate"

            # Non-custom mode: only prompt is required, max 400 characters
            if len(prompt) > 400:
                prompt = prompt[:400]  # Truncate to API limit

            payload = {
                "prompt": prompt,
                "customMode": False,  # Non-custom mode for simplicity
                "instrumental": kwargs.get('instrumental', False),
                "model": kwargs.get('model', 'V4'),  # Use provided model or default to V4
                "callBackUrl": os.getenv('CALLBACK_URL', 'https://webhook.site/unique-id')
            }
            
            # Add optional parameters if provided
            optional_params = ['negativeTags', 'vocalGender', 'styleWeight', 'weirdnessConstraint', 'audioWeight']
            for param in optional_params:
                if param in kwargs and kwargs[param] is not None:
                    payload[param] = kwargs[param]
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            
            if data.get('code') == 200:
                # Return full response data for more information
                return data.get('data', {})
            elif data.get('code') == 429:
                # Insufficient credits error
                raise Exception(f"Insufficient Suno credits: {data.get('msg')}")
            else:
                error_msg = data.get('msg', 'Unknown API error')
                raise Exception(f"Suno API error (code {data.get('code')}): {error_msg}")

        except Exception as e:
            print(f"Failed to generate music: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_music_advanced(self,
                              prompt: str,
                              style: str,
                              title: str,
                              instrumental: bool = False,
                              model: str = "V4",
                              **kwargs) -> Optional[str]:
        """Generate music with advanced parameters (Custom Mode)"""
        try:
            url = f"{self.base_url}/generate"

            # Apply character limits based on model
            if model in ['V4_5', 'V4_5PLUS']:
                # V4_5 limits
                prompt_limit = 5000
                style_limit = 1000
            else:
                # V3_5 and V4 limits
                prompt_limit = 3000
                style_limit = 200
            
            # Truncate to limits
            if prompt and len(prompt) > prompt_limit:
                prompt = prompt[:prompt_limit]
            if style and len(style) > style_limit:
                style = style[:style_limit]
            if title and len(title) > 80:
                title = title[:80]  # Title limit is 80 chars for all models

            payload = {
                "customMode": True,  # Custom mode
                "instrumental": instrumental,
                "model": model,
                "style": style,
                "title": title,
                "callBackUrl": os.getenv('CALLBACK_URL', 'https://webhook.site/unique-id')
            }
            
            # Add prompt only if not instrumental (as per API docs)
            if not instrumental:
                payload["prompt"] = prompt
            
            # Add optional parameters if provided
            optional_params = ['negativeTags', 'vocalGender', 'styleWeight', 'weirdnessConstraint', 'audioWeight']
            for param in optional_params:
                if param in kwargs and kwargs[param] is not None:
                    payload[param] = kwargs[param]

            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            if data.get('code') == 200:
                return data.get('data', {}).get('taskId')
            elif data.get('code') == 429:
                # Insufficient credits error
                raise Exception(f"Insufficient Suno credits: {data.get('msg')}")
            else:
                error_msg = data.get('msg', 'Unknown API error')
                raise Exception(f"Suno API error (code {data.get('code')}): {error_msg}")

        except Exception as e:
            print(f"Failed to generate music: {e}")
            return None

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a music generation task"""
        try:
            url = f"{self.base_url}/generate/record-info"
            params = {"taskId": task_id}

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            if data.get('code') == 200:
                return data.get('data')
            else:
                print(f"Error getting task status: {data.get('msg')}")
                return None

        except Exception as e:
            print(f"Failed to get task status: {e}")
            return None

    def generate_lyrics(self, prompt: str, **kwargs) -> Optional[str]:
        """Generate lyrics only"""
        try:
            url = f"{self.base_url}/lyrics"

            payload = {
                "prompt": prompt,
                "callBackUrl": os.getenv('CALLBACK_URL', 'https://webhook.site/unique-id'),
                **kwargs
            }

            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            if data.get('code') == 200:
                return data.get('data', {}).get('taskId')
            else:
                print(f"Error generating lyrics: {data.get('msg')}")
                return None

        except Exception as e:
            print(f"Failed to generate lyrics: {e}")
            return None

    def upload_file_url(self, file_url: str, upload_path: str = "uploads", file_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Upload file from URL for processing"""
        try:
            url = f"{self.base_url}/file-url-upload"

            payload = {
                "fileUrl": file_url,
                "uploadPath": upload_path,
                "fileName": file_name
            }

            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            if data.get('code') == 200:
                return data.get('data')
            else:
                print(f"Error uploading file: {data.get('msg')}")
                return None

        except Exception as e:
            print(f"Failed to upload file: {e}")
            return None

    def wait_for_generation_completion(self, task_id: str, max_wait_time: int = 600) -> Dict[str, Any]:
        """Wait for music generation to complete and return results"""
        import time

        print(f"🔄 Laukiama užduoties {task_id} užbaigimo...")
        start_time = time.time()
        check_interval = 15  # seconds

        while time.time() - start_time < max_wait_time:
            try:
                task_data = self.get_task_status(task_id)

                if not task_data:
                    print("❌ Nepavyko gauti užduoties būsenos")
                    raise Exception("Failed to get task status")

                status = task_data.get('status', 'UNKNOWN')
                print(f"📊 Užduoties būsena: {status}")

                if status in ['SUCCESS', 'TEXT_SUCCESS', 'AUDIO_SUCCESS', 'COMPLETE']:
                    print("✅ Užduotis sėkmingai užbaigta!")
                    return task_data
                elif status in ['FAILED', 'CREATE_TASK_FAILED', 'GENERATE_AUDIO_FAILED']:
                    error_msg = task_data.get('msg', 'Nežinoma klaida')
                    print(f"❌ Užduotis nepavyko: {error_msg}")
                    raise Exception(f"Task failed: {error_msg}")
                elif status == 'SENSITIVE_WORD_ERROR':
                    print("❌ Užduotis atmesta dėl turinio politikos")
                    raise Exception("Content policy violation")

                # Wait before next check
                time.sleep(check_interval)

            except Exception as e:
                print(f"❌ Klaida tikrinant užduoties būseną: {e}")
                time.sleep(check_interval)

        # Timeout
        print(f"⏰ Laukimo laikas ({max_wait_time}s) baigėsi")
        raise Exception(f"Task completion timeout after {max_wait_time} seconds")
