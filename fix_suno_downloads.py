#!/usr/bin/env python3
"""
Fix Suno URL downloads by testing different URL formats
"""

import os
import sys
import json
import requests
from pathlib import Path

def test_suno_url_formats():
    """Test different Suno URL formats to find working ones"""
    
    print("🧪 Testing Suno URL formats...")
    
    # Get a recent track from generation tasks
    tasks_file = Path("/home/user/webapp/data/generation_tasks.json")
    if not tasks_file.exists():
        print("❌ No generation tasks file found")
        return
    
    with open(tasks_file, 'r') as f:
        tasks_data = json.load(f)
    
    # Find the most recent completed track
    recent_track = None
    for task_id, task in reversed(list(tasks_data.items())):
        if (task.get('status') == 'completed' and 
            'suno_metadata' in task.get('result', {})):
            recent_track = task['result']['suno_metadata']
            print(f"📋 Testing with track: {recent_track.get('title', 'Unknown')}")
            break
    
    if not recent_track:
        print("❌ No recent tracks found")
        return
    
    # Extract all possible audio URLs
    url_candidates = []
    
    for key in ['audioUrl', 'sourceAudioUrl', 'streamAudioUrl', 'sourceStreamAudioUrl']:
        url = recent_track.get(key)
        if url and url.strip():
            url_candidates.append((key, url))
    
    print(f"🔍 Found {len(url_candidates)} URL candidates")
    
    # Test each URL
    working_urls = []
    
    for url_type, url in url_candidates:
        print(f"\n🔄 Testing {url_type}:")
        print(f"   URL: {url}")
        
        try:
            # Test with different approaches
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'audio/*,*/*;q=0.9',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'identity',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Add Referer for Suno URLs
            if 'suno' in url.lower():
                headers['Referer'] = 'https://suno.com/'
                headers['Origin'] = 'https://suno.com'
            
            # Try GET request
            response = requests.get(url, headers=headers, stream=True, timeout=15)
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"   Content-Length: {response.headers.get('content-length', 'N/A')}")
            
            if response.status_code == 200:
                # Check if it's actually audio
                content_type = response.headers.get('content-type', '').lower()
                content_length = response.headers.get('content-length')
                
                if content_length:
                    size_mb = int(content_length) / 1024 / 1024
                    print(f"   Size: {size_mb:.1f} MB")
                    
                    if size_mb > 0.1:  # At least 100KB
                        working_urls.append((url_type, url, size_mb))
                        print(f"   ✅ WORKING - Good size and accessible")
                    else:
                        print(f"   ❌ Too small - likely not audio")
                else:
                    # Try to read first chunk
                    try:
                        chunk = next(response.iter_content(8192), None)
                        if chunk and len(chunk) > 1000:
                            working_urls.append((url_type, url, len(chunk) / 1024))
                            print(f"   ✅ WORKING - Stream available ({len(chunk)} bytes)")
                        else:
                            print(f"   ❌ Empty or very small response")
                    except:
                        print(f"   ❌ Cannot read stream")
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.reason}")
                
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection error")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Summary
    print(f"\n📊 Results: {len(working_urls)} working URLs found")
    
    if working_urls:
        print("\n✅ Working URLs:")
        for url_type, url, size in working_urls:
            print(f"   - {url_type}: {size:.1f} MB")
            
        # Test download of the best URL
        best_url = working_urls[0]
        print(f"\n🔄 Testing full download of: {best_url[0]}")
        
        test_download_path = Path("/tmp/test_suno_download.mp3")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://suno.com/'
            }
            
            response = requests.get(best_url[1], headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(test_download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            downloaded_size = test_download_path.stat().st_size / 1024 / 1024
            print(f"✅ Full download successful: {downloaded_size:.1f} MB")
            
            # Test audio with FFprobe
            import subprocess
            try:
                result = subprocess.run([
                    'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                    '-show_format', str(test_download_path)
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    audio_info = json.loads(result.stdout)
                    duration = float(audio_info.get('format', {}).get('duration', 0))
                    print(f"✅ Audio validation: {duration:.1f} seconds")
                    
                    # Cleanup
                    test_download_path.unlink()
                    
                    return best_url[1]  # Return working URL
                else:
                    print(f"❌ Audio validation failed")
            except Exception as e:
                print(f"⚠️ Could not validate audio: {e}")
                
            # Cleanup even if validation fails
            if test_download_path.exists():
                test_download_path.unlink()
            
            return best_url[1]  # Return URL even if validation fails
            
        except Exception as e:
            print(f"❌ Full download failed: {e}")
            if test_download_path.exists():
                test_download_path.unlink()
    else:
        print("\n❌ No working URLs found")
        print("📋 Possible solutions:")
        print("   1. Suno might have changed their API")
        print("   2. Authentication might be required")
        print("   3. URLs might have expired")
    
    return None

def patch_video_creator_simple():
    """Apply simple patch to VideoCreator for better error handling"""
    
    print("\n🔧 Applying simple patch to VideoCreator...")
    
    video_creator_path = Path("/home/user/webapp/core/utils/video_creator.py")
    
    with open(video_creator_path, 'r') as f:
        content = f.read()
    
    # Add better error reporting to download_file method
    if '# Enhanced error reporting' not in content:
        # Find the download_file method and add better logging
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # After the download_file method definition, add better error handling
            if 'def download_file(self, url: str, output_path: str, file_type: str = "audio")' in line:
                # Add enhanced logging after method signature
                indent = ' ' * 8
                new_lines.extend([
                    f'{indent}"""Enhanced download with better error reporting"""',
                    f'{indent}# Enhanced error reporting',
                ])
            
            # Add better error handling in the download section
            elif 'response = requests.get(url, headers=headers, stream=True, timeout=30)' in line:
                new_lines.extend([
                    f'                print(f"🔄 Headers: {{headers}}")',
                    f'                print(f"🔄 Timeout: 30s")',
                ])
            
            # Add response validation
            elif 'response.raise_for_status()' in line:
                new_lines.extend([
                    f'                print(f"📡 Response status: {{response.status_code}}")',
                    f'                print(f"📡 Response headers: {{dict(list(response.headers.items())[:5])}}")',
                    f'                ',
                    f'                # Validate response',
                    f'                if response.status_code != 200:',
                    f'                    print(f"❌ HTTP {{response.status_code}}: {{response.reason}}")',
                    f'                    return False',
                ])
        
        # Write enhanced version
        enhanced_content = '\n'.join(new_lines)
        
        # Backup and save
        backup_path = video_creator_path.with_suffix('.py.backup')
        if not backup_path.exists():
            with open(backup_path, 'w') as f:
                f.write(content)
        
        with open(video_creator_path, 'w') as f:
            f.write(enhanced_content)
        
        print("✅ VideoCreator enhanced with better error reporting")
    else:
        print("✅ VideoCreator already enhanced")

def main():
    """Main function"""
    
    print("🔧 Suno Download Fix Tool")
    print("=" * 50)
    
    # Test Suno URL formats
    working_url = test_suno_url_formats()
    
    # Apply patches
    patch_video_creator_simple()
    
    if working_url:
        print(f"\n🎉 Found working Suno URL format!")
        print(f"🔗 URL: {working_url[:80]}...")
        print("\n📋 Video creation should now work with Suno audio!")
    else:
        print(f"\n⚠️ No working Suno URLs found")
        print("📋 Video creation may still fail with Suno audio")
        print("💡 Consider using local audio files or alternative sources")

if __name__ == "__main__":
    main()