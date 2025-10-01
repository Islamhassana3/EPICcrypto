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
│  │   - GET /                 (Web UI)                  │   │
│  │   - GET /api/coins        (List coins)              │   │
│  │   - GET /api/prediction   (Single prediction)       │   │
│  │   - GET /api/multi-timeframe (Multi analysis)       │   │
│  │   - GET /api/health       (Health check)            │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────┬──────────────────────────┬──────────────────┘
                │                          │
                │                          │
    ┌───────────▼──────────┐   ┌───────────▼──────────┐
    │   CryptoDataService  │   │     AIPredictor      │
    │  (crypto_data.py)    │   │  (ai_predictor.py)   │
    │                      │   │                      │
    │  - Fetch OHLCV data  │   │  - Feature prep      │
    │  - Yahoo Finance API │   │  - ML predictions    │
    │  - Technical analysis│   │  - Signal aggregation│
    │  - SMA, RSI, MACD    │   │  - Recommendations   │
    │  - Bollinger Bands   │   │  - Confidence scores │
    └───────────┬──────────┘   └──────────────────────┘
                │
                │
    ┌───────────▼──────────┐
    │   Yahoo Finance API  │
    │     (yfinance)       │
    │                      │
    │  - Real-time prices  │
    │  - Historical data   │
    │  - 8+ cryptocurrencies│
    └──────────────────────┘
```

---

## Component Details

### 1. Frontend (User Interface)

**Technologies**: HTML5, CSS3, Vanilla JavaScript

**Components**:
- `templates/index.html` - Main HTML structure
- `static/css/style.css` - Responsive styling with gradients
- `static/js/app.js` - Interactive functionality

**Features**:
- Cryptocurrency selector (dropdown)
- Timeframe selector (8 options)
- Analysis buttons (single & multi-timeframe)
- Results display with colored recommendations
- Technical indicators visualization
- Responsive design (mobile-friendly)

**User Flow**:
```
User arrives → Select coin → Choose timeframe → Click Analyze
              ↓
         API request sent
              ↓
         Display loading spinner
              ↓
         Receive & display results
              ↓
         Show recommendation + indicators
```

---

### 2. Backend (Flask Application)

**File**: `app.py`

**Technologies**: Flask, Flask-CORS

**Responsibilities**:
- Serve web interface
- Handle API requests
- Coordinate services
- Error handling
- Response formatting

**API Endpoints**:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serve web UI |
| `/api/coins` | GET | List supported coins |
| `/api/prediction/<symbol>` | GET | Single timeframe prediction |
| `/api/multi-timeframe/<symbol>` | GET | All timeframes analysis |
| `/api/health` | GET | Health check |

---

### 3. Data Service Layer

**File**: `services/crypto_data.py`

**Class**: `CryptoDataService`

**Responsibilities**:
- Fetch cryptocurrency data from Yahoo Finance
- Handle different timeframes (1m to 1mo)
- Calculate technical indicators
- Data validation and error handling

**Key Methods**:
```python
get_historical_data(symbol, timeframe, limit)
  → Returns: DataFrame with OHLCV data

calculate_technical_indicators(data)
  → Returns: Dict with SMA, RSI, MACD, BB
```

**Technical Indicators**:
- **SMA (20, 50)**: Simple Moving Averages for trend
- **RSI**: Relative Strength Index (overbought/oversold)
- **MACD**: Moving Average Convergence Divergence
- **Bollinger Bands**: Volatility and price levels

---

### 4. AI/ML Prediction Layer

**File**: `services/ai_predictor.py`

**Class**: `AIPredictor`

**Responsibilities**:
- Feature engineering from raw data
- Pattern recognition
- Signal aggregation
- Generate recommendations
- Calculate confidence scores

**Prediction Algorithm**:

```
1. Prepare Features
   ├─ Price returns
   ├─ Moving averages (5, 10, 20)
   ├─ Momentum indicators
   ├─ RSI
   ├─ MACD
   ├─ Volatility
   └─ Volume ratios

2. Analyze Signals
   ├─ Trend analysis (SMA crossovers)
   ├─ RSI levels (oversold/overbought)
   ├─ MACD crossovers
   └─ Volume confirmation

