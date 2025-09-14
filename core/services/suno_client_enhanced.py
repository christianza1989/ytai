import os
import requests
import json
import time
from typing import Dict, Optional, Any, Union, List
from datetime import datetime

class SunoClientEnhanced:
    """
    Enhanced Suno API client combining working legacy methods with new official API features
    Maintains backward compatibility while adding new capabilities
    """

    def __init__(self):
        self.api_key = os.getenv('SUNO_API_KEY')
        self.base_url = "https://api.sunoapi.org/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        if not self.api_key:
            raise ValueError("SUNO_API_KEY environment variable is required")

    def _send_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Private method for sending API requests with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, **kwargs)
            else:
                response = requests.get(url, headers=self.headers, **kwargs)
            
            response.raise_for_status()
            result = response.json()

            if result.get('code') == 200:
                return result.get('data')
            elif result.get('code') == 401:
                raise Exception(f"🔑 Authentication Error: {result.get('msg')} - Check API key")
            else:
                raise Exception(f"API Error ({result.get('code')}): {result.get('msg')}")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network Error: {e}")

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

    # ===== LEGACY METHODS (WORKING) =====
    
    def generate_music_simple(self, prompt: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Generate music with simple parameters (LEGACY - WORKING)
        Uses the working /generate endpoint
        """
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
        """
        Generate music with advanced parameters (LEGACY - WORKING)
        Uses the working /generate endpoint with custom mode
        """
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
        """Get detailed information about a music generation task (LEGACY - WORKING)"""
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

    def wait_for_generation_completion(self, task_id: str, max_wait_time: int = 600) -> Dict[str, Any]:
        """Wait for music generation to complete and return results (LEGACY - WORKING)"""
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

    # ===== NEW OFFICIAL API METHODS =====
    
    def generate_lyrics(self, 
                       prompt: str,
                       callback_url: str = None) -> str:
        """
        Generate song lyrics using official API endpoint
        
        Args:
            prompt: Description of desired lyrics (max 200 words)
            callback_url: URL for receiving results
            
        Returns:
            Task ID
        """
        if not callback_url:
            callback_url = os.getenv('CALLBACK_URL', 'https://webhook.site/unique-id')
            
        # Validate prompt length (approximate word count)
        word_count = len(prompt.split())
        if word_count > 200:
            raise ValueError(f"Prompt too long ({word_count} words). Maximum 200 words allowed.")
        
        payload = {
            "prompt": prompt,
            "callBackUrl": callback_url
        }
        
        data = self._send_request('POST', '/lyrics', json=payload)
        return data.get('taskId')

    def extend_music(self,
                    audio_id: str,
                    model: str,
                    callback_url: str = None,
                    default_param_flag: bool = False,
                    prompt: Optional[str] = None,
                    style: Optional[str] = None,
                    title: Optional[str] = None,
                    continue_at: Optional[float] = None,
                    **kwargs) -> str:
        """
        Extend existing music track using official API
        """
        if not callback_url:
            callback_url = os.getenv('CALLBACK_URL', 'https://webhook.site/unique-id')
            
        if default_param_flag:
            required_params = ['prompt', 'style', 'title', 'continue_at']
            for param in required_params:
                if locals()[param] is None:
                    raise ValueError(f"{param} is required when default_param_flag is True")
        
        payload = {
            "audioId": audio_id,
            "defaultParamFlag": default_param_flag,
            "model": model,
            "callBackUrl": callback_url
        }
        
        if default_param_flag:
            payload.update({
                "prompt": prompt,
                "style": style,
                "title": title,
                "continueAt": continue_at
            })
        
        # Add optional parameters
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value
        
        data = self._send_request('POST', '/generate/extend', json=payload)
        return data.get('taskId')

    def separate_vocals(self,
                       task_id: str,
                       audio_id: str,
                       callback_url: str = None,
                       separation_type: str = "separate_vocal") -> str:
        """
        Separate vocals and instruments from audio using official API
        """
        if not callback_url:
            callback_url = os.getenv('CALLBACK_URL', 'https://webhook.site/unique-id')
            
        payload = {
            "taskId": task_id,
            "audioId": audio_id,
            "callBackUrl": callback_url,
            "type": separation_type
        }
        
        data = self._send_request('POST', '/vocal-removal/generate', json=payload)
        return data.get('taskId')

    def create_music_video(self,
                          task_id: str,
                          audio_id: str,
                          callback_url: str = None,
                          author: Optional[str] = None,
                          domain_name: Optional[str] = None) -> str:
        """
        Create MP4 music video with visualizations using official API
        """
        if not callback_url:
            callback_url = os.getenv('CALLBACK_URL', 'https://webhook.site/unique-id')
            
        payload = {
            "taskId": task_id,
            "audioId": audio_id,
            "callBackUrl": callback_url
        }
        
        if author:
            if len(author) > 50:
                author = author[:50]
            payload["author"] = author
            
        if domain_name:
            if len(domain_name) > 50:
                domain_name = domain_name[:50]
            payload["domainName"] = domain_name
        
        data = self._send_request('POST', '/mp4/generate', json=payload)
        return data.get('taskId')

    def get_lyrics_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status for lyrics generation using official API"""
        try:
            data = self._send_request('GET', '/lyrics/record-info', params={'taskId': task_id})
            return data
        except Exception as e:
            print(f"Failed to get lyrics status: {e}")
            return None

    # ===== ENHANCED UTILITY METHODS =====
    
    def wait_for_any_task_completion(self, task_id: str, task_type: str = "music", max_wait_time: int = 600) -> Dict[str, Any]:
        """
        Universal task completion waiter for any task type
        
        Args:
            task_id: Task ID to monitor
            task_type: "music", "lyrics", "vocal_separation", "video", "extend"
            max_wait_time: Maximum wait time in seconds
            
        Returns:
            Task completion data
        """
        start_time = time.time()
        check_interval = 15
        
        print(f"🔄 Waiting for {task_type} task {task_id} completion...")
        
        while time.time() - start_time < max_wait_time:
            try:
                if task_type == "lyrics":
                    task_data = self.get_lyrics_status(task_id)
                else:
                    task_data = self.get_task_status(task_id)

                if not task_data:
                    raise Exception("Failed to get task status")

                status = task_data.get('status', 'UNKNOWN')
                print(f"📊 Task status: {status}")

                if status in ['SUCCESS', 'TEXT_SUCCESS', 'AUDIO_SUCCESS', 'COMPLETE']:
                    print("✅ Task completed successfully!")
                    return task_data
                elif status in ['FAILED', 'CREATE_TASK_FAILED', 'GENERATE_AUDIO_FAILED', 'SENSITIVE_WORD_ERROR']:
                    error_msg = task_data.get('errorMessage', 'Unknown error')
                    raise Exception(f"Task failed: {error_msg}")

                time.sleep(check_interval)

            except Exception as e:
                print(f"❌ Error checking task status: {e}")
                time.sleep(check_interval)

        raise Exception(f"Task completion timeout after {max_wait_time} seconds")

    def get_all_capabilities(self) -> Dict[str, bool]:
        """
        Return a dictionary of all available capabilities
        """
        return {
            "basic_music_generation": True,
            "advanced_music_generation": True, 
            "lyrics_generation": True,
            "music_extension": True,
            "vocal_separation": True,
            "music_video_creation": True,
            "task_status_monitoring": True,
            "credits_checking": True,
            "character_limit_validation": True,
            "enhanced_parameters": True
        }