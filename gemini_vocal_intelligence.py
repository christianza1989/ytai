#!/usr/bin/env python3
"""
🧠 GEMINI AI VOCAL INTELLIGENCE ENGINE
Advanced AI-powered vocal decision system using Gemini 2.5 Flash
"""

import os
import json
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

try:
    import google.generativeai as genai
except ImportError:
    print("⚠️  Google Generative AI not installed. Install with: pip install google-generativeai")
    genai = None

from advanced_genre_system import VocalType, VocalConfiguration

class GeminiVocalIntelligenceEngine:
    """Advanced AI vocal decision engine powered by Gemini 2.5 Flash"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = 'gemini-2.5-flash'
        
        if self.api_key and self.api_key != 'your_gemini_api_key_here' and genai:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.is_configured = True
        else:
            self.model = None
            self.is_configured = False
            
        # Market intelligence data
        self.market_intelligence = {
            "time_patterns": {
                "morning": {"vocal_boost": 0.3, "preferred_types": ["atmospheric", "uplifting"]},
                "work_hours": {"vocal_boost": -0.6, "preferred_types": ["instrumental", "minimal"]},
                "evening": {"vocal_boost": 0.4, "preferred_types": ["full_vocals", "emotional"]},
                "night": {"vocal_boost": -0.2, "preferred_types": ["ambient", "chill"]},
                "weekend": {"vocal_boost": 0.2, "preferred_types": ["energetic", "party"]}
            },
            "audience_intelligence": {
                "study": {"vocal_avoid": 0.8, "keywords": ["focus", "concentration", "productivity"]},
                "workout": {"vocal_boost": 0.7, "keywords": ["energy", "motivation", "power"]},
                "sleep": {"vocal_avoid": 0.9, "keywords": ["calm", "peaceful", "relaxing"]},
                "gaming": {"vocal_mixed": 0.5, "keywords": ["epic", "intense", "atmospheric"]},
                "work": {"vocal_avoid": 0.6, "keywords": ["professional", "ambient", "non-distracting"]},
                "relaxation": {"vocal_minimal": 0.4, "keywords": ["soothing", "gentle", "meditative"]}
            },
            "trending_patterns": {
                "vocal_trends_2025": {
                    "atmospheric_vocals": {"popularity": 0.85, "growth": 0.45},
                    "ai_generated_vocals": {"popularity": 0.78, "growth": 0.65},
                    "multilingual_vocals": {"popularity": 0.72, "growth": 0.38},
                    "minimal_vocals": {"popularity": 0.80, "growth": 0.25},
                    "nature_integrated": {"popularity": 0.68, "growth": 0.55}
                }
            }
        }
    
    def analyze_vocal_requirements(self, context: Dict) -> Dict:
        """Analyze context and determine optimal vocal strategy using Gemini AI"""
        
        if not self.is_configured:
            return self._fallback_vocal_analysis(context)
        
        try:
            # Prepare context for Gemini analysis
            analysis_prompt = self._build_analysis_prompt(context)
            
            # Get Gemini's analysis
            response = self.model.generate_content(analysis_prompt)
            gemini_analysis = self._parse_gemini_response(response.text)
            
            # Combine Gemini insights with market intelligence
            final_analysis = self._combine_intelligence(gemini_analysis, context)
            
            return final_analysis
            
        except Exception as e:
            print(f"Gemini analysis failed: {e}")
            return self._fallback_vocal_analysis(context)
    
    def _build_analysis_prompt(self, context: Dict) -> str:
        """Build comprehensive prompt for Gemini analysis"""
        
        genre_info = context.get('genre_info', {})
        user_context = context.get('user_context', {})
        
        prompt = f"""
        You are an AI music industry expert specializing in vocal strategy optimization for YouTube content.
        
        CONTEXT ANALYSIS:
        Genre: {genre_info.get('category', 'Unknown')} -> {genre_info.get('subgenre', 'Unknown')}
        Target Audience: {user_context.get('target_audience', 'general')}
        Upload Schedule: {user_context.get('upload_schedule', 'weekly')}
        Time Context: {user_context.get('time_context', 'any')}
        Revenue Target: ${user_context.get('target_revenue', 2000)}/month
        
        CURRENT MARKET DATA (2025):
        - Instrumental content: 40% higher engagement in study/work contexts
        - Atmospheric vocals: 85% popularity, 45% growth trend
        - AI-generated vocals: 78% popularity, 65% growth trend
        - Minimal vocals: 80% popularity, stable growth
        
        ANALYZE AND PROVIDE:
        1. Vocal Type Recommendation (instrumental/atmospheric_vocals/full_lyrics/minimal_vocals/rap_vocals/humming_vocals/nature_sounds/vocal_chops)
        2. Confidence Score (0-100%)
        3. Market Rationale (why this choice maximizes revenue potential)
        4. Audience Impact (how this affects target audience engagement)
        5. Competitive Advantage (what makes this unique in current market)
        6. Risk Assessment (potential downsides)
        7. Optimization Tips (3-5 specific recommendations)
        
        Respond in JSON format with these exact keys: vocal_type, confidence_score, market_rationale, audience_impact, competitive_advantage, risk_assessment, optimization_tips
        
        Focus on maximizing YouTube monetization potential while maintaining audience retention.
        """
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse Gemini's JSON response"""
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_text = response_text[json_start:json_end]
            return json.loads(json_text)
            
        except Exception as e:
            print(f"Failed to parse Gemini response: {e}")
            # Return fallback structure
            return {
                "vocal_type": "atmospheric_vocals",
                "confidence_score": 75,
                "market_rationale": "Gemini response parsing failed, using market-based fallback",
                "audience_impact": "Moderate positive impact expected",
                "competitive_advantage": "Safe choice for most genres",
                "risk_assessment": "Low risk, established market preference",
                "optimization_tips": ["Test multiple variations", "Monitor audience feedback", "Adjust based on analytics"]
            }
    
    def _combine_intelligence(self, gemini_analysis: Dict, context: Dict) -> Dict:
        """Combine Gemini insights with market intelligence"""
        
        user_context = context.get('user_context', {})
        genre_info = context.get('genre_info', {})
        
        # Apply market intelligence corrections
        vocal_type = gemini_analysis.get('vocal_type', 'atmospheric_vocals')
        confidence = gemini_analysis.get('confidence_score', 75)
        
        # Time-based adjustments
        time_context = user_context.get('time_context', 'any')
        if time_context in self.market_intelligence['time_patterns']:
            time_data = self.market_intelligence['time_patterns'][time_context]
            if 'vocal_boost' in time_data:
                confidence += time_data['vocal_boost'] * 10
        
        # Audience-based adjustments
        audience = user_context.get('target_audience', 'general')
        if audience in self.market_intelligence['audience_intelligence']:
            audience_data = self.market_intelligence['audience_intelligence'][audience]
            if 'vocal_avoid' in audience_data:
                if vocal_type in ['full_lyrics', 'rap_vocals']:
                    confidence -= audience_data['vocal_avoid'] * 30
            elif 'vocal_boost' in audience_data:
                if vocal_type in ['full_lyrics', 'rap_vocals']:
                    confidence += audience_data['vocal_boost'] * 20
        
        # Trending pattern adjustments
        trending_data = self.market_intelligence['trending_patterns']['vocal_trends_2025']
        if vocal_type in trending_data:
            trend_info = trending_data[vocal_type]
            confidence += trend_info['popularity'] * 15
            confidence += trend_info['growth'] * 10
        
        # Ensure confidence is within bounds
        confidence = max(60, min(95, confidence))
        
        # Enhanced analysis with market intelligence
        enhanced_analysis = gemini_analysis.copy()
        enhanced_analysis.update({
            'confidence_score': int(confidence),
            'market_intelligence': {
                'trending_factor': self._get_trending_factor(vocal_type),
                'audience_compatibility': self._get_audience_compatibility(vocal_type, audience),
                'revenue_optimization': self._get_revenue_optimization(vocal_type, context),
                'competitive_landscape': self._get_competitive_landscape(vocal_type, genre_info)
            },
            'actionable_insights': self._generate_actionable_insights(vocal_type, context)
        })
        
        return enhanced_analysis
    
    def _get_trending_factor(self, vocal_type: str) -> Dict:
        """Get trending analysis for vocal type"""
        trending_data = self.market_intelligence['trending_patterns']['vocal_trends_2025']
        
        if vocal_type in trending_data:
            data = trending_data[vocal_type]
            return {
                'trend_score': data['popularity'],
                'growth_rate': data['growth'],
                'recommendation': 'highly_recommended' if data['popularity'] > 0.8 else 'recommended' if data['popularity'] > 0.7 else 'consider_alternatives'
            }
        else:
            return {
                'trend_score': 0.6,
                'growth_rate': 0.1,
                'recommendation': 'emerging_trend'
            }
    
    def _get_audience_compatibility(self, vocal_type: str, audience: str) -> Dict:
        """Analyze audience compatibility"""
        audience_data = self.market_intelligence['audience_intelligence'].get(audience, {})
        
        compatibility_score = 0.7  # default
        
        if 'vocal_avoid' in audience_data:
            if vocal_type in ['full_lyrics', 'rap_vocals']:
                compatibility_score = 1.0 - audience_data['vocal_avoid']
        elif 'vocal_boost' in audience_data:
            if vocal_type in ['full_lyrics', 'rap_vocals']:
                compatibility_score = 0.7 + audience_data['vocal_boost'] * 0.3
        
        return {
            'compatibility_score': compatibility_score,
            'optimal_match': compatibility_score > 0.8,
            'audience_keywords': audience_data.get('keywords', [])
        }
    
    def _get_revenue_optimization(self, vocal_type: str, context: Dict) -> Dict:
        """Calculate revenue optimization potential"""
        user_context = context.get('user_context', {})
        target_revenue = user_context.get('target_revenue', 2000)
        
        # Revenue multipliers based on vocal type performance data
        revenue_multipliers = {
            'instrumental': 0.95,
            'atmospheric_vocals': 1.1,
            'full_lyrics': 1.15,
            'minimal_vocals': 1.05,
            'rap_vocals': 1.0,
            'humming_vocals': 0.9,
            'nature_sounds': 0.85,
            'vocal_chops': 1.08
        }
        
        multiplier = revenue_multipliers.get(vocal_type, 1.0)
        projected_revenue = target_revenue * multiplier
        
        return {
            'revenue_multiplier': multiplier,
            'projected_monthly_revenue': projected_revenue,
            'revenue_confidence': 'high' if multiplier > 1.05 else 'medium' if multiplier > 0.95 else 'conservative'
        }
    
    def _get_competitive_landscape(self, vocal_type: str, genre_info: Dict) -> Dict:
        """Analyze competitive landscape"""
        # Simulated competitive analysis based on genre and vocal type
        competition_levels = {
            'instrumental': 0.7,
            'atmospheric_vocals': 0.6,
            'full_lyrics': 0.85,
            'minimal_vocals': 0.65,
            'rap_vocals': 0.9,
            'humming_vocals': 0.4,
            'nature_sounds': 0.5,
            'vocal_chops': 0.7
        }
        
        competition_level = competition_levels.get(vocal_type, 0.7)
        
        return {
            'competition_level': competition_level,
            'market_saturation': 'high' if competition_level > 0.8 else 'medium' if competition_level > 0.6 else 'low',
            'differentiation_opportunity': 1.0 - competition_level,
            'recommended_strategy': 'focus_on_quality' if competition_level > 0.8 else 'scale_production' if competition_level < 0.6 else 'balanced_approach'
        }
    
    def _generate_actionable_insights(self, vocal_type: str, context: Dict) -> List[str]:
        """Generate specific actionable insights"""
        insights = []
        
        user_context = context.get('user_context', {})
        audience = user_context.get('target_audience', 'general')
        
        # Vocal type specific insights
        if vocal_type == 'instrumental':
            insights.extend([
                "Focus on rich harmonic progressions to maintain engagement without vocals",
                "Consider adding subtle ambient textures for emotional depth",
                "Optimize for study/work playlists which have high replay value"
            ])
        elif vocal_type == 'atmospheric_vocals':
            insights.extend([
                "Use ethereal vocal pads to create immersive soundscapes",
                "Layer multiple vocal textures for depth without lyrics complexity",
                "Perfect for meditation and ambient music markets"
            ])
        elif vocal_type == 'full_lyrics':
            insights.extend([
                "Invest in high-quality vocal production for competitive advantage",
                "Focus on memorable hooks and emotional storytelling",
                "Consider multiple language versions for global reach"
            ])
        
        # Audience-specific insights
        if audience == 'study':
            insights.append("Ensure tempo and dynamics support concentration flow states")
        elif audience == 'workout':
            insights.append("Maintain consistent energy levels throughout the track")
        elif audience == 'sleep':
            insights.append("Use gradual volume fades and avoid sudden dynamic changes")
        
        return insights
    
    def _fallback_vocal_analysis(self, context: Dict) -> Dict:
        """Fallback analysis when Gemini is not available"""
        
        user_context = context.get('user_context', {})
        genre_info = context.get('genre_info', {})
        
        # Simple rule-based fallback
        audience = user_context.get('target_audience', 'general')
        
        if audience in ['study', 'work', 'sleep']:
            vocal_type = 'instrumental'
            confidence = 85
        elif audience in ['workout', 'party']:
            vocal_type = 'full_lyrics'
            confidence = 80
        else:
            vocal_type = 'atmospheric_vocals'
            confidence = 75
        
        return {
            'vocal_type': vocal_type,
            'confidence_score': confidence,
            'market_rationale': 'Rule-based analysis - Gemini AI not available',
            'audience_impact': f'Optimized for {audience} audience engagement',
            'competitive_advantage': 'Safe market-tested approach',
            'risk_assessment': 'Low risk, established patterns',
            'optimization_tips': [
                'Monitor audience engagement metrics',
                'A/B test different vocal approaches',
                'Adjust based on performance data'
            ],
            'fallback_mode': True
        }
    
    def generate_vocal_configuration(self, analysis: Dict, context: Dict) -> VocalConfiguration:
        """Generate detailed vocal configuration from analysis"""
        
        vocal_type_str = analysis.get('vocal_type', 'atmospheric_vocals')
        user_context = context.get('user_context', {})
        
        # Map string to enum
        vocal_type_mapping = {
            'instrumental': VocalType.INSTRUMENTAL,
            'atmospheric_vocals': VocalType.ATMOSPHERIC_VOCALS,
            'full_lyrics': VocalType.FULL_LYRICS,
            'minimal_vocals': VocalType.MINIMAL_VOCALS,
            'rap_vocals': VocalType.RAP_VOCALS,
            'humming_vocals': VocalType.HUMMING_VOCALS,
            'nature_sounds': VocalType.NATURE_SOUNDS,
            'vocal_chops': VocalType.VOCAL_CHOPS
        }
        
        vocal_type = vocal_type_mapping.get(vocal_type_str, VocalType.ATMOSPHERIC_VOCALS)
        
        # Generate configuration based on type and context
        if vocal_type == VocalType.INSTRUMENTAL:
            return VocalConfiguration(
                vocal_type=vocal_type,
                language="none",
                mood="neutral",
                style="instrumental",
                lyrics_complexity="none",
                vocal_effects=[]
            )
        
        elif vocal_type == VocalType.ATMOSPHERIC_VOCALS:
            return VocalConfiguration(
                vocal_type=vocal_type,
                language="wordless",
                mood=random.choice(["ethereal", "dreamy", "peaceful"]),
                style="atmospheric",
                lyrics_complexity="simple",
                vocal_effects=["reverb", "chorus", "delay"]
            )
        
        elif vocal_type == VocalType.FULL_LYRICS:
            return VocalConfiguration(
                vocal_type=vocal_type,
                language=user_context.get('preferred_language', 'en'),
                mood=random.choice(["emotional", "uplifting", "energetic"]),
                style="melodic",
                lyrics_complexity="medium",
                vocal_effects=["reverb", "compression", "eq"]
            )
        
        elif vocal_type == VocalType.MINIMAL_VOCALS:
            return VocalConfiguration(
                vocal_type=vocal_type,
                language=random.choice(["en", "wordless"]),
                mood=random.choice(["chill", "mysterious", "ambient"]),
                style="sparse",
                lyrics_complexity="simple",
                vocal_effects=["reverb", "filter"]
            )
        
        else:  # Other vocal types
            return VocalConfiguration(
                vocal_type=vocal_type,
                language="mixed",
                mood="varied",
                style="creative",
                lyrics_complexity="medium",
                vocal_effects=["reverb", "creative_fx"]
            )
    
    def get_comprehensive_vocal_strategy(self, context: Dict) -> Dict:
        """Get complete vocal strategy with Gemini AI analysis"""
        
        # Run AI analysis
        analysis = self.analyze_vocal_requirements(context)
        
        # Generate vocal configuration
        vocal_config = self.generate_vocal_configuration(analysis, context)
        
        # Combine everything
        strategy = {
            'ai_analysis': analysis,
            'vocal_configuration': {
                'vocal_type': vocal_config.vocal_type.value,
                'language': vocal_config.language,
                'mood': vocal_config.mood,
                'style': vocal_config.style,
                'lyrics_complexity': vocal_config.lyrics_complexity,
                'vocal_effects': vocal_config.vocal_effects
            },
            'implementation_guide': {
                'suno_prompt_additions': self._get_suno_prompt_additions(vocal_config),
                'production_tips': analysis.get('optimization_tips', []),
                'quality_checkpoints': self._get_quality_checkpoints(vocal_config)
            },
            'success_metrics': {
                'confidence_score': analysis.get('confidence_score', 75),
                'expected_engagement': self._calculate_expected_engagement(analysis, context),
                'revenue_projection': analysis.get('market_intelligence', {}).get('revenue_optimization', {}),
                'competitive_advantage': analysis.get('market_intelligence', {}).get('competitive_landscape', {})
            },
            'generated_at': datetime.now().isoformat(),
            'ai_powered': self.is_configured
        }
        
        return strategy
    
    def _get_suno_prompt_additions(self, vocal_config: VocalConfiguration) -> List[str]:
        """Get Suno-specific prompt additions for vocal configuration"""
        
        additions = []
        
        if vocal_config.vocal_type == VocalType.INSTRUMENTAL:
            additions.extend(["instrumental", "no vocals", "melodic instruments"])
        elif vocal_config.vocal_type == VocalType.ATMOSPHERIC_VOCALS:
            additions.extend(["atmospheric vocals", "ambient voices", "ethereal soundscape"])
        elif vocal_config.vocal_type == VocalType.FULL_LYRICS:
            additions.extend([f"{vocal_config.mood} vocals", "clear lyrics", "melodic singing"])
        elif vocal_config.vocal_type == VocalType.MINIMAL_VOCALS:
            additions.extend(["sparse vocals", "minimal lyrics", "subtle voice"])
        
        # Add mood and effects
        if vocal_config.mood != "neutral":
            additions.append(f"{vocal_config.mood} mood")
        
        if vocal_config.vocal_effects:
            additions.extend([f"vocal {effect}" for effect in vocal_config.vocal_effects[:2]])  # Limit to 2 effects
        
        return additions
    
    def _get_quality_checkpoints(self, vocal_config: VocalConfiguration) -> List[str]:
        """Get quality checkpoints for vocal production"""
        
        checkpoints = [
            "Verify audio clarity and balance",
            "Check vocal/instrumental mix levels",
            "Ensure consistent volume throughout"
        ]
        
        if vocal_config.vocal_type == VocalType.FULL_LYRICS:
            checkpoints.extend([
                "Confirm lyrics are intelligible",
                "Check vocal pitch accuracy",
                "Verify emotional delivery matches mood"
            ])
        elif vocal_config.vocal_type == VocalType.ATMOSPHERIC_VOCALS:
            checkpoints.extend([
                "Ensure vocals blend with atmosphere",
                "Check reverb/delay balance",
                "Verify spatial positioning"
            ])
        
        return checkpoints
    
    def _calculate_expected_engagement(self, analysis: Dict, context: Dict) -> Dict:
        """Calculate expected engagement metrics"""
        
        confidence = analysis.get('confidence_score', 75)
        market_intel = analysis.get('market_intelligence', {})
        
        base_engagement = confidence / 100
        
        # Adjust for trending factors
        trending_factor = market_intel.get('trending_factor', {}).get('trend_score', 0.7)
        audience_compatibility = market_intel.get('audience_compatibility', {}).get('compatibility_score', 0.7)
        
        adjusted_engagement = base_engagement * 0.5 + trending_factor * 0.3 + audience_compatibility * 0.2
        
        return {
            'engagement_score': round(adjusted_engagement * 100, 1),
            'expected_retention': f"{round(adjusted_engagement * 80, 1)}%",
            'replay_likelihood': 'high' if adjusted_engagement > 0.8 else 'medium' if adjusted_engagement > 0.6 else 'moderate',
            'viral_potential': round(adjusted_engagement * trending_factor * 100, 1)
        }

