# 🚀 Quick Start Guide

Get EPICcrypto running in 5 minutes!

## Option 1: Local Development (Fastest)

### Prerequisites
- Python 3.11+ installed
- Git installed

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Islamhassana3/EPICcrypto.git
cd EPICcrypto
```

2. **Create virtual environment**
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5000
```

That's it! 🎉

---

## Option 2: Railway.app Deployment (Production)

### Prerequisites
- GitHub account
- Railway.app account (free)

### Steps

1. **Fork the repository** on GitHub

2. **Sign in to Railway**
   - Go to https://railway.app
   - Click "Login with GitHub"

3. **Deploy**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `EPICcrypto`
   - Click "Deploy"

4. **Generate domain**
   - Click on your deployment
   - Go to "Settings"
   - Click "Generate Domain"

5. **Access your app**
   - Click on the generated URL
   - Your app is live! 🚀

Total time: ~3 minutes!

---

## Using the App

### What You'll See

The application provides:

1. **Cryptocurrency Selection**: Choose from Bitcoin, Ethereum, BNB, Cardano, Solana, XRP, and 100+ more
2. **Current Price Display**: Real-time price, 24h change, volume, and market cap
3. **Timeframe Selection**: Pick from multiple timeframes (1m to yearly)
4. **AI Predictions**: Get AI-generated price predictions with confidence scores
5. **Trading Recommendations**: Buy/Sell/Hold signals based on multiple indicators
6. **Technical Analysis**: RSI, MACD, Moving Averages, and more
7. **All Timeframes View**: See predictions across all timeframes at once

### How to Analyze

1. **Select a Cryptocurrency**
   - Choose from Bitcoin, Ethereum, or other supported coins

2. **Choose Timeframe**
   - **Short-term**: 1m, 5m, 10m, 30m (for day trading)
   - **Medium-term**: 1h, daily (for swing trading)
   - **Long-term**: monthly, yearly (for position trading)

3. **Get Analysis**
   - Click **"Analyze"** for single timeframe
   - Click **"Multi-Timeframe Analysis"** for comprehensive view

4. **Understand Results**

**Recommendation**:
- 🟢 **BUY/Strong Buy**: Strong positive signals
- 🔴 **SELL/Strong Sell**: Strong negative signals
- 🟡 **HOLD**: Mixed or neutral signals

**Confidence Scores**:
- **0.8 - 1.0**: High confidence (Strong signals)
- **0.6 - 0.8**: Good confidence (Clear trend)
- **0.4 - 0.6**: Moderate confidence (Mixed signals)
- **0.0 - 0.4**: Low confidence (Unclear trend)

**Technical Indicators**: Supporting data for the recommendation

---

## Quick API Test

### Using cURL
```bash
# Health check
curl http://localhost:5000/api/health

# Get Bitcoin price
curl http://localhost:5000/api/price/bitcoin

# Get 1-hour prediction
curl "http://localhost:5000/api/predict/bitcoin?timeframe=1h"

# Get technical analysis
curl http://localhost:5000/api/analyze/bitcoin

# Get all timeframes
curl http://localhost:5000/api/multi-timeframe/BTC-USD
```

### Using Browser
Visit these URLs:
```
http://localhost:5000/api/health
http://localhost:5000/api/coins
http://localhost:5000/api/prediction/BTC-USD?timeframe=1d
```

### Example API Response

**Price Endpoint**:
```json
{
  "symbol": "bitcoin",
  "price": 43250.50,
  "change_24h": 2.34,
  "volume_24h": 28500000000,
  "market_cap": 845000000000,
  "timestamp": "2024-01-01T12:00:00"
}
```

**Prediction Endpoint**:
```json
{
  "coin_id": "bitcoin",
  "prediction": {
    "timeframe": "1h",
    "current_price": 43250.50,
    "recommendation": {
      "action": "buy",
      "confidence": 0.75,
      "reason": "Trend: bullish, Momentum: buy"
    }
  }
}
```

**Technical Analysis**:
```json
{
  "coin_id": "bitcoin",
  "current_price": 43250.50,
  "indicators": {
    "RSI": 65.4,
    "MACD": 125.5,
    "MA_7": 43100.00,
    "MA_25": 42800.00
  },
  "technical_analysis": {
    "RSI": "Neutral",
    "MA_Cross": "Bullish"
  }
}
```

