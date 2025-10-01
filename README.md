# 🚀 EPICcrypto - AI Crypto Prediction Platform

An advanced AI-powered cryptocurrency prediction platform that provides actionable trading advice across multiple timeframes using machine learning models and technical analysis.

![Python](https://img.shields.io/badge/python-v3.11-blue)
![Flask](https://img.shields.io/badge/flask-v3.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

- **Multi-Timeframe Predictions**: 1 min, 5 min, 10 min, 30 min, 1 hour, daily, monthly, and yearly predictions
- **AI-Powered Analysis**: Uses ensemble ML models including Random Forest, Gradient Boosting, Linear Regression, and ARIMA
- **Technical Indicators**: Comprehensive technical analysis including RSI, MACD, Moving Averages, Bollinger Bands, and Volatility analysis
- **Real-Time Data**: Integration with CoinGecko, Binance APIs, and Yahoo Finance for live market data
- **Smart Recommendations**: AI-generated buy/sell/hold advice with confidence scores
- **Multiple Cryptocurrencies**: Support for Bitcoin, Ethereum, BNB, Cardano, Solana, XRP, Polkadot, Dogecoin, and 100+ more
- **Beautiful UI**: Modern, responsive dashboard with real-time updates
- **Railway Deployment**: Ready to deploy on railway.app with one click

## 📊 Supported Cryptocurrencies

- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Cardano (ADA)
- Solana (SOL)
- XRP (Ripple)
- Polkadot (DOT)
- Dogecoin (DOGE)
- And 100+ more...

## 🏗️ Architecture

```
EPICcrypto/
├── backend/
│   ├── api/              # REST API routes
│   ├── data/             # Data fetching and preprocessing
│   ├── models/           # ML prediction models
│   └── utils/            # Utilities and caching
├── frontend/
│   ├── static/           # CSS, JS assets
│   └── templates/        # HTML templates
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
└── railway.json          # Railway deployment config
```

### AI/ML Models

The application uses a hybrid approach for predictions:

1. **Technical Analysis Engine**:
   - Moving Averages (SMA 5, 10, 20, 50)
   - Relative Strength Index (RSI)
   - Moving Average Convergence Divergence (MACD)
   - Bollinger Bands
   - Volume Analysis
   - Momentum Indicators

2. **Machine Learning Pipeline**:
   - Feature engineering from historical OHLCV data
   - Pattern recognition using recent price movements
   - Trend analysis and signal aggregation
   - Confidence scoring based on indicator alignment

3. **Multi-Timeframe Consensus**:
   - Analyzes market across multiple timeframes
   - Provides comprehensive view of short to long-term trends

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Islamhassana3/EPICcrypto.git
cd EPICcrypto
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
cp .env.example .env
```

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
```
http://localhost:5000
```

## 🌐 Deploy to Railway.app

### Method 1: One-Click Deploy

1. Fork this repository
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked repository
5. Railway will automatically detect configuration and deploy

### Method 2: Railway CLI

1. **Install Railway CLI**
```bash
npm i -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize project**
```bash
railway init
```

4. **Deploy**
```bash
railway up
```

5. **Add domain (optional)**
```bash
railway domain
```

### Alternative Deployment Platforms

#### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku open
```

#### Docker (for any platform)
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
```

Build and run:
```bash
docker build -t epiccrypto .
docker run -p 5000:5000 epiccrypto
```

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api  # Local
https://your-app.railway.app/api  # Production
```

### Endpoints

#### Health Check
```http
GET /api/health
```

#### Get Supported Coins
```http
GET /api/coins
```

#### Get Current Price
```http
GET /api/price/{coin_id}
```
Example: `/api/price/bitcoin`

#### Get Historical Data
```http
GET /api/historical/{coin_id}?days=30
```

#### Get Prediction
```http
GET /api/predict/{coin_id}?timeframe=1h
```
Timeframes: `1m`, `5m`, `10m`, `30m`, `1h`, `daily`, `monthly`, `yearly`

#### Get All Timeframe Predictions
```http
GET /api/predict/{coin_id}/all
```

#### Get Technical Analysis
```http
GET /api/analyze/{coin_id}
```

#### Get Recommendation
```http
GET /api/recommendation/{coin_id}?timeframe=1h
```

#### Example Response
```json
{
  "symbol": "BTC-USD",
  "timeframe": "1d",
  "current_price": 45000.00,
  "predicted_price": 46350.00,
  "price_change_percent": 3.0,
  "recommendation": "BUY",
  "confidence": 0.75,
  "technical_indicators": {
    "sma_20": 44500.00,
    "sma_50": 43800.00,
    "rsi": 62.5,
    "macd": 250.00
  }
}
```

## 🤖 AI Models

### Ensemble Models
- **Random Forest Regressor**: Captures non-linear patterns
- **Gradient Boosting Regressor**: Sequential error correction
- **Linear Regression**: Trend analysis
- **ARIMA**: Time series forecasting

### Technical Indicators
- **RSI (Relative Strength Index)**: Momentum indicator
- **MACD**: Trend-following momentum
- **Moving Averages**: MA7, MA25, MA50
- **Bollinger Bands**: Volatility measurement
- **Volatility**: Price variance analysis

## 📈 Prediction Methodology

1. **Data Collection**: Fetch real-time and historical data from APIs
2. **Preprocessing**: Calculate technical indicators and normalize data
3. **Feature Engineering**: Extract meaningful features from price data
4. **Model Training**: Train ensemble of ML models on historical data
5. **Prediction**: Generate predictions using trained models
6. **Recommendation**: Combine signals to produce buy/sell/hold advice
7. **Confidence Scoring**: Calculate confidence based on model agreement

## 🎯 Recommendation Signals

- **Strong Buy**: High confidence bullish signals (Score ≥ 3)
- **Buy**: Moderate bullish signals (Score ≥ 1)
- **Hold**: Neutral or mixed signals (Score -1 to 1)
- **Sell**: Moderate bearish signals (Score ≤ -1)
- **Strong Sell**: High confidence bearish signals (Score ≤ -3)

### Understanding Recommendations

- **BUY**: Strong positive signals across multiple indicators
- **SELL**: Strong negative signals indicating potential downtrend
- **HOLD**: Mixed or neutral signals, wait for clearer trend

**Confidence Levels**:
- High (>70%): Strong agreement among indicators
- Medium (50-70%): Moderate agreement, proceed with caution
- Low (<50%): Weak signals, high uncertainty

## 💻 Technology Stack

- **Backend**: Python 3.11, Flask
- **AI/ML**: TensorFlow, scikit-learn
- **Data**: yfinance, pandas, numpy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Railway.app (or any platform supporting Python apps)

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
PORT=5000
FLASK_ENV=production
```

### Railway Environment Variables

Set in Railway dashboard:
- `PORT`: Automatically set by Railway
- `SECRET_KEY`: Generate a secure random key

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=backend tests/
```

## 📦 Dependencies

### Core
- Flask 3.0.0 - Web framework
- Gunicorn 21.2.0 - WSGI server

### Data & APIs
- pandas 2.1.4 - Data manipulation
- numpy 1.26.2 - Numerical computing
- requests 2.31.0 - HTTP library
- pycoingecko 3.1.0 - CoinGecko API
- python-binance 1.0.19 - Binance API
- yfinance - Yahoo Finance API

### Machine Learning
- scikit-learn 1.3.2 - ML algorithms
- tensorflow 2.15.0 - Deep learning
- statsmodels 0.14.1 - Time series analysis

## 🔒 Security

- API rate limiting implemented
- Input validation on all endpoints
- CORS protection
- Environment variables for sensitive data
- No API keys required for basic functionality
- No financial data storage - app does not store personal information

## ⚠️ Disclaimer

**IMPORTANT**: This application provides AI-generated predictions for educational and informational purposes only.

- **NOT FINANCIAL ADVICE**: Do not use as sole basis for investment decisions
- **PAST PERFORMANCE**: Historical data does not guarantee future results
- **RISK WARNING**: Cryptocurrency trading involves substantial risk
- **DO YOUR RESEARCH**: Always conduct thorough research before investing
- **CONSULT PROFESSIONALS**: Seek advice from qualified financial advisors

The predictions are based on historical data and technical analysis. Always:
- Do your own research (DYOR)
- Consult with financial advisors
- Only invest what you can afford to lose
- Understand the risks involved in crypto trading

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/Islamhassana3/EPICcrypto/issues)

## 🙏 Acknowledgments

- CoinGecko API for cryptocurrency data
- Binance API for real-time trading data
- Yahoo Finance API for market data
- Railway.app for hosting platform
- Open source ML libraries

## 📊 Performance

- Response time: < 2s for predictions
- API uptime: 99.9% target
- Real-time data updates every 60 seconds
- Cached responses for improved performance

## 🗺️ Roadmap

- [ ] LSTM deep learning models for improved predictions
- [ ] Real-time WebSocket updates
- [ ] Portfolio tracking and management
- [ ] Alert notifications (email/SMS)
- [ ] More cryptocurrencies support
- [ ] Historical prediction accuracy tracking
- [ ] Sentiment analysis from social media
- [ ] Advanced charting with TradingView
- [ ] Mobile app version

---

**Built with ❤️ by the EPICcrypto Team**

*Powered by AI • Deployed on Railway.app • Real-time Crypto Analysis*

Made with ❤️ for the crypto community