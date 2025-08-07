#!/usr/bin/env python3
"""
Cryptocurrency Market Analysis Tool
Main entry point for the application
"""

import argparse
import sys
from crypto_analyzer import CryptoAnalyzer

def main():
    """Main function to run the cryptocurrency analysis tool"""
    parser = argparse.ArgumentParser(
        description='Advanced Cryptocurrency Market Analysis Tool - Analyze single coins or top 30 by market cap',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --moeda BTC          # Analyze single cryptocurrency
  python main.py --moeda ETH
  python main.py --moeda ADA
  python main.py --top30              # Analyze top 30 cryptocurrencies by market cap
        """
    )
    
    parser.add_argument(
        '--moeda',
        type=str,
        help='Cryptocurrency symbol to analyze (e.g., BTC, ETH, ADA)'
    )
    
    parser.add_argument(
        '--top30',
        action='store_true',
        help='Analyze the top 30 cryptocurrencies by market cap'
    )
    
    parser.add_argument(
        '--exchange',
        type=str,
        default='binance',
        help='Exchange to fetch data from (default: binance)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run in demo mode with simulated data (for testing when exchanges are unavailable)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.top30:
            # Use enhanced analyzer for top 30 cryptocurrencies
            from enhanced_analyzer import EnhancedCryptoAnalyzer
            
            print("🔍 Analyzing top 30 cryptocurrencies by market cap...")
            enhanced_analyzer = EnhancedCryptoAnalyzer(verbose=args.verbose)
            
            result = enhanced_analyzer.find_best_opportunities(max_coins=30, top_results=5)
            
            if result.get('success'):
                opportunities = result.get('opportunities', [])
                print(f"\n✅ Analysis complete: {len(opportunities)} opportunities found")
                print(f"📊 Analyzed {result.get('total_analyzed', 0)} cryptocurrencies")
                print(f"⏱️  Analysis time: {result.get('analysis_time', 0)}s")
                print(f"🕐 Timestamp: {result.get('timestamp', 'N/A')}")
                print("\n" + "="*80)
                
                for i, signal in enumerate(opportunities, 1):
                    formatted_signal = enhanced_analyzer.format_signal_for_display(signal)
                    if formatted_signal:
                        print(f"\n{i}. {formatted_signal['signal']}")
                        print(f"   📈 Potential Gain: {formatted_signal['potential_gain']}%")
                        print(f"   🏆 Market Cap Rank: #{formatted_signal['market_cap_rank']}")
                        print(f"   💰 Market Cap: ${formatted_signal['market_cap']:,.0f}")
                        print(f"   📊 Momentum Score: {formatted_signal['momentum_score']}")
                        print("-" * 60)
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                sys.exit(1)
                
        elif args.moeda:
            # Initialize the analyzer for single cryptocurrency
            analyzer = CryptoAnalyzer(
                symbol=args.moeda.upper(),
                exchange=args.exchange,
                verbose=args.verbose,
                demo_mode=args.demo
            )
            
            # Run the analysis
            result = analyzer.analyze()
            
            if result:
                print(result)
            else:
                print("❌ Analysis failed. Please check your inputs and try again.")
                sys.exit(1)
        else:
            print("❌ Please specify either --moeda <SYMBOL> or --top50")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ Analysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
