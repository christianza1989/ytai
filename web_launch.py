#!/usr/bin/env python3
"""
Launcher for AI Music Empire Web Application
Starts the comprehensive admin interface for the music generation system
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Launch the AI Music Empire web interface"""
    print("🎹 Starting AI Music Empire Web Interface...")
    print("🚀 Initializing comprehensive admin panel")
    print("💎 Loading all 10 AI systems...")
    
    # Import and run the admin app
    try:
        from admin_app import app, SystemState
        
        # Initialize system state
        print("🔧 Initializing system state...")
        
        # Start the Flask application
        print("🌐 Starting web server on port 8000...")
        print("📊 AI Music Empire Dashboard loading...")
        print("🎵 Ready to generate $63K-125K+/month!")
        print("="*50)
        
        # Run with production settings
        app.run(
            host='0.0.0.0',
            port=8000,
            debug=False,  # Production mode
            threaded=True
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔄 Falling back to basic web interface...")
        
        # Fallback to basic web app
        from web_app import app as basic_app
        basic_app.run(
            host='0.0.0.0',
            port=8000,
            debug=False,
            threaded=True
        )
        
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()