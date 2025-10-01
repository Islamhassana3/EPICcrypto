"""
Production configuration for EPICcrypto
"""
import os

class Config:
    """Base configuration"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # App settings
    PORT = int(os.environ.get('PORT', 5000))
    HOST = '0.0.0.0'
    
    # Cache settings
    CACHE_DURATION = int(os.environ.get('CACHE_DURATION', 60))
    
    # API settings
    API_TIMEOUT = int(os.environ.get('API_TIMEOUT', 30))
    MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'production')
    return config.get(env, config['default'])
