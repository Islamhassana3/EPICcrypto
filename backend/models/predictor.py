"""
AI/ML models for crypto price prediction
Supports multiple timeframes and prediction methods
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')


class CryptoPricePredictor:
    """Multi-model crypto price predictor"""
    
    def __init__(self):
        self.models = {
            'rf': RandomForestRegressor(n_estimators=100, random_state=42),
            'gb': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'lr': LinearRegression()
        }
        self.trained_models = {}
        
    def train_ensemble(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """Train ensemble of models"""
        results = {}
        
        if len(X) < 10 or len(y) < 10:
            return {'error': 'Insufficient data for training'}
        
        for name, model in self.models.items():
            try:
                model.fit(X, y)
                self.trained_models[name] = model
                score = model.score(X, y)
                results[name] = {'trained': True, 'score': float(score)}
            except Exception as e:
                results[name] = {'trained': False, 'error': str(e)}
        
        return results
    
    def predict_ensemble(self, X: np.ndarray) -> Dict:
        """Make predictions using ensemble of models"""
        predictions = {}
        
        for name, model in self.trained_models.items():
            try:
                pred = model.predict(X)
                predictions[name] = pred.tolist() if hasattr(pred, 'tolist') else [float(pred)]
            except Exception as e:
                predictions[name] = None
        
        # Calculate ensemble average
        valid_preds = [p for p in predictions.values() if p is not None]
        if valid_preds:
            ensemble_pred = np.mean(valid_preds, axis=0)
            predictions['ensemble'] = ensemble_pred.tolist() if hasattr(ensemble_pred, 'tolist') else [float(ensemble_pred)]
        
        return predictions
    
    def predict_trend_simple(self, prices: List[float], periods_ahead: int = 1) -> Dict:
        """Simple trend prediction using linear regression"""
        if len(prices) < 5:
            return {'error': 'Insufficient data'}
        
        X = np.arange(len(prices)).reshape(-1, 1)
        y = np.array(prices)
        
        # Train simple linear model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict future values
        future_X = np.arange(len(prices), len(prices) + periods_ahead).reshape(-1, 1)
        predictions = model.predict(future_X)
        
        # Calculate trend
        slope = model.coef_[0]
        trend = 'bullish' if slope > 0 else 'bearish' if slope < 0 else 'neutral'
        
        return {
            'predictions': predictions.tolist(),
            'trend': trend,
            'slope': float(slope),
            'confidence': float(model.score(X, y))
        }
    
    def predict_arima(self, prices: List[float], periods_ahead: int = 1) -> Dict:
        """ARIMA time series prediction"""
        try:
            if len(prices) < 20:
                return {'error': 'Insufficient data for ARIMA'}
            
            # Fit ARIMA model
            model = ARIMA(prices, order=(5, 1, 0))
            fitted_model = model.fit()
            
            # Make predictions
            forecast = fitted_model.forecast(steps=periods_ahead)
            
            return {
                'predictions': forecast.tolist() if hasattr(forecast, 'tolist') else [float(forecast)],
                'method': 'ARIMA',
                'aic': float(fitted_model.aic)
            }
        except Exception as e:
            return {'error': f'ARIMA prediction failed: {str(e)}'}
    
    def analyze_momentum(self, prices: List[float]) -> Dict:
        """Analyze price momentum"""
        if len(prices) < 10:
            return {'error': 'Insufficient data'}
        
        # Calculate rate of change
        recent_prices = prices[-10:]
        older_prices = prices[-20:-10] if len(prices) >= 20 else prices[:10]
        
        recent_avg = np.mean(recent_prices)
        older_avg = np.mean(older_prices)
        
        momentum = ((recent_avg - older_avg) / older_avg) * 100
        
        # Volatility
        volatility = np.std(prices[-20:]) if len(prices) >= 20 else np.std(prices)
        
        return {
            'momentum': float(momentum),
            'volatility': float(volatility),
            'recent_avg': float(recent_avg),
            'signal': 'strong_buy' if momentum > 5 else 'buy' if momentum > 2 else 'hold' if momentum > -2 else 'sell' if momentum > -5 else 'strong_sell'
        }


class MultiTimeframePredictor:
    """Predictor for multiple timeframes"""
    
    TIMEFRAMES = {
        '1m': {'interval': '1m', 'limit': 60, 'periods': 1},
        '5m': {'interval': '5m', 'limit': 100, 'periods': 1},
        '10m': {'interval': '5m', 'limit': 120, 'periods': 2},
        '30m': {'interval': '30m', 'limit': 100, 'periods': 1},
        '1h': {'interval': '1h', 'limit': 100, 'periods': 1},
        'daily': {'interval': '1d', 'limit': 100, 'periods': 1},
        'monthly': {'interval': '1d', 'limit': 365, 'periods': 30},
        'yearly': {'interval': '1d', 'limit': 730, 'periods': 365}
    }
    
    def __init__(self):
        self.predictor = CryptoPricePredictor()
    
    def predict_for_timeframe(self, data: List[dict], timeframe: str) -> Dict:
        """Make prediction for specific timeframe"""
        if timeframe not in self.TIMEFRAMES:
            return {'error': f'Invalid timeframe: {timeframe}'}
        
        if not data or len(data) < 10:
            return {'error': 'Insufficient data'}
        
        # Extract prices
        prices = [d.get('price', d.get('close', 0)) for d in data]
        
        config = self.TIMEFRAMES[timeframe]
        periods = config['periods']
        
        # Get predictions
        trend_pred = self.predictor.predict_trend_simple(prices, periods)
        arima_pred = self.predictor.predict_arima(prices, periods)
        momentum = self.predictor.analyze_momentum(prices)
        
        # Combine predictions
        result = {
            'timeframe': timeframe,
            'current_price': float(prices[-1]),
            'trend_prediction': trend_pred,
            'arima_prediction': arima_pred,
            'momentum_analysis': momentum,
            'recommendation': self._generate_recommendation(trend_pred, momentum)
        }
        
        return result
    
    def _generate_recommendation(self, trend: Dict, momentum: Dict) -> Dict:
        """Generate buy/sell/hold recommendation"""
        if 'error' in trend or 'error' in momentum:
            return {'action': 'hold', 'confidence': 0.0, 'reason': 'Insufficient data'}
        
        # Score based on trend and momentum
        score = 0
        
        if trend.get('trend') == 'bullish':
            score += 2
        elif trend.get('trend') == 'bearish':
            score -= 2
        
        momentum_signal = momentum.get('signal', 'hold')
        if momentum_signal == 'strong_buy':
            score += 3
        elif momentum_signal == 'buy':
            score += 1
        elif momentum_signal == 'sell':
            score -= 1
        elif momentum_signal == 'strong_sell':
            score -= 3
        
        # Determine action
        if score >= 3:
            action = 'strong_buy'
            confidence = min(0.9, 0.6 + abs(score) * 0.1)
        elif score >= 1:
            action = 'buy'
            confidence = 0.6
        elif score <= -3:
            action = 'strong_sell'
            confidence = min(0.9, 0.6 + abs(score) * 0.1)
        elif score <= -1:
            action = 'sell'
            confidence = 0.6
        else:
            action = 'hold'
            confidence = 0.5
        
        reason_parts = []
        if trend.get('trend'):
            reason_parts.append(f"Trend: {trend['trend']}")
        if momentum_signal:
            reason_parts.append(f"Momentum: {momentum_signal}")
        
        return {
            'action': action,
            'confidence': float(confidence),
            'reason': ', '.join(reason_parts),
            'score': score
        }
    
    def predict_all_timeframes(self, historical_data: Dict) -> Dict:
        """Generate predictions for all timeframes"""
        results = {}
        
        for timeframe in self.TIMEFRAMES.keys():
            data = historical_data.get(timeframe, [])
            results[timeframe] = self.predict_for_timeframe(data, timeframe)
        
        return results
