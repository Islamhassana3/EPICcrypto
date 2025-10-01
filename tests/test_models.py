"""
Tests for prediction models
"""
import numpy as np
from backend.models.predictor import CryptoPricePredictor, MultiTimeframePredictor


def test_predict_trend_simple():
    """Test simple trend prediction"""
    predictor = CryptoPricePredictor()
    prices = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118]
    
    result = predictor.predict_trend_simple(prices, periods_ahead=1)
    
    assert 'predictions' in result
    assert 'trend' in result
    assert 'slope' in result
    assert result['trend'] == 'bullish'


def test_analyze_momentum():
    """Test momentum analysis"""
    predictor = CryptoPricePredictor()
    prices = [100] * 10 + [110] * 10
    
    result = predictor.analyze_momentum(prices)
    
    assert 'momentum' in result
    assert 'volatility' in result
    assert 'signal' in result


def test_multi_timeframe_predictor():
    """Test multi-timeframe predictor initialization"""
    predictor = MultiTimeframePredictor()
    
    assert '1m' in predictor.TIMEFRAMES
    assert '1h' in predictor.TIMEFRAMES
    assert 'daily' in predictor.TIMEFRAMES
