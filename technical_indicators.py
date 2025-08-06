"""
Technical Indicators Module
Implements various technical analysis indicators
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression

class TechnicalIndicators:
    """Class for calculating technical indicators"""
    
    def __init__(self, verbose=False):
        """Initialize technical indicators calculator"""
        self.verbose = verbose
    
    def log(self, message):
        """Log message if verbose mode is enabled"""
        if self.verbose:
            print(f"[TECH] {message}")
    
    def calculate_all_indicators(self, df):
        """
        Calculate all technical indicators for the given data
        
        Args:
            df (pandas.DataFrame): OHLCV data
            
        Returns:
            dict: Dictionary containing all calculated indicators
        """
        indicators = {}
        
        try:
            # Moving Averages
            indicators['sma_20'] = self.sma(df['close'], 20)
            indicators['sma_50'] = self.sma(df['close'], 50)
            indicators['ema_12'] = self.ema(df['close'], 12)
            indicators['ema_26'] = self.ema(df['close'], 26)
            
            # RSI
            indicators['rsi'] = self.rsi(df['close'], 14)
            
            # MACD
            macd_data = self.macd(df['close'])
            indicators.update(macd_data)
            
            # Bollinger Bands
            bb_data = self.bollinger_bands(df['close'], 20, 2)
            indicators.update(bb_data)
            
            # Volume indicators
            indicators['volume_sma'] = self.sma(df['volume'], 20)
            indicators['volume_ratio'] = df['volume'].iloc[-1] / indicators['volume_sma'].iloc[-1]
            
            # Volatility and standard deviation
            indicators['volatility'] = self.calculate_volatility(df['close'])
            indicators['std_dev'] = df['close'].rolling(20).std().iloc[-1]
            
            # Support and resistance levels
            support_resistance = self.find_support_resistance(df)
            indicators.update(support_resistance)
            
            # Linear regression for trend prediction
            indicators['linear_trend'] = self.linear_regression_trend(df['close'])
            
            # Price position relative to recent high/low
            indicators['price_position'] = self.calculate_price_position(df)
            
            self.log("Calculated all technical indicators")
            return indicators
            
        except Exception as e:
            self.log(f"Error calculating indicators: {str(e)}")
            return {}
    
    def sma(self, prices, period):
        """Calculate Simple Moving Average"""
        return prices.rolling(window=period).mean()
    
    def ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        return prices.ewm(span=period).mean()
    
    def rsi(self, prices, period=14):
        """
        Calculate Relative Strength Index
        
        Args:
            prices (pandas.Series): Price series
            period (int): RSI period
            
        Returns:
            pandas.Series: RSI values
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def macd(self, prices, fast=12, slow=26, signal=9):
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Returns:
            dict: MACD line, signal line, and histogram
        """
        ema_fast = self.ema(prices, fast)
        ema_slow = self.ema(prices, slow)
        macd_line = ema_fast - ema_slow
        signal_line = self.ema(macd_line, signal)
        histogram = macd_line - signal_line
        
        return {
            'macd_line': macd_line,
            'macd_signal': signal_line,
            'macd_histogram': histogram
        }
    
    def bollinger_bands(self, prices, period=20, std_dev=2):
        """
        Calculate Bollinger Bands
        
        Returns:
            dict: Upper band, lower band, and middle band (SMA)
        """
        sma = self.sma(prices, period)
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return {
            'bb_upper': upper_band,
            'bb_middle': sma,
            'bb_lower': lower_band
        }
    
    def calculate_volatility(self, prices, period=20):
        """
        Calculate historical volatility
        
        Returns:
            float: Annualized volatility percentage
        """
        returns = prices.pct_change().dropna()
        volatility = returns.rolling(window=period).std().iloc[-1] * np.sqrt(365) * 100
        return volatility
    
    def find_support_resistance(self, df, window=20):
        """
        Find support and resistance levels using local minima and maxima
        
        Returns:
            dict: Support and resistance levels
        """
        highs = df['high'].rolling(window=window, center=True).max()
        lows = df['low'].rolling(window=window, center=True).min()
        
        # Find recent resistance (highest high in recent period)
        resistance = df['high'].tail(50).max()
        
        # Find recent support (lowest low in recent period)
        support = df['low'].tail(50).min()
        
        return {
            'resistance': resistance,
            'support': support
        }
    
    def linear_regression_trend(self, prices, period=20):
        """
        Calculate linear regression trend
        
        Returns:
            dict: Trend slope, R-squared, and predicted next value
        """
        try:
            recent_prices = prices.tail(period).values
            x = np.arange(len(recent_prices)).reshape(-1, 1)
            y = recent_prices
            
            model = LinearRegression()
            model.fit(x, y)
            
            slope = model.coef_[0]
            r_squared = model.score(x, y)
            next_prediction = model.predict([[len(recent_prices)]])[0]
            
            return {
                'trend_slope': slope,
                'trend_r_squared': r_squared,
                'trend_prediction': next_prediction
            }
            
        except Exception as e:
            self.log(f"Error in linear regression: {str(e)}")
            return {'trend_slope': 0, 'trend_r_squared': 0, 'trend_prediction': prices.iloc[-1]}
    
    def calculate_price_position(self, df, period=20):
        """
        Calculate where current price sits relative to recent high/low range
        
        Returns:
            float: Position from 0 (at low) to 1 (at high)
        """
        recent_high = df['high'].tail(period).max()
        recent_low = df['low'].tail(period).min()
        current_price = df['close'].iloc[-1]
        
        if recent_high == recent_low:
            return 0.5
        
        position = (current_price - recent_low) / (recent_high - recent_low)
        return position
    
    def fibonacci_levels(self, high, low):
        """
        Calculate Fibonacci retracement levels
        
        Returns:
            dict: Fibonacci levels
        """
        diff = high - low
        
        levels = {
            'fib_0': high,
            'fib_236': high - 0.236 * diff,
            'fib_382': high - 0.382 * diff,
            'fib_500': high - 0.500 * diff,
            'fib_618': high - 0.618 * diff,
            'fib_786': high - 0.786 * diff,
            'fib_100': low
        }
        
        return levels
