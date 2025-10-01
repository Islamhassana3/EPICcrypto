"""
API routes for crypto prediction service
"""
import pandas as pd
from flask import Blueprint, jsonify, request
from backend.data.crypto_api import CryptoDataFetcher
from backend.data.preprocessor import DataPreprocessor
from backend.models.predictor import MultiTimeframePredictor
from backend.utils.cache import CacheManager
import traceback

api_bp = Blueprint('api', __name__)

# Initialize services
data_fetcher = CryptoDataFetcher()
preprocessor = DataPreprocessor()
predictor = MultiTimeframePredictor()
cache = CacheManager()


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'crypto-prediction-api',
        'version': '1.0.0'
    })


@api_bp.route('/coins', methods=['GET'])
def get_supported_coins():
    """Get list of supported cryptocurrencies"""
    try:
        # Check cache first
        cached = cache.get('supported_coins')
        if cached:
            return jsonify(cached)
        
        coins = data_fetcher.get_supported_coins()
        
        # Popular coins for quick access
        popular = [
            {'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin'},
            {'id': 'ethereum', 'symbol': 'eth', 'name': 'Ethereum'},
            {'id': 'binancecoin', 'symbol': 'bnb', 'name': 'Binance Coin'},
            {'id': 'cardano', 'symbol': 'ada', 'name': 'Cardano'},
            {'id': 'solana', 'symbol': 'sol', 'name': 'Solana'},
            {'id': 'ripple', 'symbol': 'xrp', 'name': 'XRP'},
        ]
        
        result = {
            'popular': popular,
            'all': coins[:100]
        }
        
        cache.set('supported_coins', result, ttl=3600)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/price/<coin_id>', methods=['GET'])
def get_current_price(coin_id):
    """Get current price for a cryptocurrency"""
    try:
        cache_key = f'price_{coin_id}'
        cached = cache.get(cache_key)
        if cached:
            return jsonify(cached)
        
        data = data_fetcher.get_current_price(coin_id)
        if not data:
            return jsonify({'error': 'Failed to fetch price data'}), 404
        
        cache.set(cache_key, data, ttl=60)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/historical/<coin_id>', methods=['GET'])
