# 📡 API Documentation

Complete API reference for the EPICcrypto AI Crypto Prediction Platform.

## Base URL

**Local Development:**
```
http://localhost:5000/api
```

**Production (Railway):**
```
https://your-app.railway.app/api
```

## Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

## Rate Limiting

The API implements internal caching to minimize requests to external APIs:
- Price data: Cached for 60 seconds
- Historical data: Cached for 5 minutes
- Technical analysis: Cached for 5 minutes
- Predictions: Cached for 60-120 seconds

## Response Format

All responses are in JSON format.

### Success Response
```json
{
  "data": {},
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error message description"
}
```

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "crypto-prediction-api",
  "version": "1.0.0"
}
```

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

### 2. Get Supported Coins

Retrieve list of supported cryptocurrencies.

**Endpoint:** `GET /api/coins`

**Response:**
```json
{
  "popular": [
    {
      "id": "bitcoin",
      "symbol": "btc",
      "name": "Bitcoin"
    },
    {
      "id": "ethereum",
      "symbol": "eth",
      "name": "Ethereum"
    }
  ],
  "all": [
    // Array of 100+ coins
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/coins
```

---

### 3. Get Current Price

Get real-time price data for a cryptocurrency.

**Endpoint:** `GET /api/price/{coin_id}`

**Parameters:**
- `coin_id` (path parameter): Coin identifier (e.g., "bitcoin", "ethereum")

**Response:**
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

**Example:**
```bash
curl http://localhost:5000/api/price/bitcoin
```

---

### 4. Get Historical Data

Retrieve historical price data.

**Endpoint:** `GET /api/historical/{coin_id}`

**Parameters:**
- `coin_id` (path parameter): Coin identifier
- `days` (query parameter, optional): Number of days of history (default: 30)

**Response:**
```json
{
  "coin_id": "bitcoin",
  "days": 30,
  "data": [
    {
      "timestamp": "2024-01-01T00:00:00",
      "price": 42000.00,
      "volume": 25000000000,
      "market_cap": 820000000000
    },
    // More data points...
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/historical/bitcoin?days=7
```

---

### 5. Get Prediction

Generate AI prediction for a specific timeframe.

**Endpoint:** `GET /api/predict/{coin_id}`

**Parameters:**
- `coin_id` (path parameter): Coin identifier
- `timeframe` (query parameter, optional): Prediction timeframe (default: "1h")
  - Valid values: `1m`, `5m`, `10m`, `30m`, `1h`, `daily`, `monthly`, `yearly`

**Response:**
```json
{
  "coin_id": "bitcoin",
  "prediction": {
    "timeframe": "1h",
    "current_price": 43250.50,
    "trend_prediction": {
      "predictions": [43500.00],
      "trend": "bullish",
      "slope": 15.5,
      "confidence": 0.85
    },
    "arima_prediction": {
      "predictions": [43480.00],
      "method": "ARIMA",
      "aic": 1234.56
    },
    "momentum_analysis": {
      "momentum": 3.2,
      "volatility": 0.025,
      "recent_avg": 43200.00,
      "signal": "buy"
    },
    "recommendation": {
      "action": "buy",
      "confidence": 0.75,
      "reason": "Trend: bullish, Momentum: buy",
      "score": 3
    }
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/predict/bitcoin?timeframe=1h
```

---

### 6. Get All Timeframe Predictions

Generate predictions for all supported timeframes.

**Endpoint:** `GET /api/predict/{coin_id}/all`

**Parameters:**
- `coin_id` (path parameter): Coin identifier

**Response:**
```json
{
  "coin_id": "bitcoin",
  "predictions": {
    "1m": {
      "timeframe": "1m",
      "current_price": 43250.50,
      "recommendation": {
        "action": "hold",
        "confidence": 0.60
      }
    },
    "5m": { /* ... */ },
    "10m": { /* ... */ },
    "30m": { /* ... */ },
    "1h": { /* ... */ },
    "daily": { /* ... */ },
    "monthly": { /* ... */ },
    "yearly": { /* ... */ }
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/predict/bitcoin/all
```

---

### 7. Get Technical Analysis

Get comprehensive technical analysis with indicators.

**Endpoint:** `GET /api/analyze/{coin_id}`

**Parameters:**
- `coin_id` (path parameter): Coin identifier

**Response:**
```json
{
  "coin_id": "bitcoin",
  "current_price": 43250.50,
  "indicators": {
    "MA_7": 43100.00,
    "MA_25": 42800.00,
    "RSI": 65.4,
    "MACD": 125.5,
    "Volatility": 0.025
  },
  "technical_analysis": {
    "RSI": "Neutral",
    "MA_Cross": "Bullish - Short MA above long MA",
    "MACD": "Bullish momentum"
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/analyze/bitcoin
```

---

### 8. Get Recommendation

Get trading recommendation for a specific timeframe.

**Endpoint:** `GET /api/recommendation/{coin_id}`

**Parameters:**
- `coin_id` (path parameter): Coin identifier
- `timeframe` (query parameter, optional): Timeframe for recommendation (default: "1h")

**Response:**
```json
{
  "coin_id": "bitcoin",
  "timeframe": "1h",
  "recommendation": {
    "action": "buy",
    "confidence": 0.75,
    "reason": "Trend: bullish, Momentum: buy",
    "score": 3
  },
  "current_price": 43250.50,
  "timestamp": "2024-01-01T12:00:00"
}
```

**Example:**
```bash
curl http://localhost:5000/api/recommendation/bitcoin?timeframe=1h
```

---

## Recommendation Actions

The API returns the following recommendation actions:

| Action | Score Range | Description |
|--------|-------------|-------------|
| `strong_buy` | ≥ 3 | High confidence bullish signals |
| `buy` | 1 to 2 | Moderate bullish signals |
| `hold` | -1 to 1 | Neutral or mixed signals |
| `sell` | -2 to -1 | Moderate bearish signals |
| `strong_sell` | ≤ -3 | High confidence bearish signals |

## Timeframes

| Timeframe | Interval | Data Points | Best For |
|-----------|----------|-------------|----------|
| `1m` | 1 minute | 60 | Scalping |
| `5m` | 5 minutes | 100 | Day trading |
| `10m` | 5 minutes | 120 | Short-term |
| `30m` | 30 minutes | 100 | Intraday |
| `1h` | 1 hour | 100 | Swing trading |
| `daily` | 1 day | 30 | Position trading |
| `monthly` | 1 day | 90 | Long-term |
| `yearly` | 1 day | 365 | Investment |

## Technical Indicators

### RSI (Relative Strength Index)
- Range: 0-100
- Overbought: > 70
- Oversold: < 30
- Neutral: 30-70

### MACD (Moving Average Convergence Divergence)
- Positive: Bullish momentum
- Negative: Bearish momentum

### Moving Averages
- MA_7: 7-day simple moving average
- MA_25: 25-day simple moving average
- MA_50: 50-day simple moving average

### Volatility
- Low: < 0.02
- Moderate: 0.02-0.05
- High: > 0.05

## Error Codes

| HTTP Code | Description |
|-----------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Coin not found |
| 500 | Internal Server Error |

## Common Error Responses

### Coin Not Found
```json
{
  "error": "Failed to fetch price data"
}
```

### Invalid Timeframe
```json
{
  "error": "Invalid timeframe: 2h"
}
```

### Insufficient Data
```json
{
  "error": "Insufficient data for prediction"
}
```

## Best Practices

1. **Caching**: Implement client-side caching to reduce API calls
2. **Error Handling**: Always handle errors gracefully
3. **Rate Limiting**: Respect the built-in caching mechanisms
4. **Timeframe Selection**: Choose appropriate timeframe for your use case
5. **Multiple Indicators**: Use multiple endpoints for comprehensive analysis

## Example Integration

### Python
```python
import requests

BASE_URL = "http://localhost:5000/api"

# Get prediction
response = requests.get(f"{BASE_URL}/predict/bitcoin?timeframe=1h")
data = response.json()

if 'error' not in data:
    recommendation = data['prediction']['recommendation']
    print(f"Action: {recommendation['action']}")
    print(f"Confidence: {recommendation['confidence']}")
else:
    print(f"Error: {data['error']}")
```

### JavaScript
```javascript
const BASE_URL = 'http://localhost:5000/api';

async function getPrediction(coinId, timeframe) {
  const response = await fetch(
    `${BASE_URL}/predict/${coinId}?timeframe=${timeframe}`
  );
  const data = await response.json();
  
  if (data.error) {
    console.error('Error:', data.error);
    return null;
  }
  
  return data.prediction;
}

// Usage
const prediction = await getPrediction('bitcoin', '1h');
console.log('Recommendation:', prediction.recommendation);
```

### cURL
```bash
# Get all data for Bitcoin
curl http://localhost:5000/api/price/bitcoin
curl http://localhost:5000/api/predict/bitcoin?timeframe=1h
curl http://localhost:5000/api/analyze/bitcoin
curl http://localhost:5000/api/recommendation/bitcoin
```

## WebSocket Support (Future)

WebSocket support for real-time updates is planned for future releases.

## Versioning

Current API version: **v1.0.0**

The API version is returned in the health check endpoint.

## Support

For API issues or questions:
- GitHub Issues: https://github.com/Islamhassana3/EPICcrypto/issues
- Email: api-support@epiccrypto.com

## Changelog

### v1.0.0 (2024-01-01)
- Initial API release
- Support for 8 timeframes
- 6+ cryptocurrencies
- Technical indicators
- AI-powered predictions
- Caching system

---

**Note:** This API is provided for educational purposes. Always do your own research before making investment decisions.