"""
Main Cryptocurrency Analyzer Class
Coordinates data fetching, technical analysis, and signal generation
"""

import os
from data_fetcher import DataFetcher
from technical_indicators import TechnicalIndicators
from signal_generator import SignalGenerator
from utils import format_price

class CryptoAnalyzer:
    """Main analyzer class that orchestrates the entire analysis process"""
    
    def __init__(self, symbol, exchange='binance', verbose=False, demo_mode=False):
        """
        Initialize the analyzer
        
        Args:
            symbol (str): Cryptocurrency symbol (e.g., 'BTC')
            exchange (str): Exchange name (default: 'binance')
            verbose (bool): Enable verbose logging
            demo_mode (bool): Use demo data when exchanges are unavailable
        """
        self.symbol = symbol
        self.exchange_name = exchange
        self.verbose = verbose
        self.demo_mode = demo_mode
        self.pair = f"{symbol}/USDT"
        
        # Initialize components
        self.data_fetcher = DataFetcher(exchange, verbose, demo_mode)
        self.technical_indicators = TechnicalIndicators(verbose)
        self.signal_generator = SignalGenerator(verbose)
        
    def log(self, message):
        """Log message if verbose mode is enabled"""
        if self.verbose:
            print(f"[DEBUG] {message}")
    
    def analyze(self):
        """
        Perform complete analysis and generate trading signal
        
        Returns:
            str: Formatted trading signal or None if analysis fails
        """
        try:
            self.log(f"Starting analysis for {self.pair}")
            
            # Fetch historical data for multiple timeframes
            timeframes = ['1h', '4h', '1d']  # Multiple timeframes for analysis
            all_data = {}
            
            for timeframe in timeframes:
                self.log(f"Fetching data for {timeframe} timeframe")
                data = self.data_fetcher.get_historical_data(
                    symbol=self.pair,
                    timeframe=timeframe,
                    limit=500  # Get enough data for technical analysis
                )
                
                if data is None or data.empty:
                    print(f"❌ Failed to fetch data for {timeframe} timeframe")
                    return None
                
                all_data[timeframe] = data
                self.log(f"Fetched {len(data)} candles for {timeframe}")
            
            # Get current price
            current_price = self.data_fetcher.get_current_price(self.pair)
            if current_price is None:
                print("❌ Failed to fetch current price")
                return None
            
            self.log(f"Current price: {current_price}")
            
            # Calculate technical indicators for each timeframe
            indicators = {}
            for timeframe, data in all_data.items():
                self.log(f"Calculating indicators for {timeframe}")
                indicators[timeframe] = self.technical_indicators.calculate_all_indicators(data)
            
            # Generate trading signal based on multi-timeframe analysis
            signal = self.signal_generator.generate_signal(
                symbol=self.symbol,
                current_price=current_price,
                indicators=indicators,
                timeframes=timeframes
            )
            
            if signal:
                return self._format_signal_output(signal)
            else:
                print("❌ Unable to generate trading signal")
                return None
                
        except Exception as e:
            self.log(f"Error in analysis: {str(e)}")
            raise
    
    def _format_signal_output(self, signal):
        """
        Format the signal into the required output format
        
        Args:
            signal (dict): Signal data from signal generator
            
        Returns:
            str: Formatted signal output
        """
        symbol = signal['symbol']
        signal_type = signal['type']
        direction_emoji = "🔼" if signal_type == "LONG" else "🔽"
        
        # Format prices with appropriate decimal places
        entry = format_price(signal['entry'])
        tp1 = format_price(signal['tp1'])
        tp2 = format_price(signal['tp2'])
        tp3 = format_price(signal['tp3'])
        tp4 = format_price(signal['tp4'])
        stop_loss = format_price(signal['stop_loss'])
        safe_stop_loss = format_price(signal['safe_stop_loss'])
        leverage = signal['leverage']
        
        output = f"""{symbol}/USDT {direction_emoji} {signal_type}
📍 Entry: {entry}
🎯 Take-Profit Targets:
✅ TP1: {tp1}
✅ TP2: {tp2}
✅ TP3: {tp3}
✅ TP4: {tp4}
❌ Stop-loss: {stop_loss}
❌ Safe Stop-loss: {safe_stop_loss}
📈 Leverage: {leverage}x"""
        
        return output
