from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from services.crypto_data import CryptoDataService
from services.ai_predictor import AIPredictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure Flask for production
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Initialize services with error handling
try:
    crypto_service = CryptoDataService()
    ai_predictor = AIPredictor()
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize services: {str(e)}")
    raise

@app.route('/')
def index():
    """Main page with UI for crypto predictions"""
    return render_template('index.html')

@app.route('/api/coins')
def get_supported_coins():
    """Get list of supported cryptocurrencies"""
    coins = [
        {'symbol': 'BTC-USD', 'name': 'Bitcoin'},
        {'symbol': 'ETH-USD', 'name': 'Ethereum'},
        {'symbol': 'BNB-USD', 'name': 'Binance Coin'},
        {'symbol': 'ADA-USD', 'name': 'Cardano'},
        {'symbol': 'SOL-USD', 'name': 'Solana'},
        {'symbol': 'XRP-USD', 'name': 'Ripple'},
        {'symbol': 'DOT-USD', 'name': 'Polkadot'},
        {'symbol': 'DOGE-USD', 'name': 'Dogecoin'},
    ]
    return jsonify(coins)

@app.route('/api/prediction/<symbol>')
def get_prediction(symbol):
    """Get AI prediction for a specific cryptocurrency"""
    try:
        # Get timeframe from query params (default to 1d)
        timeframe = request.args.get('timeframe', '1d')
        
        # Fetch historical data
        data = crypto_service.get_historical_data(symbol, timeframe)
        
        if data is None or data.empty:
            return jsonify({'error': 'Unable to fetch data for this coin'}), 404
        
        # Get AI prediction
        prediction = ai_predictor.predict(data, timeframe)
        
        # Get current price
        current_price = float(data['Close'].iloc[-1])
        
        return jsonify({
            'symbol': symbol,
            'timeframe': timeframe,
            'current_price': current_price,
            'prediction': prediction['prediction'],
            'confidence': prediction['confidence'],
            'recommendation': prediction['recommendation'],
            'predicted_price': prediction['predicted_price'],
            'price_change_percent': prediction['price_change_percent'],
            'technical_indicators': prediction['technical_indicators']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/multi-timeframe/<symbol>')
def get_multi_timeframe_prediction(symbol):
    """Get predictions across multiple timeframes"""
    try:
        timeframes = ['1m', '5m', '15m', '1h', '4h', '1d', '1wk', '1mo']
        predictions = {}
        
        for tf in timeframes:
            data = crypto_service.get_historical_data(symbol, tf)
            if data is not None and not data.empty:
                pred = ai_predictor.predict(data, tf)
                predictions[tf] = {
                    'recommendation': pred['recommendation'],
                    'confidence': pred['confidence'],
                    'predicted_price': pred['predicted_price'],
                    'price_change_percent': pred['price_change_percent']
                }
        
        return jsonify({
            'symbol': symbol,
            'predictions': predictions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({'status': 'healthy', 'service': 'EPICcrypto'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
