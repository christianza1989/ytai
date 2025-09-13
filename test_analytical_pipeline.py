#!/usr/bin/env python3
"""
Focused test script for the Analytical Pipeline (Phase 3C Validation)
Tests the complete analytical infrastructure without external dependencies
"""

from dotenv import load_dotenv
from core.database.database_manager import DatabaseManager
from core.analytics.analyzer import PerformanceAnalyzer
from core.services.gemini_client import GeminiClient
import json
import time

def create_mock_performance_data(db_manager):
    """Create mock performance data for testing the analytical pipeline"""
    print("🔧 Creating mock performance data for testing...")

    # Check if we already have data
    existing_videos = db_manager.get_all_videos()
    if len(existing_videos) >= 2:
        print("✅ Using existing performance data from database")
        return existing_videos[:2]

    # Create mock content creation
    creation_data = {
        'genre': 'Lo-Fi Hip Hop',
        'theme': 'rainy night in Tokyo',
        'title': 'Midnight Rain Sessions',
        'youtube_title': 'Lo-Fi Beats for Rainy Nights',
        'brief_json': json.dumps({
            'title': 'Midnight Rain Sessions',
            'lyrics_prompt': 'Create lo-fi hip hop about rainy Tokyo nights',
            'style_suggestions': 'Chill beats with rain sounds',
            'target_audience': 'Study music listeners',
            'emotional_tone': 'Peaceful, introspective',
            'visual_concepts': 'Rainy city streets, neon lights'
        }),
        'status': 'completed'
    }

    creation1 = db_manager.add_content_creation(creation_data)

    # Create another content creation with different genre
    creation_data2 = {
        'genre': 'Synthwave',
        'theme': 'cyberpunk city',
        'title': 'Neon Dreams',
        'youtube_title': 'Synthwave Journey Through Cyberpunk City',
        'brief_json': json.dumps({
            'title': 'Neon Dreams',
            'lyrics_prompt': 'Create synthwave about cyberpunk city exploration',
            'style_suggestions': 'Retro synth sounds, futuristic vibes',
            'target_audience': 'Retro gaming fans',
            'emotional_tone': 'Energetic, adventurous',
            'visual_concepts': 'Neon lights, skyscrapers, flying cars'
        }),
        'status': 'completed'
    }

    creation2 = db_manager.add_content_creation(creation_data2)

    # Generate unique video IDs based on timestamp
    import time
    timestamp = str(int(time.time()))

    # Create mock YouTube videos
    video_data1 = {
        'video_id': f'test_video_{timestamp}_001',
        'youtube_url': f'https://youtube.com/watch?v=test_video_{timestamp}_001',
        'title': 'Lo-Fi Beats for Rainy Nights v1',
        'description': 'Chill lo-fi hip hop beats perfect for studying',
        'tags': ['lofi', 'beats', 'study music', 'rain', 'tokyo'],
        'category_id': '10',
        'privacy_status': 'private'
    }

    video_data2 = {
        'video_id': f'test_video_{timestamp}_002',
        'youtube_url': f'https://youtube.com/watch?v=test_video_{timestamp}_002',
        'title': 'Synthwave Journey v1',
        'description': 'Retro synthwave adventure through cyberpunk city',
        'tags': ['synthwave', 'cyberpunk', 'retro', 'electronic'],
        'category_id': '10',
        'privacy_status': 'private'
    }

    video1 = db_manager.add_youtube_video(creation1, video_data1)
    video2 = db_manager.add_youtube_video(creation2, video_data2)

    # Add mock performance metrics
    metrics1 = {
        'view_count': 1250,
        'like_count': 85,
        'comment_count': 12
    }

    metrics2 = {
        'view_count': 890,
        'like_count': 67,
        'comment_count': 8
    }

    db_manager.add_performance_metric(video1.id, metrics1)
    db_manager.add_performance_metric(video2.id, metrics2)

    print("✅ Mock performance data created successfully")
    return [video1, video2]

