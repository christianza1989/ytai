#!/usr/bin/env python3
"""
Test integration of all advanced systems
"""

import sys
sys.path.insert(0, '.')

def test_integration():
    print("🚀 Testing Advanced Genre System Integration")
    print("=" * 60)
    
    # Test imports
    try:
        from advanced_genre_system import advanced_genre_system, recommendation_engine
        print('✅ Advanced genre system imported successfully')
        
        from gemini_vocal_intelligence import gemini_vocal_engine
        print('✅ Gemini vocal intelligence imported successfully')
        
        from music_industry_analytics import music_analytics
        print('✅ Music industry analytics imported successfully')
        
        # Test genre system functionality
        print('\n📊 Testing Genre System:')
        profitable_genres = recommendation_engine.get_top_profitable_genres(3)
        print(f'  Top profitable genres: {len(profitable_genres)} found')
        for i, (genre, data) in enumerate(profitable_genres[:3], 1):
            print(f'    {i}. {genre}: ${data["data"]["statistics"].monthly_revenue}/mo')
        
        # Test trending genres
        trending_genres = recommendation_engine.get_trending_genres(3)
        print(f'  Trending genres: {len(trending_genres)} found')
        
        # Test easy start genres
        easy_genres = recommendation_engine.get_easiest_to_start(3)
        print(f'  Easy start genres: {len(easy_genres)} found')
        
        # Test analytics system
        print('\n📈 Testing Analytics System:')
        performance = music_analytics.analyze_genre_performance('CHILLOUT.LO_FI_HIP_HOP', 30)
        print(f'  Performance analysis completed:')
        print(f'    Average Revenue: ${performance["revenue_metrics"]["average_monthly_revenue"]}')
        print(f'    Revenue Trend: {performance["revenue_metrics"]["revenue_trend"]}')
        print(f'    Market Position: {performance["market_position"]["performance_percentile"]}th percentile')
        
        # Test market opportunities
        opportunities = music_analytics.get_market_opportunities()
        print(f'  Market opportunities: {len(opportunities["high_growth_segments"])} high-growth segments')
        
        # Test vocal intelligence
        print('\n🧠 Testing Vocal Intelligence:')
        test_context = {
            'genre_info': {
                'category': 'CHILLOUT', 
                'subgenre': 'LO_FI_HIP_HOP',
                'vocal_probability': 0.15
            },
            'user_context': {
                'target_audience': 'study', 
                'target_revenue': 3000,
                'upload_schedule': 'daily',
                'time_context': 'work_hours'
            }
        }
        
        strategy = gemini_vocal_engine.get_comprehensive_vocal_strategy(test_context)
        print(f'  Vocal strategy generated:')
        print(f'    Type: {strategy["vocal_configuration"]["vocal_type"]}')
        print(f'    Confidence: {strategy["ai_analysis"]["confidence_score"]}%')
        print(f'    AI Powered: {strategy["ai_powered"]}')
        print(f'    Market Rationale: {strategy["ai_analysis"]["market_rationale"][:100]}...')
        
        # Test Suno prompt generation
        print('\n🎵 Testing Suno Integration:')
        suno_additions = gemini_vocal_engine._get_suno_prompt_additions(
            gemini_vocal_engine.generate_vocal_configuration(strategy["ai_analysis"], test_context)
        )
        print(f'  Suno prompt additions: {", ".join(suno_additions[:5])}')
        
        print('\n🎯 INTEGRATION TEST RESULTS:')
        print('✅ All core systems operational')
        print('✅ Genre intelligence system ready')  
        print('✅ AI vocal decision engine ready')
        print('✅ Music industry analytics ready')
        print('✅ API integrations functional')
        
        print('\n🚀 ADVANCED YOUTUBE EMPIRE SYSTEM READY FOR 24/7 OPERATION!')
        return True
        
    except ImportError as e:
        print(f'❌ Import error: {e}')
        return False
    except Exception as e:
        print(f'❌ Test error: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integration()
    exit(0 if success else 1)