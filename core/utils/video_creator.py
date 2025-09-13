import os
from typing import Optional
from pathlib import Path

try:
    from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, ColorClip, VideoFileClip
    MOVIEPY_AVAILABLE = True
    print("✅ MoviePy successfully loaded - video creation enabled")
except ImportError as e:
    print(f"⚠️  MoviePy not available: {e}. Video creation will be disabled.")
    MOVIEPY_AVAILABLE = False

class VideoCreator:
    """Utility class for creating videos from audio and image files"""

    def __init__(self):
        self.moviepy_available = MOVIEPY_AVAILABLE
        if not self.moviepy_available:
            print("⚠️  Video creation functions are disabled due to missing MoviePy dependency.")

    def create_video_from_audio_and_image(self, image_path: str, audio_path: str, output_path: str, title: str) -> bool:
        """Create MP4 video from image and audio files"""
        if not self.moviepy_available:
            print("❌ Video creation is disabled - MoviePy not available")
            print(f"📝 Would create video: {title}")
            print(f"   Image: {image_path}")
            print(f"   Audio: {audio_path}")
            print(f"   Output: {output_path}")
            return False
            
        try:
            print(f"🎬 Kuriamas video failas: {title}")

            # Check if input files exist
            if not Path(image_path).exists():
                print(f"❌ Paveikslėlio failas nerastas: {image_path}")
                return False

            if not Path(audio_path).exists():
                print(f"❌ Garso failas nerastas: {audio_path}")
                return False

            # Ensure output directory exists
            Path(output_path).mkdir(parents=True, exist_ok=True)

            # Load audio file to get duration
            print("📏 Kraunamas garso failas...")
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            print(f"🎵 Garso trukmė: {duration:.1f} sekundžių")

            # Load image and set duration to match audio
            print("🖼️ Kraunamas paveikslėlis...")
            image_clip = ImageClip(image_path, duration=duration)

            # Resize image to standard video dimensions (1920x1080) while maintaining aspect ratio
            image_clip = image_clip.resize(height=1080)
            if image_clip.w > 1920:
                image_clip = image_clip.resize(width=1920)

            # Center the image
            image_clip = image_clip.set_position('center')

            # Create background (black)
            background = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=duration)

            # Combine background, image, and audio
            print("🎬 Kombinuojami elementai...")
            video = CompositeVideoClip([background, image_clip])
            video = video.set_audio(audio_clip)

            # Generate output filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            output_filename = f"{safe_title}.mp4"
            output_file_path = Path(output_path) / output_filename

            # Export video
            print(f"💾 Eksportuojamas video: {output_file_path}")
            video.write_videofile(
                str(output_file_path),
                fps=24,  # Standard frame rate
                codec='libx264',  # H.264 codec
                audio_codec='aac',  # AAC audio codec
                temp_audiofile=None,
                remove_temp=True,
                verbose=False,
                logger=None
            )

            # Clean up clips
            audio_clip.close()
            image_clip.close()
            video.close()

            # Get file size
            file_size = output_file_path.stat().st_size
            print(f"✅ Video sukurtas: {output_file_path} ({file_size / (1024*1024):.1f} MB)")

            return True

        except Exception as e:
            print(f"❌ Klaida kuriant video: {e}")
            return False

    def create_video_batch(self, image_path: str, audio_files: list, output_path: str, base_title: str) -> list:
        """Create multiple videos from one image and multiple audio files"""
        results = []

        for i, audio_path in enumerate(audio_files, 1):
            title = f"{base_title}_v{i}"
            success = self.create_video_from_audio_and_image(
                image_path=image_path,
                audio_path=audio_path,
                output_path=output_path,
                title=title
            )
            results.append({
                'audio_file': audio_path,
                'title': title,
                'success': success
            })

        return results

    def get_video_info(self, video_path: str) -> Optional[dict]:
        """Get information about a video file"""
        if not self.moviepy_available:
            print("❌ Video info retrieval is disabled - MoviePy not available")
            return None
            
        try:
            if not Path(video_path).exists():
                return None

            clip = VideoFileClip(video_path)
            info = {
                'duration': clip.duration,
                'size': clip.size,
                'fps': clip.fps,
                'path': video_path
            }
            clip.close()

            return info

        except Exception as e:
            print(f"❌ Klaida gaunant video informaciją: {e}")
            return None