# Global instance
gemini_vocal_engine = GeminiVocalIntelligenceEngine()

if __name__ == "__main__":
    # Test the engine
    print("🧠 GEMINI VOCAL INTELLIGENCE ENGINE TEST")
    print("=" * 60)
    
    test_context = {
        'genre_info': {
            'category': 'CHILLOUT',
            'subgenre': 'LO_FI_HIP_HOP',
            'substyle': 'STUDY_BEATS'
        },
        'user_context': {
            'target_audience': 'study',
            'upload_schedule': 'daily',
            'time_context': 'work_hours',
            'target_revenue': 3000,
            'preferred_language': 'en'
        }
    }
    
    strategy = gemini_vocal_engine.get_comprehensive_vocal_strategy(test_context)
    
    print(f"AI Analysis: {strategy['ai_analysis']['vocal_type']}")
    print(f"Confidence: {strategy['ai_analysis']['confidence_score']}%")
    print(f"Market Rationale: {strategy['ai_analysis']['market_rationale']}")
    print(f"AI Powered: {strategy['ai_powered']}")
    
    print("\nVocal Configuration:")
    config = strategy['vocal_configuration']
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    print(f"\nExpected Engagement: {strategy['success_metrics']['expected_engagement']['engagement_score']}%")
    print(f"Revenue Projection: {strategy['success_metrics'].get('revenue_projection', {})}")