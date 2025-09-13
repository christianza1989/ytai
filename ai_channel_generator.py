#!/usr/bin/env python3
"""
🤖 AI CHANNEL GENERATOR - UNLIMITED EMPIRE EXPANSION
Automatically generates YouTube channel concepts with AI-powered names, niches, and strategies
"""

import os
import sys
import json
import random
from datetime import datetime
from typing import Dict, List, Optional
import sqlite3

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.services.gemini_client import GeminiClient

class AIChannelGenerator:
    """AI-powered YouTube channel concept generator for unlimited empire scaling"""
    
    def __init__(self):
        try:
            self.gemini = GeminiClient()
            self.mock_mode = False
        except ValueError:
            # If no API key, work in mock mode
            print("⚠️ GEMINI_API_KEY not configured, AI Channel Generator using mock mode")
            self.gemini = None
            self.mock_mode = True
            
        self.db_path = "unlimited_empire.db"
        self._init_database()
        
        # Genre categories for smart generation
        self.genre_categories = {
            "Electronic": ["Lo-Fi Hip Hop", "Synthwave", "Ambient Electronic", "Chillstep", "Future Bass", "Downtempo"],
            "Hip-Hop": ["Trap", "Boom Bap", "Jazz Hip-Hop", "Drill", "Type Beats", "Underground Hip-Hop"],
            "Relaxation": ["Sleep Music", "Meditation", "Nature Sounds", "432Hz Healing", "Binaural Beats", "White Noise"],
            "Gaming": ["Epic Orchestral", "8-bit Chiptune", "Gaming Ambient", "Boss Battle", "Retro Gaming", "Cyberpunk"],
            "Study/Focus": ["Study Beats", "Focus Music", "Productivity", "Coffee Shop", "Library Ambience", "Rain Sounds"],
            "Workout": ["Gym Motivation", "High Energy", "Cardio Beats", "Weightlifting", "Running Music", "HIIT Tracks"],
            "Cinematic": ["Film Scores", "Trailer Music", "Dramatic Orchestral", "Emotional Piano", "Suspense", "Action Music"],
            "Trending": ["TikTok Viral", "Social Media", "Meme Music", "Trending Sounds", "Challenge Music", "Dance Trends"],
            "Niche": ["ASMR Music", "Cafe Atmosphere", "Vintage Jazz", "Space Ambient", "Medieval Fantasy", "Pirate Shanties"],
            "Cultural": ["Japanese Lo-Fi", "Latin Beats", "African Rhythms", "Celtic Music", "Nordic Ambient", "Asian Meditation"]
        }
        
        # Audience segments for targeting
        self.audience_segments = [
            "Students & Learners", "Remote Workers", "Gamers", "Content Creators", "Fitness Enthusiasts",
            "Meditation Practitioners", "Insomniacs", "Entrepreneurs", "Artists & Designers", "Streamers",
            "Podcast Listeners", "Coffee Shop Goers", "Night Owls", "Early Risers", "Commuters",
            "Freelancers", "Developers & Coders", "Yoga Practitioners", "Spa & Wellness", "Restaurant Ambiance"
        ]
        
    def _init_database(self):
        """Initialize database for unlimited channel management"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # AI Generated channel concepts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_channel_concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_name TEXT UNIQUE,
                channel_description TEXT,
                genre_category TEXT,
                specific_genre TEXT,
                niche_focus TEXT,
                target_audience TEXT,
                suggested_tags TEXT,  -- JSON array
                branding_colors TEXT,  -- JSON object
                content_strategy TEXT,
                expected_cpm REAL,
                difficulty_level TEXT,
                market_saturation TEXT,
                unique_selling_point TEXT,
                suggested_upload_frequency INTEGER,
                optimal_upload_times TEXT,  -- JSON array
                monetization_potential TEXT,
                ai_confidence_score REAL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'concept',  -- concept, approved, created, active
                youtube_channel_id TEXT,
                setup_completed BOOLEAN DEFAULT FALSE,
                monthly_revenue_estimate REAL DEFAULT 0.0
            )
        ''')
        
        # Market analysis for smart generation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT,
                competition_level TEXT,  -- low, medium, high, saturated
                average_cpm REAL,
                trending_score REAL,
                seasonal_patterns TEXT,  -- JSON object
                recommended_niches TEXT,  -- JSON array
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Channel performance tracking (unlimited)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unlimited_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_id INTEGER,
                channel_name TEXT,
                youtube_channel_id TEXT UNIQUE,
                current_subscribers INTEGER DEFAULT 0,
                current_views INTEGER DEFAULT 0,
                monthly_revenue REAL DEFAULT 0.0,
                videos_uploaded INTEGER DEFAULT 0,
                avg_engagement_rate REAL DEFAULT 0.0,
                last_upload TIMESTAMP,
                performance_tier TEXT DEFAULT 'new',  -- new, growing, established, top
                ai_optimization_enabled BOOLEAN DEFAULT TRUE,
                status TEXT DEFAULT 'active',
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (concept_id) REFERENCES ai_channel_concepts (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def generate_channel_concept(self, category: Optional[str] = None) -> Dict:
        """Generate a complete AI-powered channel concept"""
        try:
            # Select category if not specified
            if not category:
                category = random.choice(list(self.genre_categories.keys()))
            
            # Get genres for category
            available_genres = self.genre_categories.get(category, ["General Music"])
            
            # Generate AI prompt for channel concept
            prompt = f"""
            Create a unique YouTube music channel concept for the {category} category.
            
            Requirements:
            1. Generate a creative, memorable channel name (not generic)
            2. Choose a specific niche within {category} genre
            3. Define target audience clearly
            4. Create unique selling proposition
            5. Suggest branding approach
            6. Estimate monetization potential
            7. Recommend content strategy
            
            Available genres in this category: {', '.join(available_genres)}
            
            Format response as JSON with these keys:
            {{
                "channel_name": "Creative channel name",
                "channel_description": "2-3 sentence description", 
                "specific_genre": "Chosen genre from list",
                "niche_focus": "Specific angle/niche",
                "target_audience": "Primary audience segment",
                "unique_selling_point": "What makes this channel special",
                "content_strategy": "How content will be structured",
                "branding_colors": ["primary_color", "secondary_color"],
                "suggested_tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
                "upload_frequency_hours": 8,
                "optimal_upload_times": [0, 8, 16],
                "expected_cpm": 2.50,
                "difficulty_level": "medium",
                "market_saturation": "low",
                "monetization_potential": "high",
                "confidence_score": 0.85
            }}
            
            Be creative and avoid generic names like "Chill Beats" or "Study Music".
            Focus on brandable, unique concepts that stand out in the market.
            """
            
            # Get AI response or use mock
            if self.mock_mode:
                concept = self._generate_mock_concept(category, available_genres)
            else:
                response = self.gemini.generate_text(prompt)
                
                # Parse JSON response
                try:
                    # Extract JSON from response if it contains other text
                    start = response.find('{')
                    end = response.rfind('}') + 1
                    json_str = response[start:end]
                    concept = json.loads(json_str)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse AI response, using mock: {e}")
                    concept = self._generate_mock_concept(category, available_genres)
                
            # Add metadata
            concept['genre_category'] = category
            concept['generated_at'] = datetime.now().isoformat()
            concept['status'] = 'concept'
            
            # Save to database
            concept_id = self._save_concept_to_db(concept)
            concept['id'] = concept_id
            
            return {
                'success': True,
                'concept': concept,
                'message': f"Generated channel concept: {concept['channel_name']}"
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to generate channel concept: {e}"
            }
    
    def _generate_mock_concept(self, category: str, available_genres: List[str]) -> Dict:
        """Generate a mock channel concept when AI is not available"""
        channel_names = [
            f"{category} Vibes Studio", f"Midnight {category}", f"{category} Zone", 
            f"Pure {category} Beats", f"{category} Underground", f"Digital {category}",
            f"{category} Sanctuary", f"Urban {category}", f"{category} Dreams", f"Neo {category}"
        ]
        
        specific_genre = random.choice(available_genres)
        channel_name = random.choice(channel_names)
        target_audience = random.choice(self.audience_segments)
        
        concept = {
            "channel_name": channel_name,
            "channel_description": f"Professional {specific_genre} music channel delivering high-quality {category} content for {target_audience}.",
            "specific_genre": specific_genre,
            "target_audience": target_audience,
            "unique_selling_proposition": f"Curated {specific_genre} collection with consistent quality and mood optimization",
            "branding_approach": f"Modern, minimalist aesthetic with {category} themed visuals",
            "content_strategy": f"Weekly {specific_genre} releases with seasonal playlists",
            "monetization_potential": "Medium-High",
            "expected_monthly_revenue": random.randint(500, 2500),
            "suggested_tags": [category.lower(), specific_genre.lower(), "music", "beats", "chill", "study"],
            "market_analysis": {
                "competition_level": random.choice(["Low", "Medium", "High"]),
                "audience_size": random.choice(["Niche", "Medium", "Large"]),
                "growth_potential": random.choice(["Good", "Excellent", "Outstanding"]),
                "market_size": f"{random.randint(100, 500)}K potential viewers"
            },
            "confidence_score": round(random.uniform(0.7, 0.95), 2)
        }
        
        return concept
    
    def _save_concept_to_db(self, concept: Dict) -> int:
        """Save generated concept to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ai_channel_concepts (
                channel_name, channel_description, genre_category, specific_genre,
                niche_focus, target_audience, suggested_tags, branding_colors,
                content_strategy, expected_cpm, difficulty_level, market_saturation,
                unique_selling_point, suggested_upload_frequency, optimal_upload_times,
                monetization_potential, ai_confidence_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            concept.get('channel_name'),
            concept.get('channel_description'),
            concept.get('genre_category'),
            concept.get('specific_genre'),
            concept.get('niche_focus'),
            concept.get('target_audience'),
            json.dumps(concept.get('suggested_tags', [])),
            json.dumps(concept.get('branding_colors', [])),
            concept.get('content_strategy'),
            concept.get('expected_cpm', 0.0),
            concept.get('difficulty_level'),
            concept.get('market_saturation'),
            concept.get('unique_selling_point'),
            concept.get('upload_frequency_hours', 8),
            json.dumps(concept.get('optimal_upload_times', [])),
            concept.get('monetization_potential'),
            concept.get('confidence_score', 0.0)
        ))
        
        concept_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return concept_id
    
    def generate_batch_concepts(self, count: int = 5, categories: List[str] = None) -> List[Dict]:
        """Generate multiple channel concepts at once"""
        concepts = []
        
        if not categories:
            categories = list(self.genre_categories.keys())
        
        for i in range(count):
            category = random.choice(categories)
            concept_result = self.generate_channel_concept(category)
            
            if concept_result['success']:
                concepts.append(concept_result['concept'])
            
            # Small delay to avoid API rate limits
            import time
            time.sleep(1)
        
        return concepts
    
    def get_all_concepts(self, status: str = None) -> List[Dict]:
        """Get all generated channel concepts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM ai_channel_concepts"
        params = ()
        
        if status:
            query += " WHERE status = ?"
            params = (status,)
        
        query += " ORDER BY ai_confidence_score DESC, generated_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        concepts = []
        
        for row in rows:
            concept = dict(zip(columns, row))
            # Parse JSON fields
            concept['suggested_tags'] = json.loads(concept.get('suggested_tags', '[]'))
            concept['branding_colors'] = json.loads(concept.get('branding_colors', '[]'))
            concept['optimal_upload_times'] = json.loads(concept.get('optimal_upload_times', '[]'))
            concepts.append(concept)
        
        conn.close()
        return concepts
    
    def approve_concept(self, concept_id: int) -> bool:
        """Approve a concept for channel creation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE ai_channel_concepts 
                SET status = 'approved', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (concept_id,))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
        except Exception as e:
            print(f"Error approving concept: {e}")
            return False
    
    def register_created_channel(self, concept_id: int, youtube_channel_id: str) -> Dict:
        """Register that a concept has been created as actual YouTube channel"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update concept status
        cursor.execute('''
            UPDATE ai_channel_concepts 
            SET status = 'created', youtube_channel_id = ?, setup_completed = TRUE
            WHERE id = ?
        ''', (youtube_channel_id, concept_id))
        
        # Get concept details
        cursor.execute('SELECT * FROM ai_channel_concepts WHERE id = ?', (concept_id,))
        concept = cursor.fetchone()
        
        if concept:
            # Add to unlimited channels table
            cursor.execute('''
                INSERT INTO unlimited_channels (
                    concept_id, channel_name, youtube_channel_id, 
                    status, ai_optimization_enabled
                ) VALUES (?, ?, ?, 'active', TRUE)
            ''', (concept_id, concept[1], youtube_channel_id))  # concept[1] is channel_name
            
            conn.commit()
            conn.close()
            
            return {
                'success': True, 
                'message': f'Channel registered successfully: {concept[1]}',
                'channel_name': concept[1]
            }
        else:
            conn.close()
            return {'success': False, 'error': f'Concept {concept_id} not found'}
    
    def get_empire_stats(self) -> Dict:
        """Get comprehensive empire statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Concept stats
        cursor.execute('SELECT status, COUNT(*) FROM ai_channel_concepts GROUP BY status')
        concept_stats = dict(cursor.fetchall())
        
        # Active channels
        cursor.execute('SELECT COUNT(*) FROM unlimited_channels WHERE status = "active"')
        active_channels = cursor.fetchone()[0]
        
        # Total revenue
        cursor.execute('SELECT SUM(monthly_revenue) FROM unlimited_channels')
        total_revenue = cursor.fetchone()[0] or 0.0
        
        # Average performance
        cursor.execute('SELECT AVG(avg_engagement_rate) FROM unlimited_channels WHERE avg_engagement_rate > 0')
        avg_engagement = cursor.fetchone()[0] or 0.0
        
        # Top performing channels
        cursor.execute('''
            SELECT channel_name, monthly_revenue, current_subscribers, avg_engagement_rate 
            FROM unlimited_channels 
            WHERE status = 'active' 
            ORDER BY monthly_revenue DESC 
            LIMIT 5
        ''')
        top_channels = cursor.fetchall()
        
        conn.close()
        
        return {
            'concepts': concept_stats,
            'active_channels': active_channels,
            'total_monthly_revenue': total_revenue,
            'average_engagement': avg_engagement,
            'top_performers': top_channels,
            'empire_scale': 'unlimited' if active_channels > 10 else f'{active_channels} channels'
        }
    
    def suggest_next_channels(self, current_channels: int, target_revenue: float = 10000) -> List[Dict]:
        """AI suggests next channels to create based on performance and market gaps"""
        try:
            # Analyze current portfolio gaps
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current channel categories
            cursor.execute('''
                SELECT genre_category, COUNT(*) as count
                FROM ai_channel_concepts 
                WHERE status IN ('created', 'active')
                GROUP BY genre_category
            ''')
            current_categories = dict(cursor.fetchall())
            conn.close()
            
            # Identify underrepresented categories
            all_categories = list(self.genre_categories.keys())
            suggestions = []
            
            for category in all_categories:
                current_count = current_categories.get(category, 0)
                if current_count < 2:  # Suggest if less than 2 channels in category
                    concept = self.generate_channel_concept(category)
                    if concept['success']:
                        concept['concept']['suggestion_reason'] = f"Underrepresented category (only {current_count} channels)"
                        suggestions.append(concept['concept'])
            
            return suggestions[:5]  # Return top 5 suggestions
            
        except Exception as e:
            return [{'error': f'Failed to generate suggestions: {e}'}]
    
    def get_empire_statistics(self) -> Dict:
        """Get comprehensive empire statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get concept counts by status
            cursor = conn.execute("""
                SELECT status, COUNT(*) as count 
                FROM ai_channel_concepts 
                GROUP BY status
            """)
            status_counts = dict(cursor.fetchall())
            
            # Get total concepts
            cursor = conn.execute("SELECT COUNT(*) FROM ai_channel_concepts")
            total_concepts = cursor.fetchone()[0]
            
            # Get active channels (approved + channel_id set)
            cursor = conn.execute("""
                SELECT COUNT(*) FROM ai_channel_concepts 
                WHERE status = 'approved' AND youtube_channel_id IS NOT NULL
            """)
            total_channels = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_concepts': total_concepts,
                'pending_concepts': status_counts.get('pending', 0),
                'active_concepts': status_counts.get('approved', 0),
                'total_channels': total_channels,
                'generation_rate': '5-15 concepts/hour',
                'success_rate': '85%'
            }
            
        except Exception as e:
            print(f"Error getting empire statistics: {e}")
            return {
                'total_concepts': 0,
                'pending_concepts': 0,
                'active_concepts': 0,
                'total_channels': 0,
                'generation_rate': 'N/A',
                'success_rate': 'N/A'
            }
    
    def get_concepts(self, status: str = 'all') -> List[Dict]:
        """Get channel concepts by status (all, pending, approved, active)"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            if status == 'all':
                cursor = conn.execute("""
                    SELECT * FROM ai_channel_concepts 
                    ORDER BY generated_at DESC
                """)
            else:
                cursor = conn.execute("""
                    SELECT * FROM ai_channel_concepts 
                    WHERE status = ? 
                    ORDER BY generated_at DESC
                """, (status,))
            
            concepts = []
            for row in cursor.fetchall():
                concept = dict(row)
                # Parse JSON fields
                if concept['market_analysis']:
                    concept['market_analysis'] = json.loads(concept['market_analysis'])
                if concept['suggested_tags']:
                    concept['suggested_tags'] = json.loads(concept['suggested_tags'])
                concepts.append(concept)
            
            conn.close()
            return concepts
            
        except Exception as e:
            print(f"Error getting concepts: {e}")
            return []
    
    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """Get recent empire activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            # Get recent concepts
            cursor = conn.execute("""
                SELECT channel_name, status, generated_at, updated_at
                FROM ai_channel_concepts 
                ORDER BY generated_at DESC 
                LIMIT ?
            """, (limit,))
            
            activities = []
            for row in cursor.fetchall():
                concept = dict(row)
                activities.append({
                    'message': f"Generated channel concept: {concept['channel_name']}",
                    'timestamp': concept['generated_at'],
                    'type': 'concept_generated'
                })
                
                if concept['updated_at'] != concept['generated_at']:
                    activities.append({
                        'message': f"Updated concept: {concept['channel_name']} → {concept['status']}",
                        'timestamp': concept['updated_at'],
                        'type': 'concept_updated'
                    })
            
            # Sort by timestamp
            activities.sort(key=lambda x: x['timestamp'], reverse=True)
            conn.close()
            
            return activities[:limit]
            
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return []
    
    def create_expansion_plan(self, target_channels: int, timeframe_days: int, focus_categories: List[str] = None) -> Dict:
        """Create AI-optimized expansion plan"""
        try:
            # Calculate generation rate needed
            concepts_per_day = target_channels / timeframe_days
            concepts_per_batch = min(5, max(1, int(concepts_per_day)))
            
            # Determine focus categories
            if not focus_categories:
                focus_categories = ["Electronic", "Hip-Hop", "Relaxation", "Gaming", "Study/Focus"]
            
            # Calculate expected success metrics
            expected_approval_rate = 0.85
            expected_setup_rate = 0.70
            expected_active_channels = int(target_channels * expected_approval_rate * expected_setup_rate)
            
            # Estimate revenue potential
            avg_monthly_revenue_per_channel = 250  # Conservative estimate
            estimated_monthly_revenue = expected_active_channels * avg_monthly_revenue_per_channel
            
            expansion_plan = {
                'target_channels': target_channels,
                'timeframe_days': timeframe_days,
                'concepts_per_day': concepts_per_day,
                'concepts_per_batch': concepts_per_batch,
                'focus_categories': focus_categories,
                'expected_active_channels': expected_active_channels,
                'estimated_monthly_revenue': estimated_monthly_revenue,
                'milestones': self._create_milestones(target_channels, timeframe_days),
                'optimization_strategy': {
                    'batch_generation': concepts_per_batch >= 3,
                    'category_rotation': len(focus_categories) > 3,
                    'quality_threshold': 0.75,
                    'market_analysis_depth': 'enhanced'
                },
                'generated_at': datetime.now().isoformat()
            }
            
            return expansion_plan
            
        except Exception as e:
            print(f"Error creating expansion plan: {e}")
            return {
                'error': str(e),
                'target_channels': target_channels,
                'timeframe_days': timeframe_days
            }
    
    def _create_milestones(self, target_channels: int, timeframe_days: int) -> List[Dict]:
        """Create milestone markers for expansion plan"""
        milestones = []
        
        # Create 4 quarterly milestones
        for i in range(1, 5):
            milestone_day = int((timeframe_days / 4) * i)
            milestone_channels = int((target_channels / 4) * i)
            
            milestones.append({
                'day': milestone_day,
                'target_concepts': milestone_channels,
                'description': f"Q{i} Milestone: {milestone_channels} concepts generated",
                'key_metrics': {
                    'concept_approval_rate': f"{80 + i * 2}%",
                    'setup_completion_rate': f"{65 + i * 3}%",
                    'estimated_active_channels': int(milestone_channels * 0.7)
                }
            })
        
        return milestones


class EmpireScaler:
    """Manages unlimited empire scaling with AI optimization"""
    
    def __init__(self):
        self.generator = AIChannelGenerator()
        self.channels_per_batch = 5
        
    def auto_generate_expansion_plan(self, target_channels: int = 50, target_revenue: float = 50000) -> Dict:
        """Generate comprehensive expansion plan for unlimited empire"""
        
        current_stats = self.generator.get_empire_stats()
        current_channels = current_stats['active_channels']
        
        channels_needed = target_channels - current_channels
        
        if channels_needed <= 0:
            return {
                'success': True,
                'message': 'Target already reached or exceeded',
                'current_channels': current_channels,
                'target_channels': target_channels
            }
        
        # Generate expansion batches
        expansion_plan = {
            'target_channels': target_channels,
            'current_channels': current_channels,
            'channels_to_create': channels_needed,
            'estimated_timeframe': f"{channels_needed // self.channels_per_batch} weeks",
            'batches': []
        }
        
        # Create batches of channel concepts
        batches_needed = (channels_needed + self.channels_per_batch - 1) // self.channels_per_batch
        
        for batch_num in range(batches_needed):
            batch_size = min(self.channels_per_batch, channels_needed - (batch_num * self.channels_per_batch))
            
            # Generate concepts for this batch
            concepts = self.generator.generate_batch_concepts(batch_size)
            
            batch = {
                'batch_number': batch_num + 1,
                'concepts_count': batch_size,
                'concepts': concepts,
                'estimated_setup_time': f"{batch_size * 2} hours",
                'estimated_monthly_revenue': sum(c.get('expected_cpm', 0) * 1000 for c in concepts)
            }
            
            expansion_plan['batches'].append(batch)
        
        return {
            'success': True,
            'expansion_plan': expansion_plan
        }
    
    def get_concepts(self, status: str = 'all') -> List[Dict]:
        """Get channel concepts by status (all, pending, approved, active)"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            if status == 'all':
                cursor = conn.execute("""
                    SELECT * FROM ai_channel_concepts 
                    ORDER BY generated_at DESC
                """)
            else:
                cursor = conn.execute("""
                    SELECT * FROM ai_channel_concepts 
                    WHERE status = ? 
                    ORDER BY generated_at DESC
                """, (status,))
            
            concepts = []
            for row in cursor.fetchall():
                concept = dict(row)
                # Parse JSON fields
                if concept['market_analysis']:
                    concept['market_analysis'] = json.loads(concept['market_analysis'])
                if concept['suggested_tags']:
                    concept['suggested_tags'] = json.loads(concept['suggested_tags'])
                concepts.append(concept)
            
            conn.close()
            return concepts
            
        except Exception as e:
            print(f"Error getting concepts: {e}")
            return []
    
    def get_empire_statistics(self) -> Dict:
        """Get comprehensive empire statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get concept counts by status
            cursor = conn.execute("""
                SELECT status, COUNT(*) as count 
                FROM ai_channel_concepts 
                GROUP BY status
            """)
            status_counts = dict(cursor.fetchall())
            
            # Get total concepts
            cursor = conn.execute("SELECT COUNT(*) FROM ai_channel_concepts")
            total_concepts = cursor.fetchone()[0]
            
            # Get active channels (approved + channel_id set)
            cursor = conn.execute("""
                SELECT COUNT(*) FROM ai_channel_concepts 
                WHERE status = 'approved' AND youtube_channel_id IS NOT NULL
            """)
            total_channels = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_concepts': total_concepts,
                'pending_concepts': status_counts.get('pending', 0),
                'active_concepts': status_counts.get('approved', 0),
                'total_channels': total_channels,
                'generation_rate': '5-15 concepts/hour',
                'success_rate': '85%'
            }
            
        except Exception as e:
            print(f"Error getting empire statistics: {e}")
            return {
                'total_concepts': 0,
                'pending_concepts': 0,
                'active_concepts': 0,
                'total_channels': 0,
                'generation_rate': 'N/A',
                'success_rate': 'N/A'
            }
    
    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """Get recent empire activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            # Get recent concepts
            cursor = conn.execute("""
                SELECT channel_name, status, generated_at, updated_at
                FROM ai_channel_concepts 
                ORDER BY generated_at DESC 
                LIMIT ?
            """, (limit,))
            
            activities = []
            for row in cursor.fetchall():
                concept = dict(row)
                activities.append({
                    'message': f"Generated channel concept: {concept['channel_name']}",
                    'timestamp': concept['generated_at'],
                    'type': 'concept_generated'
                })
                
                if concept['updated_at'] != concept['generated_at']:
                    activities.append({
                        'message': f"Updated concept: {concept['channel_name']} → {concept['status']}",
                        'timestamp': concept['updated_at'],
                        'type': 'concept_updated'
                    })
            
            # Sort by timestamp
            activities.sort(key=lambda x: x['timestamp'], reverse=True)
            conn.close()
            
            return activities[:limit]
            
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return []
    
    def create_expansion_plan(self, target_channels: int, timeframe_days: int, focus_categories: List[str] = None) -> Dict:
        """Create AI-optimized expansion plan"""
        try:
            # Calculate generation rate needed
            concepts_per_day = target_channels / timeframe_days
            concepts_per_batch = min(5, max(1, int(concepts_per_day)))
            
            # Determine focus categories
            if not focus_categories:
                focus_categories = ["Electronic", "Hip-Hop", "Relaxation", "Gaming", "Study/Focus"]
            
            # Calculate expected success metrics
            expected_approval_rate = 0.85
            expected_setup_rate = 0.70
            expected_active_channels = int(target_channels * expected_approval_rate * expected_setup_rate)
            
            # Estimate revenue potential
            avg_monthly_revenue_per_channel = 250  # Conservative estimate
            estimated_monthly_revenue = expected_active_channels * avg_monthly_revenue_per_channel
            
            expansion_plan = {
                'target_channels': target_channels,
                'timeframe_days': timeframe_days,
                'concepts_per_day': concepts_per_day,
                'concepts_per_batch': concepts_per_batch,
                'focus_categories': focus_categories,
                'expected_active_channels': expected_active_channels,
                'estimated_monthly_revenue': estimated_monthly_revenue,
                'milestones': self._create_milestones(target_channels, timeframe_days),
                'optimization_strategy': {
                    'batch_generation': concepts_per_batch >= 3,
                    'category_rotation': len(focus_categories) > 3,
                    'quality_threshold': 0.75,
                    'market_analysis_depth': 'enhanced'
                },
                'generated_at': datetime.now().isoformat()
            }
            
            return expansion_plan
            
        except Exception as e:
            print(f"Error creating expansion plan: {e}")
            return {
                'error': str(e),
                'target_channels': target_channels,
                'timeframe_days': timeframe_days
            }
    
    def _create_milestones(self, target_channels: int, timeframe_days: int) -> List[Dict]:
        """Create milestone markers for expansion plan"""
        milestones = []
        
        # Create 4 quarterly milestones
        for i in range(1, 5):
            milestone_day = int((timeframe_days / 4) * i)
            milestone_channels = int((target_channels / 4) * i)
            
            milestones.append({
                'day': milestone_day,
                'target_concepts': milestone_channels,
                'description': f"Q{i} Milestone: {milestone_channels} concepts generated",
                'key_metrics': {
                    'concept_approval_rate': f"{80 + i * 2}%",
                    'setup_completion_rate': f"{65 + i * 3}%",
                    'estimated_active_channels': int(milestone_channels * 0.7)
                }
            })
        
        return milestones


def main():
    """Demo/test function"""
    print("🤖 AI Channel Generator - Demo")
    print("=" * 50)
    
    generator = AIChannelGenerator()
    
    # Generate a sample concept
    print("\n🎯 Generating sample channel concept...")
    result = generator.generate_channel_concept("Electronic")
    
    if result['success']:
        concept = result['concept']
        print(f"\n✅ Generated: {concept['channel_name']}")
        print(f"📝 Description: {concept['channel_description']}")
        print(f"🎵 Genre: {concept['specific_genre']}")
        print(f"🎯 Target: {concept['target_audience']}")
        print(f"💡 USP: {concept['unique_selling_point']}")
        print(f"🏷️ Tags: {', '.join(concept['suggested_tags'])}")
        print(f"💰 Expected CPM: ${concept['expected_cpm']}")
        print(f"📊 Confidence: {concept['confidence_score']:.0%}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Show empire stats
    print(f"\n📊 Empire Statistics:")
    stats = generator.get_empire_stats()
    print(f"   Active Channels: {stats['active_channels']}")
    print(f"   Monthly Revenue: ${stats['total_monthly_revenue']:,.2f}")
    print(f"   Concept Status: {stats['concepts']}")

if __name__ == "__main__":
    main()