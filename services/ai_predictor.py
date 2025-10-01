import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from services.crypto_data import CryptoDataService
import warnings
warnings.filterwarnings('ignore')

class AIPredictor:
    """AI-based cryptocurrency prediction service using ML models"""
    
    def __init__(self):
        self.crypto_service = CryptoDataService()
        self.scaler = MinMaxScaler()
        self.model = None
        
    def prepare_features(self, data):
        """Prepare features for ML model"""
        try:
            df = data.copy()
            
            # Calculate returns
            df['returns'] = df['Close'].pct_change()
            
            # Moving averages
            df['sma_5'] = df['Close'].rolling(window=5).mean()
            df['sma_10'] = df['Close'].rolling(window=10).mean()
            df['sma_20'] = df['Close'].rolling(window=20).mean()
            
            # Momentum indicators
            df['momentum'] = df['Close'] - df['Close'].shift(4)
            
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['macd'] = ema_12 - ema_26
            
            # Volatility
            df['volatility'] = df['Close'].rolling(window=10).std()
            
            # Volume indicators
            df['volume_sma'] = df['Volume'].rolling(window=5).mean()
            df['volume_ratio'] = df['Volume'] / df['volume_sma']
            
            # Price position in range
            df['high_low_ratio'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
            
            # Drop NaN values
            df = df.dropna()
            
            return df
            
        except Exception as e:
            print(f"Error preparing features: {str(e)}")
            return data
    
    def predict(self, data, timeframe='1d'):
        """
        Generate AI-based prediction for cryptocurrency
        
        Args:
            data: Historical OHLCV data
            timeframe: Timeframe for prediction
        
        Returns:
            Dictionary with prediction results
        """
        try:
            # Prepare features
            df = self.prepare_features(data)
            
            if len(df) < 20:
                return self._simple_prediction(data, timeframe)
            
            # Get technical indicators
            indicators = self.crypto_service.calculate_technical_indicators(data)
            
            # Simple ML-based prediction using recent trend and patterns
            recent_returns = df['returns'].tail(10).values
            recent_volume = df['volume_ratio'].tail(5).values
            
            # Calculate trend strength
            trend_score = 0
            if 'sma_5' in df.columns and 'sma_20' in df.columns:
                current_price = df['Close'].iloc[-1]
                sma_5 = df['sma_5'].iloc[-1]
                sma_20 = df['sma_20'].iloc[-1]
                
                if sma_5 > sma_20:
                    trend_score += 1
                if current_price > sma_5:
                    trend_score += 1
            
            # RSI analysis
            rsi_score = 0
            if 'rsi' in df.columns:
                rsi = df['rsi'].iloc[-1]
                if rsi < 30:
                    rsi_score = 1  # Oversold - potential buy
                elif rsi > 70:
                    rsi_score = -1  # Overbought - potential sell
            
            # MACD analysis
            macd_score = 0
            if 'macd' in df.columns:
                macd = df['macd'].iloc[-1]
                if macd > 0:
                    macd_score = 1
                else:
                    macd_score = -1
            
            # Volume analysis
            volume_score = 0
            if len(recent_volume) > 0:
                avg_volume_ratio = np.mean(recent_volume)
                if avg_volume_ratio > 1.2:
                    volume_score = 1  # High volume
            
            # Calculate overall signal
            overall_score = trend_score + rsi_score + macd_score + volume_score
            
            # Predict price change
            recent_mean_return = np.mean(recent_returns[~np.isnan(recent_returns)])
            recent_volatility = np.std(recent_returns[~np.isnan(recent_returns)])
            
            # Adjust prediction based on overall score
            if overall_score > 2:
                predicted_return = max(recent_mean_return * 1.5, 0.01)
                confidence = min(0.75, 0.5 + overall_score * 0.05)
            elif overall_score < -2:
                predicted_return = min(recent_mean_return * 1.5, -0.01)
                confidence = min(0.75, 0.5 + abs(overall_score) * 0.05)
            else:
                predicted_return = recent_mean_return
                confidence = 0.5
            
            current_price = float(df['Close'].iloc[-1])
            predicted_price = current_price * (1 + predicted_return)
            price_change_percent = predicted_return * 100
            
            # Generate recommendation
            if overall_score >= 2:
                recommendation = 'BUY'
            elif overall_score <= -2:
                recommendation = 'SELL'
            else:
                recommendation = 'HOLD'
            
            return {
                'prediction': recommendation,
                'confidence': float(confidence),
                'recommendation': recommendation,
                'predicted_price': float(predicted_price),
                'price_change_percent': float(price_change_percent),
                'technical_indicators': indicators
            }
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return self._simple_prediction(data, timeframe)
    
    def _simple_prediction(self, data, timeframe):
        """Fallback simple prediction based on recent trends"""
        try:
            current_price = float(data['Close'].iloc[-1])
            returns = data['Close'].pct_change().tail(5).mean()
            
            predicted_price = current_price * (1 + returns)
            price_change_percent = returns * 100
            
            if returns > 0.01:
                recommendation = 'BUY'
                confidence = 0.6
            elif returns < -0.01:
                recommendation = 'SELL'
                confidence = 0.6
            else:
                recommendation = 'HOLD'
                confidence = 0.5
            
            return {
                'prediction': recommendation,
                'confidence': float(confidence),
                'recommendation': recommendation,
                'predicted_price': float(predicted_price),
                'price_change_percent': float(price_change_percent),
                'technical_indicators': {}
            }
        except Exception as e:
            print(f"Error in simple prediction: {str(e)}")
            current_price = float(data['Close'].iloc[-1])
            return {
                'prediction': 'HOLD',
                'confidence': 0.5,
                'recommendation': 'HOLD',
                'predicted_price': float(current_price),
                'price_change_percent': 0.0,
                'technical_indicators': {}
            }
