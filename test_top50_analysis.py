#!/usr/bin/env python3
"""
Test script for top 50 cryptocurrency analysis
"""

from enhanced_analyzer import EnhancedCryptoAnalyzer
import time

def test_top50_analysis():
    """Test the top 50 cryptocurrency analysis functionality"""
    print("🧪 Testing top 50 cryptocurrency analysis...")
    
    try:
        # Initialize the enhanced analyzer
        analyzer = EnhancedCryptoAnalyzer(verbose=True)
        
        # Test fetching top 50 cryptocurrencies
        print("\n📊 Fetching top 50 cryptocurrencies by market cap...")
        market_fetcher = analyzer.market_fetcher
        top_coins = market_fetcher.get_top_cryptocurrencies(limit=50)
        
        if not top_coins:
            print("❌ Failed to fetch top 50 cryptocurrencies")
            return False
        
        print(f"✅ Successfully fetched {len(top_coins)} cryptocurrencies")
        
        # Display first 10 cryptocurrencies
        print("\n🏆 Top 10 cryptocurrencies by market cap:")
        for i, coin in enumerate(top_coins[:10], 1):
            print(f"{i:2d}. {coin['symbol']:6s} - {coin['name']:20s} - ${coin['current_price']:,.2f} - Rank #{coin['market_cap_rank']}")
        
        # Test analysis of first 5 coins (for speed)
        print("\n🔍 Testing analysis of first 5 cryptocurrencies...")
        start_time = time.time()
        
        opportunities = []
        for i, coin in enumerate(top_coins[:5]):
            print(f"Analyzing {coin['symbol']} ({i+1}/5)...")
            signal = analyzer.analyze_single_coin(coin)
            if signal:
                opportunities.append(signal)
                print(f"  ✅ Signal generated: {signal['type']}")
            else:
                print(f"  ❌ No signal")
        
        analysis_time = time.time() - start_time
        
        print(f"\n✅ Analysis complete:")
        print(f"   📊 Analyzed: 5 cryptocurrencies")
        print(f"   🎯 Opportunities found: {len(opportunities)}")
        print(f"   ⏱️  Analysis time: {analysis_time:.2f}s")
        
        if opportunities:
            print("\n📈 Sample opportunities:")
            for i, signal in enumerate(opportunities[:3], 1):
                formatted = analyzer.format_signal_for_display(signal)
                if formatted:
                    print(f"\n{i}. {formatted['symbol']} - {formatted['type']}")
                    print(f"   Potential Gain: {formatted['potential_gain']}%")
                    print(f"   Market Cap Rank: #{formatted['market_cap_rank']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_top50_analysis()
    if success:
        print("\n🎉 Top 50 analysis test completed successfully!")
    else:
        print("\n💥 Top 50 analysis test failed!") 