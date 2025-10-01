# EPICcrypto 🚀

AI-powered cryptocurrency analysis platform that provides intelligent buy/sell advice for Bitcoin and altcoins using machine learning algorithms.

## Features

- **AI-Driven Predictions**: Advanced machine learning models analyze market patterns and provide actionable insights
- **Multi-Timeframe Analysis**: Get predictions across 8 different timeframes (1 minute to 1 month)
- **Multiple Cryptocurrencies**: Support for Bitcoin, Ethereum, Binance Coin, Cardano, Solana, Ripple, Polkadot, and Dogecoin
- **Technical Indicators**: Comprehensive technical analysis including SMA, RSI, MACD, and Bollinger Bands
- **Real-Time Data**: Live cryptocurrency data from Yahoo Finance API
- **Beautiful UI**: Modern, responsive web interface for easy access to predictions
- **Buy/Sell/Hold Recommendations**: Clear trading suggestions with confidence levels

## Technology Stack

- **Backend**: Python 3.11, Flask
- **AI/ML**: TensorFlow, scikit-learn
- **Data**: yfinance, pandas, numpy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Railway.app (or any platform supporting Python apps)

## Architecture

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

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Islamhassana3/EPICcrypto.git
cd EPICcrypto
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to `http://localhost:5000`

## Deployment to Railway.app

### Prerequisites
- GitHub account
- Railway.app account (sign up at https://railway.app)

### Deployment Steps

1. **Connect Repository to Railway**:
   - Go to [Railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose the `EPICcrypto` repository

2. **Configure Environment**:
   - Railway will automatically detect the Python application
   - Set environment variables in Railway dashboard:
     - `PORT`: Automatically set by Railway
     - `FLASK_ENV`: production

3. **Deploy**:
   - Railway will automatically deploy the application
   - The build process uses `requirements.txt` for dependencies
   - The app starts using the `Procfile` configuration

4. **Access Your App**:
   - Railway provides a public URL (e.g., `your-app.railway.app`)
   - Your AI crypto app is now live!

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

## API Documentation

### Endpoints

#### GET `/api/coins`
Returns list of supported cryptocurrencies.

**Response**:
```json
[
  {"symbol": "BTC-USD", "name": "Bitcoin"},
  {"symbol": "ETH-USD", "name": "Ethereum"}
]
```

#### GET `/api/prediction/<symbol>?timeframe=1d`
Get AI prediction for a specific cryptocurrency and timeframe.

**Parameters**:
- `symbol`: Cryptocurrency symbol (e.g., BTC-USD)
- `timeframe`: Time interval (1m, 5m, 15m, 1h, 4h, 1d, 1wk, 1mo)

**Response**:
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

#### GET `/api/multi-timeframe/<symbol>`
Get predictions across all timeframes for comprehensive analysis.

**Response**:
```json
{
  "symbol": "BTC-USD",
  "predictions": {
    "1d": {
      "recommendation": "BUY",
      "confidence": 0.75,
      "predicted_price": 46350.00,
      "price_change_percent": 3.0
    }
  }
}
```

#### GET `/api/health`
Health check endpoint for monitoring.

## Usage

### Web Interface

1. **Select Cryptocurrency**: Choose from the dropdown menu (Bitcoin, Ethereum, etc.)
2. **Choose Timeframe**: Select analysis timeframe (1 minute to 1 month)
3. **Analyze**: Click "Analyze" for single timeframe or "Multi-Timeframe Analysis" for comprehensive view
4. **Review Results**: View AI recommendations, predicted prices, and technical indicators

### Understanding Recommendations

- **BUY**: Strong positive signals across multiple indicators
- **SELL**: Strong negative signals indicating potential downtrend
- **HOLD**: Mixed or neutral signals, wait for clearer trend

**Confidence Levels**:
- High (>70%): Strong agreement among indicators
- Medium (50-70%): Moderate agreement, proceed with caution
- Low (<50%): Weak signals, high uncertainty

## Security & Best Practices

- **API Rate Limits**: The app implements caching to minimize API calls
- **Data Validation**: All inputs are sanitized and validated
- **Error Handling**: Comprehensive error handling for robust operation
- **No Financial Data Storage**: The app does not store personal or financial information

## Disclaimer

⚠️ **IMPORTANT**: This application is for educational and informational purposes only. It is NOT financial advice. Cryptocurrency trading involves substantial risk of loss. Always:

- Do your own research (DYOR)
- Consult with financial advisors
- Only invest what you can afford to lose
- Understand the risks involved in crypto trading

The predictions are based on historical data and technical analysis. Past performance does not guarantee future results.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] LSTM deep learning models for improved predictions
- [ ] Real-time WebSocket updates
- [ ] Portfolio tracking and management
- [ ] Alert notifications (email/SMS)
- [ ] More cryptocurrencies support
- [ ] Historical performance tracking
- [ ] Sentiment analysis from social media
- [ ] Advanced charting and visualization

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ for the crypto community