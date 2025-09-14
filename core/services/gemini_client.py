import os
import google.generativeai as genai
from typing import Dict, Any, Optional
import json

class GeminiClient:
    """Google Gemini AI client for creative content generation"""

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        # FIXED MODEL: gemini-2.5-flash is the LATEST and ONLY supported model
        # This model CANNOT be changed as it's the newest and most advanced version
        self.model_name = 'gemini-2.5-flash'  # LATEST MODEL - DO NOT CHANGE

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate_creative_brief(self, genre: str, theme: str, analysis_report: str = None, **kwargs) -> Dict[str, Any]:
        """Generate a creative brief for music creation, optionally using performance analysis"""
        try:
            if analysis_report and analysis_report != "INSUFFICIENT_DATA":
                # Adaptive mode: Use performance analysis to guide creative decisions
                prompt = f"""
                You are a creative YouTube music producer with access to performance analytics. Your task is to generate a new, successful music video idea based on previous performance data and recommendations.

                Here is the analysis and recommendations from your previous work:
                --- ANALYSIS START ---
                {analysis_report}
                --- ANALYSIS END ---

                Based on these insights and recommendations, generate a new creative idea for a {genre} track with the theme: "{theme}".

                IMPORTANT: Your new idea should reflect the analysis conclusions. For example:
                - If analysis recommends "space" themes, make the new idea space-related
                - If analysis shows "synthwave" performs best, focus on synthwave elements
                - If analysis suggests specific titles/tags work better, incorporate those patterns
                - If analysis identifies successful emotional tones, match those tones

                Please provide the response in the following JSON format:
                {{
                    "title": "Catchy, descriptive title for the track",
                    "description": "Brief description of the mood and atmosphere",
                    "lyrics_prompt": "Detailed prompt for lyrics generation (if applicable)",
                    "style_suggestions": "Specific style elements, instruments, or production techniques",
                    "target_audience": "Who this music is for",
                    "key_elements": ["list", "of", "key", "musical", "elements"],
                    "emotional_tone": "Primary emotional feeling the track should convey",
                    "visual_concepts": "Ideas for album art or video visuals",
                    "youtube_title": "Optimized YouTube video title (max 100 characters)",
                    "youtube_description": "Detailed YouTube description with keywords and engagement hooks",
                    "youtube_tags": ["lofi", "ai", "music", "beats", "study", "relaxing"]
                }}

                Make the lyrics_prompt detailed enough for AI music generation, incorporating successful patterns from the analysis.
                """
            else:
                # Standard mode: Generate creative idea without analysis
                prompt = f"""
                You are a creative music producer. Generate a detailed creative brief for a {genre} track with the theme: "{theme}".

                Please provide the response in the following JSON format:
                {{
                    "title": "Catchy, descriptive title for the track",
                    "description": "Brief description of the mood and atmosphere",
                    "lyrics_prompt": "Detailed prompt for lyrics generation (if applicable)",
                    "style_suggestions": "Specific style elements, instruments, or production techniques",
                    "target_audience": "Who this music is for",
                    "key_elements": ["list", "of", "key", "musical", "elements"],
                    "emotional_tone": "Primary emotional feeling the track should convey",
                    "visual_concepts": "Ideas for album art or video visuals",
                    "youtube_title": "Optimized YouTube video title (max 100 characters)",
                    "youtube_description": "Detailed YouTube description with keywords and engagement hooks",
                    "youtube_tags": ["lofi", "ai", "music", "beats", "study", "relaxing"]
                }}

                Make the lyrics_prompt detailed enough for AI music generation, including:
                - Song structure (verse, chorus, bridge)
                - Key themes and messages
                - Specific imagery and metaphors
                - Emotional progression
                - Cultural or personal references that fit the theme

                Keep the response focused and actionable for music creation.
                """

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Clean up the response (remove markdown code blocks if present)
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]

            # Parse JSON response
            brief = json.loads(response_text.strip())

            # Validate required fields
            required_fields = ['title', 'lyrics_prompt']
            for field in required_fields:
                if field not in brief:
                    brief[field] = f"Auto-generated {field} for {genre} {theme}"

            return brief

        except json.JSONDecodeError as e:
            print(f"Failed to parse Gemini response as JSON: {e}")
            # Fallback response
            return {
                "title": f"{genre} - {theme}",
                "description": f"A {genre} track exploring {theme}",
                "lyrics_prompt": f"Create lyrics for a {genre} song about {theme}. Include verses, chorus, and emotional depth.",
                "style_suggestions": f"Modern {genre} production with atmospheric elements",
                "target_audience": "Music enthusiasts and streaming listeners",
                "key_elements": [genre, theme, "atmospheric", "emotional"],
                "emotional_tone": "Reflective and immersive",
                "visual_concepts": f"Abstract representation of {theme}"
            }
        except Exception as e:
            print(f"Failed to generate creative brief: {e}")
            # Ultimate fallback
            return {
                "title": f"{genre} - {theme}",
                "lyrics_prompt": f"Create a {genre} song about {theme}"
            }

    def analyze_performance_data(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze YouTube performance data and provide insights"""
        try:
            prompt = f"""
            You are a music marketing analyst. Analyze this YouTube video performance data and provide strategic insights:

            Video Data: {json.dumps(video_data, indent=2)}

            Please provide analysis in JSON format:
            {{
                "performance_score": "A, B, C, or D rating",
                "key_insights": ["list", "of", "key", "findings"],
                "recommendations": ["specific", "actionable", "recommendations"],
                "content_suggestions": ["ideas", "for", "future", "content"],
                "optimization_tips": ["technical", "or", "content", "improvements"],
                "trend_analysis": "Analysis of what worked or didn't work"
            }}

            Focus on:
            - View count vs expected performance
            - Engagement metrics (likes, comments, shares)
            - Audience retention patterns
            - Content quality indicators
            - Optimization opportunities
            """

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Clean up response
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]

            analysis = json.loads(response_text.strip())
            return analysis

        except Exception as e:
            print(f"Failed to analyze performance data: {e}")
            return {
                "performance_score": "C",
                "key_insights": ["Analysis failed - check data format"],
                "recommendations": ["Retry analysis with complete data"],
                "content_suggestions": ["Continue with current content strategy"],
                "optimization_tips": ["Verify data collection process"],
                "trend_analysis": "Unable to analyze trends"
            }

    def generate_video_metadata(self, music_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate optimized YouTube metadata (title, description, tags)"""
        try:
            prompt = f"""
            You are a YouTube SEO expert. Generate optimized metadata for this music video:

            Music Data: {json.dumps(music_data, indent=2)}

            Create SEO-optimized content that will help the video rank well on YouTube.
            Consider trending keywords, search intent, and click-through optimization.

            Response format:
            {{
                "title": "Optimized title (under 100 characters)",
                "description": "Detailed description with keywords, timestamps, and calls-to-action",
                "tags": ["keyword1", "keyword2", "keyword3", ...],
                "hashtags": "#hashtag1 #hashtag2 #hashtag3"
            }}

            Make the title catchy and include the main keyword.
            Description should be engaging, include relevant keywords naturally, and encourage engagement.
            Tags should include primary keywords, related terms, and long-tail phrases.
            """

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Clean up response
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]

            metadata = json.loads(response_text.strip())
            return metadata

        except Exception as e:
            print(f"Failed to generate video metadata: {e}")
            return {
                "title": music_data.get('title', 'AI Generated Music'),
                "description": f"Enjoy this AI-generated music track: {music_data.get('title', 'Unknown')}",
                "tags": ["AI music", "generated music", "electronic"],
                "hashtags": "#AIMusic #GeneratedMusic #Electronic"
            }

    def generate_content(self, prompt: str) -> Optional[str]:
        """Generate content using Gemini AI with a custom prompt"""
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Clean up response (remove markdown formatting if present)
            if response_text.startswith('```'):
                # Remove opening markdown code block
                lines = response_text.split('\n')
                if len(lines) > 0 and lines[0].startswith('```'):
                    lines = lines[1:]
                if len(lines) > 0 and lines[-1].startswith('```'):
                    lines = lines[:-1]
                response_text = '\n'.join(lines).strip()

            return response_text

        except Exception as e:
            print(f"Failed to generate content: {e}")
            return None

    def refine_content_strategy(self, historical_data: list) -> Dict[str, Any]:
        """Analyze historical performance and refine content strategy"""
        try:
            prompt = f"""
            You are a content strategist for an AI music channel. Analyze this historical performance data and provide strategic recommendations:

            Historical Data: {json.dumps(historical_data, indent=2)}

            Provide analysis in JSON format:
            {{
                "strategy_adjustments": ["specific", "changes", "to", "make"],
                "genre_performance": {{"genre1": "performance_rating", "genre2": "performance_rating"}},
                "optimal_posting_times": ["best", "times", "to", "post"],
                "content_themes": ["themes", "that", "perform", "well"],
                "quality_improvements": ["ways", "to", "improve", "content", "quality"],
                "growth_opportunities": ["specific", "opportunities", "for", "growth"]
            }}

            Base recommendations on data patterns, audience engagement, and growth potential.
            """

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Clean up response
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]

            strategy = json.loads(response_text.strip())
            return strategy

        except Exception as e:
            print(f"Failed to refine content strategy: {e}")
            return {
                "strategy_adjustments": ["Continue current approach"],
                "genre_performance": {},
                "optimal_posting_times": ["Evening hours"],
                "content_themes": ["Current themes working well"],
                "quality_improvements": ["Maintain current quality standards"],
                "growth_opportunities": ["Expand to new platforms"]
            }
