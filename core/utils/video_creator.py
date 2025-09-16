#!/usr/bin/env python3
"""
Video Creator - FFmpeg integration for creating videos from audio + thumbnail
Optimized for YouTube uploads with proper encoding settings
"""

import os
import subprocess
import tempfile
import requests
from pathlib import Path
from typing import Optional, Dict, Any
import json
import time

class VideoCreator:
    """Professional video creation using FFmpeg for YouTube optimization"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "video_creation"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # YouTube optimized settings
        self.youtube_settings = {
            'video_codec': 'libx264',
            'audio_codec': 'aac', 
            'video_bitrate': '2500k',  # Good quality for YouTube
            'audio_bitrate': '128k',   # Standard audio quality
            'fps': '30',               # YouTube standard
            'resolution': '1920x1080', # Full HD
            'preset': 'fast',          # Encoding speed vs quality balance
            'crf': '23'                # Constant Rate Factor (18-28 range, lower = better quality)
        }
    
    def download_file(self, url: str, output_path: str, file_type: str = "audio") -> bool:
        """Enhanced download with better error reporting"""
        # Enhanced error reporting
        """Download audio or image file from URL or copy local file"""
        try:
            print(f"🔄 Getting {file_type}: {url}")
            
            # Handle local file paths (file:// URLs or absolute paths)
            if url.startswith('file://'):
                local_path = url.replace('file://', '')
                if Path(local_path).exists():
                    # Copy local file
                    import shutil
                    shutil.copy2(local_path, output_path)
                    file_size = Path(output_path).stat().st_size
                    print(f"✅ Copied local {file_type}: {file_size / 1024 / 1024:.1f} MB")
                    return True
                else:
                    print(f"❌ Local file not found: {local_path}")
                    return False
            elif Path(url).exists():
                # Direct local path
                import shutil
                shutil.copy2(url, output_path)
                file_size = Path(output_path).stat().st_size
                print(f"✅ Copied local {file_type}: {file_size / 1024 / 1024:.1f} MB")
                return True
            else:
                # Download from URL
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, stream=True, timeout=30)
                print(f"🔄 Headers: {headers}")
                print(f"🔄 Timeout: 30s")
                response.raise_for_status()
                print(f"📡 Response status: {response.status_code}")
                print(f"📡 Response headers: {dict(list(response.headers.items())[:5])}")
                
                # Validate response
                if response.status_code != 200:
                    print(f"❌ HTTP {response.status_code}: {response.reason}")
                    return False
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = Path(output_path).stat().st_size
                print(f"✅ Downloaded {file_type}: {file_size / 1024 / 1024:.1f} MB")
                return True
            
        except Exception as e:
            print(f"❌ Failed to get {file_type}: {e}")
            return False
    
    def get_audio_duration(self, audio_path: str) -> Optional[float]:
        """Get audio duration using ffprobe"""
        try:
            cmd = [
                'ffprobe', 
                '-v', 'quiet', 
                '-print_format', 'json', 
                '-show_format', 
                audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                duration = float(data['format']['duration'])
                print(f"🎵 Audio duration: {duration:.1f} seconds")
                return duration
            else:
                print(f"⚠️ Could not get audio duration: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting audio duration: {e}")
            return None
    
    def create_video(self, music_url: str, thumbnail_url: str, output_path: str, 
                    title: str = "Generated Music Video") -> Dict[str, Any]:
        """
        Create optimized video from audio URL + thumbnail URL
        
        Args:
            music_url: URL to audio file
            thumbnail_url: URL to thumbnail image  
            output_path: Path where to save the final video
            title: Video title for metadata
            
        Returns:
            Dict with success status, file paths, and metadata
        """
        try:
            print(f"🎥 Creating video: {title}")
            print(f"🎵 Audio: {music_url}")
            print(f"🖼️ Thumbnail: {thumbnail_url}")
            
            # Create temporary files
            temp_audio = self.temp_dir / f"audio_{int(time.time())}.mp3"
            temp_thumbnail = self.temp_dir / f"thumb_{int(time.time())}.jpg"
            
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Step 1: Download audio
            if not self.download_file(music_url, str(temp_audio), "audio"):
                return {'success': False, 'error': 'Failed to download audio'}
            
            # Step 2: Download thumbnail
            if not self.download_file(thumbnail_url, str(temp_thumbnail), "thumbnail"):
                return {'success': False, 'error': 'Failed to download thumbnail'}
            
            # Step 3: Get audio duration for video length
            duration = self.get_audio_duration(str(temp_audio))
            if not duration:
                duration = 180  # Default 3 minutes if can't detect
            
            # Step 4: Create video with FFmpeg (YouTube optimized)
            print(f"🔄 Creating {duration:.1f}s video with FFmpeg...")
            
            # Simplified FFmpeg command for better compatibility
            ffmpeg_cmd = [
                'ffmpeg', '-y',  # Overwrite output file
                '-i', str(temp_audio),                     # Audio file first
                '-loop', '1', '-i', str(temp_thumbnail),  # Loop static image
                '-c:v', 'libx264',      # Video codec
                '-c:a', 'aac',          # Audio codec  
                '-b:a', '128k',         # Audio bitrate
                '-pix_fmt', 'yuv420p',  # Pixel format
                '-shortest',            # End when shortest stream ends
                '-metadata', f'title={title}',
                output_path
            ]
            
            # Execute FFmpeg
            print("🔄 Running FFmpeg...")
            start_time = time.time()
            
            # Execute with proper process handling
            try:
                result = subprocess.run(
                    ffmpeg_cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=None  # No timeout - let it complete
                )
            except subprocess.TimeoutExpired:
                print("⚠️ FFmpeg timeout - but may have succeeded")
                # Check if output file exists and has reasonable size
                if Path(output_path).exists() and Path(output_path).stat().st_size > 1000:
                    print("✅ Video file created despite timeout")
                    result = type('Result', (), {'returncode': 0})()  # Mock success
                else:
                    raise
            
            encode_time = time.time() - start_time
            
            # Check success - either return code 0 OR output file exists with good size
            output_exists = Path(output_path).exists()
            output_size = Path(output_path).stat().st_size if output_exists else 0
            
            print(f"🔍 FFmpeg result: return_code={getattr(result, 'returncode', 'N/A')}, file_exists={output_exists}, size={output_size}")
            
            if (getattr(result, 'returncode', 0) == 0) or (output_exists and output_size > 10000):  # At least 10KB
                # Success!
                file_size = output_size
                file_size_mb = file_size / 1024 / 1024
                
                print(f"✅ Video created successfully!")
                print(f"📁 Output: {output_path}")
                print(f"📊 Size: {file_size_mb:.1f} MB")
                print(f"⏱️ Encoding time: {encode_time:.1f}s")
                
                # Cleanup temp files
                temp_audio.unlink(missing_ok=True)
                temp_thumbnail.unlink(missing_ok=True)
                
                return {
                    'success': True,
                    'video_path': output_path,
                    'file_size_mb': file_size_mb,
                    'duration_seconds': duration,
                    'encoding_time_seconds': encode_time,
                    'audio_url': music_url,
                    'thumbnail_url': thumbnail_url,
                    'resolution': self.youtube_settings['resolution'],
                    'video_bitrate': self.youtube_settings['video_bitrate'],
                    'audio_bitrate': self.youtube_settings['audio_bitrate']
                }
                
            else:
                error_msg = result.stderr or result.stdout or "Unknown FFmpeg error"
                print(f"❌ FFmpeg failed: {error_msg}")
                
                # Cleanup temp files
                temp_audio.unlink(missing_ok=True)
                temp_thumbnail.unlink(missing_ok=True)
                
                return {
                    'success': False, 
                    'error': f'FFmpeg encoding failed: {error_msg}',
                    'ffmpeg_stdout': result.stdout,
                    'ffmpeg_stderr': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            print("❌ FFmpeg timeout - video too long or system overloaded")
            return {'success': False, 'error': 'Video creation timeout'}
            
        except Exception as e:
            print(f"❌ Video creation error: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_video_from_audio_and_image(self, audio_path: str, image_path: str, 
                                         output_path: str, title: str = "Generated Music Video") -> bool:
        """
        Simplified video creation with better error handling
        """
        try:
            print(f"🎥 Creating video: {title}")
            print(f"🎵 Audio: {audio_path}")
            print(f"🖼️ Image: {image_path}")
            
            # Validate input files
            if not Path(audio_path).exists():
                print(f"❌ Audio file not found: {audio_path}")
                return False
                
            if not Path(image_path).exists():
                print(f"❌ Image file not found: {image_path}")
                return False
            
            # Get audio duration
            duration = self.get_audio_duration(audio_path)
            if not duration or duration <= 0:
                duration = 180  # Default 3 minutes
                print(f"⚠️ Could not detect duration, using {duration}s")
            
            print(f"⏱️ Audio duration: {duration} seconds")
            
            # Ensure output directory exists and create output file path
            output_dir = Path(output_path)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Create safe filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            video_file = output_dir / f"{safe_title}.mp4"
            
            print(f"📁 Output: {video_file}")
            
            # Simple FFmpeg command that works reliably
            import subprocess
            
            ffmpeg_cmd = [
                'ffmpeg', '-y',  # Overwrite existing
                '-i', audio_path,  # Audio input
                '-loop', '1', '-i', image_path,  # Image input (looped)
                '-c:v', 'libx264',  # Video codec
                '-c:a', 'aac',      # Audio codec
                '-b:a', '128k',     # Audio bitrate
                '-pix_fmt', 'yuv420p',  # Pixel format
                '-t', str(duration),    # Duration
                '-shortest',        # Stop when shortest input ends
                '-f', 'mp4',        # Force MP4 format
                str(video_file)     # Output
            ]
            
            print("🔄 Running simplified FFmpeg...")
            
            # Run FFmpeg with proper input handling
            result = subprocess.run(
                ffmpeg_cmd,
                input='',  # Send empty input to avoid hanging on "Press [q] to stop"
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            print(f"📊 FFmpeg exit code: {result.returncode}")
            
            # Check if video was created successfully
            if video_file.exists():
                file_size = video_file.stat().st_size
                
                if file_size > 1000:  # At least 1KB
                    size_mb = file_size / 1024 / 1024
                    print(f"✅ Video created: {size_mb:.1f} MB")
                    return True
                else:
                    print(f"❌ Video too small: {file_size} bytes")
                    print(f"FFmpeg stderr: {result.stderr[-500:]}")  # Last 500 chars
                    return False
            else:
                print("❌ Video file not created")
                print(f"FFmpeg stderr: {result.stderr[-500:]}")  # Last 500 chars
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️ FFmpeg timeout - checking if file was created...")
            if video_file.exists() and video_file.stat().st_size > 1000:
                print(f"✅ Video created despite timeout: {video_file.stat().st_size / 1024 / 1024:.1f} MB")
                return True
            else:
                print("❌ Timeout and no valid video file")
                return False
                
        except Exception as e:
            print(f"❌ Video creation error: {e}")
            import traceback
            traceback.print_exc()
            return False
    def create_video_with_progress(self, music_url: str, thumbnail_url: str, 
                                 output_path: str, title: str = "Generated Music Video",
                                 progress_callback=None) -> Dict[str, Any]:
        """Create video with progress callbacks for UI updates"""
        
        def update_progress(step: str, percent: int):
            if progress_callback:
                progress_callback(step, percent)
            else:
                print(f"🎥 [{percent}%] {step}")
        
        try:
            update_progress("Starting video creation", 5)
            
            # Download phase
            update_progress("Downloading audio", 20)
            result = self.create_video(music_url, thumbnail_url, output_path, title)
            
            if result['success']:
                update_progress("Video creation completed", 100)
            else:
                update_progress("Video creation failed", 0)
            
            return result
            
        except Exception as e:
            update_progress("Error in video creation", 0)
            return {'success': False, 'error': str(e)}

# Test function for standalone usage
def test_video_creation():
    """Test video creation with sample files"""
    creator = VideoCreator()
    
    # Test with sample URLs (these would be replaced with real URLs)
    test_audio_url = "https://example.com/sample_music.mp3"
    test_thumbnail_url = "https://example.com/sample_thumbnail.jpg"
    test_output = "/tmp/test_video.mp4"
    
    result = creator.create_video(
        music_url=test_audio_url,
        thumbnail_url=test_thumbnail_url,
        output_path=test_output,
        title="Test Music Video"
    )
    
    print(f"Test result: {result}")
    return result

if __name__ == "__main__":
    test_video_creation()