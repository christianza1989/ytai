#!/usr/bin/env python3
"""
Fix video creation by using alternative Suno URLs and improved error handling
"""

import os
import sys
import json
import requests
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.utils.video_creator import VideoCreator

def test_suno_urls():
    """Test different Suno URL formats"""
    
    print("🔧 Testing Suno URL formats...")
    
    # Get recent track data from generation tasks
    with open('/home/user/webapp/data/generation_tasks.json', 'r') as f:
        tasks_data = json.load(f)
    
    # Find latest successful music generation
    latest_track = None
    for task_id, task in tasks_data.items():
        if ('completed_at' in task and 
            task.get('result', {}).get('success') and 
            'suno_metadata' in task.get('result', {})):
            latest_track = task['result']['suno_metadata']
            print(f"📋 Found track: {latest_track.get('title', 'Unknown')}")
            break
    
    if not latest_track:
        print("❌ No successful tracks found")
        return None
    
    # Test different URL formats
    test_urls = []
    
    # Original URLs from metadata
    if 'audioUrl' in latest_track:
        test_urls.append(('audioUrl', latest_track['audioUrl']))
    if 'sourceAudioUrl' in latest_track:
        test_urls.append(('sourceAudioUrl', latest_track['sourceAudioUrl']))
    if 'streamAudioUrl' in latest_track:
        test_urls.append(('streamAudioUrl', latest_track['streamAudioUrl']))
    if 'sourceStreamAudioUrl' in latest_track:
        test_urls.append(('sourceStreamAudioUrl', latest_track['sourceStreamAudioUrl']))
    
    print(f"🧪 Testing {len(test_urls)} URLs...")
    
    working_url = None
    for url_type, url in test_urls:
        if not url:
            continue
            
        try:
            print(f"🔄 Testing {url_type}: {url[:50]}...")
            
            # Test with GET request (not HEAD)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(list(response.headers.items())[:3])}")
            
            if response.status_code == 200:
                content_length = response.headers.get('content-length')
                content_type = response.headers.get('content-type', '')
                
                if content_length:
                    size_mb = int(content_length) / 1024 / 1024
                    print(f"   ✅ {url_type}: {size_mb:.1f} MB, {content_type}")
                    
                    if 'audio' in content_type or 'mpeg' in content_type:
                        working_url = (url_type, url)
                        break
                else:
                    # Try to read first chunk to check if it's audio
                    chunk = next(response.iter_content(1024), None)
                    if chunk and len(chunk) > 100:
                        print(f"   ✅ {url_type}: Stream available, {len(chunk)} bytes")
                        working_url = (url_type, url)
                        break
                        
            else:
                print(f"   ❌ {url_type}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {url_type}: {e}")
    
    if working_url:
        print(f"\n✅ Working URL found: {working_url[0]} - {working_url[1]}")
        return working_url[1], latest_track
    else:
        print("\n❌ No working audio URLs found")
        return None, latest_track

