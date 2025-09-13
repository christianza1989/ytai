#!/usr/bin/env python3
"""
Test script for the Performance Analysis functionality
"""

from dotenv import load_dotenv
from core.database.database_manager import DatabaseManager
from core.analytics.analyzer import PerformanceAnalyzer
from core.services.gemini_client import GeminiClient

def test_performance_analysis():
    """Test the performance analysis functionality"""
    print("🧠 Testing Performance Analysis Module")
    print("=" * 50)

    try:
        # Load environment variables
        load_dotenv()

        # Initialize components
        print("\n🔧 Initializing components...")

        db_manager = DatabaseManager()
        gemini_client = GeminiClient()

        print("✅ Components initialized successfully")

        # Create analyzer
        analyzer = PerformanceAnalyzer(db_manager, gemini_client)

        # Run analysis
        print("\n🧠 Running performance analysis...")
        result = analyzer.run_analysis()

        print("\n" + "=" * 80)
        print("📋 ANALYSIS RESULTS")
        print("=" * 80)
        print(result)

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_performance_analysis()
    if success:
        print("\n✅ Performance Analysis test completed successfully!")
    else:
        print("\n❌ Performance Analysis test failed!")