def get_historical_data(coin_id):
    """Get historical price data"""
    try:
        days = request.args.get('days', default=30, type=int)
        
        cache_key = f'historical_{coin_id}_{days}'
        cached = cache.get(cache_key)
        if cached:
            return jsonify(cached)
        
        data = data_fetcher.get_historical_data(coin_id, days)
        if not data:
            return jsonify({'error': 'Failed to fetch historical data'}), 404
        
        cache.set(cache_key, data, ttl=300)
        return jsonify({'coin_id': coin_id, 'days': days, 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/predict/<coin_id>', methods=['GET'])
def predict_price(coin_id):
    """Generate price predictions for all timeframes"""
    try:
        timeframe = request.args.get('timeframe', default='1h', type=str)
        
        cache_key = f'prediction_{coin_id}_{timeframe}'
        cached = cache.get(cache_key)
        if cached:
            return jsonify(cached)
        
        # Fetch data based on timeframe
        if timeframe in ['1m', '5m', '10m', '30m', '1h']:
            # Use Binance for short timeframes
            symbol_map = {
                'bitcoin': 'BTCUSDT',
                'ethereum': 'ETHUSDT',
                'binancecoin': 'BNBUSDT',
                'cardano': 'ADAUSDT',
                'solana': 'SOLUSDT',
                'ripple': 'XRPUSDT'
            }
            binance_symbol = symbol_map.get(coin_id, 'BTCUSDT')
            
            interval_map = {
                '1m': '1m',
                '5m': '5m',
                '10m': '5m',
                '30m': '30m',
                '1h': '1h'
            }
            interval = interval_map.get(timeframe, '1h')
            
            data = data_fetcher.get_binance_klines(binance_symbol, interval, 100)
        else:
            # Use CoinGecko for longer timeframes
            days_map = {
                'daily': 30,
                'monthly': 90,
                'yearly': 365
            }
            days = days_map.get(timeframe, 30)
            data = data_fetcher.get_historical_data(coin_id, days)
        
        if not data:
            return jsonify({'error': 'Failed to fetch data for prediction'}), 404
        
        # Generate prediction
        prediction = predictor.predict_for_timeframe(data, timeframe)
        
        result = {
            'coin_id': coin_id,
            'prediction': prediction
        }
        
        cache.set(cache_key, result, ttl=60)
        return jsonify(result)
    except Exception as e:
        print(f"Prediction error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/predict/<coin_id>/all', methods=['GET'])
def predict_all_timeframes(coin_id):
    """Generate predictions for all timeframes"""
    try:
        cache_key = f'prediction_all_{coin_id}'
        cached = cache.get(cache_key)
        if cached:
            return jsonify(cached)
        
        # Fetch data for different timeframes
        historical_data = {}
        
        # Short timeframes from Binance
        symbol_map = {
            'bitcoin': 'BTCUSDT',
            'ethereum': 'ETHUSDT',
            'binancecoin': 'BNBUSDT',
            'cardano': 'ADAUSDT',
            'solana': 'SOLUSDT',
            'ripple': 'XRPUSDT'
        }
        binance_symbol = symbol_map.get(coin_id, 'BTCUSDT')
        
        for tf in ['1m', '5m', '30m', '1h']:
            interval_map = {'1m': '1m', '5m': '5m', '30m': '30m', '1h': '1h', '10m': '5m'}
            data = data_fetcher.get_binance_klines(binance_symbol, interval_map[tf], 100)
            historical_data[tf] = data
        
        # Long timeframes from CoinGecko
        for tf, days in [('daily', 30), ('monthly', 90), ('yearly', 365)]:
            data = data_fetcher.get_historical_data(coin_id, days)
            historical_data[tf] = data
        
        # Generate predictions for all timeframes
        predictions = predictor.predict_all_timeframes(historical_data)
        
        result = {
            'coin_id': coin_id,
            'predictions': predictions
        }
        
        cache.set(cache_key, result, ttl=120)
        return jsonify(result)
    except Exception as e:
        print(f"All timeframes prediction error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/analyze/<coin_id>', methods=['GET'])
def analyze_coin(coin_id):
    """Comprehensive analysis with technical indicators"""
    try:
        cache_key = f'analysis_{coin_id}'
        cached = cache.get(cache_key)
        if cached:
            return jsonify(cached)
        
        # Get historical data
        data = data_fetcher.get_historical_data(coin_id, 30)
        if not data:
            return jsonify({'error': 'Failed to fetch data'}), 404
        
        # Calculate technical indicators
        df = preprocessor.calculate_technical_indicators(data)
        
        # Get latest values
        latest = df.iloc[-1] if not df.empty else {}
        
        result = {
            'coin_id': coin_id,
            'current_price': float(latest.get('close', 0)) if latest else 0,
            'indicators': {
                'MA_7': float(latest.get('MA_7', 0)) if latest and not pd.isna(latest.get('MA_7')) else None,
                'MA_25': float(latest.get('MA_25', 0)) if latest and not pd.isna(latest.get('MA_25')) else None,
                'RSI': float(latest.get('RSI', 50)) if latest and not pd.isna(latest.get('RSI')) else None,
                'MACD': float(latest.get('MACD', 0)) if latest and not pd.isna(latest.get('MACD')) else None,
                'Volatility': float(latest.get('Volatility', 0)) if latest and not pd.isna(latest.get('Volatility')) else None,
            },
            'technical_analysis': self._interpret_indicators(latest) if latest else {}
        }
        
        cache.set(cache_key, result, ttl=300)
        return jsonify(result)
    except Exception as e:
        print(f"Analysis error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def _interpret_indicators(data):
    """Interpret technical indicators"""
    interpretation = {}
    
    # RSI interpretation
    rsi = data.get('RSI')
    if rsi and not pd.isna(rsi):
        if rsi > 70:
            interpretation['RSI'] = 'Overbought - Consider selling'
        elif rsi < 30:
            interpretation['RSI'] = 'Oversold - Consider buying'
        else:
            interpretation['RSI'] = 'Neutral'
    
    # Moving average cross
    ma_7 = data.get('MA_7')
    ma_25 = data.get('MA_25')
    if ma_7 and ma_25 and not pd.isna(ma_7) and not pd.isna(ma_25):
        if ma_7 > ma_25:
            interpretation['MA_Cross'] = 'Bullish - Short MA above long MA'
        else:
            interpretation['MA_Cross'] = 'Bearish - Short MA below long MA'
    
    # MACD
    macd = data.get('MACD')
    if macd and not pd.isna(macd):
        if macd > 0:
            interpretation['MACD'] = 'Bullish momentum'
        else:
            interpretation['MACD'] = 'Bearish momentum'
    
    return interpretation


@api_bp.route('/recommendation/<coin_id>', methods=['GET'])
def get_recommendation(coin_id):
    """Get trading recommendation"""
    try:
        timeframe = request.args.get('timeframe', default='1h', type=str)
        
        cache_key = f'recommendation_{coin_id}_{timeframe}'
        cached = cache.get(cache_key)
        if cached:
            return jsonify(cached)
        
        # Get prediction
        prediction_response = predict_price(coin_id)
        if prediction_response[1] != 200:
            return prediction_response
        
        prediction_data = prediction_response[0].get_json()
        prediction = prediction_data.get('prediction', {})
        
        recommendation = prediction.get('recommendation', {})
        
        result = {
            'coin_id': coin_id,
            'timeframe': timeframe,
            'recommendation': recommendation,
            'current_price': prediction.get('current_price'),
            'timestamp': prediction_data.get('timestamp')
        }
        
        cache.set(cache_key, result, ttl=60)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
