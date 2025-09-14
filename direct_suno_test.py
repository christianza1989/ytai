#!/usr/bin/env python3
"""
Direct test of Suno client outside of Flask app
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.services.suno_client import SunoClient

def main():
    print("🧪 Direct Suno Client Test")
    print("=" * 40)
    
    load_dotenv()
    
    try:
        suno = SunoClient()
        print("✅ Suno client initialized")
        
        # Test simple generation with debug output
        print("\n🎵 Testing generate_music_simple...")
        result = suno.generate_music_simple(
            prompt="upbeat electronic house music, energetic",
            instrumental=True,
            model="V4"
        )
        
        print(f"\n📋 Final result: {result}")
        print(f"📋 Result type: {type(result)}")
        
        if result:
            print("✅ Generation successful!")
        else:
            print("❌ Generation returned None")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()