3. Score Calculation
   ├─ Trend score: +1 or -1
   ├─ RSI score: +1, 0, or -1
   ├─ MACD score: +1 or -1
   ├─ Volume score: +1 or 0
   └─ Overall: Sum of scores

4. Generate Recommendation
   ├─ Score ≥ 2: BUY
   ├─ Score ≤ -2: SELL
   └─ Otherwise: HOLD

5. Calculate Confidence
   └─ Based on signal agreement (0.5 to 0.75)
```

---

## Data Flow

### Single Prediction Request

```
1. User clicks "Analyze" button
         ↓
2. Frontend sends: GET /api/prediction/BTC-USD?timeframe=1d
         ↓
3. Flask receives request
         ↓
4. CryptoDataService.get_historical_data("BTC-USD", "1d")
         ↓
5. Yahoo Finance API fetches data
         ↓
6. CryptoDataService calculates technical indicators
         ↓
7. AIPredictor.predict(data, "1d")
         ↓
8. AIPredictor prepares features & analyzes
         ↓
9. AIPredictor generates recommendation
         ↓
10. Flask formats & returns JSON response
         ↓
11. Frontend displays results with styling
```

### Multi-Timeframe Analysis

```
1. User clicks "Multi-Timeframe Analysis"
         ↓
2. Frontend sends: GET /api/multi-timeframe/BTC-USD
         ↓
3. Flask loops through timeframes: [1m, 5m, 15m, 1h, 4h, 1d, 1wk, 1mo]
         ↓
4. For each timeframe:
   ├─ Fetch data
   ├─ Run prediction
   └─ Collect results
         ↓
5. Flask returns all predictions
         ↓
6. Frontend displays grid of timeframe cards
```

---

## Machine Learning Approach

### Current Implementation: Hybrid ML

**Technique**: Rule-based ML with technical analysis

**Advantages**:
- No training data required
- Real-time predictions
- Interpretable results
- Low latency
- Works immediately

**How It Works**:

1. **Feature Extraction**
   - Calculate 10+ technical features
   - Normalize price movements
   - Analyze volume patterns

2. **Signal Aggregation**
   - Multiple independent signals
   - Weighted scoring system
   - Majority voting concept

3. **Confidence Calculation**
   - Agreement among indicators
   - Trend strength
   - Volume confirmation

### Future Enhancement: Deep Learning (LSTM)

**Planned**: Long Short-Term Memory networks

```python
# Future LSTM architecture
Model:
  Input Layer (features) → 
  LSTM Layer (64 units) → 
  Dropout (0.2) → 
  LSTM Layer (32 units) → 
  Dropout (0.2) → 
  Dense Layer (1 unit) → 
  Output (price prediction)
```

---

## Deployment Architecture

### Railway.app Deployment

```
┌─────────────────────────────────────────┐
│         Railway.app Platform            │
│  ┌───────────────────────────────────┐ │
│  │   GitHub Repository Integration   │ │
│  │   (Auto-deploy on push)           │ │
│  └───────────────┬───────────────────┘ │
│                  │                      │
│  ┌───────────────▼───────────────────┐ │
│  │   Build Process                   │ │
│  │   - Detect Python                 │ │
│  │   - Install requirements.txt      │ │
│  │   - Prepare environment           │ │
│  └───────────────┬───────────────────┘ │
│                  │                      │
│  ┌───────────────▼───────────────────┐ │
│  │   Container Instance              │ │
│  │   - Python 3.11                   │ │
│  │   - Gunicorn WSGI server          │ │
│  │   - Flask application             │ │
│  │   - Port: $PORT (dynamic)         │ │
│  └───────────────┬───────────────────┘ │
│                  │                      │
│  ┌───────────────▼───────────────────┐ │
│  │   HTTPS Load Balancer             │ │
│  │   - SSL/TLS termination           │ │
│  │   - Custom domain support         │ │
│  └───────────────┬───────────────────┘ │
└──────────────────┼──────────────────────┘
                   │
                   ▼
            Public Internet
       (your-app.railway.app)