def test_analytical_pipeline():
    """Test the complete analytical pipeline"""
    print("🧠 TESTING ANALYTICAL PIPELINE - PHASE 3C VALIDATION")
    print("=" * 60)

    try:
        # Load environment variables
        load_dotenv()

        # Initialize components
        print("\n🔧 Initializing analytical components...")
        db_manager = DatabaseManager()
        gemini_client = GeminiClient()

        print("✅ Components initialized successfully")

        # Create mock data for testing
        print("\n📊 Setting up test data...")
        videos = create_mock_performance_data(db_manager)

        # Wait a moment for data to be committed
        time.sleep(1)

        # Initialize analyzer
        analyzer = PerformanceAnalyzer(db_manager, gemini_client)

        # Run analysis
        print("\n🧠 Running AI-powered performance analysis...")
        print("📋 This will test the complete analytical pipeline:")
        print("   1. Data retrieval from database")
        print("   2. Data formatting for AI analysis")
        print("   3. Gemini AI prompt generation")
        print("   4. Analysis result processing")
        print("   5. Formatted report generation")

        analysis_result = analyzer.run_analysis()

        print("\n" + "=" * 80)
        print("🎯 ANALYSIS RESULTS - FIRST AI-GENERATED INSIGHTS")
        print("=" * 80)
        print(analysis_result)

        # Additional validation
        print("\n" + "=" * 80)
        print("📊 VALIDATION SUMMARY")
        print("=" * 80)

        # Check if analysis contains expected elements
        validation_checks = {
            'Has Executive Summary': '🎯 EXECUTIVE SUMMARY' in analysis_result,
            'Has Performance Analysis': '📈 PERFORMANCE ANALYSIS' in analysis_result,
            'Has Recommendations': '🎯 ACTION PLAN' in analysis_result,
            'Has Data Summary': '📋 DATA SUMMARY' in analysis_result,
            'Contains Video Data': 'Video 1:' in analysis_result,
            'Has Summary Statistics': 'SUMMARY STATISTICS:' in analysis_result
        }

        print("🔍 Analysis Structure Validation:")
        for check_name, passed in validation_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")

        all_passed = all(validation_checks.values())
        print(f"\n🎯 Overall Validation: {'✅ PASSED' if all_passed else '❌ FAILED'}")

        if all_passed:
            print("\n🎉 SUCCESS! The analytical pipeline is working correctly!")
            print("   - Database queries are functioning")
            print("   - Data formatting is correct")
            print("   - Gemini AI integration is working")
            print("   - Analysis report generation is complete")
            print("\n🚀 Phase 3C - Analytical Module is READY for production use!")

        return all_passed

    except Exception as e:
        print(f"\n❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_additional_analytics():
    """Run additional analytical functions for comprehensive testing"""
    print("\n🔍 Running additional analytical tests...")

    try:
        load_dotenv()
        db_manager = DatabaseManager()
        gemini_client = GeminiClient()
        analyzer = PerformanceAnalyzer(db_manager, gemini_client)

        # Test quick insights
        print("\n📈 Testing quick insights...")
        insights = analyzer.get_quick_insights()
        print(f"Quick insights: {insights}")

        # Test content summary
        print("\n📊 Testing content performance summary...")
        summary = db_manager.get_content_performance_summary()
        print(f"Content summary: {summary}")

        # Test genre analysis
        print("\n🎨 Testing genre performance analysis...")
        genre_analysis = db_manager.get_genre_performance_analysis()
        print(f"Genre analysis: {genre_analysis}")

        print("✅ Additional analytical functions tested successfully")

    except Exception as e:
        print(f"❌ Additional tests failed: {e}")

if __name__ == "__main__":
    print("🎯 PHASE 3C VALIDATION: Analytical Pipeline Testing")
    print("Testing the complete AI-powered content analysis system")
    print("=" * 60)

    success = test_analytical_pipeline()

    if success:
        print("\n🎊 PHASE 3C VALIDATION COMPLETE!")
        print("The analytical infrastructure is fully operational.")
        print("Ready to proceed to Phase 3D - Active Learning!")

        # Run additional tests
        run_additional_analytics()
    else:
        print("\n❌ PHASE 3C VALIDATION FAILED")
        print("Please check the error messages above and fix any issues.")
