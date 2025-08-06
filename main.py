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
        description='Advanced Cryptocurrency Market Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --moeda BTC
  python main.py --moeda ETH
  python main.py --moeda ADA
        """
    )
    
    parser.add_argument(
        '--moeda',
        type=str,
        required=True,
        help='Cryptocurrency symbol to analyze (e.g., BTC, ETH, ADA)'
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
        # Initialize the analyzer
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
