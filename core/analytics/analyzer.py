import os
from typing import Dict, Any, Optional
from datetime import datetime

from core.database.database_manager import DatabaseManager
from core.services.gemini_client import GeminiClient

class PerformanceAnalyzer:
    """AI-powered performance analyzer using Gemini for content insights"""

    def __init__(self, db_manager: DatabaseManager, gemini_client: GeminiClient):
        self.db_manager = db_manager
        self.gemini_client = gemini_client

    def run_analysis(self) -> str:
        """
        Run comprehensive performance analysis using Gemini AI

        Returns:
            Analysis report with insights and recommendations
        """
        print("🧠 Starting AI-powered performance analysis...")
        print("=" * 60)

        try:
            # Get performance data from database
            performance_data = self.db_manager.get_performance_summary_for_analysis()

            if "No performance data" in performance_data or "Error" in performance_data:
                return "INSUFFICIENT_DATA"

            print("📊 Retrieved performance data for analysis")
            print(f"📋 Data length: {len(performance_data)} characters")

            # Create comprehensive analysis prompt
            analysis_prompt = self._create_analysis_prompt(performance_data)

            print("🤖 Sending data to Gemini for analysis...")

            # Get analysis from Gemini
            analysis_result = self.gemini_client.generate_content(analysis_prompt)

            if not analysis_result:
                return "❌ Failed to get analysis from Gemini AI."

            # Format and return the analysis
            formatted_report = self._format_analysis_report(analysis_result, performance_data)

            print("\n✅ Analysis completed successfully!")
            print("=" * 60)

            return formatted_report

        except Exception as e:
            error_msg = f"❌ Analysis failed: {e}"
            print(error_msg)
            return error_msg

    def _create_analysis_prompt(self, performance_data: str) -> str:
        """
        Create a comprehensive analysis prompt for Gemini

        Args:
            performance_data: Formatted performance data string

        Returns:
            Complete analysis prompt
        """
        prompt = f"""You are an expert YouTube content strategist and data analyst specializing in AI-generated music content. Your task is to analyze the provided video performance data and provide actionable insights for content optimization.

PERFORMANCE DATA:
{performance_data}

ANALYSIS REQUIREMENTS:

1. **SUCCESS PATTERN IDENTIFICATION:**
   - Identify the most successful genres, themes, and content elements
   - Analyze which titles, tags, and themes correlate with higher engagement
   - Find patterns in successful vs. unsuccessful content

2. **CONTENT OPTIMIZATION INSIGHTS:**
   - Determine optimal content themes and genres for this channel
   - Identify effective title and tag strategies
   - Analyze engagement patterns (views, likes, comments)

3. **STRATEGIC RECOMMENDATIONS:**
   - Provide 5-7 specific, actionable recommendations for future content
   - Suggest content themes that should be prioritized
   - Recommend title and tag optimization strategies
   - Identify content types to avoid or minimize

4. **TREND ANALYSIS:**
   - Identify emerging patterns in the data
   - Suggest content evolution strategies
   - Provide competitive positioning insights

5. **CONTENT STRATEGY SUMMARY:**
   - Create a clear content strategy roadmap
   - Define target audience preferences
   - Suggest optimal posting frequency and content mix

FORMAT YOUR RESPONSE AS FOLLOWS:

🎯 EXECUTIVE SUMMARY
[2-3 sentence overview of key findings]

📈 PERFORMANCE ANALYSIS
[Detailed analysis of successful patterns and metrics]

🎨 CONTENT OPTIMIZATION
[Specific recommendations for content creation]

🏷️ TITLE & TAG STRATEGY
[Optimization recommendations for discoverability]

📊 TREND INSIGHTS
[Emerging patterns and future predictions]

🎯 ACTION PLAN
[5-7 prioritized recommendations for next content cycle]

⚡ QUICK WINS
[Immediate, high-impact actions to implement]

Please provide specific, actionable insights based on the actual data provided. Be data-driven in your recommendations and focus on practical strategies that can be implemented immediately."""

        return prompt

    def _format_analysis_report(self, gemini_response: str, performance_data: str) -> str:
        """
        Format the Gemini analysis response into a comprehensive report

        Args:
            gemini_response: Raw Gemini analysis response
            performance_data: Original performance data for context

        Returns:
            Formatted analysis report
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        report = "=" * 80 + "\n"
        report += "🎯 YOUTUBE CONTENT PERFORMANCE ANALYSIS REPORT\n"
        report += "=" * 80 + "\n\n"

        report += f"📅 Analysis Date: {timestamp}\n"
        report += f"🤖 AI Model: Gemini\n"
        report += f"📊 Data Source: Local Database\n\n"

        # Add Gemini's analysis
        report += "🧠 AI-GENERATED ANALYSIS\n"
        report += "-" * 40 + "\n\n"
        report += gemini_response
        report += "\n\n"

        # Add data summary
        report += "📋 DATA SUMMARY\n"
        report += "-" * 40 + "\n"
        data_lines = performance_data.split('\n')
        for line in data_lines[-10:]:  # Last 10 lines contain summary stats
            if line.strip():
                report += line + "\n"

        report += "\n" + "=" * 80 + "\n"
        report += "✅ Analysis Complete - Ready for Content Strategy Implementation\n"
        report += "=" * 80 + "\n"

        return report

    def analyze_single_video(self, video_id: str) -> str:
        """
        Analyze a single video's performance

        Args:
            video_id: YouTube video ID

        Returns:
            Individual video analysis
        """
        try:
            print(f"📊 Analyzing single video: {video_id}")

            # Get video data from database
            video = self.db_manager.get_video_by_youtube_id(video_id)
            if not video:
                return f"❌ Video {video_id} not found in database"

            # Get latest metrics
            metrics = self.db_manager.get_latest_metrics_for_video(video.id)
            if not metrics:
                return f"❌ No performance metrics found for video {video_id}"

            # Get content creation data
            creation = self.db_manager.get_creation_by_id(video.content_id)
            genre = creation.genre if creation else "Unknown"
            theme = creation.theme if creation else "Unknown"

            # Format data for analysis
            video_data = f"""SINGLE VIDEO ANALYSIS DATA:

