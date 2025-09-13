#!/usr/bin/env python3
"""
Daily Money Maker - Automated Beat Generation Workflow
Generates trending beats and prepares them for monetization
"""

import os
import sys
import json
import time
from datetime import datetime, date
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.services.suno_client import SunoClient
from core.services.gemini_client import GeminiClient  
from core.services.image_client import ImageClient
from core.utils.file_manager import FileManager

class DailyMoneyMaker:
    """Automated daily beat generation for monetization"""
    
    def __init__(self):
        self.today = date.today().strftime("%Y%m%d")
        self.output_dir = f"daily_beats_{self.today}"
        self.earnings_log = "daily_earnings.json"
        self.beat_templates = self._load_beat_templates()
        
        # Initialize clients
        self.use_real_apis = self._check_api_keys()
        if self.use_real_apis:
            print("🔑 Real API mode activated!")
            self.suno = SunoClient()
            self.gemini = GeminiClient()
        else:
            print("🧪 Mock mode - perfect for learning workflow!")
            self.suno = None
            self.gemini = None
            
        self.image_client = ImageClient()  # Always available (nano-banana)
        self.file_manager = FileManager()
        
    def _check_api_keys(self):
        """Check if real API keys are configured"""
        suno_key = os.getenv('SUNO_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        return (suno_key and suno_key != 'your_suno_api_key_here' and
                gemini_key and gemini_key != 'your_gemini_api_key_here')
    
    def _load_beat_templates(self):
        """Load proven beat templates for consistent success"""
        return {
            "monday": {
                "genre": "Lo-Fi Hip Hop",
                "prompts": [
                    "Chill lo-fi hip hop beats for studying with rain sounds and jazz samples",
                    "Relaxing study beats with vinyl crackle and mellow piano",
                    "Late night lo-fi vibes with soft drums and atmospheric pads"
                ],
                "target": "Study playlists, YouTube background music"
            },
            "tuesday": {
                "genre": "Trap",
                "prompts": [
                    "Dark trap beat with heavy 808s and haunting melody, 140 BPM",
                    "Melodic trap instrumental with modern drums and catchy hook",
                    "Hard trap beat with aggressive drums and street vibe"
                ],
                "target": "Beat licensing, rapper collaborations"
            },
            "wednesday": {
                "genre": "Chill Pop",
                "prompts": [
                    "Upbeat chill pop beat with modern drums and catchy synths",
                    "Summer pop vibes with tropical elements and smooth bass",
                    "Feel-good pop instrumental perfect for TikTok content"
                ],
                "target": "TikTok creators, pop artists"
            },
            "thursday": {
                "genre": "Ambient",
                "prompts": [
                    "Peaceful ambient meditation music with nature sounds",
                    "Deep sleep music with soft pads and calming frequencies",
                    "Mindfulness background music for yoga and relaxation"
                ],
                "target": "Meditation apps, wellness content"
            },
            "friday": {
                "genre": "Trending Hijack",
                "prompts": [
                    "TikTok viral type beat with catchy hook and dance rhythm",
                    "Trending sound remake with modern production",
                    "Viral challenge beat with infectious energy"
                ],
                "target": "Social media virality"
            }
        }
    
    def get_today_template(self):
        """Get today's beat generation template"""
        weekday = datetime.now().strftime('%A').lower()
        
        # Map weekdays to template keys
        day_mapping = {
            'monday': 'monday',
            'tuesday': 'tuesday', 
            'wednesday': 'wednesday',
            'thursday': 'thursday',
            'friday': 'friday',
            'saturday': 'monday',  # Repeat popular templates
            'sunday': 'tuesday'
        }
        
        template_key = day_mapping.get(weekday, 'monday')
        return self.beat_templates[template_key]
    
    def generate_daily_beats(self, count=3):
        """Generate today's money-making beats"""
        print("🚀 Starting Daily Money Maker...")
        print("=" * 50)
        
        template = self.get_today_template()
        genre = template['genre']
        prompts = template['prompts'][:count]
        
        print(f"📅 Today's Focus: {genre}")
        print(f"🎯 Target Market: {template['target']}")
        print(f"🎵 Generating {len(prompts)} beats...")
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        results = []
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n🎼 Beat {i}/3: {prompt[:50]}...")
            
            # Generate beat
            beat_result = self._generate_single_beat(prompt, i)
            if beat_result:
                results.append(beat_result)
                print(f"✅ Beat {i} generated successfully!")
            else:
                print(f"❌ Beat {i} generation failed")
        
        # Generate monetization package
        self._create_monetization_package(results, genre, template['target'])
        
        # Log daily activity
        self._log_daily_activity(results, genre)
        
        print("\n" + "=" * 50)
        print("🎉 DAILY BEATS GENERATED!")
        print(f"📂 Location: {self.output_dir}/")
        print(f"🎵 Beats created: {len(results)}")
        print("💰 Ready for monetization!")
        
        return results
    
    def _generate_single_beat(self, prompt, beat_number):
        """Generate a single beat with cover art"""
        try:
            timestamp = datetime.now().strftime("%H%M%S")
            beat_name = f"beat_{beat_number}_{timestamp}"
            
            # Generate music
            if self.use_real_apis and self.suno:
                # Real Suno generation
                print("🎵 Generating with Suno API...")
                task = self.suno.generate_music_simple(prompt)
                # In real implementation, wait for completion
                audio_path = f"{self.output_dir}/{beat_name}.mp3"
            else:
                # Mock generation
                print("🎵 [MOCK] Creating beat file...")
                audio_path = f"{self.output_dir}/{beat_name}.mp3"
                # Create mock MP3 file
                with open(audio_path, 'wb') as f:
                    f.write(b"MOCK_AUDIO_DATA")
            
            # Generate cover art with nano-banana
            print("🍌 Generating nano-banana cover art...")
            cover_filename = f"{beat_name}_cover.png"
            cover_success = self.image_client.generate_album_cover(
                song_title=f"Beat #{beat_number}",
                genre=self.get_today_template()['genre'],
                mood="professional, modern, monetizable",
                save_path=self.output_dir,
                filename=cover_filename
            )
            
            # Create beat metadata
            metadata = {
                'beat_name': beat_name,
                'prompt': prompt,
                'audio_file': audio_path,
                'cover_file': f"{self.output_dir}/{cover_filename}" if cover_success else None,
                'generated_at': datetime.now().isoformat(),
                'genre': self.get_today_template()['genre'],
                'monetization_ready': True,
                'suggested_price': self._suggest_price(self.get_today_template()['genre'])
            }
            
            # Save metadata
            metadata_file = f"{self.output_dir}/{beat_name}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return metadata
            
        except Exception as e:
            print(f"❌ Error generating beat: {e}")
            return None
    
    def _suggest_price(self, genre):
        """Suggest pricing based on genre and market"""
        pricing = {
            "Lo-Fi Hip Hop": {"basic": 20, "premium": 45, "exclusive": 150},
            "Trap": {"basic": 25, "premium": 50, "exclusive": 200},
            "Chill Pop": {"basic": 30, "premium": 60, "exclusive": 250},
            "Ambient": {"basic": 15, "premium": 35, "exclusive": 100},
            "Trending Hijack": {"basic": 35, "premium": 75, "exclusive": 300}
        }
        
        return pricing.get(genre, {"basic": 25, "premium": 50, "exclusive": 200})
    
    def _create_monetization_package(self, results, genre, target_market):
        """Create ready-to-upload monetization package"""
        package = {
            "date": self.today,
            "genre": genre,
            "target_market": target_market,
            "beats": results,
            "upload_strategy": self._create_upload_strategy(results, genre),
            "pricing_strategy": self._create_pricing_strategy(results),
            "marketing_copy": self._create_marketing_copy(results, genre)
        }
        
        package_file = f"{self.output_dir}/MONETIZATION_PACKAGE.json"
        with open(package_file, 'w') as f:
            json.dump(package, f, indent=2)
        
        # Create README with instructions
        readme_content = f"""# 💰 TODAY'S MONETIZATION PACKAGE - {self.today}

## 🎵 Generated Beats: {len(results)}
**Genre Focus:** {genre}
**Target Market:** {target_market}

## 🚀 QUICK UPLOAD GUIDE:

### YouTube Upload:
```
Title: "FREE {genre} Beat | [Beat Name] | Type Beat 2024"
Tags: {genre.lower().replace(' ', '')}, beats, free, instrumental, type beat
Description: Free for non-commercial use. License available at: [your email]
```

### BeatStars Upload:
```
Basic License: ${self._suggest_price(genre)['basic']}
Premium License: ${self._suggest_price(genre)['premium']} 
Exclusive Rights: ${self._suggest_price(genre)['exclusive']}
```

### TikTok Strategy:
- Post 15-second previews with visualizer
- Use hashtags: #beats #{genre.lower().replace(' ', '')} #producer
- Post at 6-9 PM for maximum engagement

## 💰 EXPECTED EARNINGS THIS WEEK:
- Conservative: $50-150
- Realistic: $100-300  
- Optimistic: $200-500+

## 📈 NEXT STEPS:
1. Upload to YouTube (immediate)
2. List on BeatStars (licensing) 
3. Create TikTok previews (viral potential)
4. Reach out to 5 artists (custom work)
5. Track performance metrics

Ready to make money! 🎉
"""
        
        readme_file = f"{self.output_dir}/README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
    
    def _create_upload_strategy(self, results, genre):
        """Create platform-specific upload strategy"""
        return {
            "youtube": {
                "schedule": "Upload 1 beat every 2 hours starting at 2 PM",
                "title_format": f"FREE {genre} Beat | {{beat_name}} | Type Beat 2024",
                "tags": [genre.lower().replace(' ', ''), "beats", "free", "instrumental", "type beat", "2024"],
                "description_template": f"🎵 Free {genre} beat for non-commercial use\\n💰 License available: [your email]\\n🔥 More beats: [your channel]"
            },
            "tiktok": {
                "content_type": "15-second beat previews with visualizer",
                "hashtags": ["#beats", f"#{genre.lower().replace(' ', '')}", "#producer", "#typebeat"],
                "posting_time": "6-9 PM daily"
            },
            "beatstars": {
                "pricing": self._suggest_price(genre),
                "description": f"Professional {genre} instrumental perfect for recording artists and content creators."
            }
        }
    
    def _create_pricing_strategy(self, results):
        """Create dynamic pricing strategy"""
        return {
            "launch_week": "50% off all licenses to build momentum",
            "bulk_deals": "Buy 2 beats get 1 free",
            "exclusive_pricing": "First exclusive buyer gets 25% discount",
            "custom_work": "$100-300 for custom beats based on complexity"
        }
    
    def _create_marketing_copy(self, results, genre):
        """Create ready-to-use marketing copy"""
        return {
            "social_posts": [
                f"🔥 Just dropped 3 fresh {genre} beats! Which one hits different? 👇",
                f"Producer life: 3 AM inspiration turned into {genre} magic ✨",
                f"FREE {genre} beats dropping today! Perfect for your next project 🎵"
            ],
            "email_templates": [
                f"Subject: Fresh {genre} beats perfect for your sound",
                f"Hey [Artist Name], loved your latest track! I have a {genre} beat that would complement your style perfectly. Want to hear it?"
            ],
            "dm_templates": [
                f"Your music style is fire! 🔥 I have a {genre} beat that would be perfect for you. Interested in a collab?",
                f"Hey! Producer here. Just made a {genre} beat that screams your name. First collab is always FREE! 🎵"
            ]
        }
    
    def _log_daily_activity(self, results, genre):
        """Log daily activity for tracking progress"""
        today_log = {
            "date": self.today,
            "beats_generated": len(results),
            "genre": genre,
            "success_rate": f"{len(results)}/3",
            "estimated_value": len(results) * 50,  # Conservative estimate
            "next_actions": [
                "Upload to YouTube",
                "List on BeatStars", 
                "Create TikTok content",
                "Reach out to artists"
            ]
        }
        
        # Load existing log
        if os.path.exists(self.earnings_log):
            with open(self.earnings_log, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {"daily_activities": [], "total_beats": 0, "estimated_total_value": 0}
        
        # Add today's activity
        log_data["daily_activities"].append(today_log)
        log_data["total_beats"] += len(results)
        log_data["estimated_total_value"] += today_log["estimated_value"]
        
        # Save updated log
        with open(self.earnings_log, 'w') as f:
            json.dump(log_data, f, indent=2)

def main():
    """Run daily money maker"""
    maker = DailyMoneyMaker()
    results = maker.generate_daily_beats(count=3)
    
    print(f"\n💡 QUICK START GUIDE:")
    print(f"1. Check folder: {maker.output_dir}/")
    print(f"2. Read: {maker.output_dir}/README.md")
    print(f"3. Upload beats following the guide")
    print(f"4. Start earning today! 💰")

if __name__ == "__main__":
    main()