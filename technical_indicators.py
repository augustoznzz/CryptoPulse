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
            
            # Volume trend analysis
            volume_trend = self.calculate_volume_trend(df['volume'])
            indicators.update(volume_trend)
            
            # Volatility and standard deviation
            indicators['volatility'] = self.calculate_volatility(df['close'])
            indicators['std_dev'] = df['close'].rolling(20).std().iloc[-1]
            
            # Support and resistance levels
            support_resistance = self.find_support_resistance(df)
            indicators.update(support_resistance)
            
            # Fibonacci retracement analysis
            fibonacci_analysis = self.fibonacci_retracement(df)
            indicators.update(fibonacci_analysis)
            
            # Linear regression for trend prediction
            indicators['linear_trend'] = self.linear_regression_trend(df['close'])

            # Price position relative to recent high/low
            indicators['price_position'] = self.calculate_price_position(df)

            # Stochastic Oscillator
            stoch = self.stochastic_oscillator(df['high'], df['low'], df['close'])
            indicators.update(stoch)

            # Ichimoku Cloud
            ichimoku = self.ichimoku_cloud(df['high'], df['low'], df['close'])
            indicators.update(ichimoku)

            # VWAP
            indicators['vwap'] = self.vwap(df)

            # On-Balance Volume
            indicators['obv'] = self.on_balance_volume(df['close'], df['volume'])

            # Parabolic SAR
            indicators['parabolic_sar'] = self.parabolic_sar(df['high'], df['low'])

            # Average Directional Index
            adx_data = self.adx(df['high'], df['low'], df['close'])
            indicators.update(adx_data)

            # Chaikin Oscillator
            indicators['chaikin_oscillator'] = self.chaikin_oscillator(df['high'], df['low'], df['close'], df['volume'])

            # Williams %R
            indicators['williams_r'] = self.williams_r(df['high'], df['low'], df['close'])
            
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
    
    def calculate_volume_trend(self, volume, period=20):
        """
        Calculate volume trend indicators
        
        Args:
            volume (pandas.Series): Volume data
            period (int): Period for trend calculation
            
        Returns:
            dict: Volume trend indicators
        """
        try:
            # Volume moving averages
            volume_sma_short = self.sma(volume, period//2)
            volume_sma_long = self.sma(volume, period)
            
            # Volume trend direction
            volume_trend_direction = 1 if volume_sma_short.iloc[-1] > volume_sma_long.iloc[-1] else -1
            
            # Volume momentum (rate of change)
            volume_momentum = (volume.iloc[-1] - volume.iloc[-period]) / volume.iloc[-period] * 100
            
            # Volume strength (current volume vs average)
            volume_strength = volume.iloc[-1] / volume_sma_long.iloc[-1]
            
            # Volume consistency (standard deviation)
            volume_consistency = volume.rolling(period).std().iloc[-1] / volume_sma_long.iloc[-1]
            
            return {
                'volume_trend_direction': volume_trend_direction,
                'volume_momentum': volume_momentum,
                'volume_strength': volume_strength,
                'volume_consistency': volume_consistency,
                'volume_sma_short': volume_sma_short.iloc[-1],
                'volume_sma_long': volume_sma_long.iloc[-1]
            }
            
        except Exception as e:
            self.log(f"Error calculating volume trend: {str(e)}")
            return {
                'volume_trend_direction': 0,
                'volume_momentum': 0,
                'volume_strength': 1,
                'volume_consistency': 0,
                'volume_sma_short': 0,
                'volume_sma_long': 0
            }
    
    def fibonacci_retracement(self, df, period=50):
        """
        Calculate Fibonacci retracement levels based on recent high/low
        
        Args:
            df (pandas.DataFrame): OHLCV data
            period (int): Period to look back for high/low
            
        Returns:
            dict: Fibonacci retracement levels and analysis
        """
        try:
            # Get recent high and low
            recent_high = df['high'].rolling(period).max().iloc[-1]
            recent_low = df['low'].rolling(period).min().iloc[-1]
            current_price = df['close'].iloc[-1]
            
            # Calculate Fibonacci levels
            fib_levels = self.fibonacci_levels(recent_high, recent_low)
            
            # Determine which Fibonacci level current price is near
            price_position = None
            nearest_level = None
            distance_to_level = float('inf')
            
            for level_name, level_value in fib_levels.items():
                distance = abs(current_price - level_value)
                if distance < distance_to_level:
                    distance_to_level = distance
                    nearest_level = level_name
                    price_position = level_value
            
            # Calculate retracement percentage
            total_range = recent_high - recent_low
            if total_range > 0:
                retracement_pct = ((recent_high - current_price) / total_range) * 100
            else:
                retracement_pct = 0
            
            return {
                'fib_levels': fib_levels,
                'nearest_level': nearest_level,
                'price_position': price_position,
                'retracement_pct': retracement_pct,
                'recent_high': recent_high,
                'recent_low': recent_low,
                'current_price': current_price,
                'total_range': total_range
            }
            
        except Exception as e:
            self.log(f"Error calculating Fibonacci retracement: {str(e)}")
            return {
                'fib_levels': {},
                'nearest_level': None,
                'price_position': None,
                'retracement_pct': 0,
                'recent_high': 0,
                'recent_low': 0,
                'current_price': 0,
                'total_range': 0
            }

    def stochastic_oscillator(self, high, low, close, k_period=14, d_period=3):
        """Calculate Stochastic Oscillator (%K and %D)"""
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        percent_k = 100 * (close - lowest_low) / (highest_high - lowest_low)
        percent_d = percent_k.rolling(window=d_period).mean()
        return {'stoch_k': percent_k, 'stoch_d': percent_d}

    def ichimoku_cloud(self, high, low, close):
        """Calculate Ichimoku Cloud components"""
        conversion_line = (high.rolling(9).max() + low.rolling(9).min()) / 2
        base_line = (high.rolling(26).max() + low.rolling(26).min()) / 2
        leading_span_a = ((conversion_line + base_line) / 2).shift(26)
        leading_span_b = ((high.rolling(52).max() + low.rolling(52).min()) / 2).shift(26)
        lagging_span = close.shift(-26)
        return {
            'ichimoku_tenkan': conversion_line,
            'ichimoku_kijun': base_line,
            'ichimoku_span_a': leading_span_a,
            'ichimoku_span_b': leading_span_b,
            'ichimoku_chikou': lagging_span
        }

    def vwap(self, df):
        """Calculate Volume Weighted Average Price"""
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        vwap = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()
        return vwap

    def on_balance_volume(self, close, volume):
        """Calculate On-Balance Volume"""
        obv = [0]
        for i in range(1, len(close)):
            if close.iloc[i] > close.iloc[i - 1]:
                obv.append(obv[-1] + volume.iloc[i])
            elif close.iloc[i] < close.iloc[i - 1]:
                obv.append(obv[-1] - volume.iloc[i])
            else:
                obv.append(obv[-1])
        return pd.Series(obv, index=close.index)

    def parabolic_sar(self, high, low, step=0.02, max_step=0.2):
        """Calculate Parabolic SAR"""
        sar = pd.Series(index=high.index, dtype='float64')
        trend_up = True
        af = step
        ep = low.iloc[0]
        sar.iloc[0] = low.iloc[0]

        for i in range(1, len(high)):
            prev_sar = sar.iloc[i - 1]
            if trend_up:
                sar.iloc[i] = prev_sar + af * (ep - prev_sar)
                sar.iloc[i] = min(sar.iloc[i], low.iloc[i - 1], low.iloc[i])
                if high.iloc[i] > ep:
                    ep = high.iloc[i]
                    af = min(af + step, max_step)
                if low.iloc[i] < sar.iloc[i]:
                    trend_up = False
                    sar.iloc[i] = ep
                    ep = low.iloc[i]
                    af = step
            else:
                sar.iloc[i] = prev_sar + af * (ep - prev_sar)
                sar.iloc[i] = max(sar.iloc[i], high.iloc[i - 1], high.iloc[i])
                if low.iloc[i] < ep:
                    ep = low.iloc[i]
                    af = min(af + step, max_step)
                if high.iloc[i] > sar.iloc[i]:
                    trend_up = True
                    sar.iloc[i] = ep
                    ep = high.iloc[i]
                    af = step
        return sar

    def adx(self, high, low, close, period=14):
        """Calculate Average Directional Index"""
        plus_dm = high.diff()
        minus_dm = low.diff() * -1
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        plus_dm[plus_dm < minus_dm] = 0
        minus_dm[minus_dm <= plus_dm] = 0

        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        atr = tr.rolling(window=period).mean()
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        adx = dx.rolling(window=period).mean()
        return {'plus_di': plus_di, 'minus_di': minus_di, 'adx': adx}

    def chaikin_oscillator(self, high, low, close, volume, short=3, long=10):
        """Calculate Chaikin Oscillator"""
        mfm = ((close - low) - (high - close)) / (high - low)
        mfm = mfm.replace([np.inf, -np.inf], 0).fillna(0)
        mfv = mfm * volume
        adl = mfv.cumsum()
        ema_short = adl.ewm(span=short).mean()
        ema_long = adl.ewm(span=long).mean()
        return ema_short - ema_long

    def williams_r(self, high, low, close, period=14):
        """Calculate Williams %R"""
        highest_high = high.rolling(window=period).max()
        lowest_low = low.rolling(window=period).min()
        wr = -100 * (highest_high - close) / (highest_high - lowest_low)
        return wr
