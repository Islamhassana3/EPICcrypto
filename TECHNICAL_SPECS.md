# Technical Specifications

## System Requirements

### Development Environment
- **Python**: 3.11 or higher
- **RAM**: Minimum 2GB, Recommended 4GB
- **Disk Space**: 500MB for application and dependencies
- **Network**: Internet connection for API access

### Production Environment
- **Platform**: Railway.app, Heroku, or Docker-compatible
- **Python**: 3.11
- **Memory**: 512MB minimum
- **CPU**: 1 core minimum
- **Bandwidth**: ~100MB/day for typical usage

---

## Technology Stack

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Runtime | Python | 3.11+ | Core language |
| Web Framework | Flask | 3.0.0 | HTTP server & routing |
| WSGI Server | Gunicorn | 21.2.0+ | Production server |
| CORS | Flask-CORS | 4.0.0+ | Cross-origin requests |

### Data & ML
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Data Processing | Pandas | 2.1.0+ | Data manipulation |
| Numerical Computing | NumPy | 1.26.0+ | Mathematical operations |
| Machine Learning | scikit-learn | 1.3.2+ | ML algorithms |
| Data Source | yfinance | 0.2.33+ | Crypto price data |

### Frontend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Structure | HTML5 | Semantic markup |
| Styling | CSS3 | Visual design |
| Interactivity | Vanilla JavaScript | Dynamic behavior |
| HTTP Client | Fetch API | API communication |

---

## API Specifications

### Endpoints

#### 1. Health Check
```
GET /api/health
```
**Response Time**: < 100ms  
**Rate Limit**: Unlimited  
**Cache**: No

**Response Structure**:
```json
{
  "status": "healthy",
  "service": "EPICcrypto"
}
```

#### 2. List Coins
```
GET /api/coins
```
**Response Time**: < 100ms  
**Rate Limit**: 100/hour recommended  
**Cache**: 1 hour

**Response Structure**:
```json
[
  {
    "symbol": "string",
    "name": "string"
  }
]
```

#### 3. Single Prediction
```
GET /api/prediction/<symbol>?timeframe=<tf>
```
**Response Time**: 2-5 seconds  
**Rate Limit**: 10/minute recommended  
**Cache**: 60 seconds

**Parameters**:
- `symbol`: Required, string (e.g., "BTC-USD")
- `timeframe`: Optional, string (default: "1d")

**Response Structure**:
```json
{
  "symbol": "string",
  "timeframe": "string",
  "current_price": float,
  "predicted_price": float,
  "price_change_percent": float,
  "recommendation": "BUY|SELL|HOLD",
  "confidence": float (0.0-1.0),
  "technical_indicators": {
    "sma_20": float,
    "sma_50": float,
    "rsi": float,
    "macd": float,
    "macd_signal": float,
    "bb_upper": float,
    "bb_lower": float
  }
}
```

#### 4. Multi-Timeframe
```
GET /api/multi-timeframe/<symbol>
```
**Response Time**: 10-20 seconds  
**Rate Limit**: 5/minute recommended  
**Cache**: 120 seconds

**Response Structure**:
```json
{
  "symbol": "string",
  "predictions": {
    "1m|5m|15m|1h|4h|1d|1wk|1mo": {
      "recommendation": "BUY|SELL|HOLD",
      "confidence": float,
      "predicted_price": float,
      "price_change_percent": float
    }
  }
}
```

---

## Data Specifications

### Historical Data Requirements

| Timeframe | Period | Interval | Min Points |
|-----------|--------|----------|------------|
| 1 Minute | 1 day | 1m | 30 |
| 5 Minutes | 5 days | 5m | 30 |
| 15 Minutes | 5 days | 15m | 30 |
| 1 Hour | 1 month | 1h | 30 |
| 4 Hours | 3 months | 1h→4h | 30 |
| 1 Day | 1 year | 1d | 50 |
| 1 Week | 2 years | 1wk | 30 |
| 1 Month | 5 years | 1mo | 30 |

