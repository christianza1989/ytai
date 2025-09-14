#!/usr/bin/env python3
"""
24/7 YouTube Automation System
Comprehensive automation for music generation, thumbnails, video creation, and YouTube uploads
"""

import os
import sys
import json
import time
import random
import threading
import schedule
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our services
from core.database.youtube_channels_db import YouTubeChannelsDB
from core.services.suno_client import SunoClient
from core.services.gemini_client import GeminiClient

class YouTubeAutomationEngine:
    """Advanced 24/7 YouTube automation engine with AI-driven decisions"""
    
    def __init__(self):
        self.db = YouTubeChannelsDB()
        self.suno = SunoClient()
        self.gemini = GeminiClient()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data/automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Automation state
        self.is_running = False
        self.automation_thread = None
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        # Generation queue
        self.generation_queue = []
        self.processing_lock = threading.Lock()
        
        self.logger.info("YouTube Automation Engine initialized")
    
    def start_automation(self) -> Dict[str, Any]:
        """Start 24/7 automation system"""
        try:
            if self.is_running:
                return {
                    'success': False,
                    'message': 'Automation is already running'
                }
            
            self.is_running = True
            
            # Schedule tasks based on channel configurations
            self._schedule_channel_tasks()
            
            # Start background thread
            self.automation_thread = threading.Thread(target=self._automation_loop, daemon=True)
            self.automation_thread.start()
            
            self.logger.info("24/7 Automation system started")
            
            return {
                'success': True,
                'message': '24/7 Automation system started successfully',
                'status': 'running'
            }
            
        except Exception as e:
            self.logger.error(f"Error starting automation: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to start automation'
            }
    
    def stop_automation(self) -> Dict[str, Any]:
        """Stop 24/7 automation system"""
        try:
            self.is_running = False
            schedule.clear()
            
            if self.automation_thread and self.automation_thread.is_alive():
                self.automation_thread.join(timeout=5)
            
            self.logger.info("24/7 Automation system stopped")
            
            return {
                'success': True,
                'message': 'Automation system stopped successfully',
                'status': 'stopped'
            }
            
        except Exception as e:
            self.logger.error(f"Error stopping automation: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to stop automation'
            }
    
    def get_automation_status(self) -> Dict[str, Any]:
        """Get current automation status and statistics"""
        try:
            # Get active channels
            active_channels = self.db.list_channels(status='active')
            automated_channels = [ch for ch in active_channels if ch.get('automation_enabled')]
            
            # Get queue statistics
            stats = self.db.get_statistics()
            
            # Get recent logs
            recent_logs = self._get_recent_logs(limit=20)
            
            return {
                'success': True,
                'automation_running': self.is_running,
                'total_channels': len(active_channels),
                'automated_channels': len(automated_channels),
                'queued_videos': stats.get('queued_videos', 0),
                'recent_logs': recent_logs,
                'next_scheduled_tasks': self._get_next_tasks()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting automation status: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to get automation status'
            }
    
    def _schedule_channel_tasks(self):
        """Schedule tasks for all automated channels"""
        try:
            active_channels = self.db.list_channels(status='active')
            automated_channels = [ch for ch in active_channels if ch.get('automation_enabled')]
            
            for channel in automated_channels:
                self._schedule_channel(channel)
            
            self.logger.info(f"Scheduled tasks for {len(automated_channels)} automated channels")
            
        except Exception as e:
            self.logger.error(f"Error scheduling channel tasks: {e}")
    
    def _schedule_channel(self, channel: Dict[str, Any]):
        """Schedule tasks for a specific channel"""
        try:
            channel_id = channel['id']
            channel_name = channel['channel_name']
            upload_schedule = channel.get('upload_schedule', 'daily')
            upload_hours = channel.get('upload_hours', [])
            
            if not upload_hours:
                upload_hours = [{"hour": 14, "vocal_probability": 0.8}]
            
            # Schedule based on frequency
            if upload_schedule == 'daily':
                for hour_config in upload_hours:
                    hour = hour_config['hour']
                    schedule.every().day.at(f"{hour:02d}:00").do(
                        self._generate_and_upload,
                        channel_id=channel_id,
                        vocal_probability=hour_config.get('vocal_probability', 0.8)
                    )
                    
            elif upload_schedule == 'every-2-days':
                hour = upload_hours[0]['hour']
                schedule.every(2).days.at(f"{hour:02d}:00").do(
                    self._generate_and_upload,
                    channel_id=channel_id,
                    vocal_probability=upload_hours[0].get('vocal_probability', 0.8)
                )
                
            elif upload_schedule == 'weekly':
                hour = upload_hours[0]['hour']
                schedule.every().monday.at(f"{hour:02d}:00").do(
                    self._generate_and_upload,
                    channel_id=channel_id,
                    vocal_probability=upload_hours[0].get('vocal_probability', 0.8)
                )
            
            self.logger.info(f"Scheduled tasks for channel: {channel_name} ({upload_schedule})")
            
        except Exception as e:
            self.logger.error(f"Error scheduling channel {channel.get('channel_name')}: {e}")
    
    def _automation_loop(self):
        """Main automation loop running in background thread"""
        self.logger.info("Starting automation loop")
        
        while self.is_running:
            try:
                # Run scheduled tasks
                schedule.run_pending()
                
                # Process generation queue
                self._process_generation_queue()
                
                # Sleep for 60 seconds
                time.sleep(60)
                
            except Exception as e:
                self.logger.error(f"Error in automation loop: {e}")
                time.sleep(60)  # Continue running even if there's an error
        
        self.logger.info("Automation loop stopped")
    
    def _generate_and_upload(self, channel_id: int, vocal_probability: float = 0.8):
        """Generate content and schedule upload for a channel"""
        try:
            channel = self.db.get_channel(channel_id)
            if not channel:
                self.logger.error(f"Channel {channel_id} not found")
                return
            
            channel_name = channel['channel_name']
            self.logger.info(f"Starting generation for channel: {channel_name}")
            
            # Add to generation queue
            generation_task = {
                'channel_id': channel_id,
                'channel_name': channel_name,
                'vocal_probability': vocal_probability,
                'selected_genres': channel.get('selected_genres', []),
                'target_audience': channel.get('target_audience', 'general'),
                'auto_thumbnails': channel.get('auto_thumbnails', True),
                'auto_seo': channel.get('auto_seo', True),
                'privacy_settings': channel.get('privacy_settings', 'private'),
                'scheduled_time': datetime.now().isoformat(),
                'status': 'queued'
            }
            
            with self.processing_lock:
                self.generation_queue.append(generation_task)
            
            # Log the task
            self.db._log_event(
                channel_id, 
                'generation_scheduled', 
                f'Content generation scheduled for {channel_name}',
                {'vocal_probability': vocal_probability}
            )
            
        except Exception as e:
            self.logger.error(f"Error scheduling generation for channel {channel_id}: {e}")
    
    def _process_generation_queue(self):
        """Process queued generation tasks"""
        try:
            with self.processing_lock:
                if not self.generation_queue:
                    return
                
                # Get next task
                task = self.generation_queue.pop(0)
            
            # Submit to thread pool for processing
            future = self.executor.submit(self._process_generation_task, task)
            
        except Exception as e:
            self.logger.error(f"Error processing generation queue: {e}")
    
    def _process_generation_task(self, task: Dict[str, Any]):
        """Process individual generation task"""
        try:
            channel_id = task['channel_id']
            channel_name = task['channel_name']
            
            self.logger.info(f"Processing generation task for: {channel_name}")
            
            # Step 1: AI Decision - Vocal vs Instrumental
            vocal_decision = self._make_vocal_decision(
                task['vocal_probability'],
                task['selected_genres'],
                task['target_audience']
            )
            
            # Step 2: Select genre for this generation
            selected_genre = self._select_genre(task['selected_genres'])
            
            # Step 3: Generate music prompt
            music_prompt = self._generate_music_prompt(
                selected_genre,
                vocal_decision['vocal_type'],
                task['target_audience']
            )
            
            self.logger.info(f"Generated prompt for {channel_name}: {music_prompt[:100]}...")
            
            # Step 4: Generate music with Suno API
            music_result = self._generate_music(music_prompt, vocal_decision)
            
            if not music_result.get('success'):
                raise Exception(f"Music generation failed: {music_result.get('error')}")
            
            # Step 5: Generate 16:9 thumbnail (if enabled)
            thumbnail_result = None
            if task['auto_thumbnails']:
                thumbnail_result = self._generate_thumbnail(selected_genre, vocal_decision['vocal_type'])
            
            # Step 6: Generate SEO metadata (if enabled)
            seo_metadata = {}
            if task['auto_seo']:
                seo_metadata = self._generate_seo_metadata(
                    selected_genre,
                    vocal_decision['vocal_type'],
                    task['target_audience']
                )
            
            # Step 7: Create video (combine music + thumbnail)
            video_result = self._create_video(
                music_result['audio_url'],
                thumbnail_result['image_url'] if thumbnail_result else None,
                seo_metadata
            )
            
            # Step 8: Upload to YouTube (if auto_upload enabled)
            upload_result = None
            if task.get('auto_upload', True):
                upload_result = self._upload_to_youtube(
                    channel_id,
                    video_result,
                    seo_metadata,
                    task['privacy_settings']
                )
            
            # Log successful completion
            self.db._log_event(
                channel_id,
                'generation_completed',
                f'Successfully generated and uploaded content for {channel_name}',
                {
                    'genre': selected_genre,
                    'vocal_type': vocal_decision['vocal_type'],
                    'music_url': music_result.get('audio_url'),
                    'thumbnail_url': thumbnail_result.get('image_url') if thumbnail_result else None,
                    'youtube_video_id': upload_result.get('video_id') if upload_result else None
                }
            )
            
            self.logger.info(f"Successfully completed generation task for: {channel_name}")
            
        except Exception as e:
            self.logger.error(f"Error processing generation task: {e}")
            
            # Log error
            self.db._log_event(
                task['channel_id'],
                'generation_error',
                f'Generation failed for {task["channel_name"]}: {str(e)}',
                {'error': str(e)}
            )
    
    def _make_vocal_decision(self, vocal_probability: float, genres: List[str], audience: str) -> Dict[str, Any]:
        """AI-driven decision for vocal vs instrumental content"""
        try:
            # Base decision on probability
            is_vocal = random.random() < vocal_probability
            
            # AI enhancement based on context
            context = {
                'genres': genres,
                'audience': audience,
                'time_of_day': datetime.now().hour,
                'day_of_week': datetime.now().weekday()
            }
            
            # Simple AI logic (can be enhanced with Gemini API)
            genre_vocal_preference = {
                'lo-fi-hip-hop': 0.3,  # Usually instrumental
                'ambient': 0.1,
                'meditation': 0.05,
                'study-music': 0.2,
                'jazz': 0.6,
                'pop': 0.9,
                'rock': 0.85,
                'trap': 0.7
            }
            
            # Adjust based on genre preference
            if genres:
                avg_genre_preference = sum(genre_vocal_preference.get(g, 0.5) for g in genres) / len(genres)
                # Blend original probability with genre preference
                final_probability = (vocal_probability + avg_genre_preference) / 2
                is_vocal = random.random() < final_probability
            
            vocal_type = 'vocal' if is_vocal else 'instrumental'
            
            return {
                'vocal_type': vocal_type,
                'confidence': abs(vocal_probability - 0.5) * 2,  # Higher confidence when probability is further from 50%
                'reasoning': f'AI decision based on {vocal_probability*100:.0f}% vocal probability and genre context',
                'context': context
            }
            
        except Exception as e:
            self.logger.error(f"Error in vocal decision: {e}")
            return {
                'vocal_type': 'instrumental',
                'confidence': 0.5,
                'reasoning': f'Default decision due to error: {str(e)}'
            }
    
    def _select_genre(self, available_genres: List[str]) -> str:
        """Select genre for current generation (rotational with randomness)"""
        if not available_genres:
            return 'lo-fi-hip-hop'
        
        return random.choice(available_genres)
    
    def _generate_music_prompt(self, genre: str, vocal_type: str, audience: str) -> str:
        """Generate optimized music prompt"""
        try:
            # Genre-specific templates
            genre_templates = {
                'lo-fi-hip-hop': {
                    'instrumental': 'Relaxing lo-fi hip hop beats with warm vinyl crackle, mellow piano chords, soft drum patterns, perfect for studying and focus',
                    'vocal': 'Lo-fi hip hop with smooth vocal melodies, laid-back rap verses, jazzy chords, and nostalgic atmosphere'
                },
                'ambient': {
                    'instrumental': 'Ethereal ambient soundscape with atmospheric pads, gentle drones, subtle textures, creating peaceful meditation environment',
                    'vocal': 'Ambient music with angelic vocals, whispered lyrics, floating melodies over atmospheric background'
                },
                'study-music': {
                    'instrumental': 'Focused study music with gentle piano, soft strings, minimal percussion, designed for concentration and productivity',
                    'vocal': 'Study music with soft vocal harmonies, motivational lyrics, uplifting melodies that inspire learning'
                },
                'jazz': {
                    'instrumental': 'Smooth jazz with sophisticated piano, walking bass lines, gentle brushed drums, sophisticated chord progressions',
                    'vocal': 'Jazz with smooth vocals, classic standards, sophisticated lyrics, backed by professional jazz ensemble'
                },
                'meditation': {
                    'instrumental': 'Deep meditation music with Tibetan bowls, nature sounds, long sustained tones, perfect for mindfulness practice',
                    'vocal': 'Meditation music with guided vocal elements, mantras, healing frequencies, spiritual atmosphere'
                }
            }
            
            # Get template or default
            template = genre_templates.get(genre, {}).get(vocal_type, f'{vocal_type} {genre} music')
            
            # Add audience-specific elements
            audience_elements = {
                'students': ', optimized for studying and learning',
                'workers': ', perfect for office background and productivity',
                'gamers': ', energetic and engaging for gaming sessions',
                'meditation': ', designed for deep relaxation and mindfulness'
            }
            
            prompt = template + audience_elements.get(audience, '')
            
            return prompt
            
        except Exception as e:
            self.logger.error(f"Error generating music prompt: {e}")
            return f'{vocal_type} {genre} music'
    
    def _generate_music(self, prompt: str, vocal_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Generate music using Suno API"""
        try:
            result = self.suno.generate_music_simple(
                prompt=prompt,
                make_instrumental=(vocal_decision['vocal_type'] == 'instrumental'),
                wait_audio=True
            )
            
            if result and len(result) > 0:
                return {
                    'success': True,
                    'audio_url': result[0].get('audio_url'),
                    'title': result[0].get('title'),
                    'duration': result[0].get('duration', 0)
                }
            else:
                return {
                    'success': False,
                    'error': 'No music generated'
                }
                
        except Exception as e:
            self.logger.error(f"Error generating music: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_thumbnail(self, genre: str, vocal_type: str) -> Dict[str, Any]:
        """Generate 16:9 thumbnail using Nano-Banana (via image_generation tool)"""
        try:
            from core.services.image_client import ImageClient
            
            image_client = ImageClient()
            
            # Create genre-specific thumbnail prompt
            thumbnail_prompts = {
                'lo-fi-hip-hop': 'Cozy lo-fi aesthetic with vintage room, warm lighting, vinyl records, plants, retro computer setup',
                'ambient': 'Ethereal abstract landscape with flowing colors, soft gradients, dreamy atmosphere, cosmic elements',
                'study-music': 'Clean minimalist study space with books, soft lighting, focused atmosphere, productivity vibes',
                'jazz': 'Sophisticated jazz club atmosphere with dim lighting, musical instruments, elegant décor',
                'meditation': 'Peaceful zen garden with stones, flowing water, soft natural lighting, mindful atmosphere'
            }
            
            prompt = thumbnail_prompts.get(genre, f'Beautiful {genre} music visualization')
            prompt += ', 16:9 aspect ratio, YouTube thumbnail style, high quality, modern aesthetic'
            
            # Add vocal/instrumental specific elements
            if vocal_type == 'vocal':
                prompt += ', with subtle musical note elements, expressive atmosphere'
            else:
                prompt += ', abstract musical visualization, instrumental mood'
            
            result = image_client.generate_image(
                prompt=prompt,
                model='fal-ai/nano-banana',  # Best for 16:9 thumbnails
                aspect_ratio='16:9',
                task_summary='YouTube thumbnail generation'
            )
            
            if result.get('success'):
                return {
                    'success': True,
                    'image_url': result.get('image_url'),
                    'prompt_used': prompt
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Thumbnail generation failed')
                }
                
        except Exception as e:
            self.logger.error(f"Error generating thumbnail: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_seo_metadata(self, genre: str, vocal_type: str, audience: str) -> Dict[str, Any]:
        """Generate SEO-optimized title, description, and tags"""
        try:
            # Genre-specific keywords and templates
            genre_keywords = {
                'lo-fi-hip-hop': ['lofi', 'chill', 'study', 'beats', 'relax', 'focus'],
                'ambient': ['ambient', 'atmospheric', 'peaceful', 'meditation', 'calm'],
                'study-music': ['study', 'focus', 'concentration', 'productivity', 'learning'],
                'jazz': ['jazz', 'smooth', 'sophisticated', 'classic', 'elegant'],
                'meditation': ['meditation', 'mindfulness', 'zen', 'spiritual', 'healing']
            }
            
            keywords = genre_keywords.get(genre, [genre])
            if vocal_type == 'instrumental':
                keywords.extend(['instrumental', 'no vocals', 'background'])
            else:
                keywords.extend(['vocal', 'lyrics', 'singing'])
            
            # Generate title
            title_templates = [
                f'{genre.title()} Music for {audience.title()} - {vocal_type.title()}',
                f'Relaxing {genre.title()} - Perfect for {audience.title()}',
                f'{vocal_type.title()} {genre.title()} - {audience.title()} Playlist',
                f'Beautiful {genre.title()} Music - {vocal_type.title()}'
            ]
            
            title = random.choice(title_templates)
            
            # Generate description
            description = f"""🎵 {title}
            
Perfect {genre} music for {audience}. This {vocal_type} track is designed to enhance your {audience} experience with beautiful {genre} sounds.

🔸 Genre: {genre.title()}
🔸 Type: {vocal_type.title()}
🔸 Perfect for: {audience.title()}

#️⃣ Tags: {', '.join([f'#{tag}' for tag in keywords[:10]])}

🎧 Subscribe for more amazing {genre} music!

⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
            
            # Generate tags
            tags = keywords + [
                'music', 'audio', 'soundtrack', 'playlist', 'youtube',
                audience, '2024', 'relaxing', 'background', 'mood'
            ]
            
            # Remove duplicates and limit to 30 tags
            tags = list(set(tags))[:30]
            
            return {
                'title': title,
                'description': description,
                'tags': tags,
                'category': 'Music'
            }
            
        except Exception as e:
            self.logger.error(f"Error generating SEO metadata: {e}")
            return {
                'title': f'{genre.title()} - {vocal_type.title()} Music',
                'description': f'Beautiful {genre} music - {vocal_type}',
                'tags': [genre, vocal_type, 'music'],
                'category': 'Music'
            }
    
    def _create_video(self, audio_url: str, thumbnail_url: Optional[str], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create video combining audio and thumbnail"""
        try:
            # This would integrate with actual video creation service
            # For now, return mock result
            video_id = f"video_{int(time.time())}"
            
            return {
                'success': True,
                'video_id': video_id,
                'video_url': f'output/videos/{video_id}.mp4',
                'duration': 180,  # 3 minutes default
                'title': metadata.get('title', 'Generated Music'),
                'description': metadata.get('description', ''),
                'tags': metadata.get('tags', [])
            }
            
        except Exception as e:
            self.logger.error(f"Error creating video: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _upload_to_youtube(self, channel_id: int, video_data: Dict[str, Any], metadata: Dict[str, Any], privacy: str) -> Dict[str, Any]:
        """Upload video to YouTube using channel credentials"""
        try:
            # This would integrate with actual YouTube Data API v3
            # For now, return mock result
            
            youtube_video_id = f"YT_{int(time.time())}"
            
            # Log upload simulation
            self.logger.info(f"Simulating YouTube upload for channel {channel_id}")
            
            return {
                'success': True,
                'video_id': youtube_video_id,
                'video_url': f'https://youtube.com/watch?v={youtube_video_id}',
                'upload_status': 'completed',
                'privacy_status': privacy
            }
            
        except Exception as e:
            self.logger.error(f"Error uploading to YouTube: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_recent_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent automation logs"""
        try:
            # This would query the automation_logs table
            # For now, return mock data
            return [
                {
                    'timestamp': datetime.now().isoformat(),
                    'channel': 'Lo-Fi Channel',
                    'type': 'generation_completed',
                    'message': 'Successfully generated lo-fi track',
                    'status': 'success'
                }
            ]
            
        except Exception as e:
            self.logger.error(f"Error getting recent logs: {e}")
            return []
    
    def _get_next_tasks(self) -> List[Dict[str, Any]]:
        """Get next scheduled tasks"""
        try:
            # This would return actual scheduled tasks
            # For now, return mock data
            return [
                {
                    'channel': 'Lo-Fi Channel',
                    'scheduled_time': (datetime.now() + timedelta(hours=2)).isoformat(),
                    'task_type': 'generate_and_upload',
                    'genre': 'lo-fi-hip-hop'
                }
            ]
            
        except Exception as e:
            self.logger.error(f"Error getting next tasks: {e}")
            return []

# Global automation engine instance
automation_engine = YouTubeAutomationEngine()

def get_automation_engine():
    """Get the global automation engine instance"""
    return automation_engine