# 🏗️ Architecture Documentation

EPICcrypto system architecture and design decisions.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│                  (Frontend - HTML/CSS/JS)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     Flask Application                        │
│                      (app.py)                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼               ▼
┌──────────────┐ ┌──────────┐ ┌────────────────┐
│   API Layer  │ │  Models  │ │  Data Layer    │
│  (routes.py) │ │(predictor│ │  (crypto_api)  │
└──────┬───────┘ └────┬─────┘ └────────┬───────┘
       │              │                 │
       │              │                 │
       ▼              ▼                 ▼
┌──────────────────────────────────────────────┐
│              Cache Manager                    │
│           (In-Memory Caching)                 │
└──────────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼               ▼
┌──────────────┐ ┌──────────┐ ┌────────────┐
│  CoinGecko   │ │  Binance │ │ External   │
│     API      │ │   API    │ │  Services  │
└──────────────┘ └──────────┘ └────────────┘
```

## Component Architecture

### 1. Frontend Layer

**Location**: `frontend/`

**Components**:
- `templates/index.html` - Single-page application UI
- `static/css/styles.css` - Styling and responsive design
- `static/js/app.js` - Interactive JavaScript logic

**Responsibilities**:
- Display cryptocurrency data and predictions
- Handle user interactions (coin/timeframe selection)
- Make API calls to backend
- Render charts and visualizations
- Update UI dynamically

**Technology Stack**:
- Vanilla JavaScript (no frameworks)
- CSS3 with gradients and animations
- Responsive design (mobile-friendly)

### 2. Backend Layer

**Location**: `backend/`

#### 2.1 API Routes (`backend/api/routes.py`)

**Endpoints**:
- `/api/health` - Health check
- `/api/coins` - Supported cryptocurrencies
- `/api/price/{coin_id}` - Current price
- `/api/historical/{coin_id}` - Historical data
- `/api/predict/{coin_id}` - Predictions
- `/api/predict/{coin_id}/all` - All timeframes
- `/api/analyze/{coin_id}` - Technical analysis
- `/api/recommendation/{coin_id}` - Trading recommendations

**Responsibilities**:
- Handle HTTP requests
- Validate input parameters
- Coordinate between data and model layers
- Implement caching strategy
- Return JSON responses

#### 2.2 Data Layer (`backend/data/`)

**crypto_api.py**:
- CoinGecko API integration
- Binance API integration
- Real-time price fetching
- Historical data retrieval
- Error handling and retries

**preprocessor.py**:
- Data normalization
- Feature engineering
- Technical indicator calculation
- Time series preparation
- Data quality validation

#### 2.3 Model Layer (`backend/models/`)

**predictor.py**:

**Classes**:
- `CryptoPricePredictor`: Core prediction engine
- `MultiTimeframePredictor`: Multi-timeframe coordinator

**Models**:
- Random Forest Regressor
- Gradient Boosting Regressor
- Linear Regression
- ARIMA Time Series

**Prediction Methods**:
- Ensemble predictions
- Trend analysis
- Momentum analysis
- Time series forecasting

#### 2.4 Utilities (`backend/utils/`)

**cache.py**:
- In-memory caching with TTL
- Cache invalidation
- Performance optimization

### 3. Application Core

**app.py**:
- Flask application factory
- CORS configuration
- Blueprint registration
- Environment setup
- Server initialization

## Data Flow

### User Request Flow

```
1. User Action (UI)
   ↓
2. JavaScript Handler
   ↓
3. API Request (fetch)
   ↓
4. Flask Route Handler
   ↓
5. Check Cache
   ↓
6. [Cache Hit] → Return Cached Data
   |
   └─ [Cache Miss] → Fetch Fresh Data
                      ↓
                   7. Data API Layer
                      ↓
                   8. External API (CoinGecko/Binance)
                      ↓
                   9. Preprocess Data
                      ↓
                  10. ML Prediction
                      ↓
                  11. Cache Result
                      ↓
                  12. Return JSON
                      ↓
                  13. Update UI
```

### Prediction Pipeline

```
1. Fetch Historical Data
   ↓
2. Preprocess & Normalize
   ↓
3. Calculate Technical Indicators
   ↓
4. Prepare Features
   ↓
5. Apply ML Models (Parallel)
   ├─ Random Forest
   ├─ Gradient Boosting
   ├─ Linear Regression
   └─ ARIMA
   ↓
6. Ensemble Predictions
   ↓
7. Analyze Momentum
   ↓
8. Generate Recommendation
   ↓
9. Calculate Confidence Score
   ↓
10. Return Result
```

## Design Patterns

### 1. Factory Pattern
- `create_app()` in `app.py`
- Creates and configures Flask application
- Registers blueprints and middleware

### 2. Singleton Pattern
- Cache manager instances
- API client instances
- Predictor instances

### 3. Strategy Pattern
- Multiple prediction strategies
- Different data source strategies
- Timeframe-specific strategies

### 4. Facade Pattern
- `MultiTimeframePredictor` provides simple interface
- Hides complexity of multiple models
- Unified API for predictions

## Caching Strategy

### Cache Hierarchy

```
Level 1: API Response Cache (60-300s TTL)
   ├─ Price data: 60s
   ├─ Historical data: 300s
   ├─ Predictions: 60-120s
   └─ Technical analysis: 300s

Level 2: Data Processing Cache
   ├─ Preprocessed features
   ├─ Technical indicators
   └─ Model outputs
```

### Cache Invalidation

- Time-based (TTL)
- Manual cleanup on demand
- Automatic cleanup of expired entries

## Scalability Considerations

### Current Architecture (Single Instance)

**Capacity**:
- Supports 100+ concurrent users
- Handles 1000+ requests/hour
- Response time < 2s

**Limitations**:
- Single server instance
- In-memory cache (non-persistent)
- No load balancing

### Scaling Strategy (Future)

**Horizontal Scaling**:
```
┌─────────────────────────────────────┐
│         Load Balancer               │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│Instance│ │Instance│ │Instance│
│   1    │ │   2    │ │   3    │
└────┬───┘ └────┬───┘ └────┬───┘
     └──────────┼──────────┘
                ▼
         ┌─────────────┐
         │    Redis    │
         │   (Cache)   │
         └─────────────┘
```

**Improvements**:
- Redis for shared caching
- Database for user preferences
- WebSocket for real-time updates
- CDN for static assets
- Message queue for async tasks

## Security Architecture

### Current Implementation

**Input Validation**:
- Parameter type checking
- Path parameter sanitization
- Query parameter validation

**CORS**:
- Enabled for cross-origin requests
- Configurable origins

**Rate Limiting**:
- Built-in caching provides natural rate limiting
- External APIs have their own limits

**Environment Variables**:
- Secret key management
- Configuration externalization

### Security Enhancements (Future)

- API key authentication
- Request rate limiting
- Input sanitization
- SQL injection prevention (if adding database)
- XSS protection
- HTTPS enforcement
- Security headers

## Error Handling

### Error Flow

```
Error Occurs
   ↓
Caught by try/except
   ↓
Logged to console
   ↓
Return error JSON
   ↓
Display in UI
```

### Error Types

1. **API Errors**: External API failures
2. **Data Errors**: Invalid/insufficient data
3. **Model Errors**: Prediction failures
4. **Network Errors**: Connection issues

### Error Response Format

```json
{
  "error": "Error description",
  "details": "Additional context"
}
```

## Performance Optimization

### Current Optimizations

1. **Caching**: Reduce redundant API calls
2. **Lazy Loading**: Load data on demand
3. **Efficient Algorithms**: Optimized ML models
4. **Connection Pooling**: Reuse HTTP connections
5. **Minification**: Compressed frontend assets

### Metrics

- **API Response Time**: < 2s average
- **Cache Hit Rate**: ~80%
- **Memory Usage**: < 500MB
- **CPU Usage**: < 50% average

## Monitoring & Observability

### Logging

- Console logging for development
- Structured logging format
- Error stack traces

### Metrics (Future)

- Request count
- Response times
- Error rates
- Cache hit rates
- API usage

## Deployment Architecture

### Railway.app Deployment

```
GitHub Repository
      ↓
Railway Build System
      ↓
Docker Container
      ↓
Railway Runtime
      ↓
Public URL
```

**Configuration**:
- `railway.json`: Railway config
- `Procfile`: Process definition
- `runtime.txt`: Python version
- `requirements.txt`: Dependencies

### Environment

- Python 3.11+
- Gunicorn WSGI server
- 4 worker processes
- Auto-restart on failure

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **WSGI Server**: Gunicorn 21.2.0
- **ML Libraries**: scikit-learn 1.3.2
- **Time Series**: statsmodels 0.14.1
- **Data Processing**: pandas 2.1.4, numpy 1.26.2

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling
- **JavaScript ES6**: Interactive functionality

### APIs
- **CoinGecko API**: Cryptocurrency data
- **Binance API**: Real-time trading data

### Testing
- **pytest**: Unit testing framework

## Future Enhancements

### Phase 1: Foundation
- [x] Core prediction engine
- [x] Multi-timeframe support
- [x] Technical indicators
- [x] Web interface

### Phase 2: Enhancement
- [ ] WebSocket real-time updates
- [ ] Historical prediction accuracy tracking
- [ ] More cryptocurrencies
- [ ] Advanced charting

### Phase 3: Scale
- [ ] Redis caching
- [ ] User accounts
- [ ] Portfolio tracking
- [ ] Mobile app

### Phase 4: Intelligence
- [ ] Sentiment analysis
- [ ] Social media integration
- [ ] Advanced AI models
- [ ] Market trend detection

## Contributing

See `CONTRIBUTING.md` for development guidelines and architecture standards.

## References

- Flask Documentation: https://flask.palletsprojects.com/
- scikit-learn: https://scikit-learn.org/
- Railway.app: https://railway.app/
- CoinGecko API: https://www.coingecko.com/api/
- Binance API: https://binance-docs.github.io/

---

Last Updated: 2024-01-01
Version: 1.0.0