### OHLCV Data Structure
```python
DataFrame columns:
- Date (index): datetime
- Open: float64
- High: float64
- Low: float64
- Close: float64
- Volume: int64
```

---

## Machine Learning Model

### Algorithm: Hybrid Technical Analysis + ML

#### Feature Engineering
```python
Features (10 total):
1. returns: price_t / price_(t-1) - 1
2. sma_5: Simple moving average (5 periods)
3. sma_10: Simple moving average (10 periods)
4. sma_20: Simple moving average (20 periods)
5. momentum: price_t - price_(t-4)
6. rsi: Relative Strength Index (14 periods)
7. macd: EMA(12) - EMA(26)
8. volatility: std(close, 10 periods)
9. volume_ratio: volume / sma(volume, 5)
10. high_low_ratio: (close - low) / (high - low)
```

#### Signal Generation
```python
Scoring System:
- Trend Score: -1 to +2
  * SMA5 > SMA20: +1
  * Price > SMA5: +1
  
- RSI Score: -1 to +1
  * RSI < 30: +1 (oversold)
  * RSI > 70: -1 (overbought)
  * Otherwise: 0
  
- MACD Score: -1 to +1
  * MACD > 0: +1
  * MACD < 0: -1
  
- Volume Score: 0 to +1
  * Volume Ratio > 1.2: +1
  * Otherwise: 0

Total Score Range: -3 to +5
```

#### Recommendation Logic
```python
if total_score >= 2:
    recommendation = "BUY"
    confidence = min(0.75, 0.5 + score * 0.05)
elif total_score <= -2:
    recommendation = "SELL"
    confidence = min(0.75, 0.5 + abs(score) * 0.05)
else:
    recommendation = "HOLD"
    confidence = 0.5
```

#### Price Prediction
```python
predicted_return = recent_mean_return * adjustment_factor
adjustment_factor:
  - BUY: 1.5 (amplify positive trend)
  - SELL: 1.5 (amplify negative trend)
  - HOLD: 1.0 (maintain current trend)

predicted_price = current_price * (1 + predicted_return)
```

---

## Performance Specifications

### Response Times

| Operation | Target | Maximum |
|-----------|--------|---------|
| Static page load | < 500ms | 1s |
| Health check | < 100ms | 200ms |
| List coins | < 100ms | 200ms |
| Single prediction | 2-3s | 10s |
| Multi-timeframe | 10-15s | 30s |

### Throughput

| Metric | Development | Production |
|--------|------------|-----------|
| Concurrent users | 1-5 | 10-100 |
| Requests/second | 1-2 | 10-50 |
| Daily predictions | 100-1000 | 10,000+ |

### Reliability

| Metric | Target |
|--------|--------|
| Uptime | 99%+ |
| Error rate | < 1% |
| API success rate | > 95% |

---

## Security Specifications

### Input Validation

```python
# Cryptocurrency Symbol
Pattern: ^[A-Z0-9]+-USD$
Max length: 20 characters
Allowed: Alphanumeric + hyphen

# Timeframe
Allowed values: ["1m", "5m", "15m", "1h", "4h", "1d", "1wk", "1mo"]
Default: "1d"
```

### CORS Configuration

```python
Origins: "*" (development) or specific domains (production)
Methods: ["GET", "POST", "OPTIONS"]
Headers: ["Content-Type"]
```

### Rate Limiting (Recommended)

```python
Global: 100 requests/hour/IP
Prediction: 10 requests/minute/IP
Multi-timeframe: 5 requests/minute/IP
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Valid prediction returned |
| 400 | Bad Request | Invalid symbol format |
| 404 | Not Found | Coin data unavailable |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal processing error |
| 503 | Service Unavailable | External API down |

### Error Response Format

```json
{
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional context"
  }
}
```

---

## Database Specifications

### Current: No Database
- Stateless application
- No data persistence
- All data from external API

### Future: Optional Database

**Recommended**: PostgreSQL 14+

**Schema**:
```sql
-- Predictions history
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    predicted_at TIMESTAMP NOT NULL,
    current_price DECIMAL(18, 8),
    predicted_price DECIMAL(18, 8),
    recommendation VARCHAR(10),
    confidence DECIMAL(3, 2),
    actual_price DECIMAL(18, 8),
    INDEX idx_symbol_time (symbol, predicted_at)
);

