#!/usr/bin/env python3
"""
Fix for Suno credits issue and provide user guidance
"""

import os
from dotenv import load_dotenv

def check_suno_credits():
    """Check current Suno credit balance"""
    print("🔍 Checking Suno AI Credits")
    print("=" * 40)
    
    load_dotenv()
    
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from core.services.suno_client import SunoClient
        
        suno = SunoClient()
        credits = suno.get_credits()
        
        print(f"💳 Current Suno Credits: {credits}")
        
        if credits <= 0:
            print("\n❌ ISSUE IDENTIFIED:")
            print("Your Suno AI account has insufficient credits for music generation.")
            print("\n🛠️ SOLUTION:")
            print("1. Visit: https://api.sunoapi.org/")
            print("2. Login to your account")
            print("3. Add credits to your balance")
            print("4. Minimum recommended: 50 credits")
            print("5. Each song generation typically costs 5-10 credits")
            
            print("\n💡 COST ESTIMATION:")
            print("- Simple song: ~5 credits")
            print("- Advanced song: ~8-10 credits")
            print("- 50 credits = ~5-10 songs")
            print("- 100 credits = ~10-20 songs")
            
            return False
            
        elif credits < 10:
            print("\n⚠️ WARNING:")
            print(f"Low credit balance ({credits} credits remaining)")
            print("Consider adding more credits soon.")
            print("Visit: https://api.sunoapi.org/")
            return True
            
        else:
            print("\n✅ CREDITS OK:")
            print(f"Sufficient credits available ({credits})")
            estimated_songs = credits // 5
            print(f"Estimated songs you can generate: ~{estimated_songs}")
            return True
            
    except Exception as e:
        print(f"❌ Error checking credits: {e}")
        return False

def update_env_with_demo_mode():
    """Add demo mode option to .env file"""
    print("\n🛠️ Adding Demo Mode Configuration")
    print("=" * 40)
    
    env_path = ".env"
    
    # Read current .env content
    env_lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            env_lines = f.readlines()
    
    # Check if DEMO_MODE already exists
    has_demo_mode = any('DEMO_MODE' in line for line in env_lines)
    
    if not has_demo_mode:
        # Add demo mode configuration
        env_lines.append('\n# Demo Mode Configuration\n')
        env_lines.append('DEMO_MODE=false\n')
        env_lines.append('# Set DEMO_MODE=true to enable demo generation without Suno credits\n')
        
        with open(env_path, 'w') as f:
            f.writelines(env_lines)
        
        print("✅ Added DEMO_MODE configuration to .env file")
        print("💡 You can set DEMO_MODE=true to test without using Suno credits")
    else:
        print("✅ DEMO_MODE already configured in .env file")

if __name__ == "__main__":
    print("🚀 Suno AI Credits Fix & Configuration")
    print("=" * 60)
    
    has_credits = check_suno_credits()
    update_env_with_demo_mode()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY:")
    
    if has_credits:
        print("✅ Your Suno AI setup is ready for music generation!")
        print("🎵 You can now use the music generator successfully.")
    else:
        print("❌ ACTION REQUIRED: Add credits to your Suno AI account")
        print("🔗 Visit: https://api.sunoapi.org/")
        print("💡 Alternative: Enable DEMO_MODE=true in .env for testing")
    
    print("\n🌐 Access your application at:")
    print("https://5000-i76do3fgbtdxky0vs2439-6532622b.e2b.dev/")
    print("\n🏁 Configuration complete!")