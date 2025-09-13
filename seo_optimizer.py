#!/usr/bin/env python3
"""
YouTube SEO Optimizer & Trending Analysis
Advanced system for maximizing video discoverability and monetization
"""

import json
import random
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import re

class YouTubeTrendingAnalyzer:
    """Analizuoja YouTube trends ir optimizuoja content strategiją"""
    
    def __init__(self):
        self.trending_keywords = {}
        self.seasonal_trends = {}
        self.competitor_data = {}
        
        # Load trending data (in production would fetch from APIs)
        self.load_trending_data()
    
    def load_trending_data(self):
        """Įkelia trending data iš šaltinių"""
        
        # Current trending keywords by category
        self.trending_keywords = {
            'lofi': {
                'hot': ['aesthetic', 'cozy vibes', 'rain sounds', 'coffee shop', 'productivity'],
                'rising': ['dark academia', 'cottage core', 'study with me', 'pomodoro'],
                'seasonal': ['autumn vibes', 'winter study', 'spring cleaning', 'summer nights'],
                'evergreen': ['focus music', 'background music', 'chill beats', 'study music']
            },
            'trap': {
                'hot': ['type beat', 'hard beat', 'drill beat', 'dark trap', 'street music'],
                'rising': ['UK drill', 'melodic trap', 'guitar trap', 'rage beats'],
                'seasonal': ['summer bangers', 'winter vibes', 'holiday trap', 'new year energy'],
                'evergreen': ['rap instrumental', 'hip hop beat', 'producer beat', 'free beat']
            },
            'meditation': {
                'hot': ['432Hz', '528Hz', 'sound healing', 'chakra music', 'binaural beats'],
                'rising': ['quantum healing', 'DNA repair', 'abundance frequency', 'manifestation'],
                'seasonal': ['new moon', 'full moon', 'equinox energy', 'solstice healing'],
                'evergreen': ['meditation music', 'healing frequency', 'deep relaxation', 'spiritual music']
            },
            'gaming': {
                'hot': ['epic music', 'boss battle', 'victory theme', 'intense gaming', 'focus music'],
                'rising': ['anime gaming', 'retro gaming', 'cyberpunk music', 'fantasy RPG'],
                'seasonal': ['tournament season', 'holiday gaming', 'summer gaming', 'back to school'],
                'evergreen': ['background music', 'gaming playlist', 'action music', 'adventure music']
            }
        }
        
        # RPM (Revenue Per Mille) data by category
        self.rpm_data = {
            'lofi': {'min': 1.5, 'avg': 2.8, 'max': 4.2},
            'trap': {'min': 0.8, 'avg': 1.9, 'max': 3.5},
            'meditation': {'min': 2.2, 'avg': 3.5, 'max': 5.8},
            'gaming': {'min': 1.2, 'avg': 2.3, 'max': 4.1}
        }
        
        # Optimal upload times by audience
        self.upload_schedule = {
            'lofi': {
                'weekday': ['14:00', '18:00', '20:00'],  # After school/work
                'weekend': ['10:00', '15:00', '19:00']   # Relaxed schedule
            },
            'trap': {
                'weekday': ['16:00', '19:00', '21:00'],  # Young audience
                'weekend': ['13:00', '17:00', '20:00']
            },
            'meditation': {
                'weekday': ['06:00', '12:00', '21:00'],  # Morning/lunch/evening
                'weekend': ['07:00', '14:00', '20:00']
            },
            'gaming': {
                'weekday': ['15:00', '18:00', '20:00', '22:00'],  # Gaming prime time
                'weekend': ['12:00', '16:00', '19:00', '23:00']
            }
        }

    def generate_optimized_title(self, style: str, mood: str = None, trending_boost: bool = True) -> str:
        """Generuoja SEO optimizuotą pavadinimą"""
        
        base_templates = {
            'lofi': [
                "Lo-Fi Hip Hop Beats - {mood} Music for Study & Work [{duration}]",
                "Chill {mood} Lo-Fi - Perfect Study Playlist 2024",
                "{mood} Lo-Fi Beats - Relaxing Background Music [{duration} Hours]",
                "Study Music - {mood} Lo-Fi Hip Hop Beats to Focus/Relax",
                "{mood} Aesthetic Lo-Fi - Cozy Study Vibes [{duration}]"
            ],
            'trap': [
                "FREE Trap Beat - \"{beat_name}\" | Hard {mood} Type Beat 2024",
                "{mood} Trap Beat - Hard Rap Instrumental (Prod. AI)",
                "FREE Type Beat - \"{beat_name}\" | {mood} Trap Instrumental",
                "{mood} Drill Beat - Hard UK Type Beat | Rap Instrumental",
                "Trap Beat - \"{beat_name}\" | {mood} Hip Hop Instrumental"
            ],
            'meditation': [
                "{frequency}Hz - {mood} Meditation Music | Healing Frequency Sounds",
                "Deep {mood} Meditation - {frequency}Hz Healing Music [{duration} Min]",
                "{frequency}Hz {mood} Frequency - Powerful Healing Meditation Music",
                "{mood} Chakra Healing Music - {frequency}Hz Meditation Sounds",
                "Healing {mood} Music - {frequency}Hz Frequency for Deep Meditation"
            ],
            'gaming': [
                "EPIC Gaming Music - {mood} Soundtrack for {game_type} Games",
                "{mood} Gaming Music - Perfect for Streaming & Focus [{duration}]",
                "Epic {mood} Music - Intense Gaming Soundtrack 2024",
                "{mood} Boss Battle Music - Epic Gaming Background Music",
                "Gaming Playlist - {mood} Music for Victory & Focus"
            ]
        }
        
        template = random.choice(base_templates.get(style, base_templates['lofi']))
        
        # Fill in variables
        replacements = {
            'mood': (mood or random.choice(['Chill', 'Dark', 'Epic', 'Peaceful'])).title(),
            'duration': random.choice(['1 Hour', '2 Hours', '3 Hours', '30 Min', '45 Min']),
            'frequency': random.choice(['432Hz', '528Hz', '639Hz', '741Hz', '963Hz']),
            'beat_name': self.generate_beat_name(style),
            'game_type': random.choice(['RPG', 'FPS', 'MOBA', 'Battle Royale', 'Racing'])
        }
        
        title = template.format(**replacements)
        
        # Add trending keywords if enabled
        if trending_boost:
            trending = random.choice(self.trending_keywords.get(style, {}).get('hot', []))
            if len(title) + len(trending) + 3 < 100:  # YouTube title limit
                title = f"{title} | {trending.title()}"
        
        return title[:100]  # Ensure within YouTube limits

    def generate_beat_name(self, style: str) -> str:
        """Generuoja beat pavadinimą"""
        
        prefixes = {
            'trap': ['Dark', 'Hard', 'Heavy', 'Savage', 'Street', 'Raw'],
            'lofi': ['Midnight', 'Cozy', 'Dreamy', 'Soft', 'Warm', 'Gentle'],
            'meditation': ['Sacred', 'Divine', 'Pure', 'Crystal', 'Golden', 'Cosmic'],
            'gaming': ['Epic', 'Legendary', 'Heroic', 'Mighty', 'Power', 'Victory']
        }
        
        suffixes = {
            'trap': ['Vibes', 'Energy', 'Power', 'Force', 'Mood', 'Flow'],
            'lofi': ['Dreams', 'Nights', 'Cafe', 'Study', 'Vibes', 'Rain'],
            'meditation': ['Light', 'Peace', 'Harmony', 'Flow', 'Energy', 'Bliss'],
            'gaming': ['Quest', 'Battle', 'Arena', 'Victory', 'Legend', 'Hero']
        }
        
        prefix = random.choice(prefixes.get(style, prefixes['lofi']))
        suffix = random.choice(suffixes.get(style, suffixes['lofi']))
        
        return f"{prefix} {suffix}"

    def generate_seo_description(self, style: str, title: str, mood: str = None) -> str:
        """Generuoja SEO optimizuotą aprašymą"""
        
        base_descriptions = {
            'lofi': [
                "Immerse yourself in these relaxing lo-fi beats perfect for studying, working, or unwinding. {mood_desc} 📚✨\n\n🎧 Perfect for: Study sessions, work focus, reading, relaxation\n🎵 Genre: Lo-Fi Hip Hop, Chill Beats\n⏰ Best time: Anytime you need to focus",
                "Chill lo-fi hip hop beats to help you focus and relax. These {mood_desc} are perfect background music for productivity and peace of mind. 🌙\n\n💤 Great for: Study, work, sleep, meditation\n🎼 Style: Aesthetic lo-fi, chill vibes\n📖 Use: Background music, study playlist"
            ],
            'trap': [
                "🔥 Hard trap beat perfect for rap vocals and freestyle sessions! This {mood_desc} instrumental is available for non-commercial use.\n\n📝 License: Free for non-commercial use\n💰 Buy lease: [Contact for pricing]\n🎤 BPM: 140-150 | Key: {key}",
                "Heavy trap instrumental with {mood_desc}! Perfect for rappers, producers, and hip hop artists. 💯\n\n🎵 Type: Trap/Hip Hop Beat\n🔊 Quality: High-quality WAV/MP3\n📧 Beats: Contact for exclusive rights"
            ],
            'meditation': [
                "Experience deep healing and inner peace with these powerful {frequency} frequencies. Perfect for meditation, chakra healing, and spiritual growth. 🧘‍♀️✨\n\n🎵 Frequency: {frequency}\n💫 Benefits: Deep relaxation, stress relief, spiritual healing\n🧘 Use: Meditation, yoga, healing sessions",
                "Immerse yourself in these sacred {frequency} healing vibrations. {mood_desc} designed to promote inner peace, balance, and spiritual awakening. 🌟\n\n⭐ Benefits: Chakra alignment, emotional healing, stress relief\n🔮 Frequency: {frequency} Hz\n🙏 Perfect for: Meditation, prayer, healing"
            ],
            'gaming': [
                "Epic gaming music to enhance your gameplay experience! This {mood_desc} soundtrack is perfect for streaming, competitive gaming, and focus sessions. 🎮⚡\n\n🎯 Perfect for: Gaming, streaming, focus work\n🏆 Genre: Epic/Cinematic music\n🔥 Energy: High intensity, motivational",
                "Intense gaming soundtrack to keep you focused and motivated! {mood_desc} designed for victory and peak performance. 💪🏆\n\n🎮 Use: Gaming background music, streams, workouts\n⚡ Mood: Epic, intense, motivational\n🏅 Perfect for: Competitive gaming, focus sessions"
            ]
        }
        
        template = random.choice(base_descriptions.get(style, base_descriptions['lofi']))
        
        # Mood descriptions
        mood_descriptions = {
            'chill': 'calming and peaceful vibes',
            'dark': 'mysterious and intense atmosphere',
            'epic': 'powerful and energetic sounds',
            'peaceful': 'tranquil and harmonious melodies'
        }
        
        mood_desc = mood_descriptions.get(mood, 'beautiful and inspiring sounds')
        
        # Fill variables
        description = template.format(
            mood_desc=mood_desc,
            frequency=random.choice(['432Hz', '528Hz', '639Hz', '741Hz']),
            key=random.choice(['C Major', 'D Minor', 'G Major', 'A Minor', 'F Major'])
        )
        
        # Add call-to-action
        cta_options = [
            "\n\n🔔 SUBSCRIBE for daily uploads!",
            "\n\n👍 LIKE if this helped you!",
            "\n\n💬 COMMENT your favorite moment!",
            "\n\n🔄 SHARE with friends who need this!"
        ]
        description += random.choice(cta_options)
        
        # Add hashtags
        hashtags = self.generate_hashtags(style, mood)
        description += f"\n\n{' '.join(hashtags)}"
        
        return description[:5000]  # YouTube description limit

    def generate_hashtags(self, style: str, mood: str = None) -> List[str]:
        """Generuoja trending hashtag'us"""
        
        base_hashtags = {
            'lofi': ['#lofi', '#studymusic', '#chillbeats', '#relaxingmusic', '#backgroundmusic'],
            'trap': ['#trapbeat', '#typebeat', '#rapinstrumental', '#hiphopbeat', '#freebeat'],
            'meditation': ['#meditationmusic', '#healingfrequency', '#spiritualmusic', '#chakramusic'],
            'gaming': ['#gamingmusic', '#epicmusic', '#backgroundmusic', '#focusmusic', '#gamemusic']
        }
        
        hashtags = base_hashtags.get(style, base_hashtags['lofi']).copy()
        
        # Add trending hashtags
        trending = self.trending_keywords.get(style, {})
        for category in ['hot', 'rising']:
            if category in trending:
                trend_tag = random.choice(trending[category])
                hashtags.append(f"#{trend_tag.replace(' ', '').lower()}")
        
        # Add year and general trending
        hashtags.extend(['#2024', '#viral', '#trending'])
        
        # Mood-specific hashtag
        if mood:
            hashtags.append(f"#{mood.lower()}music")
        
        return hashtags[:15]  # Reasonable limit

    def calculate_engagement_potential(self, style: str, title: str, description: str) -> Dict:
        """Apskaičiuoja engagement potencialą"""
        
        score = 0
        factors = {}
        
        # Title analysis
        title_lower = title.lower()
        
        # Check for trending keywords
        trending_matches = 0
        for keyword in self.trending_keywords.get(style, {}).get('hot', []):
            if keyword.lower() in title_lower:
                trending_matches += 1
        
        factors['trending_keywords'] = trending_matches * 10
        score += factors['trending_keywords']
        
        # Check for emotional words
        emotional_words = ['epic', 'amazing', 'incredible', 'powerful', 'beautiful', 'perfect', 'best']
        emotional_matches = sum(1 for word in emotional_words if word in title_lower)
        factors['emotional_impact'] = emotional_matches * 5
        score += factors['emotional_impact']
        
        # Check for numbers/time indicators
        if any(time_word in title_lower for time_word in ['hour', 'min', 'hours', '2024', 'new']):
            factors['time_relevance'] = 10
            score += 10
        
        # Description analysis
        desc_lower = description.lower()
        
        # Check for call-to-action
        cta_words = ['subscribe', 'like', 'comment', 'share', 'follow']
        cta_matches = sum(1 for word in cta_words if word in desc_lower)
        factors['call_to_action'] = min(cta_matches * 5, 15)
        score += factors['call_to_action']
        
        # Check for emojis (simple check)
        emoji_count = len(re.findall(r'[🎵🎧📚✨🌙💯🔥⚡🧘‍♀️💫🎮🏆]', description))
        factors['visual_appeal'] = min(emoji_count * 2, 10)
        score += factors['visual_appeal']
        
        # Style-specific bonuses
        style_bonuses = {
            'lofi': 15 if 'study' in title_lower or 'chill' in title_lower else 0,
            'trap': 15 if 'free' in title_lower or 'beat' in title_lower else 0,
            'meditation': 15 if any(freq in title_lower for freq in ['432hz', '528hz', '741hz']) else 0,
            'gaming': 15 if 'epic' in title_lower or 'gaming' in title_lower else 0
        }
        
        factors['style_optimization'] = style_bonuses.get(style, 0)
        score += factors['style_optimization']
        
        # Calculate final percentage
        max_possible_score = 100
        engagement_percentage = min((score / max_possible_score) * 100, 100)
        
        return {
            'engagement_score': round(engagement_percentage, 1),
            'factors': factors,
            'recommendations': self.generate_recommendations(factors, style)
        }

    def generate_recommendations(self, factors: Dict, style: str) -> List[str]:
        """Generuoja rekomendacijas optimizacijai"""
        
        recommendations = []
        
        if factors.get('trending_keywords', 0) < 10:
            recommendations.append(f"Add more trending {style} keywords to title")
        
        if factors.get('emotional_impact', 0) < 5:
            recommendations.append("Include more emotional words (epic, amazing, powerful)")
        
        if factors.get('time_relevance', 0) == 0:
            recommendations.append("Add time indicators (2024, hours, new)")
        
        if factors.get('call_to_action', 0) < 10:
            recommendations.append("Include stronger call-to-action in description")
        
        if factors.get('visual_appeal', 0) < 5:
            recommendations.append("Add more relevant emojis to description")
        
        if factors.get('style_optimization', 0) < 15:
            style_tips = {
                'lofi': "Emphasize 'study' and 'chill' aspects",
                'trap': "Highlight 'free' and 'beat' in title",
                'meditation': "Include specific frequencies (432Hz, 528Hz)",
                'gaming': "Emphasize 'epic' and 'gaming' keywords"
            }
            recommendations.append(style_tips.get(style, "Optimize for style-specific keywords"))
        
        return recommendations

    def get_optimal_upload_time(self, style: str, timezone: str = 'UTC') -> str:
        """Grąžina optimalų įkėlimo laiką"""
        
        # Check if it's weekend
        today = datetime.now()
        is_weekend = today.weekday() >= 5
        
        schedule_key = 'weekend' if is_weekend else 'weekday'
        times = self.upload_schedule.get(style, {}).get(schedule_key, ['18:00'])
        
        return random.choice(times)

    def estimate_revenue_potential(self, style: str, estimated_views: int, engagement_score: float) -> Dict:
        """Apskaičiuoja revenue potencialą"""
        
        rpm_info = self.rpm_data.get(style, {'min': 1.0, 'avg': 2.0, 'max': 4.0})
        
        # Adjust RPM based on engagement score
        engagement_multiplier = 0.5 + (engagement_score / 100) * 0.5  # 0.5 to 1.0
        
        estimated_rpm = rpm_info['avg'] * engagement_multiplier
        estimated_revenue = (estimated_views / 1000) * estimated_rpm
        
        # Revenue ranges
        min_revenue = (estimated_views / 1000) * rpm_info['min'] * 0.8
        max_revenue = (estimated_views / 1000) * rpm_info['max'] * 1.2
        
        return {
            'estimated_revenue': round(estimated_revenue, 2),
            'revenue_range': {
                'min': round(min_revenue, 2),
                'max': round(max_revenue, 2)
            },
            'estimated_rpm': round(estimated_rpm, 2),
            'engagement_factor': round(engagement_multiplier, 2)
        }


