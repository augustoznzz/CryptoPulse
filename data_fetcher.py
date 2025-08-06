"""
Data Fetcher Module
Handles cryptocurrency data retrieval using CCXT
"""

import ccxt
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

class DataFetcher:
    """Handles data fetching from cryptocurrency exchanges"""
    
    def __init__(self, exchange_name='binance', verbose=False, demo_mode=False):
        """
        Initialize data fetcher
        
        Args:
            exchange_name (str): Name of the exchange
            verbose (bool): Enable verbose logging
            demo_mode (bool): Use demo data when exchanges are unavailable
        """
        self.exchange_name = exchange_name
        self.verbose = verbose
        self.demo_mode = demo_mode
        self.exchange = None
        
        if not demo_mode:
            try:
                self.exchange = self._initialize_exchange()
            except Exception as e:
                self.log(f"Failed to initialize any exchange: {str(e)}")
                self.log("Falling back to demo mode")
                self.demo_mode = True
    
    def log(self, message):
        """Log message if verbose mode is enabled"""
        if self.verbose:
            print(f"[DATA] {message}")
    
    def _initialize_exchange(self):
        """Initialize CCXT exchange object with fallback mechanism"""
        exchanges_to_try = [
            ('coinbase', lambda: ccxt.coinbase({
                'rateLimit': 1000,
                'enableRateLimit': True,
                'sandbox': False,
            })),
            ('kraken', lambda: ccxt.kraken({
                'rateLimit': 3000,
                'enableRateLimit': True,
            })),
            ('binance', lambda: ccxt.binance({
                'rateLimit': 1200,
                'enableRateLimit': True,
            })),
            ('bitfinex', lambda: ccxt.bitfinex({
                'rateLimit': 1500,
                'enableRateLimit': True,
            }))
        ]
        
        # If user specified an exchange, try it first
        if self.exchange_name.lower() != 'binance':
            for name, factory in exchanges_to_try:
                if name == self.exchange_name.lower():
                    exchanges_to_try.insert(0, (name, factory))
                    break
        
        last_error = None
        for exchange_name, exchange_factory in exchanges_to_try:
            try:
                self.log(f"Trying to initialize {exchange_name} exchange")
                exchange = exchange_factory()
                
                # Test the exchange with a simple call
                exchange.load_markets()
                self.log(f"Successfully initialized {exchange.name} exchange")
                return exchange
                
            except Exception as e:
                last_error = e
                self.log(f"Failed to initialize {exchange_name}: {str(e)}")
                continue
        
        # If all exchanges failed, raise the last error
        raise Exception(f"All exchanges failed. Last error: {str(last_error)}")
    
    def get_historical_data(self, symbol, timeframe='1h', limit=500):
        """
        Fetch historical OHLCV data
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT')
            timeframe (str): Timeframe for candles (e.g., '1h', '4h', '1d')
            limit (int): Number of candles to fetch
            
        Returns:
            pandas.DataFrame: OHLCV data with datetime index
        """
        if self.demo_mode:
            return self._generate_demo_data(symbol, timeframe, limit)
        
        try:
            if self.exchange is None:
                return None
                
            self.log(f"Fetching {limit} candles for {symbol} on {timeframe}")
            
            # Convert timeframe for Coinbase compatibility
            timeframe_map = {
                '1h': '3600',
                '4h': '14400', 
                '1d': '86400'
            }
            
            # Use mapped timeframe for Coinbase, original for others
            if 'coinbase' in self.exchange.name.lower():
                tf = timeframe_map.get(timeframe, timeframe)
            else:
                tf = timeframe
            
            # Fetch OHLCV data
            ohlcv = self.exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=tf,
                limit=limit
            )
            
            if not ohlcv:
                self.log("No data received from exchange")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv)
            df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            
            # Convert timestamp to datetime
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('datetime', inplace=True)
            
            # Remove timestamp column as we have datetime index
            df.drop('timestamp', axis=1, inplace=True)
            
            self.log(f"Successfully fetched {len(df)} candles")
            return df
            
        except Exception as e:
            self.log(f"Error fetching historical data: {str(e)}")
            return None
    
    def get_current_price(self, symbol):
        """
        Get current price for a symbol
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT')
            
        Returns:
            float: Current price or None if error
        """
        if self.demo_mode:
            return self._get_demo_price(symbol)
        
        try:
            if self.exchange is None:
                return None
                
            ticker = self.exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            self.log(f"Current price for {symbol}: {current_price}")
            return current_price
            
        except Exception as e:
            self.log(f"Error fetching current price: {str(e)}")
            return None
    
    def get_24h_stats(self, symbol):
        """
        Get 24-hour statistics for a symbol
        
        Args:
            symbol (str): Trading pair symbol
            
        Returns:
            dict: 24h statistics or None if error
        """
        try:
            if self.exchange is None:
                return None
                
            ticker = self.exchange.fetch_ticker(symbol)
            stats = {
                'price_change_24h': ticker['change'],
                'price_change_percent_24h': ticker['percentage'],
                'high_24h': ticker['high'],
                'low_24h': ticker['low'],
                'volume_24h': ticker['baseVolume']
            }
            return stats
            
        except Exception as e:
            self.log(f"Error fetching 24h stats: {str(e)}")
            return None
    
    def _generate_demo_data(self, symbol, timeframe='1h', limit=500):
        """
        Generate realistic demo data for testing purposes
        
        Args:
            symbol (str): Trading pair symbol
            timeframe (str): Timeframe for candles
            limit (int): Number of candles to generate
            
        Returns:
            pandas.DataFrame: Generated OHLCV data
        """
        self.log(f"Generating demo data for {symbol} on {timeframe}")
        
        # Base prices for different cryptocurrencies
        base_prices = {
            'BTC/USDT': 65000,
            'ETH/USDT': 3500,
            'ADA/USDT': 0.45,
            'XRP/USDT': 0.60,
            'DOT/USDT': 7.5,
            'LINK/USDT': 18.0,
            'SOL/USDT': 180.0
        }
        
        base_price = base_prices.get(symbol, 100.0)
        
        # Determine timeframe in minutes
        timeframe_minutes = {
            '1h': 60,
            '4h': 240,
            '1d': 1440
        }
        minutes = timeframe_minutes.get(timeframe, 60)
        
        # Generate timestamps
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=minutes * limit)
        timestamps = pd.date_range(start=start_time, end=end_time, periods=limit)
        
        # Generate realistic price movement using random walk
        np.random.seed(42)  # For reproducible results
        
        # Generate returns based on volatility
        daily_volatility = 0.02  # 2% daily volatility
        period_volatility = daily_volatility * np.sqrt(minutes / 1440)  # Adjust for timeframe
        
        returns = np.random.normal(0, period_volatility, limit)
        
        # Add some trend and mean reversion
        trend = np.linspace(-0.001, 0.001, limit)  # Slight upward trend
        returns += trend
        
        # Calculate prices using cumulative product
        price_multipliers = np.cumprod(1 + returns)
        prices = base_price * price_multipliers
        
        # Generate OHLCV data
        data = []
        for i, (timestamp, close) in enumerate(zip(timestamps, prices)):
            # Generate realistic high/low/open based on close
            volatility_factor = np.random.uniform(0.5, 1.5)
            high_low_spread = close * period_volatility * volatility_factor
            
            open_price = prices[i-1] if i > 0 else close
            high = close + np.random.uniform(0, high_low_spread)
            low = close - np.random.uniform(0, high_low_spread)
            
            # Ensure OHLC logic is maintained
            high = max(high, open_price, close)
            low = min(low, open_price, close)
            
            # Generate volume (higher volume during price movements)
            price_change = abs(close - open_price) / open_price
            base_volume = base_price * 1000  # Base volume proportional to price
            volume = base_volume * (1 + price_change * 10) * np.random.uniform(0.5, 2.0)
            
            data.append({
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
        
        df = pd.DataFrame(data, index=timestamps)
        self.log(f"Generated {len(df)} demo candles")
        return df
    
    def _get_demo_price(self, symbol):
        """
        Get demo current price for a symbol
        
        Args:
            symbol (str): Trading pair symbol
            
        Returns:
            float: Demo current price
        """
        base_prices = {
            'BTC/USDT': 65432.50,
            'ETH/USDT': 3567.89,
            'ADA/USDT': 0.4523,
            'XRP/USDT': 0.6012,
            'DOT/USDT': 7.45,
            'LINK/USDT': 18.23,
            'SOL/USDT': 183.45
        }
        
        price = base_prices.get(symbol, 100.0)
        self.log(f"Demo current price for {symbol}: {price}")
        return price
