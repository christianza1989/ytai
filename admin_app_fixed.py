#!/usr/bin/env python3
"""
This is a fixed version of admin_app.py with duplicate routes removed
"""

import os
import shutil
from pathlib import Path

# Read the original file
with open('/home/user/webapp/admin_app.py', 'r') as f:
    content = f.read()

# Split content by lines
lines = content.split('\n')

# Find the problematic section and remove it
output_lines = []
skip_lines = False
skip_start_patterns = [
    "@app.route('/api/youtube/channels/save', methods=['POST'])",
    "def api_youtube_channels_save():",
]
skip_end_patterns = [
    "return jsonify({'success': True, 'task_id': task_id})"
]

i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if we should start skipping (old YouTube endpoints)
    if any(pattern in line for pattern in skip_start_patterns) and 'DatabaseManager' in lines[i+3:i+10]:
        skip_lines = True
        output_lines.append("# OLD YOUTUBE ENDPOINTS REMOVED - DUPLICATE ROUTES")
        output_lines.append("# These were conflicting with the new youtube_channels_db endpoints")
        output_lines.append("")
    
    # If we're not skipping, add the line
    if not skip_lines:
        output_lines.append(line)
    
    # Check if we should stop skipping
    if skip_lines and (
        line.strip().startswith("@app.route") and 
        not any(pattern in line for pattern in skip_start_patterns)
    ):
        skip_lines = False
        output_lines.append(line)  # Add the new route that ends the skip
    
    i += 1

# Write the fixed content
with open('/home/user/webapp/admin_app.py', 'w') as f:
    f.write('\n'.join(output_lines))

print("Fixed duplicate routes in admin_app.py")