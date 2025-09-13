import os
import re
import requests
from typing import Optional
from pathlib import Path

class FileManager:
    """Utility class for managing files and directories"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def create_song_directory(self, title: str) -> str:
        """Create a safe directory name from song title and create the directory"""
        # Create safe directory name
        safe_name = re.sub(r'[^\w\s-]', '', title)  # Remove special characters
        safe_name = re.sub(r'[-\s]+', '_', safe_name)  # Replace spaces and dashes with underscores
        safe_name = safe_name.strip('_')  # Remove leading/trailing underscores

        # Add timestamp to ensure uniqueness
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = f"{safe_name}_{timestamp}"

        # Create full path
        song_dir = self.output_dir / dir_name
        song_dir.mkdir(parents=True, exist_ok=True)

        print(f"📁 Sukurtas aplankas: {song_dir}")
        return str(song_dir)

    def download_file(self, url: str, save_path: str, filename: str) -> bool:
        """Download file from URL and save to specified location"""
        try:
            print(f"⬇️ Atsisiunčiamas failas: {filename}")

            # Ensure save_path exists
            Path(save_path).mkdir(parents=True, exist_ok=True)

            # Full file path
            file_path = Path(save_path) / filename

            # Download file
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            # Save file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            file_size = file_path.stat().st_size
            print(f"✅ Failas išsaugotas: {file_path} ({file_size} bytes)")

            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Nepavyko atsisiųsti failo {filename}: {e}")
            return False
        except Exception as e:
            print(f"❌ Klaida išsaugant failą {filename}: {e}")
            return False

    def save_text_file(self, content: str, save_path: str, filename: str) -> bool:
        """Save text content to a file"""
        try:
            # Ensure save_path exists
            Path(save_path).mkdir(parents=True, exist_ok=True)

            # Full file path
            file_path = Path(save_path) / filename

            # Save text content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Tekstinis failas išsaugotas: {file_path}")
            return True

        except Exception as e:
            print(f"❌ Klaida išsaugant tekstinį failą {filename}: {e}")
            return False

    def list_directory_contents(self, directory: str) -> list:
        """List all files in a directory"""
        try:
            path = Path(directory)
            if not path.exists():
                return []

            return [str(f) for f in path.iterdir() if f.is_file()]

        except Exception as e:
            print(f"❌ Klaida skaitant aplanką {directory}: {e}")
            return []

    def get_file_info(self, file_path: str) -> Optional[dict]:
        """Get information about a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return None

            stat = path.stat()
            return {
                'name': path.name,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'path': str(path)
            }

        except Exception as e:
            print(f"❌ Klaida gaunant failo informaciją {file_path}: {e}")
            return None