-- User settings (if auth added)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    preferences JSONB
);
```

---

## Caching Strategy

### Recommended Redis Configuration

```python
Cache Structure:
{
  "prediction:{symbol}:{timeframe}": {
    "data": {...},
    "ttl": 60  # seconds
  },
  "historical:{symbol}:{timeframe}": {
    "data": DataFrame,
    "ttl": 300  # seconds
  }
}
```

---

## Monitoring & Logging

### Metrics to Track

**Application Metrics**:
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (percentage)
- Active users

**Business Metrics**:
- Predictions generated
- Most popular coins
- Most used timeframes
- Recommendation distribution (BUY/SELL/HOLD)

**Infrastructure Metrics**:
- CPU usage
- Memory usage
- Network I/O
- Disk I/O

### Log Levels

```python
DEBUG: Detailed diagnostic information
INFO: General application flow
WARNING: Unexpected but handled situations
ERROR: Serious issues requiring attention
CRITICAL: System failure imminent
```

### Log Format

```
[TIMESTAMP] [LEVEL] [MODULE] [MESSAGE] [CONTEXT]

Example:
[2024-01-15 10:30:45] [INFO] [app] Prediction requested for BTC-USD, timeframe=1d
[2024-01-15 10:30:47] [INFO] [ai_predictor] Generated BUY recommendation with 75% confidence
```

---

## Deployment Specifications

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| PORT | No | 5000 | Application port |
| FLASK_ENV | No | production | Flask environment |
| LOG_LEVEL | No | INFO | Logging level |
| CORS_ORIGINS | No | * | Allowed CORS origins |

### Build Process

```bash
1. Clone repository
2. Install Python 3.11
3. pip install -r requirements.txt
4. Set environment variables
5. gunicorn app:app
```

### Health Check Endpoint

```
Path: /api/health
Method: GET
Expected: 200 OK with JSON body
Timeout: 5 seconds
```

---

## Testing Specifications

### Unit Tests

```python
# Services
test_crypto_data.py
  - test_get_historical_data()
  - test_calculate_technical_indicators()
  - test_invalid_symbol()

test_ai_predictor.py
  - test_prepare_features()
  - test_predict()
  - test_confidence_calculation()
```

### Integration Tests

```python
test_api.py
  - test_health_endpoint()
  - test_coins_endpoint()
  - test_prediction_endpoint()
  - test_multi_timeframe_endpoint()
  - test_error_handling()
```

### Load Tests

```python
Scenarios:
1. 10 concurrent users, 1 minute
2. 100 sequential predictions
3. 50 multi-timeframe requests
```

---

## Version History

### v1.0.0 (Current)
- Initial release
- 8 supported cryptocurrencies
- 8 timeframes
- Technical analysis + ML
- Web UI
- REST API

### Planned v1.1.0
- LSTM deep learning model
- Redis caching
- Rate limiting
- 50+ cryptocurrencies

### Planned v2.0.0
- User authentication
- Portfolio tracking
- Price alerts
- Mobile app

---

## Compliance & Legal

### Data Privacy
- No personal data collected
- No cookies used
- No tracking implemented
- All data from public APIs

### Disclaimer
Application provides predictions for educational purposes only.
Not financial advice. Users responsible for their trading decisions.

---

## Support & Maintenance

### Update Frequency
- Dependencies: Monthly security updates
- Features: Quarterly releases
- Bug fixes: As needed

### Backup Strategy
- Code: Git repository
- No user data to backup
- Configuration: Environment variables

---

Last Updated: 2024
Version: 1.0.0
