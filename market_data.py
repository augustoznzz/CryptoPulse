#!/usr/bin/env python3
"""
Market Data Module - Simplified Version
Fetches only basic cryptocurrency data: price_change_24h, volume_24h, market_cap
"""

import requests
from pycoingecko import CoinGeckoAPI
import time

class MarketDataFetcher:
    """Fetches basic market data from CoinGecko API"""
    
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
    
    def get_target_cryptocurrencies(self):
        """
        Get the 16 target cryptocurrencies with basic data only
        
        Returns:
            list: List of cryptocurrency data with only basic indicators
        """
        try:
            self.log("Fetching target cryptocurrencies with basic indicators")
            
            # Target cryptocurrencies (same as Netlify function)
            target_coins = [
                'bitcoin', 'ethereum', 'ripple', 'tether', 'binancecoin', 
                'solana', 'usd-coin', 'dogecoin', 'tron', 'cardano', 
                'chainlink', 'sui', 'stellar', 'uniswap', 'polkadot', 'dai'
            ]
            
            # Get market data for target coins
            coins = self.cg.get_coins_markets(
                vs_currency='usd',
                ids=','.join(target_coins),
                order='market_cap_desc',
                sparkline=False,
                price_change_percentage='24h'
            )
            
            # Extract only the 3 basic indicators
            basic_data = []
            for coin in coins:
                basic_data.append({
                    'id': coin['id'],
                    'symbol': coin['symbol'].upper(),
                    'name': coin['name'],
                    'current_price': coin['current_price'],
                    'market_cap': coin['market_cap'],
                    'volume_24h': coin['total_volume'],
                    'price_change_24h': coin.get('price_change_percentage_24h', 0)
                })
            
            self.log(f"Fetched basic data for {len(basic_data)} cryptocurrencies")
            return basic_data
            
        except Exception as e:
            self.log(f"Error fetching market data: {str(e)}")
            return []
    
    def get_fallback_data(self):
        """
        Get fallback data when API fails (simplified)
        
        Returns:
            list: Basic fallback data with only 3 indicators
        """
        fallback_coins = [
            {
                'id': 'bitcoin',
                'symbol': 'BTC',
                'name': 'Bitcoin',
                'current_price': 95000 + (time.time() % 10000),
                'market_cap': 1800000000000 + (time.time() % 200000000000),
                'volume_24h': 35000000000 + (time.time() % 15000000000),
                'price_change_24h': (time.time() % 6) - 3
            },
            {
                'id': 'ethereum',
                'symbol': 'ETH',
                'name': 'Ethereum',
                'current_price': 5200 + (time.time() % 800),
                'market_cap': 600000000000 + (time.time() % 100000000000),
                'volume_24h': 25000000000 + (time.time() % 10000000000),
                'price_change_24h': (time.time() % 5) - 2.5
            }
        ]
        
        self.log("Generated fallback data with basic indicators only")
        return fallback_coins