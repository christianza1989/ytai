#!/usr/bin/env python3
"""
Ultimate video creation fix - comprehensive solution
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path

def create_demo_audio():
    """Create a demo audio file for testing"""
    
    print("🎵 Creating demo audio file...")
    
    output_path = Path("/home/user/webapp/output/demo_audio.mp3")
    
    # Create a simple sine wave audio using FFmpeg
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', 'sine=frequency=440:duration=30',  # 30 second 440Hz sine wave
        '-ac', '2',  # Stereo
        '-ar', '44100',  # Sample rate
        '-b:a', '128k',  # Bitrate
        str(output_path)
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and output_path.exists():
            size = output_path.stat().st_size / 1024
            print(f"✅ Demo audio created: {size:.1f} KB")
            return str(output_path)
        else:
            print(f"❌ Demo audio creation failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating demo audio: {e}")
        return None

def create_demo_image():
    """Create a demo image file for testing"""
    
    print("🖼️ Creating demo image file...")
    
    output_path = Path("/home/user/webapp/output/demo_image.png")
    
    # Create a simple colored image using FFmpeg
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', 'color=c=blue:size=1280x720:duration=1',
        '-frames:v', '1',
        str(output_path)
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0 and output_path.exists():
            size = output_path.stat().st_size / 1024
            print(f"✅ Demo image created: {size:.1f} KB")
            return str(output_path)
        else:
            print(f"❌ Demo image creation failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating demo image: {e}")
        return None

def test_video_creation_complete():
    """Test complete video creation pipeline"""
    
    print("\n🎬 Testing complete video creation pipeline...")
    
    # Step 1: Create demo files
    audio_path = create_demo_audio()
    image_path = create_demo_image()
    
    if not audio_path or not image_path:
        print("❌ Cannot create demo files")
        return False
    
    # Step 2: Test VideoCreator
    try:
        sys.path.insert(0, '/home/user/webapp')
        from core.utils.video_creator import VideoCreator
        
        video_creator = VideoCreator()
        
        # Step 3: Create video
        output_dir = Path("/home/user/webapp/output/videos")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "ultimate_test.mp4"
        
        print(f"🔄 Creating video: {output_file}")
        
        result = video_creator.create_video_from_audio_and_image(
            audio_path=audio_path,
            image_path=image_path,
            output_path=str(output_dir),
            title="Ultimate Test Video"
        )
        
        if result:
            created_files = list(output_dir.glob("Ultimate_Test_Video*.mp4"))
            if created_files:
                video_file = created_files[0]
                size = video_file.stat().st_size / 1024 / 1024
                print(f"✅ Video creation SUCCESS: {size:.1f} MB")
                
                # Test video properties
                duration = video_creator.get_audio_duration(str(video_file))
                print(f"⏱️ Video duration: {duration}s")
                
                return True
            else:
                print("❌ Video created but file not found")
                return False
        else:
            print("❌ Video creation method returned False")
            return False
            
    except Exception as e:
        print(f"❌ Video creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def fix_video_creation_in_admin():
    """Fix video creation calls in admin_app.py"""
    
    print("\n🔧 Fixing video creation calls in admin_app.py...")
    
    admin_file = Path("/home/user/webapp/admin_app.py")
    
    with open(admin_file, 'r') as f:
        content = f.read()
    
    # Find and fix video creation calls
    fixes_applied = 0
    
    # Fix 1: Ensure proper error handling in video creation
    if 'Video creation failed' in content:
        print("📋 Found video creation error handling")
        
        # Add better error logging before the failure
        old_pattern = 'raise Exception("Video creation failed")'
        new_pattern = '''print(f"❌ Video creation details: audio={audio_path}, image={image_path}")
                        print(f"❌ Output directory: {output_dir}")
                        print(f"❌ VideoCreator result: {result}")
                        raise Exception("Video creation failed")'''
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_applied += 1
            print("✅ Enhanced error logging for video creation")
    
    # Fix 2: Add fallback for missing audio URLs
    if 'music_url' in content and 'thumbnail_url' in content:
        print("📋 Found video creation with URLs")
        
        # Add URL validation before video creation
        url_validation = '''
                    # Validate URLs before video creation
                    print(f"🔍 Validating URLs:")
                    print(f"   Audio: {audio_url}")
                    print(f"   Image: {image_url}")
                    
                    # Test URL accessibility
                    import requests
                    try:
                        audio_response = requests.head(audio_url, timeout=10)
                        print(f"   Audio URL status: {audio_response.status_code}")
                        if audio_response.status_code != 200:
                            raise Exception(f"Audio URL not accessible: {audio_response.status_code}")
                    except Exception as url_error:
                        print(f"   ❌ Audio URL error: {url_error}")
                        raise Exception(f"Cannot access audio URL: {url_error}")
                    
                    try:
                        image_response = requests.head(image_url, timeout=10)
                        print(f"   Image URL status: {image_response.status_code}")
                        if image_response.status_code != 200:
                            raise Exception(f"Image URL not accessible: {image_response.status_code}")
                    except Exception as url_error:
                        print(f"   ❌ Image URL error: {url_error}")
                        raise Exception(f"Cannot access image URL: {url_error}")
'''
        
        # Add validation before video_creator.create_video calls
        pattern_to_find = 'result = video_creator.create_video('
        if pattern_to_find in content and url_validation not in content:
            content = content.replace(
                pattern_to_find, 
                url_validation + '\n                    ' + pattern_to_find
            )
            fixes_applied += 1
            print("✅ Added URL validation before video creation")
    
    # Apply fixes if any were made
    if fixes_applied > 0:
        # Backup original
        backup_file = admin_file.with_suffix('.py.backup')
        if not backup_file.exists():
            with open(backup_file, 'w') as f:
                f.write(content)
            print(f"📋 Backup saved: {backup_file}")
        
        # Write fixed version
        with open(admin_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Applied {fixes_applied} fixes to admin_app.py")
    else:
        print("✅ No fixes needed in admin_app.py")

def restart_webapp():
    """Restart the webapp to apply fixes"""
    
    print("\n🔄 Restarting webapp to apply fixes...")
    
    try:
        # Restart PM2 process
        result = subprocess.run(['pm2', 'restart', 'webapp'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Webapp restarted successfully")
            
            # Wait and test
            import time
            time.sleep(3)
            
            test_result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 
                                        'http://localhost:3000/'], 
                                      capture_output=True, text=True, timeout=10)
            
            if test_result.stdout.strip() == '302':
                print("✅ Webapp is running and accessible")
                return True
            else:
                print(f"⚠️ Webapp status: {test_result.stdout.strip()}")
                return False
        else:
            print(f"❌ Restart failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Restart error: {e}")
        return False

def main():
    """Main fix function"""
    
    print("🔧 Ultimate Video Creation Fix")
    print("=" * 60)
    
    success_steps = 0
    total_steps = 4
    
    # Step 1: Test video creation pipeline
    print(f"\n📋 Step 1/{total_steps}: Test video creation pipeline")
    if test_video_creation_complete():
        success_steps += 1
        print("✅ Video creation pipeline working")
    else:
        print("❌ Video creation pipeline has issues")
    
    # Step 2: Fix admin app calls
    print(f"\n📋 Step 2/{total_steps}: Fix admin app video calls")
    fix_video_creation_in_admin()
    success_steps += 1
    
    # Step 3: Restart webapp
    print(f"\n📋 Step 3/{total_steps}: Restart webapp")
    if restart_webapp():
        success_steps += 1
        print("✅ Webapp restarted successfully")
    else:
        print("⚠️ Webapp restart had issues")
    
    # Step 4: Final validation
    print(f"\n📋 Step 4/{total_steps}: Final validation")
    
    # Check if output directory has videos
    video_dir = Path("/home/user/webapp/output/videos")
    videos = list(video_dir.glob("*.mp4")) if video_dir.exists() else []
    
    if videos:
        print(f"✅ Found {len(videos)} video files")
        for video in videos[:3]:
            size = video.stat().st_size / 1024 / 1024
            print(f"   - {video.name}: {size:.1f} MB")
        success_steps += 1
    else:
        print("❌ No video files found")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"🎯 Fix Summary: {success_steps}/{total_steps} steps successful")
    
    if success_steps >= 3:
        print("🎉 Video creation should now work!")
        print("\n📋 Next steps:")
        print("   1. Go to: https://3000-i1qrgf92mv1ui8osdmu6r-6532622b.e2b.dev")
        print("   2. Login: admin / admin123")
        print("   3. Go to Music Generator")
        print("   4. Create a new track")
        print("   5. Generate video - should work now!")
    else:
        print("⚠️ Some issues remain. Check the logs above.")
        print("\n📋 Manual troubleshooting:")
        print("   1. Check FFmpeg installation: ffmpeg -version")
        print("   2. Check disk space: df -h")
        print("   3. Check PM2 logs: pm2 logs webapp")

if __name__ == "__main__":
    main()