```

---

## Security Considerations

### Current Security Measures

1. **CORS Configuration**
   - Flask-CORS enabled
   - Configurable origins

2. **Input Validation**
   - Cryptocurrency symbols validated
   - Timeframe parameters sanitized

3. **Error Handling**
   - Try-catch blocks throughout
   - No sensitive data in error messages

4. **No Data Storage**
   - Stateless application
   - No user data collected
   - No API keys required

### Recommended Enhancements

1. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

2. **API Key Authentication** (for production)
   ```python
   @app.before_request
   def check_api_key():
       if request.headers.get('X-API-Key') != API_KEY:
           abort(401)
   ```

3. **HTTPS Enforcement**
   ```python
   from flask_talisman import Talisman
   Talisman(app, force_https=True)
   ```

---

## Performance Optimization

### Current Optimizations

1. **Efficient Data Fetching**
   - Limited historical data (100 points)
   - Caching opportunity in service layer

2. **Minimal Dependencies**
   - Only essential packages
   - Fast startup time

3. **Lightweight Frontend**
   - No heavy frameworks
   - Vanilla JavaScript
   - Optimized CSS

### Recommended Improvements

1. **Redis Caching**
   ```python
   # Cache predictions for 60 seconds
   @cache.memoize(timeout=60)
   def get_prediction(symbol, timeframe):
       ...
   ```

2. **Database for Historical Data**
   - Store past predictions
   - Track accuracy
   - Faster response times

3. **CDN for Static Assets**
   - Serve CSS/JS from CDN
   - Faster global access

---

## Monitoring & Logging

### Current Logging

```python
# Console logging for errors
print(f"Error: {error_message}")
```

### Recommended Monitoring

1. **Application Monitoring**
   - Sentry for error tracking
   - New Relic for performance

2. **Health Checks**
   - `/api/health` endpoint exists
   - Can add detailed health info

3. **Metrics Collection**
   ```python
   # Track prediction requests
   # Monitor response times
   # Log accuracy (if feedback available)
   ```

---

## Scalability

### Current Architecture

- **Stateless**: Easy to scale horizontally
- **No database**: Simple deployment
- **External API**: Yahoo Finance handles data load

### Scaling Strategy

```
Low Traffic (< 100 users)
  → Single instance on Railway.app

Medium Traffic (100-1000 users)
  → Add Redis caching
  → Multiple instances with load balancer

High Traffic (1000+ users)
  → Database for data persistence
  → Separate API and frontend
  → CDN for static assets
  → Background workers for predictions
```

---

## Technology Choices - Rationale

| Technology | Why Chosen |
|------------|------------|
| **Python** | Best for ML/AI, extensive libraries |
| **Flask** | Lightweight, easy to deploy, flexible |
| **yfinance** | Free, reliable crypto data, no API key |
| **scikit-learn** | Industry standard ML library |
| **Vanilla JS** | Fast, no build step, easy to understand |
| **Railway.app** | Easiest deployment, free tier, auto-deploy |
| **Gunicorn** | Production-ready WSGI server |

---

## Future Enhancements Roadmap

### Phase 1: Core Improvements
- [ ] Add LSTM deep learning models
- [ ] Implement Redis caching
- [ ] Add more cryptocurrencies (50+)
- [ ] Historical accuracy tracking

### Phase 2: Features
- [ ] User accounts and portfolios
- [ ] Price alerts (email/SMS)
- [ ] Real-time WebSocket updates
- [ ] Trading simulation mode

### Phase 3: Advanced AI
- [ ] Sentiment analysis (Twitter, Reddit)
- [ ] News impact analysis
- [ ] Ensemble model predictions
- [ ] Backtesting framework

### Phase 4: Platform
- [ ] Mobile app (React Native)
- [ ] Browser extension
- [ ] Trading bot integration
- [ ] API marketplace

---

## Contributing to Architecture

If you want to improve the architecture:

1. **Maintain Simplicity**: Keep deployment easy
2. **Document Changes**: Update this file
3. **Test Thoroughly**: Ensure changes work
4. **Consider Scale**: Think about performance
5. **Security First**: Always validate inputs

---

Last Updated: 2024