class SEOOptimizer:
    """SEO optimizacijos sistema YouTube video"""
    
    def __init__(self):
        self.trending_analyzer = YouTubeTrendingAnalyzer()
    
    def optimize_video_metadata(self, style: str, mood: str = None, custom_title: str = None) -> Dict:
        """Optimizuoja pilną video metadata"""
        
        # Generate or use custom title
        title = custom_title or self.trending_analyzer.generate_optimized_title(style, mood)
        
        # Generate optimized description
        description = self.trending_analyzer.generate_seo_description(style, title, mood)
        
        # Generate hashtags
        hashtags = self.trending_analyzer.generate_hashtags(style, mood)
        
        # Analyze engagement potential
        engagement_analysis = self.trending_analyzer.calculate_engagement_potential(style, title, description)
        
        # Get optimal upload time
        upload_time = self.trending_analyzer.get_optimal_upload_time(style)
        
        # Estimate views (simplified)
        estimated_views = self.estimate_views_potential(style, engagement_analysis['engagement_score'])
        
        # Calculate revenue potential
        revenue_potential = self.trending_analyzer.estimate_revenue_potential(
            style, estimated_views, engagement_analysis['engagement_score']
        )
        
        return {
            'title': title,
            'description': description,
            'hashtags': hashtags,
            'optimal_upload_time': upload_time,
            'engagement_analysis': engagement_analysis,
            'estimated_views': estimated_views,
            'revenue_potential': revenue_potential,
            'seo_score': self.calculate_seo_score(engagement_analysis, hashtags, title),
            'optimization_timestamp': datetime.now().isoformat()
        }
    
    def estimate_views_potential(self, style: str, engagement_score: float) -> int:
        """Apskaičiuoja views potencialą"""
        
        # Base views by style popularity
        base_views = {
            'lofi': (8000, 80000),
            'trap': (5000, 50000),
            'meditation': (3000, 30000),
            'gaming': (15000, 150000)
        }
        
        min_views, max_views = base_views.get(style, (2000, 20000))
        
        # Adjust based on engagement score
        engagement_multiplier = 0.3 + (engagement_score / 100) * 0.7  # 0.3 to 1.0
        
        estimated_min = int(min_views * engagement_multiplier)
        estimated_max = int(max_views * engagement_multiplier)
        
        return random.randint(estimated_min, estimated_max)
    
    def calculate_seo_score(self, engagement_analysis: Dict, hashtags: List[str], title: str) -> int:
        """Apskaičiuoja bendrą SEO score"""
        
        engagement_score = engagement_analysis.get('engagement_score', 0)
        hashtag_score = min(len(hashtags) * 5, 30)  # Max 30 points for hashtags
        title_length_score = 20 if 30 <= len(title) <= 80 else 10  # Optimal length
        
        total_score = engagement_score * 0.6 + hashtag_score * 0.2 + title_length_score * 0.2
        
        return min(round(total_score), 100)


