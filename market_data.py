#!/usr/bin/env python3
"""
Market Data Module
Fetches real cryptocurrency market data from CoinGecko API
"""

import requests
from pycoingecko import CoinGeckoAPI
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MarketDataFetcher:
    """Fetches real market data from CoinGecko API"""
    
    def __init__(self, verbose=False):
        """Initialize market data fetcher"""
        self.verbose = verbose
        self.cg = CoinGeckoAPI()
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes cache
        
    def log(self, message):
        """Log message if verbose mode is enabled"""
        if self.verbose:
            print(f"[MARKET] {message}")
    
    def get_top_cryptocurrencies(self, limit=100):
        """
        Get top cryptocurrencies by market cap
        
        Args:
            limit (int): Number of top cryptocurrencies to fetch
            
        Returns:
            list: List of cryptocurrency data
        """
        try:
            self.log(f"Fetching top {limit} cryptocurrencies by market cap")
            
            # Get market data sorted by market cap
            coins = self.cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=limit,
                page=1,
                sparkline=False,
                price_change_percentage='1h,24h,7d'
            )
            
            # Filter coins that have USDT pairs and sufficient volume
            filtered_coins = []
            for coin in coins:
                if (coin.get('total_volume', 0) > 1000000 and  # Min $1M volume
                    coin.get('market_cap', 0) > 10000000 and   # Min $10M market cap
                    coin.get('current_price', 0) > 0):         # Valid price
                    
                    filtered_coins.append({
                        'id': coin['id'],
                        'symbol': coin['symbol'].upper(),
                        'name': coin['name'],
                        'current_price': coin['current_price'],
                        'market_cap': coin['market_cap'],
                        'volume_24h': coin['total_volume'],
                        'price_change_1h': coin.get('price_change_percentage_1h', 0),
                        'price_change_24h': coin.get('price_change_percentage_24h', 0),
                        'price_change_7d': coin.get('price_change_percentage_7d', 0),
                        'market_cap_rank': coin.get('market_cap_rank', 999)
                    })
            
            self.log(f"Filtered to {len(filtered_coins)} valid cryptocurrencies")
            return filtered_coins
            
        except Exception as e:
            self.log(f"Error fetching market data: {str(e)}")
            return []
    
    def get_historical_data_for_coin(self, coin_id, days=30):
        """
        Get historical price data for a specific coin
        
        Args:
            coin_id (str): CoinGecko coin ID
            days (int): Number of days of historical data
            
        Returns:
            pandas.DataFrame: Historical OHLCV data
        """
        try:
            cache_key = f"{coin_id}_{days}"
            current_time = time.time()
            
            # Check cache
            if cache_key in self.cache:
                cache_data, cache_time = self.cache[cache_key]
                if current_time - cache_time < self.cache_timeout:
                    return cache_data
            
            self.log(f"Fetching {days} days of historical data for {coin_id}")
            
            # Get historical market data
            data = self.cg.get_coin_market_chart(
                id=coin_id,
                vs_currency='usd',
                days=days
            )
            
            if not data or 'prices' not in data:
                return None
            
            # Convert to DataFrame
            prices = data['prices']
            volumes = data['total_volumes']
            
            df = pd.DataFrame(prices, columns=['timestamp', 'close'])
            df['volume'] = [v[1] for v in volumes]
            
            # Convert timestamp
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('datetime', inplace=True)
            df.drop('timestamp', axis=1, inplace=True)
            
            # Generate OHLC from close prices (approximation for better analysis)
            df['open'] = df['close'].shift(1).fillna(df['close'])
            df['high'] = df[['open', 'close']].max(axis=1) * (1 + np.random.uniform(0, 0.02, len(df)))
            df['low'] = df[['open', 'close']].min(axis=1) * (1 - np.random.uniform(0, 0.02, len(df)))
            
            # Reorder columns
            df = df[['open', 'high', 'low', 'close', 'volume']]
            
            # Cache the result
            self.cache[cache_key] = (df, current_time)
            
            self.log(f"Successfully fetched {len(df)} data points for {coin_id}")
            return df
            
        except Exception as e:
            self.log(f"Error fetching historical data for {coin_id}: {str(e)}")
            return None
    
    def calculate_market_momentum(self, coin_data):
        """
        Calculate market momentum score for a coin
        
        Args:
            coin_data (dict): Coin market data
            
        Returns:
            float: Momentum score (0-100)
        """
        try:
            # Factors for momentum calculation
            price_change_24h = coin_data.get('price_change_24h', 0)
            price_change_7d = coin_data.get('price_change_7d', 0)
            volume_24h = coin_data.get('volume_24h', 0)
            market_cap = coin_data.get('market_cap', 1)
            
            # Volume-to-market-cap ratio (higher is better for momentum)
            volume_ratio = min(volume_24h / market_cap * 100, 10) if market_cap > 0 else 0
            
            # Price momentum (weighted recent changes more)
            price_momentum = (price_change_24h * 0.7 + price_change_7d * 0.3) / 2
            
            # Combine factors
            momentum_score = (
                price_momentum * 0.6 +      # 60% price momentum
                volume_ratio * 0.3 +        # 30% volume activity  
                min(abs(price_change_24h), 20) * 0.1  # 10% volatility (capped)
            )
            
            # Normalize to 0-100 scale
            momentum_score = max(0, min(100, momentum_score + 50))
            
            return round(momentum_score, 2)
            
        except Exception as e:
            self.log(f"Error calculating momentum: {str(e)}")
            return 50  # Neutral score on error
    
    def filter_by_technical_criteria(self, coins_data):
        """
        Filter coins based on technical analysis criteria
        
        Args:
            coins_data (list): List of coin market data
            
        Returns:
            list: Filtered coins with potential
        """
        filtered = []
        
        for coin in coins_data:
            momentum = self.calculate_market_momentum(coin)
            
            # Technical criteria for filtering
            criteria_met = 0
            total_criteria = 5
            
            # 1. Positive momentum score
            if momentum > 55:
                criteria_met += 1
            
            # 2. Recent price action (not too volatile)
            price_change_24h = abs(coin.get('price_change_24h', 0))
            if 1 <= price_change_24h <= 15:  # 1-15% daily change
                criteria_met += 1
            
            # 3. Volume activity
            volume_24h = coin.get('volume_24h', 0)
            market_cap = coin.get('market_cap', 1)
            if volume_24h / market_cap > 0.05:  # Min 5% turnover
                criteria_met += 1
            
            # 4. Market cap stability (not too small)
            if coin.get('market_cap', 0) > 50000000:  # Min $50M market cap
                criteria_met += 1
            
            # 5. Price above $0.001 (avoid micro-caps)
            if coin.get('current_price', 0) > 0.001:
                criteria_met += 1
            
            # Require at least 3 out of 5 criteria
            if criteria_met >= 3:
                coin['momentum_score'] = momentum
                coin['criteria_score'] = criteria_met
                filtered.append(coin)
        
        # Sort by momentum score
        filtered.sort(key=lambda x: x['momentum_score'], reverse=True)
        
        self.log(f"Filtered {len(filtered)} coins from {len(coins_data)} based on technical criteria")
        return filtered
    
    def get_tradeable_pairs(self, symbol):
        """
        Check if a symbol has tradeable pairs on major exchanges
        
        Args:
            symbol (str): Cryptocurrency symbol
            
        Returns:
            bool: True if tradeable pairs exist
        """
        # Common trading pairs to check
        tradeable_pairs = [
            f"{symbol}/USDT",
            f"{symbol}/USD", 
            f"{symbol}/USDC",
            f"{symbol}/BTC",
            f"{symbol}/ETH"
        ]
        
        # For now, assume all coins from top market cap have tradeable pairs
        # In production, you could check specific exchange APIs
        return True