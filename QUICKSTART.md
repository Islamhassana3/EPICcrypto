# 🚀 Quick Start Guide

Get EPICcrypto running in minutes!

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Islamhassana3/EPICcrypto.git
cd EPICcrypto
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

Navigate to: `http://localhost:5000`

## What You'll See

The application provides:

1. **Cryptocurrency Selection**: Choose from Bitcoin, Ethereum, BNB, Cardano, Solana, XRP
2. **Current Price Display**: Real-time price, 24h change, volume, and market cap
3. **Timeframe Selection**: Pick from 8 different timeframes (1m to yearly)
4. **AI Predictions**: Get AI-generated price predictions with confidence scores
5. **Trading Recommendations**: Buy/Sell/Hold signals based on multiple indicators
6. **Technical Analysis**: RSI, MACD, Moving Averages, and more
7. **All Timeframes View**: See predictions across all timeframes at once

## API Usage Examples

### Get Bitcoin Price

```bash
curl http://localhost:5000/api/price/bitcoin
```

Response:
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

### Get 1-Hour Prediction

```bash
curl http://localhost:5000/api/predict/bitcoin?timeframe=1h
```

Response:
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

### Get Technical Analysis

```bash
curl http://localhost:5000/api/analyze/bitcoin
```

Response:
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

## Features

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

## Understanding Recommendations

### Action Signals

| Signal | Meaning | When to Use |
|--------|---------|-------------|
| **Strong Buy** | Very bullish signals | Consider entering position |
| **Buy** | Bullish signals | Good entry point |
| **Hold** | Neutral or mixed | Wait for clearer signals |
| **Sell** | Bearish signals | Consider taking profits |
| **Strong Sell** | Very bearish signals | Consider exiting position |

### Confidence Scores

- **0.8 - 1.0**: High confidence (Strong signals)
- **0.6 - 0.8**: Good confidence (Clear trend)
- **0.4 - 0.6**: Moderate confidence (Mixed signals)
- **0.0 - 0.4**: Low confidence (Unclear trend)

## Troubleshooting

### Port Already in Use

If port 5000 is busy, run on a different port:

```bash
export PORT=8000
python app.py
```

Then visit: `http://localhost:8000`

### API Connection Errors

The app fetches data from CoinGecko and Binance APIs. If you see connection errors:

1. Check your internet connection
2. Wait a moment and refresh (APIs may have rate limits)
3. Try a different cryptocurrency

### Slow Predictions

First prediction takes longer as models are initialized. Subsequent predictions are faster due to caching.

## Environment Variables

Optional configuration via `.env` file:

```env
SECRET_KEY=your-secret-key
FLASK_ENV=development
PORT=5000
```

## Next Steps

1. **Explore the UI**: Click through different coins and timeframes
2. **Try the API**: Use curl or Postman to test endpoints
3. **Read Documentation**: Check out `README.md` and `API_DOCUMENTATION.md`
4. **Deploy to Railway**: Follow `DEPLOYMENT.md` for production deployment

## Important Disclaimer

⚠️ **This is for educational purposes only!**

- Not financial advice
- Do your own research (DYOR)
- Cryptocurrency trading involves substantial risk
- Past performance doesn't guarantee future results
- Consult with financial professionals before investing

## Support

- GitHub Issues: https://github.com/Islamhassana3/EPICcrypto/issues
- Documentation: See `README.md`, `API_DOCUMENTATION.md`, `DEPLOYMENT.md`

## What's Next?

Check out these guides:
- `README.md` - Complete project documentation
- `API_DOCUMENTATION.md` - Full API reference
- `DEPLOYMENT.md` - Deploy to Railway.app

---

**Enjoy EPICcrypto!** 🚀📈💰