# Example usage and testing
if __name__ == "__main__":
    print("🎯 YouTube SEO Optimizer - Demo")
    
    optimizer = SEOOptimizer()
    
    # Test different styles
    styles = ['lofi', 'trap', 'meditation', 'gaming']
    
    for style in styles:
        print(f"\n{'='*50}")
        print(f"🎵 Style: {style.upper()}")
        print(f"{'='*50}")
        
        # Generate optimized metadata
        metadata = optimizer.optimize_video_metadata(style, mood='chill')
        
        print(f"📝 Title: {metadata['title']}")
        print(f"🎯 SEO Score: {metadata['seo_score']}/100")
        print(f"📊 Engagement Score: {metadata['engagement_analysis']['engagement_score']}/100")
        print(f"👀 Estimated Views: {metadata['estimated_views']:,}")
        print(f"💰 Estimated Revenue: ${metadata['revenue_potential']['estimated_revenue']}")
        print(f"⏰ Optimal Upload Time: {metadata['optimal_upload_time']}")
        print(f"🏷️ Hashtags: {' '.join(metadata['hashtags'][:5])}")
        
        if metadata['engagement_analysis']['recommendations']:
            print("📋 Recommendations:")
            for rec in metadata['engagement_analysis']['recommendations'][:3]:
                print(f"   • {rec}")
    
    print(f"\n🎉 SEO optimization complete!")