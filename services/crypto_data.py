import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class CryptoDataService:
    """Service for fetching cryptocurrency data"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 60  # Cache for 60 seconds
    
    def get_historical_data(self, symbol, timeframe='1d', limit=100):
        """
        Fetch historical data for a cryptocurrency
        
        Args:
            symbol: Crypto symbol (e.g., 'BTC-USD')
            timeframe: Time interval (1m, 5m, 15m, 1h, 4h, 1d, 1wk, 1mo)
            limit: Number of data points to fetch
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Map timeframes to yfinance periods and intervals
            timeframe_map = {
                '1m': {'period': '1d', 'interval': '1m'},
                '5m': {'period': '5d', 'interval': '5m'},
                '15m': {'period': '5d', 'interval': '15m'},
                '1h': {'period': '1mo', 'interval': '1h'},
                '4h': {'period': '3mo', 'interval': '1h'},  # Get 1h and aggregate
                '1d': {'period': '1y', 'interval': '1d'},
                '1wk': {'period': '2y', 'interval': '1wk'},
                '1mo': {'period': '5y', 'interval': '1mo'}
            }
            
            if timeframe not in timeframe_map:
                timeframe = '1d'
            
            config = timeframe_map[timeframe]
            
            # Fetch data from yfinance
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=config['period'], interval=config['interval'])
            
            if data.empty:
                return None
            
            # For 4h timeframe, aggregate 1h data
            if timeframe == '4h':
                data = data.resample('4H').agg({
                    'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last',
                    'Volume': 'sum'
                }).dropna()
            
            # Limit to requested number of points
            if len(data) > limit:
                data = data.tail(limit)
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def calculate_technical_indicators(self, data):
        """Calculate technical indicators for the data"""
        try:
            indicators = {}
            
            # Simple Moving Averages
            indicators['sma_20'] = data['Close'].rolling(window=20).mean().iloc[-1]
            indicators['sma_50'] = data['Close'].rolling(window=50).mean().iloc[-1]
            
            # Relative Strength Index (RSI)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            indicators['rsi'] = (100 - (100 / (1 + rs))).iloc[-1]
            
            # MACD
            ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9, adjust=False).mean()
            indicators['macd'] = macd.iloc[-1]
            indicators['macd_signal'] = signal.iloc[-1]
            
            # Bollinger Bands
            sma_20 = data['Close'].rolling(window=20).mean()
            std_20 = data['Close'].rolling(window=20).std()
            indicators['bb_upper'] = (sma_20 + (std_20 * 2)).iloc[-1]
            indicators['bb_lower'] = (sma_20 - (std_20 * 2)).iloc[-1]
            
            # Convert numpy types to Python types for JSON serialization
            for key, value in indicators.items():
                if isinstance(value, (np.integer, np.floating)):
                    indicators[key] = float(value)
            
            return indicators
            
        except Exception as e:
            print(f"Error calculating indicators: {str(e)}")
            return {}
