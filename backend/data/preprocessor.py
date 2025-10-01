"""
Data preprocessing for ML models
"""
import numpy as np
import pandas as pd
from typing import Tuple, List
from sklearn.preprocessing import MinMaxScaler


class DataPreprocessor:
    """Preprocess crypto data for ML models"""
    
    def __init__(self):
        self.scaler = MinMaxScaler()
        
    def prepare_time_series_data(self, data: List[dict], sequence_length: int = 60) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare time series data for LSTM model
        
        Args:
            data: List of price data dictionaries
            sequence_length: Number of time steps to use for prediction
            
        Returns:
            X: Input sequences
            y: Target values
        """
        if not data or len(data) < sequence_length + 1:
            return np.array([]), np.array([])
        
        # Extract prices
        prices = [d.get('price', d.get('close', 0)) for d in data]
        prices = np.array(prices).reshape(-1, 1)
        
        # Normalize data
        scaled_data = self.scaler.fit_transform(prices)
        
        # Create sequences
        X, y = [], []
        for i in range(sequence_length, len(scaled_data)):
            X.append(scaled_data[i-sequence_length:i, 0])
            y.append(scaled_data[i, 0])
        
        return np.array(X), np.array(y)
    
    def calculate_technical_indicators(self, data: List[dict]) -> pd.DataFrame:
        """Calculate technical indicators from price data"""
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Ensure we have price data
        if 'close' not in df.columns and 'price' in df.columns:
            df['close'] = df['price']
        
        if 'close' not in df.columns:
            return df
        
        # Moving Averages
        df['MA_7'] = df['close'].rolling(window=7).mean()
        df['MA_25'] = df['close'].rolling(window=25).mean()
        df['MA_50'] = df['close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
        df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
        
        # Volatility
        df['Volatility'] = df['close'].pct_change().rolling(window=20).std()
        
        return df
    
    def prepare_features_for_ml(self, data: List[dict]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for traditional ML models"""
        df = self.calculate_technical_indicators(data)
        
        if df.empty or len(df) < 2:
            return np.array([]), np.array([])
        
        # Features to use
        feature_columns = ['close', 'MA_7', 'MA_25', 'RSI', 'MACD', 'Volatility']
        feature_columns = [col for col in feature_columns if col in df.columns]
        
        # Drop NaN values
        df = df.dropna()
        
        if len(df) < 2:
            return np.array([]), np.array([])
        
        # Prepare X (features) and y (target - next price)
        X = df[feature_columns].iloc[:-1].values
        y = df['close'].iloc[1:].values
        
        # Normalize features
        X = self.scaler.fit_transform(X)
        
        return X, y
    
    def inverse_transform_predictions(self, predictions: np.ndarray) -> np.ndarray:
        """Convert scaled predictions back to original scale"""
        if len(predictions.shape) == 1:
            predictions = predictions.reshape(-1, 1)
        return self.scaler.inverse_transform(predictions).flatten()
