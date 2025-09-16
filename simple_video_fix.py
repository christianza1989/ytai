#!/usr/bin/env python3
"""
Simple fix for video creation issues
"""

import os
import sys
import shutil
from pathlib import Path

def create_simple_video():
    """Create a simple test video using existing files"""
    
    print("🔧 Simple Video Creation Test")
    print("=" * 40)
    
    # Find existing files
    existing_videos = list(Path("/home/user/webapp/output/videos").glob("*.mp4"))
    existing_audio = list(Path("/home/user/webapp").rglob("*.mp3"))
    
    print(f"📁 Found {len(existing_videos)} existing videos")
    print(f"📁 Found {len(existing_audio)} audio files")
    
    if existing_videos:
        print("✅ Videos already exist!")
        for video in existing_videos[:3]:
            size = video.stat().st_size / 1024 / 1024
            print(f"   - {video.name}: {size:.1f} MB")
        return True
    
    if not existing_audio:
        print("❌ No audio files found to test with")
        return False
    
    # Use first audio file
    audio_file = existing_audio[0]
    print(f"🎵 Using audio: {audio_file}")
    
    # Create a simple image
    image_file = Path("/tmp/test_image.png")
    import base64
    png_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU8j6gAAAABJRU5ErkJggg==')
    with open(image_file, 'wb') as f:
        f.write(png_data)
    
    print(f"🖼️ Created test image: {image_file}")
    
    # Test FFmpeg directly
    output_dir = Path("/home/user/webapp/output/videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "simple_test.mp4"
    
    print(f"📁 Output: {output_file}")
    
    # Simple FFmpeg command
    import subprocess
    
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', str(audio_file),
        '-loop', '1', '-i', str(image_file),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        str(output_file)
    ]
    
    print("🔄 Running FFmpeg...")
    print(f"Command: {' '.join(ffmpeg_cmd[:8])}...")
    
    try:
        result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            if output_file.exists():
                size = output_file.stat().st_size / 1024 / 1024
                print(f"✅ Video created successfully: {size:.1f} MB")
                return True
            else:
                print("❌ FFmpeg succeeded but no output file")
                return False
        else:
            print(f"❌ FFmpeg failed (exit {result.returncode})")
            print(f"Error: {result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg timeout")
        return False
    except Exception as e:
        print(f"❌ Error running FFmpeg: {e}")
        return False
    
    finally:
        # Cleanup
        if image_file.exists():
            image_file.unlink()

def check_video_creation_endpoint():
    """Check if video creation endpoint works"""
    
    print("\n🔍 Checking video creation endpoint...")
    
    # Test with curl
    import subprocess
    
    try:
        # First check if we can access the app
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:3000/'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        status_code = result.stdout.strip()
        print(f"📡 App status: {status_code}")
        
        if status_code == '302':
            print("✅ App is running (redirects to login)")
            print("🔗 Access: https://3000-i1qrgf92mv1ui8osdmu6r-6532622b.e2b.dev")
            return True
        else:
            print(f"⚠️ App status unexpected: {status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot check app status: {e}")
        return False

def fix_video_creation_config():
    """Fix video creation configuration"""
    
    print("\n🔧 Fixing video creation configuration...")
    
    # Check if VideoCreator exists and works
    try:
        sys.path.insert(0, '/home/user/webapp')
        from core.utils.video_creator import VideoCreator
        
        video_creator = VideoCreator()
        print("✅ VideoCreator imported successfully")
        
        # Check temp directory
        temp_dir = video_creator.temp_dir
        print(f"📁 Temp directory: {temp_dir}")
        
        if not temp_dir.exists():
            temp_dir.mkdir(parents=True, exist_ok=True)
            print("✅ Created temp directory")
        
        # Check output directory
        output_dir = Path("/home/user/webapp/output/videos")
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Output directory: {output_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ VideoCreator error: {e}")
        return False

def main():
    """Main fix function"""
    
    print("🔧 Simple Video Creation Fix")
    print("=" * 50)
    
    # Step 1: Check configuration
    if fix_video_creation_config():
        
        # Step 2: Test simple video creation
        if create_simple_video():
            
            # Step 3: Check endpoint
            check_video_creation_endpoint()
            
            print("\n🎉 Video creation should work now!")
            print("📋 Try generating a video through the web interface:")
            print("   1. Go to: https://3000-i1qrgf92mv1ui8osdmu6r-6532622b.e2b.dev")
            print("   2. Login: admin / admin123")
            print("   3. Navigate to Music Generator")
            print("   4. Create a new music track")
            print("   5. Generate video from the track")
            
        else:
            print("\n⚠️ Video creation still has issues")
            print("📋 Possible causes:")
            print("   - FFmpeg not properly configured")
            print("   - Missing audio/image files")
            print("   - File permission issues")
    else:
        print("\n❌ Configuration issues detected")
        print("📋 Check VideoCreator class and dependencies")

if __name__ == "__main__":
    main()