Video: '{video.title}'
Genre: '{genre}'
Theme: '{theme}'
Tags: {', '.join([f'"{tag}"' for tag in video.tags]) if video.tags else 'None'}
Performance: {metrics.view_count} views, {metrics.like_count} likes, {metrics.comment_count} comments
Upload Date: {video.upload_date.isoformat() if video.upload_date else 'Unknown'}
Last Checked: {metrics.check_date.isoformat() if metrics.check_date else 'Unknown'}
"""

            # Create focused analysis prompt
            prompt = f"""Analyze this single video's performance and provide specific recommendations for improvement:

{video_data}

Please provide:
1. Performance assessment (good/average/poor)
2. Title effectiveness analysis
3. Tag optimization suggestions
4. Content theme feedback
5. Specific improvement recommendations

Be specific and actionable in your recommendations."""

            # Get analysis from Gemini
            analysis = self.gemini_client.generate_content(prompt)

            if analysis:
                return f"🎬 SINGLE VIDEO ANALYSIS: {video.title}\n\n{analysis}"
            else:
                return f"❌ Failed to analyze video {video_id}"

        except Exception as e:
            return f"❌ Single video analysis failed: {e}"

    def generate_content_strategy_report(self) -> str:
        """
        Generate a comprehensive content strategy report

        Returns:
            Complete content strategy document
        """
        try:
            print("📋 Generating comprehensive content strategy report...")

            # Run full analysis
            analysis = self.run_analysis()

            if "❌" in analysis:
                return analysis

            # Get additional data for strategy
            summary = self.db_manager.get_content_performance_summary()
            top_videos = self.db_manager.get_top_performing_videos(limit=5)
            genre_analysis = self.db_manager.get_genre_performance_analysis()

            # Create strategy document
            strategy = f"""{analysis}

🎯 CONTENT STRATEGY IMPLEMENTATION GUIDE
{'=' * 50}

📈 CURRENT PERFORMANCE BASELINE:
• Total Videos: {summary.get('total_videos', 0)}
• Total Views: {summary.get('total_views', 0):,}
• Average Performance: {summary.get('total_views', 0) / max(summary.get('total_videos', 1), 1):.0f} views/video

🏆 TOP PERFORMING CONTENT:
"""

            for i, video in enumerate(top_videos, 1):
                strategy += f"{i}. {video['title']} - {video['views']:,} views\n"

            strategy += f"\n🎨 GENRE PERFORMANCE:\n"
            for genre, stats in genre_analysis.items():
                strategy += f"• {genre}: {stats['avg_views']:.0f} avg views, {stats['creation_count']} videos\n"

            strategy += f"""
📅 IMPLEMENTATION TIMELINE:
Week 1-2: Implement title and tag optimizations
Week 3-4: Focus on high-performing themes
Week 5-8: Scale successful content patterns
Week 9-12: Test new content variations

⚡ SUCCESS METRICS TO TRACK:
• View count growth rate
• Like-to-view ratio improvement
• Comment engagement increase
• Content discovery through optimized titles/tags

This strategy is based on your actual performance data and should be reviewed monthly as new data becomes available."""

            return strategy

        except Exception as e:
            return f"❌ Strategy report generation failed: {e}"

    def get_quick_insights(self) -> Dict[str, Any]:
        """
        Get quick performance insights without full analysis

        Returns:
            Dictionary with key performance indicators
        """
        try:
            summary = self.db_manager.get_content_performance_summary()
            top_videos = self.db_manager.get_top_performing_videos(limit=3)

            insights = {
                'total_videos': summary.get('total_videos', 0),
                'total_views': summary.get('total_views', 0),
                'avg_views_per_video': summary.get('total_views', 0) / max(summary.get('total_videos', 1), 1),
                'top_performer': top_videos[0] if top_videos else None,
                'recent_activity': summary.get('recent_videos', 0),
                'data_freshness': 'current' if summary else 'no_data'
            }

            return insights

        except Exception as e:
            return {
                'error': str(e),
                'data_freshness': 'error'
            }
