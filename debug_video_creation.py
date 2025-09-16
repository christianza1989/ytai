#!/usr/bin/env python3
"""
Debug video creation issues
"""

import sys
import os
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.utils.video_creator import VideoCreator

def test_video_creation():
    """Test video creation with sample files"""
    
    print("🧪 Debug Video Creation")
    print("=" * 50)
    
    # Initialize video creator
    video_creator = VideoCreator()
    
    # Create test audio file (minimal MP3)
    test_audio = tempfile.mktemp(suffix='.mp3')
    with open(test_audio, 'wb') as f:
        # Write minimal MP3 header
        f.write(b'ID3\x04\x00\x00\x00\x00\x00\x00')  # ID3 header
        f.write(b'TIT2\x00\x00\x00\x0b\x00\x00\x00Test Title')  # Title frame
        f.write(b'\xff\xfb\x90\x00' + b'\x00' * 1000)  # MP3 audio frame with padding
    
    # Create test image file (minimal PNG)
    test_image = tempfile.mktemp(suffix='.png')
    import base64
    png_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU8j6gAAAABJRU5ErkJggg==')
    with open(test_image, 'wb') as f:
        f.write(png_data)
    
    print(f"📁 Test audio: {test_audio}")
    print(f"📁 Test image: {test_image}")
    
    # Create output directory
    output_dir = Path(tempfile.gettempdir()) / "test_video"
    output_dir.mkdir(exist_ok=True)
    output_video = output_dir / "test_output.mp4"
    
    print(f"📁 Output video: {output_video}")
    
    try:
        # Test local file creation
        print("\n🎬 Testing local file video creation...")
        result = video_creator.create_video_from_audio_and_image(
            audio_path=test_audio,
            image_path=test_image,
            output_path=str(output_dir),
            title="Debug Test Video"
        )
        
        if result:
            print("✅ Local file video creation: SUCCESS")
            
            # Check if video was created
            created_files = list(output_dir.glob("*.mp4"))
            if created_files:
                video_file = created_files[0]
                file_size = video_file.stat().st_size
                print(f"📁 Created video: {video_file}")
                print(f"📊 File size: {file_size / 1024:.1f} KB")
                
                # Test video properties
                print("\n🔍 Testing video properties...")
                duration = video_creator.get_audio_duration(str(video_file))
                print(f"⏱️ Duration: {duration}s")
                
            else:
                print("❌ No video files found in output directory")
        else:
            print("❌ Local file video creation: FAILED")
            
    except Exception as e:
        print(f"❌ Video creation error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup test files
        try:
            os.remove(test_audio)
            os.remove(test_image)
            # Remove created videos
            for video_file in output_dir.glob("*.mp4"):
                video_file.unlink()
            output_dir.rmdir()
            print("\n🧹 Cleaned up test files")
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")

def test_url_download():
    """Test downloading from URLs"""
    
    print("\n🌐 Testing URL downloads...")
    
    video_creator = VideoCreator()
    
    # Test with a sample audio URL (you can use one from your recent generations)
    sample_audio_url = "https://mfile.erweima.ai/ZjA4OWQ4OWYtZWI2MS00NTJjLWI2NTktYjBkMDdlNTIyZmE3"
    sample_image_url = "https://ideogram.ai/api/images/ephemeral/G6C7UbcxQbORoup-2P0i_w.png?exp=1758118930&sig=05d640f15e7171335b7a393b803a97d28dc13bcf017386f1487b02675b58d055"
    
    temp_audio = tempfile.mktemp(suffix='.mp3')
    temp_image = tempfile.mktemp(suffix='.png')
    
    try:
        print(f"🔄 Downloading audio from: {sample_audio_url[:50]}...")
        audio_ok = video_creator.download_file(sample_audio_url, temp_audio, "audio")
        print(f"📁 Audio download: {'✅ SUCCESS' if audio_ok else '❌ FAILED'}")
        
        if audio_ok:
            file_size = Path(temp_audio).stat().st_size
            print(f"📊 Audio file size: {file_size / 1024:.1f} KB")
        
        print(f"🔄 Downloading image from: {sample_image_url[:50]}...")
        image_ok = video_creator.download_file(sample_image_url, temp_image, "image")
        print(f"📁 Image download: {'✅ SUCCESS' if image_ok else '❌ FAILED'}")
        
        if image_ok:
            file_size = Path(temp_image).stat().st_size
            print(f"📊 Image file size: {file_size / 1024:.1f} KB")
            
        if audio_ok and image_ok:
            print("✅ URL downloads working correctly")
            
            # Test creating video from downloaded files
            output_dir = Path(tempfile.gettempdir()) / "test_video_urls"
            output_dir.mkdir(exist_ok=True)
            
            print("\n🎬 Testing video creation from URLs...")
            result = video_creator.create_video_from_audio_and_image(
                audio_path=temp_audio,
                image_path=temp_image,
                output_path=str(output_dir),
                title="URL Test Video"
            )
            
            if result:
                print("✅ Video creation from URLs: SUCCESS")
                created_files = list(output_dir.glob("*.mp4"))
                if created_files:
                    print(f"📁 Created video: {created_files[0].name}")
            else:
                print("❌ Video creation from URLs: FAILED")
                
    except Exception as e:
        print(f"❌ URL test error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        try:
            if Path(temp_audio).exists():
                os.remove(temp_audio)
            if Path(temp_image).exists():
                os.remove(temp_image)
            # Remove test directory
            test_dir = Path(tempfile.gettempdir()) / "test_video_urls"
            if test_dir.exists():
                for f in test_dir.glob("*"):
                    f.unlink()
                test_dir.rmdir()
        except:
            pass

def main():
    """Run all tests"""
    print("🔧 Video Creation Debug Suite")
    print("=" * 60)
    
    # Test 1: Basic video creation
    test_video_creation()
    
    # Test 2: URL downloads
    test_url_download()
    
    print("\n🎉 Debug tests completed!")
    print("📋 If all tests passed, video creation should work in your app")

if __name__ == "__main__":
    main()