---

## Features Overview

### Supported Cryptocurrencies
- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Cardano (ADA)
- Solana (SOL)
- XRP (Ripple)
- 100+ more via API

### Prediction Timeframes
- **1 minute**: Ultra-short term (scalping)
- **5 minutes**: Short-term trading
- **10 minutes**: Day trading
- **30 minutes**: Intraday trading
- **1 hour**: Swing trading
- **Daily**: Position trading
- **Monthly**: Long-term investment
- **Yearly**: Strategic planning

### AI Models Used
- Random Forest Regressor
- Gradient Boosting Regressor
- Linear Regression
- ARIMA Time Series

### Technical Indicators
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Moving Averages (7, 25, 50 day)
- Bollinger Bands
- Volatility Analysis

---

## Troubleshooting

### Port Already in Use

**Good news!** The application now automatically detects if port 5000 is in use and finds an available alternative port.

When you run the app or use the preview scripts, you'll see:
```
⚠️  Port 5000 is already in use.
✅ Starting server on alternative port: 5001
🌐 Access the application at: http://localhost:5001
```

If you want to manually specify a different port:
```bash
# Change port in .env file
echo "PORT=8000" > .env

# Or run with custom port
export PORT=8000
python app.py
```

The app will use your specified port if available, or find the next available port automatically.

### Dependencies Won't Install
```bash
# Upgrade pip
pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

### API Connection Errors

The app fetches data from CoinGecko and Binance APIs. If you see connection errors:

1. Check your internet connection
2. Wait a moment and refresh (APIs may have rate limits)
3. Try a different cryptocurrency

### Slow Predictions

First prediction takes longer as models are initialized. Subsequent predictions are faster due to caching.

### Can't Access from Other Devices
```bash
# Run with host 0.0.0.0
python app.py
# App will be accessible at http://YOUR_IP:5000
```

---

## Environment Variables

Optional configuration via `.env` file:

```env
SECRET_KEY=your-secret-key
FLASK_ENV=development
PORT=5000
```

---

## Example Use Cases

### Day Trading
```
1. Check 1m, 5m, 15m timeframes
2. Look for consistent BUY/SELL across all
3. High confidence (>70%) is better
4. Act quickly on strong signals
```

### Swing Trading
```
1. Check 1h, 4h, 1d timeframes
2. Look for trend alignment
3. Medium to high confidence
4. Hold positions for days/weeks
```

### Long-term Investing
```
1. Check 1d, 1wk, 1mo timeframes
2. Look for long-term trends
3. Don't over-react to short-term noise
4. Hold for months/years
```

---

## Next Steps

1. **Explore the UI**: Click through different coins and timeframes
2. **Try the API**: Use curl or Postman to test endpoints
3. **Read Documentation**: Check out `README.md` and `API_DOCUMENTATION.md`
4. **Deploy to Railway**: Follow `DEPLOYMENT.md` for production deployment

### Additional Resources
- [README.md](README.md) - Complete project documentation
- [API_DOCS.md](API_DOCS.md) - Full API reference
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment options
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture

---

## Tips

### For Developers
- The main app is in `app.py`
- AI logic is in `services/ai_predictor.py`
- Data fetching is in `services/crypto_data.py`
- UI files are in `templates/` and `static/`

### For Traders
- Use multiple timeframes for better decisions
- Higher confidence = stronger signals
- Always combine with your own analysis
- This is NOT financial advice!

### For Deployment
- Railway.app: Easiest (recommended)
- Heroku: Good alternative
- Docker: Most flexible
- See DEPLOYMENT.md for all options

---

## Getting Help

- **Issues**: https://github.com/Islamhassana3/EPICcrypto/issues
- **Documentation**: Check other .md files in repository
- **Logs**: Check console output for errors

---

## Important Disclaimer

⚠️ **This is for educational purposes only!**

- Not financial advice
- Do your own research (DYOR)
- Cryptocurrency trading involves substantial risk
- Past performance doesn't guarantee future results
- Only invest what you can afford to lose
- Consult with financial professionals before investing

---

**Enjoy EPICcrypto!** 🚀📈💰