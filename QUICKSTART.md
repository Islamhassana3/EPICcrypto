# Quick Start Guide

Get EPICcrypto running in 5 minutes!

## Option 1: Local Development (Fastest)

### Prerequisites
- Python 3.11+ installed
- Git installed

### Steps

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

4. **Run the app**
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

### 1. Select a Cryptocurrency
- Choose from Bitcoin, Ethereum, or other supported coins

### 2. Choose Timeframe
- **Short-term**: 1m, 5m, 15m (for day trading)
- **Medium-term**: 1h, 4h, 1d (for swing trading)
- **Long-term**: 1wk, 1mo (for position trading)

### 3. Get Analysis
- Click **"Analyze"** for single timeframe
- Click **"Multi-Timeframe Analysis"** for comprehensive view

### 4. Understand Results

**Recommendation**:
- 🟢 **BUY**: Strong positive signals
- 🔴 **SELL**: Strong negative signals
- 🟡 **HOLD**: Mixed or neutral signals

**Confidence**: How certain the AI is (higher is better)

**Technical Indicators**: Supporting data for the recommendation

---

## Quick API Test

### Using cURL
```bash
# Health check
curl http://localhost:5000/api/health

# Get Bitcoin prediction
curl "http://localhost:5000/api/prediction/BTC-USD?timeframe=1d"

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

---

## Troubleshooting

### Port Already in Use
```bash
# Change port in .env file
echo "PORT=8000" > .env

# Or run with custom port
PORT=8000 python app.py
```

### Dependencies Won't Install
```bash
# Upgrade pip
pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

### Can't Access from Other Devices
```bash
# Run with host 0.0.0.0
python app.py
# App will be accessible at http://YOUR_IP:5000
```

---

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [API_DOCS.md](API_DOCS.md) for API reference
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options
- Customize the app for your needs

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

## Getting Help

- **Issues**: https://github.com/Islamhassana3/EPICcrypto/issues
- **Documentation**: Check other .md files in repository
- **Logs**: Check console output for errors

---

## Disclaimer

⚠️ **Important**: This app provides predictions based on AI/ML models. It is NOT financial advice.

- Do your own research
- Understand the risks
- Only invest what you can afford to lose
- Cryptocurrency trading is highly volatile

---

Happy Trading! 📈🚀