def create_test_video_with_working_url():
    """Create a test video using working Suno URL"""
    
    print("\n🎬 Creating test video with working Suno URL...")
    
    # Test Suno URLs
    audio_url, track_data = test_suno_urls()
    
    if not audio_url:
        print("❌ Cannot create video - no working audio URL")
        return False
    
    # Get image URL from track data
    image_url = track_data.get('imageUrl') or track_data.get('sourceImageUrl')
    if not image_url:
        print("❌ No image URL found in track data")
        return False
    
    print(f"🎵 Audio: {audio_url}")
    print(f"🖼️ Image: {image_url}")
    
    # Create video
    video_creator = VideoCreator()
    output_dir = Path("/home/user/webapp/output/videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    title = track_data.get('title', 'Test Video')
    output_file = output_dir / f"{title.replace(' ', '_')}_fixed.mp4"
    
    try:
        print(f"🔄 Creating video: {output_file}")
        
        result = video_creator.create_video(
            music_url=audio_url,
            thumbnail_url=image_url,
            output_path=str(output_file),
            title=title
        )
        
        if result.get('success'):
            print("✅ Video creation SUCCESS!")
            print(f"📁 Created: {output_file}")
            print(f"📊 Size: {result.get('file_size_mb', 0):.1f} MB")
            return True
        else:
            print(f"❌ Video creation failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during video creation: {e}")
        import traceback
        traceback.print_exc()
        return False

def patch_video_creator():
    """Patch VideoCreator to handle Suno URLs better"""
    
    print("\n🔧 Patching VideoCreator for better Suno support...")
    
    # Read the current VideoCreator
    video_creator_path = Path("/home/user/webapp/core/utils/video_creator.py")
    
    with open(video_creator_path, 'r') as f:
        content = f.read()
    
    # Add better Suno URL handling
    patch_code = '''
    def download_file_improved(self, url: str, output_path: str, file_type: str = "audio") -> bool:
        """Improved download with better Suno support"""
        try:
            print(f"🔄 Getting {file_type}: {url}")
            
            # Handle local file paths
            if url.startswith('file://') or Path(url).exists():
                # Local file handling (existing code)
                if url.startswith('file://'):
                    local_path = url.replace('file://', '')
                else:
                    local_path = url
                    
                if Path(local_path).exists():
                    import shutil
                    shutil.copy2(local_path, output_path)
                    file_size = Path(output_path).stat().st_size
                    print(f"✅ Copied local {file_type}: {file_size / 1024 / 1024:.1f} MB")
                    return True
                else:
                    print(f"❌ Local file not found: {local_path}")
                    return False
            else:
                # Enhanced URL download for Suno
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': '*/*',
                    'Accept-Encoding': 'identity',  # Prevent compression issues
                    'Connection': 'keep-alive'
                }
                
                # Special handling for audiopipe.suno.ai
                if 'audiopipe.suno.ai' in url:
                    headers['Referer'] = 'https://suno.com/'
                    
                print(f"🔄 Downloading from: {url[:80]}...")
                
                response = requests.get(url, headers=headers, stream=True, timeout=60)
                
                # Log response details for debugging
                print(f"   Response: {response.status_code} {response.reason}")
                if response.status_code != 200:
                    print(f"   Headers: {dict(response.headers)}")
                
                response.raise_for_status()
                
                # Download with progress
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Show progress for large files
                            if total_size > 0 and downloaded % (1024*1024) == 0:
                                progress = (downloaded / total_size) * 100
                                print(f"   📥 {progress:.1f}% ({downloaded/1024/1024:.1f}MB)")
                
                file_size = Path(output_path).stat().st_size
                
                # Validate download
                if file_size == 0:
                    print(f"❌ Downloaded file is empty")
                    return False
                    
                if file_type == "audio" and file_size < 1000:
                    print(f"❌ Audio file too small: {file_size} bytes")
                    return False
                
                print(f"✅ Downloaded {file_type}: {file_size / 1024 / 1024:.1f} MB")
                return True
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error downloading {file_type}: {e}")
            return False
        except Exception as e:
            print(f"❌ Failed to get {file_type}: {e}")
            return False
'''
    
    # Check if patch is needed
    if 'download_file_improved' not in content:
        print("📝 Adding improved download method to VideoCreator...")
        
        # Insert after the __init__ method
        init_pos = content.find('def download_file(')
        if init_pos > 0:
            # Replace the download_file method
            content_lines = content.split('\n')
            new_lines = []
            skip_lines = False
            indent_count = 0
            
            for line in content_lines:
                if 'def download_file(' in line:
                    skip_lines = True
                    indent_count = len(line) - len(line.lstrip())
                    new_lines.append(patch_code.strip())
                    continue
                    
                if skip_lines:
                    current_indent = len(line) - len(line.lstrip()) if line.strip() else indent_count + 1
                    
                    # Continue skipping if we're still in the method
                    if line.strip() and current_indent <= indent_count:
                        skip_lines = False
                    else:
                        continue
                
                new_lines.append(line)
            
            # Write patched version
            patched_content = '\n'.join(new_lines)
            
            # Replace method name in usage
            patched_content = patched_content.replace(
                'self.download_file(music_url',
                'self.download_file_improved(music_url'
            )
            patched_content = patched_content.replace(
                'self.download_file(thumbnail_url',
                'self.download_file_improved(thumbnail_url'
            )
            
            # Backup original
            backup_path = video_creator_path.with_suffix('.py.backup')
            with open(backup_path, 'w') as f:
                f.write(content)
            
            # Write patched version
            with open(video_creator_path, 'w') as f:
                f.write(patched_content)
            
            print("✅ VideoCreator patched successfully!")
            print(f"📋 Backup saved as: {backup_path}")
            return True
    else:
        print("✅ VideoCreator already patched")
        return True

def main():
    """Main function"""
    print("🔧 Video Creation Fix Tool")
    print("=" * 50)
    
    # Step 1: Test Suno URLs
    test_suno_urls()
    
    # Step 2: Patch VideoCreator
    if patch_video_creator():
        
        # Step 3: Test video creation
        if create_test_video_with_working_url():
            print("\n🎉 Video creation fix successful!")
            print("📋 Your video generation should now work correctly")
        else:
            print("\n⚠️ Video creation still has issues")
            
    else:
        print("\n❌ Could not patch VideoCreator")

if __name__ == "__main__":
    main()