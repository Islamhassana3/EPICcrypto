"""
Tests for data preprocessor
"""
import numpy as np
from backend.data.preprocessor import DataPreprocessor


def test_prepare_time_series_data():
    """Test time series data preparation"""
    preprocessor = DataPreprocessor()
    
    # Create sample data
    data = [{'price': 100 + i} for i in range(100)]
    
    X, y = preprocessor.prepare_time_series_data(data, sequence_length=10)
    
    assert len(X) > 0
    assert len(y) > 0
    assert X.shape[1] == 10


def test_calculate_technical_indicators():
    """Test technical indicators calculation"""
    preprocessor = DataPreprocessor()
    
    # Create sample data
    data = [{'close': 100 + i * 0.5} for i in range(100)]
    
    df = preprocessor.calculate_technical_indicators(data)
    
    assert not df.empty
    assert 'MA_7' in df.columns
    assert 'RSI' in df.columns
    assert 'MACD' in df.columns


def test_empty_data_handling():
    """Test handling of empty data"""
    preprocessor = DataPreprocessor()
    
    X, y = preprocessor.prepare_time_series_data([], sequence_length=10)
    
    assert len(X) == 0
    assert len(y) == 0
