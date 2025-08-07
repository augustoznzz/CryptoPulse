#!/usr/bin/env python3
"""
Enhanced Cryptocurrency Analyzer
Analyzes real market data for comprehensive trading signals
"""

import pandas as pd
import numpy as np
from market_data import MarketDataFetcher
from technical_indicators import TechnicalIndicators
from signal_generator import SignalGenerator
from utils import format_price
import time

class EnhancedCryptoAnalyzer:
    """Enhanced analyzer that works with real market data"""
    
    def __init__(self, verbose=False):
        """Initialize the enhanced analyzer"""
        self.verbose = verbose
        self.market_fetcher = MarketDataFetcher(verbose)
        self.technical_indicators = TechnicalIndicators(verbose)
        self.signal_generator = SignalGenerator(verbose)
        
    def log(self, message):
        """Log message if verbose mode is enabled"""
        if self.verbose:
            print(f"[ENHANCED] {message}")
    
    def analyze_single_coin(self, coin_data):
        """
        Analyze a single cryptocurrency for trading opportunities
        
        Args:
            coin_data (dict): Coin market data from MarketDataFetcher
            
        Returns:
            dict: Analysis result with signal or None if no opportunity
        """
        try:
            symbol = coin_data['symbol']
            coin_id = coin_data['id']
            current_price = coin_data['current_price']
            
            self.log(f"Analyzing {symbol} (ID: {coin_id})")
            
            # Get historical data for technical analysis
            historical_data = self.market_fetcher.get_historical_data_for_coin(coin_id, days=30)
            
            if historical_data is None or len(historical_data) < 20:
                self.log(f"Insufficient data for {symbol}")
                return None
            
            # Calculate technical indicators
            indicators = self.technical_indicators.calculate_all_indicators(historical_data)
            
            if not indicators:
                self.log(f"Failed to calculate indicators for {symbol}")
                return None
            
            # Prepare multi-timeframe data simulation from daily data
            timeframes = ['1h', '4h', '1d']
            multi_timeframe_indicators = {}
            
            # For real implementation, we simulate different timeframes
            # In production, you'd fetch actual timeframe data
            for tf in timeframes:
                # Use the same indicators but with different weights/interpretations
                tf_indicators = indicators.copy()
                
                # Adjust indicator sensitivity based on timeframe
                if tf == '1h':
                    # More sensitive for short-term
                    tf_indicators['volatility'] = tf_indicators.get('volatility', 10) * 1.2
                elif tf == '4h':
                    # Balanced sensitivity
                    tf_indicators['volatility'] = tf_indicators.get('volatility', 10) * 1.0
                else:  # 1d
                    # Less sensitive for long-term
                    tf_indicators['volatility'] = tf_indicators.get('volatility', 10) * 0.8
                
                multi_timeframe_indicators[tf] = tf_indicators
            
            # Generate trading signal
            signal = self.signal_generator.generate_signal(
                symbol=symbol,
                current_price=current_price,
                indicators=multi_timeframe_indicators,
                timeframes=timeframes
            )
            
            if signal:
                # Add market data context
                signal['coin_data'] = coin_data
                signal['momentum_score'] = coin_data.get('momentum_score', 50)
                signal['market_cap_rank'] = coin_data.get('market_cap_rank', 999)
                signal['volume_24h'] = coin_data.get('volume_24h', 0)
                
                self.log(f"Generated signal for {symbol}: {signal['type']}")
                return signal
            else:
                self.log(f"No clear signal for {symbol}")
                return None
                
        except Exception as e:
            self.log(f"Error analyzing {coin_data.get('symbol', 'Unknown')}: {str(e)}")
            return None
    
    def find_best_opportunities(self, max_coins=30, top_results=5):
        """
        Find the best trading opportunities from the top 30 cryptocurrencies by market cap
        (excluding stablecoins)
        
        Args:
            max_coins (int): Maximum number of coins to analyze (default: 30)
            top_results (int): Number of top results to return (default: 5)
            
        Returns:
            dict: Analysis results with best opportunities
        """
        try:
            self.log(f"Starting comprehensive market analysis of top {max_coins} cryptocurrencies by market cap (excluding stablecoins)")
            start_time = time.time()
            
            # Get top 30 cryptocurrencies from market
            top_coins = self.market_fetcher.get_top_cryptocurrencies(limit=max_coins)
            
            if not top_coins:
                return {'success': False, 'error': 'Failed to fetch market data'}
            
            # Filter coins based on technical criteria
            filtered_coins = self.market_fetcher.filter_by_technical_criteria(top_coins)
            
            # Limit analysis to manageable number
            coins_to_analyze = filtered_coins[:max_coins]
            
            self.log(f"Analyzing {len(coins_to_analyze)} filtered coins")
            
            # Analyze each coin
            opportunities = []
            for i, coin in enumerate(coins_to_analyze):
                self.log(f"Progress: {i+1}/{len(coins_to_analyze)} - {coin['symbol']}")
                
                signal = self.analyze_single_coin(coin)
                if signal:
                    opportunities.append(signal)
                
                # Small delay to avoid rate limiting
                time.sleep(0.1)
            
            # Sort opportunities by potential and quality
            opportunities.sort(key=lambda x: self._calculate_opportunity_score(x), reverse=True)
            
            # Take top results
            best_opportunities = opportunities[:top_results]
            
            analysis_time = time.time() - start_time
            
            self.log(f"Analysis complete: {len(best_opportunities)} opportunities found in {analysis_time:.2f}s")
            
            return {
                'success': True,
                'opportunities': best_opportunities,
                'total_analyzed': len(coins_to_analyze),
                'total_opportunities': len(opportunities),
                'analysis_time': round(analysis_time, 2),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            self.log(f"Error in market analysis: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _calculate_opportunity_score(self, signal):
        """
        Calculate a comprehensive opportunity score for ranking
        
        Args:
            signal (dict): Trading signal data
            
        Returns:
            float: Opportunity score
        """
        try:
            # Base factors
            entry_price = signal.get('entry', 1)
            tp1_price = signal.get('tp1', 1)
            
            # Calculate potential return
            if signal.get('type') == 'LONG':
                potential_return = ((tp1_price - entry_price) / entry_price) * 100
            else:
                potential_return = ((entry_price - tp1_price) / entry_price) * 100
            
            # Market factors
            momentum_score = signal.get('momentum_score', 50)
            market_cap_rank = signal.get('market_cap_rank', 999)
            volume_24h = signal.get('volume_24h', 0)
            
            # Calculate composite score
            score = (
                potential_return * 0.4 +                    # 40% potential return
                (momentum_score - 50) * 0.3 +               # 30% momentum
                max(0, (100 - market_cap_rank) / 10) * 0.2 + # 20% market cap rank
                min(10, volume_24h / 10000000) * 0.1        # 10% volume (normalized)
            )
            
            return score
            
        except Exception as e:
            self.log(f"Error calculating opportunity score: {str(e)}")
            return 0
    
    def format_signal_for_display(self, signal):
        """
        Format signal for web display
        
        Args:
            signal (dict): Trading signal
            
        Returns:
            dict: Formatted signal data
        """
        try:
            symbol = signal['symbol']
            signal_type = signal['type']
            coin_data = signal.get('coin_data', {})
            
            # Calculate potential gain
            entry = signal.get('entry', 0)
            tp1 = signal.get('tp1', 0)
            
            if entry > 0 and tp1 > 0:
                if signal_type == 'LONG':
                    potential_gain = ((tp1 - entry) / entry) * 100
                else:
                    potential_gain = ((entry - tp1) / entry) * 100
            else:
                potential_gain = 0
            
            # Format the complete signal text
            direction_emoji = "🔼" if signal_type == "LONG" else "🔽"
            
            signal_text = f"""{symbol}/USDT {direction_emoji} {signal_type}
📍 Entry: {format_price(signal.get('entry', 0))}
🎯 Take-Profit Targets:
✅ TP1: {format_price(signal.get('tp1', 0))}
✅ TP2: {format_price(signal.get('tp2', 0))}
✅ TP3: {format_price(signal.get('tp3', 0))}
✅ TP4: {format_price(signal.get('tp4', 0))}
❌ Stop-loss: {format_price(signal.get('stop_loss', 0))}
❌ Safe Stop-loss: {format_price(signal.get('safe_stop_loss', 0))}
📈 Leverage: {signal.get('leverage', 1)}x"""
            
            return {
                'symbol': symbol,
                'signal': signal_text,
                'type': signal_type,
                'potential_gain': round(potential_gain, 2),
                'entry_price': entry,
                'momentum_score': signal.get('momentum_score', 50),
                'market_cap_rank': coin_data.get('market_cap_rank', 999),
                'market_cap': coin_data.get('market_cap', 0),
                'volume_24h': coin_data.get('volume_24h', 0),
                'coin_name': coin_data.get('name', symbol)
            }
            
        except Exception as e:
            self.log(f"Error formatting signal: {str(e)}")
            return None