"""
Main Flask application for AI Crypto Prediction
"""
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from backend.api.routes import api_bp
from backend.utils.port_finder import find_available_port
from services.crypto_data import CryptoDataService
from services.ai_predictor import AIPredictor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__,
                template_folder='frontend/templates',
                static_folder='frontend/static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Root route
    @app.route('/')
    def index():
        """Render main dashboard"""
        return render_template('index.html')
    
    return app


# Create app instance for WSGI servers (gunicorn, etc.)
app = create_app()


if __name__ == '__main__':
    preferred_port = int(os.environ.get('PORT', 5000))
    port = find_available_port(preferred_port)
    
    if port != preferred_port:
        logger.warning(f"Port {preferred_port} was not available. Using port {port} instead.")
        print(f"\n⚠️  Port {preferred_port} is already in use.")
        print(f"✅ Starting server on alternative port: {port}")
        print(f"🌐 Access the application at: http://localhost:{port}\n")
    
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False') == 'True')