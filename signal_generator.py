"""
Signal Generator Module
Generates trading signals based on technical analysis
"""

import numpy as np
from utils import calculate_fibonacci_targets

class SignalGenerator:
    """Generates trading signals based on multi-timeframe analysis"""
    
    def __init__(self, verbose=False):
        """Initialize signal generator"""
        self.verbose = verbose
    
    def log(self, message):
        """Log message if verbose mode is enabled"""
        if self.verbose:
            print(f"[SIGNAL] {message}")
    
    def generate_signal(self, symbol, current_price, indicators, timeframes):
        """
        Generate trading signal based on multi-timeframe analysis
        
        Args:
            symbol (str): Cryptocurrency symbol
            current_price (float): Current market price
            indicators (dict): Technical indicators for each timeframe
            timeframes (list): List of timeframes analyzed
            
        Returns:
            dict: Complete trading signal with entry, targets, and stops
        """
        try:
            self.log("Analyzing signals across timeframes")
            
            # Analyze each timeframe
            timeframe_signals = {}
            for tf in timeframes:
                tf_indicators = indicators[tf]
                timeframe_signals[tf] = self._analyze_timeframe(tf_indicators, current_price)
            
            # Determine overall signal direction
            signal_direction = self._determine_overall_signal(timeframe_signals)
            
            if signal_direction == 'NEUTRAL':
                self.log("No clear signal detected")
                return None
            
            # Calculate entry point
            entry_price = self._calculate_entry_point(current_price, indicators, signal_direction)
            
            # Calculate take profit targets using Fibonacci and risk-reward ratios
            take_profits = self._calculate_take_profits(
                entry_price, indicators, signal_direction
            )
            
            # Calculate stop losses
            stop_losses = self._calculate_stop_losses(
                entry_price, indicators, signal_direction
            )
            
            # Determine appropriate leverage based on volatility
            leverage = self._calculate_leverage(indicators)
            
            signal = {
                'symbol': symbol,
                'type': signal_direction,
                'entry': entry_price,
                'tp1': take_profits['tp1'],
                'tp2': take_profits['tp2'],
                'tp3': take_profits['tp3'],
                'tp4': take_profits['tp4'],
                'stop_loss': stop_losses['stop_loss'],
                'safe_stop_loss': stop_losses['safe_stop_loss'],
                'leverage': leverage,
                'confidence': self._calculate_confidence(timeframe_signals)
            }
            
            self.log(f"Generated {signal_direction} signal with {leverage}x leverage")
            return signal
            
        except Exception as e:
            self.log(f"Error generating signal: {str(e)}")
            return None
    
    def _analyze_timeframe(self, indicators, current_price):
        """
        Analyze a single timeframe for bullish/bearish signals
        
        Returns:
            dict: Timeframe analysis results
        """
        signals = []
        confidence = 0
        
        try:
            # RSI Analysis
            current_rsi = indicators['rsi'].iloc[-1]
            if current_rsi < 30:
                signals.append('LONG')  # Oversold
                confidence += 2
            elif current_rsi > 70:
                signals.append('SHORT')  # Overbought
                confidence += 2
            elif 40 <= current_rsi <= 60:
                confidence += 1  # Neutral zone
            
            # MACD Analysis
            macd_line = indicators['macd_line'].iloc[-1]
            macd_signal = indicators['macd_signal'].iloc[-1]
            macd_prev = indicators['macd_line'].iloc[-2]
            signal_prev = indicators['macd_signal'].iloc[-2]
            
            if macd_line > macd_signal and macd_prev <= signal_prev:
                signals.append('LONG')  # Bullish crossover
                confidence += 2
            elif macd_line < macd_signal and macd_prev >= signal_prev:
                signals.append('SHORT')  # Bearish crossover
                confidence += 2
            
            # Moving Average Analysis
            sma_20 = indicators['sma_20'].iloc[-1]
            sma_50 = indicators['sma_50'].iloc[-1]
            ema_12 = indicators['ema_12'].iloc[-1]
            ema_26 = indicators['ema_26'].iloc[-1]
            
            if current_price > sma_20 > sma_50 and ema_12 > ema_26:
                signals.append('LONG')  # Price above MAs and bullish alignment
                confidence += 1
            elif current_price < sma_20 < sma_50 and ema_12 < ema_26:
                signals.append('SHORT')  # Price below MAs and bearish alignment
                confidence += 1
            
            # Bollinger Bands Analysis
            bb_upper = indicators['bb_upper'].iloc[-1]
            bb_lower = indicators['bb_lower'].iloc[-1]
            bb_middle = indicators['bb_middle'].iloc[-1]
            
            if current_price <= bb_lower:
                signals.append('LONG')  # Potential bounce from lower band
                confidence += 1
            elif current_price >= bb_upper:
                signals.append('SHORT')  # Potential rejection from upper band
                confidence += 1
            
            # Volume confirmation
            volume_ratio = indicators.get('volume_ratio', 1)
            if volume_ratio > 1.5:  # High volume
                confidence += 1
            
            # Linear trend analysis
            trend_slope = indicators['linear_trend']['trend_slope']
            if trend_slope > 0:
                signals.append('LONG')
                confidence += 1
            elif trend_slope < 0:
                signals.append('SHORT')
                confidence += 1
            
            # Determine predominant signal
            long_signals = signals.count('LONG')
            short_signals = signals.count('SHORT')
            
            if long_signals > short_signals:
                direction = 'LONG'
            elif short_signals > long_signals:
                direction = 'SHORT'
            else:
                direction = 'NEUTRAL'
            
            return {
                'direction': direction,
                'confidence': confidence,
                'signals': signals,
                'rsi': current_rsi,
                'support': indicators.get('support'),
                'resistance': indicators.get('resistance')
            }
            
        except Exception as e:
            self.log(f"Error analyzing timeframe: {str(e)}")
            return {'direction': 'NEUTRAL', 'confidence': 0, 'signals': []}
    
    def _determine_overall_signal(self, timeframe_signals):
        """
        Determine overall signal direction from multiple timeframes
        """
        directions = []
        total_confidence = 0
        
        for tf, signal in timeframe_signals.items():
            if signal['direction'] != 'NEUTRAL':
                directions.append(signal['direction'])
                total_confidence += signal['confidence']
        
        if not directions:
            return 'NEUTRAL'
        
        long_count = directions.count('LONG')
        short_count = directions.count('SHORT')
        
        # Require at least 60% agreement for a signal
        if long_count / len(directions) >= 0.6:
            return 'LONG'
        elif short_count / len(directions) >= 0.6:
            return 'SHORT'
        else:
            return 'NEUTRAL'
    
    def _calculate_entry_point(self, current_price, indicators, direction):
        """
        Calculate optimal entry point based on support/resistance and current price
        """
        # Use the primary timeframe (usually 1h or 4h) for entry calculation
        primary_indicators = indicators.get('4h', indicators.get('1h', list(indicators.values())[0]))
        
        support = primary_indicators.get('support', current_price * 0.98)
        resistance = primary_indicators.get('resistance', current_price * 1.02)
        
        if direction == 'LONG':
            # For long positions, enter slightly above current price or at support
            entry = min(current_price * 1.001, (current_price + support) / 2)
        else:  # SHORT
            # For short positions, enter slightly below current price or at resistance
            entry = max(current_price * 0.999, (current_price + resistance) / 2)
        
        return entry
    
    def _calculate_take_profits(self, entry_price, indicators, direction):
        """
        Calculate take profit levels using Fibonacci ratios and risk-reward multiples
        """
        # Use primary timeframe indicators
        primary_indicators = indicators.get('4h', indicators.get('1h', list(indicators.values())[0]))
        
        volatility = primary_indicators.get('volatility', 10)  # Default 10% volatility
        std_dev = primary_indicators.get('std_dev', entry_price * 0.02)
        
        # Base distance calculation using volatility and standard deviation
        base_distance = max(std_dev, entry_price * (volatility / 100) * 0.5)
        
        if direction == 'LONG':
            # Fibonacci-based targets for long positions
            tp1 = entry_price + base_distance * 0.618  # 61.8% Fibonacci
            tp2 = entry_price + base_distance * 1.0    # 100% extension
            tp3 = entry_price + base_distance * 1.618  # 161.8% Fibonacci
            tp4 = entry_price + base_distance * 2.618  # 261.8% Fibonacci
        else:  # SHORT
            # Fibonacci-based targets for short positions
            tp1 = entry_price - base_distance * 0.618
            tp2 = entry_price - base_distance * 1.0
            tp3 = entry_price - base_distance * 1.618
            tp4 = entry_price - base_distance * 2.618
        
        return {
            'tp1': tp1,
            'tp2': tp2,
            'tp3': tp3,
            'tp4': tp4
        }
    
    def _calculate_stop_losses(self, entry_price, indicators, direction):
        """
        Calculate stop loss levels based on support/resistance and volatility
        """
        primary_indicators = indicators.get('4h', indicators.get('1h', list(indicators.values())[0]))
        
        support = primary_indicators.get('support', entry_price * 0.95)
        resistance = primary_indicators.get('resistance', entry_price * 1.05)
        volatility = primary_indicators.get('volatility', 10)
        
        # Calculate stop loss based on nearest support/resistance
        if direction == 'LONG':
            # Stop loss below support
            stop_loss = support * 0.995  # Slightly below support
            safe_stop_loss = entry_price * (1 - volatility / 200)  # More conservative
        else:  # SHORT
            # Stop loss above resistance
            stop_loss = resistance * 1.005  # Slightly above resistance
            safe_stop_loss = entry_price * (1 + volatility / 200)  # More conservative
        
        return {
            'stop_loss': stop_loss,
            'safe_stop_loss': safe_stop_loss
        }
    
    def _calculate_leverage(self, indicators):
        """
        Calculate appropriate leverage based on volatility and market conditions
        """
        # Use primary timeframe for leverage calculation
        primary_indicators = indicators.get('4h', indicators.get('1h', list(indicators.values())[0]))
        
        volatility = primary_indicators.get('volatility', 10)
        
        # Lower volatility allows higher leverage
        if volatility < 5:
            leverage = 5
        elif volatility < 10:
            leverage = 3
        elif volatility < 20:
            leverage = 2
        else:
            leverage = 1
        
        return leverage
    
    def _calculate_confidence(self, timeframe_signals):
        """
        Calculate overall confidence score for the signal
        """
        total_confidence = sum(signal['confidence'] for signal in timeframe_signals.values())
        max_possible = len(timeframe_signals) * 10  # Assuming max 10 confidence per timeframe
        
        confidence_percentage = min(100, (total_confidence / max_possible) * 100)
        return round(confidence_percentage, 1)
