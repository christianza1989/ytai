import os
import requests
import json
import time
from typing import Dict, Optional, Any, Union, List
from datetime import datetime

class SunoClientUpdated:
    """
    Updated Suno API client matching official documentation
    Supports all official API endpoints and parameters
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
            data = self._send_request('GET', '/generate/credit')
            return data if isinstance(data, int) else 0
        except Exception as e:
            print(f"❌ Failed to get credits: {e}")
            return 0

    def generate_music(self, 
                      upload_url: Optional[str] = None,
                      prompt: Optional[str] = None,
                      custom_mode: bool = False,
                      instrumental: bool = False,
                      model: str = "V4",
                      callback_url: str = "https://your-domain.com/callback",
                      style: Optional[str] = None,
                      title: Optional[str] = None,
                      negative_tags: Optional[str] = None,
                      vocal_gender: Optional[str] = None,
                      style_weight: Optional[float] = None,
                      weirdness_constraint: Optional[float] = None,
                      audio_weight: Optional[float] = None) -> str:
        """
        Generate music using official Suno API endpoint
        
        Args:
            upload_url: URL of audio file to process (required by API)
            prompt: Description of desired music (required if not instrumental in custom mode)
            custom_mode: Enable custom mode with style and title
            instrumental: Generate instrumental music
            model: Model version (V3_5, V4, V4_5, V4_5PLUS)
            callback_url: URL for receiving results
            style: Music style (required in custom mode)
            title: Song title (required in custom mode)
            negative_tags: Styles to avoid
            vocal_gender: 'm' or 'f'
            style_weight: 0.00-1.00
            weirdness_constraint: 0.00-1.00
            audio_weight: 0.00-1.00
            
        Returns:
            Task ID
        """
        
        # Validate required parameters
        if custom_mode:
            if not style:
                raise ValueError("Style is required when customMode is True")
            if not title:
                raise ValueError("Title is required when customMode is True")
            if not instrumental and not prompt:
                raise ValueError("Prompt is required when customMode is True and instrumental is False")
        
        # Apply character limits based on model
        if model in ['V4_5', 'V4_5PLUS']:
            prompt_limit = 5000
            style_limit = 1000
            title_limit = 100
        else:
            prompt_limit = 3000
            style_limit = 200
            title_limit = 80
        
        # Truncate to limits
        if prompt and len(prompt) > prompt_limit:
            prompt = prompt[:prompt_limit]
        if style and len(style) > style_limit:
            style = style[:style_limit]
        if title and len(title) > title_limit:
            title = title[:title_limit]

        # Build payload
        payload = {
            "customMode": custom_mode,
            "instrumental": instrumental,
            "model": model,
            "callBackUrl": callback_url
        }
        
        # Add upload URL if provided (required by official API)
        if upload_url:
            payload["uploadUrl"] = upload_url
        
        # Add required parameters for custom mode
        if custom_mode:
            if style:
                payload["style"] = style
            if title:
                payload["title"] = title
        
        # Add prompt if not instrumental
        if not instrumental and prompt:
            payload["prompt"] = prompt
        
        # Add optional parameters
        optional_params = {
            "negativeTags": negative_tags,
            "vocalGender": vocal_gender,
            "styleWeight": style_weight,
            "weirdnessConstraint": weirdness_constraint,
            "audioWeight": audio_weight
        }
        
        for key, value in optional_params.items():
            if value is not None:
                payload[key] = value

        # Use correct endpoint from documentation
        data = self._send_request('POST', '/generate/upload-cover', json=payload)
        return data.get('taskId')

    def generate_lyrics(self, 
                       prompt: str,
                       callback_url: str = "https://your-domain.com/lyrics-callback") -> str:
        """
        Generate song lyrics
        
        Args:
            prompt: Description of desired lyrics (max 200 words)
            callback_url: URL for receiving results
            
        Returns:
            Task ID
        """
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
                    callback_url: str,
                    default_param_flag: bool = False,
                    prompt: Optional[str] = None,
                    style: Optional[str] = None,
                    title: Optional[str] = None,
                    continue_at: Optional[float] = None,
                    **kwargs) -> str:
        """
        Extend existing music track
        
        Args:
            audio_id: ID of track to extend
            model: Model version (must match original)
            callback_url: URL for receiving results
            default_param_flag: Use custom parameters or original track parameters
            prompt: How to continue the music (required if default_param_flag=True)
            style: New style (required if default_param_flag=True)
            title: New title (required if default_param_flag=True)
            continue_at: Time point to start extension (required if default_param_flag=True)
            
        Returns:
            Task ID
        """
        
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
                       callback_url: str,
                       separation_type: str = "separate_vocal") -> str:
        """
        Separate vocals and instruments from audio
        
        Args:
            task_id: Original music generation task ID
            audio_id: Specific audio track ID
            callback_url: URL for receiving results
            separation_type: "separate_vocal" or "split_stem"
            
        Returns:
            Task ID
        """
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
                          callback_url: str,
                          author: Optional[str] = None,
                          domain_name: Optional[str] = None) -> str:
        """
        Create MP4 music video with visualizations
        
        Args:
            task_id: Original music generation task ID
            audio_id: Specific audio track ID
            callback_url: URL for receiving results
            author: Artist/creator name (max 50 chars)
            domain_name: Website/brand name for watermark (max 50 chars)
            
        Returns:
            Task ID
        """
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

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status for music generation"""
        try:
            data = self._send_request('GET', '/generate/record-info', params={'taskId': task_id})
            return data
        except Exception as e:
            print(f"Failed to get task status: {e}")
            return None

    def get_lyrics_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status for lyrics generation"""
        try:
            data = self._send_request('GET', '/lyrics/record-info', params={'taskId': task_id})
            return data
        except Exception as e:
            print(f"Failed to get lyrics status: {e}")
            return None

    def wait_for_completion(self, task_id: str, task_type: str = "music", max_wait_time: int = 600) -> Dict[str, Any]:
        """
        Wait for task completion with polling
        
        Args:
            task_id: Task ID to monitor
            task_type: "music" or "lyrics"
            max_wait_time: Maximum wait time in seconds
            
        Returns:
            Task completion data
        """
        start_time = time.time()
        check_interval = 15  # seconds
        
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

                # Wait before next check
                time.sleep(check_interval)

            except Exception as e:
                print(f"❌ Error checking task status: {e}")
                time.sleep(check_interval)

        raise Exception(f"Task completion timeout after {max_wait_time} seconds")

    # Backward compatibility methods
    def generate_music_simple(self, prompt: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Backward compatibility method"""
        try:
            task_id = self.generate_music(
                prompt=prompt,
                custom_mode=False,
                **kwargs
            )
            return {"taskId": task_id}
        except Exception as e:
            print(f"Failed to generate music: {e}")
            return None

    def generate_music_advanced(self, prompt: str, style: str, title: str, **kwargs) -> Optional[str]:
        """Backward compatibility method"""
        try:
            return self.generate_music(
                prompt=prompt,
                style=style,
                title=title,
                custom_mode=True,
                **kwargs
            )
        except Exception as e:
            print(f"Failed to generate advanced music: {e}")
            return None