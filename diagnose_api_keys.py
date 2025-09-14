#!/usr/bin/env python3
"""
Diagnostic script to check API key display logic
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("🔍 API Key Display Diagnostic")
print("=" * 40)

# Replicate the exact logic from api_config route
env_config = {}
for key in ['SUNO_API_KEY', 'GEMINI_API_KEY', 'GEMINI_MODEL']:
    value = os.getenv(key, '')
    print(f"\n🔑 {key}:")
    print(f"   Raw value: '{value}'")
    print(f"   Length: {len(value)}")
    print(f"   Is not empty: {bool(value)}")
    print(f"   Not placeholder: {value != f'your_{key.lower()}_here'}")
    
    if value and value != f'your_{key.lower()}_here':
        # For display purposes, mask the key but store full value in data attribute
        if key in ['SUNO_API_KEY', 'GEMINI_API_KEY'] and len(value) > 12:
            masked_value = value[:8] + '...' + value[-4:]
            env_config[key] = masked_value
            print(f"   Masked value: '{masked_value}'")
        else:
            env_config[key] = value  # GEMINI_MODEL and short keys shown fully
            print(f"   Full value (short): '{value}'")
    else:
        env_config[key] = 'not_configured'
        print(f"   Status: not_configured")

print(f"\n📋 Final env_config passed to template:")
for key, value in env_config.items():
    print(f"   {key}: '{value}'")

# Test the condition logic specifically
print(f"\n🧪 Testing condition logic:")
suno_key = os.getenv('SUNO_API_KEY', '')
print(f"SUNO_API_KEY = '{suno_key}'")
print(f"bool(suno_key) = {bool(suno_key)}")
print(f"suno_key != 'your_suno_api_key_here' = {suno_key != 'your_suno_api_key_here'}")
print(f"Combined condition = {suno_key and suno_key != 'your_suno_api_key_here'}")
print(f"Length > 12 = {len(suno_key) > 12}")

gemini_key = os.getenv('GEMINI_API_KEY', '')
print(f"\nGEMINI_API_KEY = '{gemini_key}'")
print(f"bool(gemini_key) = {bool(gemini_key)}")
print(f"gemini_key != 'your_gemini_api_key_here' = {gemini_key != 'your_gemini_api_key_here'}")
print(f"Combined condition = {gemini_key and gemini_key != 'your_gemini_api_key_here'}")
print(f"Length > 12 = {len(gemini_key) > 12}")