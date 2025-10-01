# EPICcrypto Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                     (Web Browser - UI)                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/REST API
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      Flask Web Server                        │
│                         (app.py)                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   Routes & Controllers                               │   │
│  │   - GET /                 (Web UI)                    │   │
│  │   - GET /api/coins        (List coins)                │   │
│  │   - GET /api/prediction/<symbol> (Single prediction)  │   │
│  │   - GET /api/multi-timeframe/<symbol> (Multi analysis)│   │
│  │   - GET /api/health       (Health check)              │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────┬──────────────────────────┬──────────────────┘
                │                          │
                │                          │
    ┌───────────▼──────────┐   ┌───────────▼──────────┐
    │   CryptoDataService  │   │     AIPredictor      │
    │  (crypto_data.py)    │   │  (ai_predictor.py)   │
    │                      │   │                      │
    │  - Fetch OHLCV data  │   │  - Feature prep      │
    │  - yfinance API      │   │  - Rule-based ML     │
    │  - Technical analysis│   │  - Signal aggregation│
    │  - SMA, RSI, MACD    │   │  - Recommendations   │
    │  - Bollinger Bands   │   │  - Confidence scores │
    └───────────┬──────────┘   └──────────────────────┘
                │
                │
    ┌───────────▼──────────┐
    │    yfinance API      │
    │  - Real-time prices  │
    │  - Historical data   │
    │  - 8+ cryptos        │
    └──────────────────────┘
```

## Component Details

### 1. Frontend (User Interface)
- Technologies: HTML5, CSS3, Vanilla JavaScript (no frameworks)
- Files:
  - templates/index.html – Main UI
  - static/css/style.css – Responsive styling with gradients/animations
  - static/js/app.js – Interactive logic, API calls, charts
- Features:
  - Cryptocurrency selector and timeframe selector (8 options)
  - Single and multi-timeframe analysis
  - Results with recommendations and indicators
  - Responsive design (mobile-friendly)

### 2. Backend (Flask Application)
- File: app.py
- Technologies: Flask 3, Flask-CORS, Gunicorn (production)
- Responsibilities: serve UI, handle API routes, coordinate services, error handling, JSON responses
- API Endpoints:
  - GET /                       – Serve web UI
  - GET /api/coins              – List supported coins
  - GET /api/prediction/<symbol>?timeframe=… – Single timeframe prediction
  - GET /api/multi-timeframe/<symbol>        – All timeframes analysis
  - GET /api/health             – Health check

### 3. Data Service Layer
- File: services/crypto_data.py
- Class: CryptoDataService
- Responsibilities:
  - Fetch crypto data via yfinance
  - Handle timeframes (1m to 1mo)
  - Calculate indicators (SMA 20/50, RSI, MACD, Bollinger Bands)
  - Validation and error handling

### 4. AI/ML Prediction Layer
- File: services/ai_predictor.py
- Class: AIPredictor
- Responsibilities:
  - Feature engineering from OHLCV + indicators
  - Rule-based signal analysis (trend, momentum, RSI, MACD, volume)
  - Generate BUY/HOLD/SELL recommendation
  - Confidence score based on signal agreement (0.5–0.75)

## Data Flows

### Single Prediction Request
1) Frontend → GET /api/prediction/BTC-USD?timeframe=1d
2) Flask routes → CryptoDataService.get_historical_data
3) yfinance fetch → indicators → AIPredictor.predict
4) Return JSON → Frontend renders results

### Multi-Timeframe Analysis
1) Frontend → GET /api/multi-timeframe/BTC-USD
2) Loop over timeframes [1m, 5m, 15m, 1h, 4h, 1d, 1wk, 1mo]
3) Fetch data + run prediction per timeframe
4) Return aggregated results → Grid UI

## Caching & Performance
- In-memory caching for API responses within the process
- Typical TTLs: price (60s), historical (300s), predictions (60–120s)
- Current targets: <2s response time, ~80% cache hit under load
- Future: Redis for shared caching across instances

## Deployment
- Railway.app with GitHub auto-deploy
- Python 3.11, Gunicorn WSGI server, dynamic $PORT
- Config files: railway.json, Procfile, runtime.txt, requirements.txt

## Security
- Input validation for symbols/timeframes
- CORS enabled with configurable origins
- No sensitive data persisted; stateless service
- Future: API key auth, rate limiting, HTTPS enforcement, security headers

## Technology Stack
- Backend: Flask 3, Gunicorn 21, pandas 2.1, numpy 1.26
- ML/Analysis: Rule-based signals; statsmodels/scikit-learn optional for future use
- Data: yfinance (Yahoo Finance)
- Frontend: HTML5, CSS3, JavaScript ES6
- Testing: pytest

## Scalability
- Current: single instance, in-memory cache
- Future: horizontal scaling behind load balancer + Redis; CDN for static assets; background workers for heavy tasks

## Future Enhancements
- LSTM-based deep learning (planned)
- Redis caching and metrics/monitoring (Sentry/New Relic)
- More cryptocurrencies, accuracy tracking, WebSocket updates

Last Updated: 2025-10-01
Version: 1.1.0