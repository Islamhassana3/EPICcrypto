# EPICcrypto API Documentation

Complete reference for the EPICcrypto REST API.

## Base URL

```
Local Development: http://localhost:5000
Production: https://your-app.railway.app
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

---

## Endpoints

### 1. Get Supported Coins

Returns a list of all supported cryptocurrencies.

**Endpoint**: `GET /api/coins`

**Parameters**: None

**Response**:
```json
[
  {
    "symbol": "BTC-USD",
    "name": "Bitcoin"
  },
  {
    "symbol": "ETH-USD",
    "name": "Ethereum"
  },
  {
    "symbol": "BNB-USD",
    "name": "Binance Coin"
  },
  {
    "symbol": "ADA-USD",
    "name": "Cardano"
  },
  {
    "symbol": "SOL-USD",
    "name": "Solana"
  },
  {
    "symbol": "XRP-USD",
    "name": "Ripple"
  },
  {
    "symbol": "DOT-USD",
    "name": "Polkadot"
  },
  {
    "symbol": "DOGE-USD",
    "name": "Dogecoin"
  }
]
```

**Example Request**:
```bash
curl https://your-app.railway.app/api/coins
```

---

### 2. Get Prediction for Single Timeframe

Get AI-powered prediction for a specific cryptocurrency and timeframe.

**Endpoint**: `GET /api/prediction/<symbol>`

**URL Parameters**:
- `symbol` (required): Cryptocurrency symbol (e.g., `BTC-USD`)

**Query Parameters**:
- `timeframe` (optional): Time interval for analysis
  - Options: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`, `1wk`, `1mo`
  - Default: `1d`

**Response**:
```json
{
  "symbol": "BTC-USD",
  "timeframe": "1d",
  "current_price": 45000.50,
  "predicted_price": 46350.75,
  "price_change_percent": 3.00,
  "recommendation": "BUY",
  "confidence": 0.75,
  "technical_indicators": {
    "sma_20": 44500.00,
    "sma_50": 43800.00,
    "rsi": 62.50,
    "macd": 250.00,
    "macd_signal": 200.00,
    "bb_upper": 46000.00,
    "bb_lower": 43000.00
  }
}
```

**Response Fields**:
- `symbol`: Cryptocurrency symbol
- `timeframe`: Analysis timeframe
- `current_price`: Current market price
- `predicted_price`: AI-predicted price
- `price_change_percent`: Expected price change percentage
- `recommendation`: Trading recommendation (`BUY`, `SELL`, or `HOLD`)
- `confidence`: Prediction confidence (0.0 to 1.0)
- `technical_indicators`: Technical analysis indicators

**Example Requests**:
```bash
# Daily prediction for Bitcoin
curl https://your-app.railway.app/api/prediction/BTC-USD?timeframe=1d

# Hourly prediction for Ethereum
curl https://your-app.railway.app/api/prediction/ETH-USD?timeframe=1h

# Weekly prediction for Solana
curl https://your-app.railway.app/api/prediction/SOL-USD?timeframe=1wk
```

**Error Responses**:
```json
// 404 - Coin not found or no data available
{
  "error": "Unable to fetch data for this coin"
}

// 500 - Server error
{
  "error": "Error message describing the issue"
}
```

---

### 3. Get Multi-Timeframe Predictions

Get predictions across all timeframes for comprehensive analysis.

**Endpoint**: `GET /api/multi-timeframe/<symbol>`

**URL Parameters**:
- `symbol` (required): Cryptocurrency symbol (e.g., `BTC-USD`)

**Query Parameters**: None

**Response**:
```json
{
  "symbol": "BTC-USD",
  "predictions": {
    "1m": {
      "recommendation": "HOLD",
      "confidence": 0.60,
      "predicted_price": 45025.00,
      "price_change_percent": 0.05
    },
    "5m": {
      "recommendation": "BUY",
      "confidence": 0.65,
      "predicted_price": 45100.00,
      "price_change_percent": 0.22
    },
    "15m": {
      "recommendation": "BUY",
      "confidence": 0.68,
      "predicted_price": 45200.00,
      "price_change_percent": 0.44
    },
    "1h": {
      "recommendation": "BUY",
      "confidence": 0.70,
      "predicted_price": 45500.00,
      "price_change_percent": 1.11
    },
    "4h": {
      "recommendation": "BUY",
      "confidence": 0.72,
      "predicted_price": 45900.00,
      "price_change_percent": 2.00
    },
    "1d": {
      "recommendation": "BUY",
      "confidence": 0.75,
      "predicted_price": 46350.00,
      "price_change_percent": 3.00
    },
    "1wk": {
      "recommendation": "BUY",
      "confidence": 0.68,
      "predicted_price": 47000.00,
      "price_change_percent": 4.44
    },
    "1mo": {
      "recommendation": "HOLD",
      "confidence": 0.62,
      "predicted_price": 46500.00,
      "price_change_percent": 3.33
    }
  }
}
```

**Example Request**:
```bash
curl https://your-app.railway.app/api/multi-timeframe/BTC-USD
```

**Error Responses**:
```json
// 500 - Server error
{
  "error": "Error message describing the issue"
}
```

---

### 4. Health Check

Check if the API is running and healthy.

**Endpoint**: `GET /api/health`

**Parameters**: None

**Response**:
```json
{
  "status": "healthy",
  "service": "EPICcrypto"
}
```

**Example Request**:
```bash
curl https://your-app.railway.app/api/health
```

---

## Data Models

### Recommendation Types

| Value | Description |
|-------|-------------|
| `BUY` | Strong positive signals, good buying opportunity |
| `SELL` | Strong negative signals, consider selling |
| `HOLD` | Neutral or mixed signals, wait for clearer trend |

### Confidence Levels

| Range | Interpretation |
|-------|----------------|
| 0.0 - 0.5 | Low confidence, high uncertainty |
| 0.5 - 0.7 | Medium confidence, moderate certainty |
| 0.7 - 1.0 | High confidence, strong signal agreement |

### Technical Indicators

| Indicator | Description |
|-----------|-------------|
| `sma_20` | 20-period Simple Moving Average |
| `sma_50` | 50-period Simple Moving Average |
| `rsi` | Relative Strength Index (0-100) |
| `macd` | Moving Average Convergence Divergence |
| `macd_signal` | MACD Signal Line |
| `bb_upper` | Bollinger Band Upper Limit |
| `bb_lower` | Bollinger Band Lower Limit |

---

## Rate Limiting

Currently, there are no rate limits enforced. However, please be respectful:
- Avoid excessive requests (more than 1 per second)
- Cache responses when possible
- Use multi-timeframe endpoint instead of multiple single requests

**Recommended**: Implement client-side caching for 30-60 seconds.

---

## Error Handling

All errors follow this format:

```json
{
  "error": "Human-readable error message"
}
```

**HTTP Status Codes**:
- `200`: Success
- `404`: Resource not found or no data available
- `500`: Internal server error

---

## Best Practices

### 1. Caching
Cache API responses to reduce load:
```javascript
// Example: 60-second cache
const cache = new Map();
const CACHE_DURATION = 60000; // 60 seconds

async function getCachedPrediction(symbol, timeframe) {
  const key = `${symbol}-${timeframe}`;
  const cached = cache.get(key);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  const data = await fetchPrediction(symbol, timeframe);
  cache.set(key, { data, timestamp: Date.now() });
  return data;
}
```

### 2. Error Handling
Always handle potential errors:
```javascript
try {
  const response = await fetch('/api/prediction/BTC-USD');
  if (!response.ok) {
    throw new Error('API request failed');
  }
  const data = await response.json();
  // Process data
} catch (error) {
  console.error('Error:', error);
  // Show user-friendly message
}
```

### 3. Batch Requests
Use multi-timeframe endpoint instead of multiple requests:
```javascript
// Good: Single request
const allTimeframes = await fetch('/api/multi-timeframe/BTC-USD');

// Avoid: Multiple requests
const day = await fetch('/api/prediction/BTC-USD?timeframe=1d');
const week = await fetch('/api/prediction/BTC-USD?timeframe=1wk');
const month = await fetch('/api/prediction/BTC-USD?timeframe=1mo');
```

---

## Integration Examples

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_BASE = 'https://your-app.railway.app';

// Get prediction
async function getPrediction(symbol, timeframe = '1d') {
  try {
    const response = await axios.get(
      `${API_BASE}/api/prediction/${symbol}`,
      { params: { timeframe } }
    );
    return response.data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Get multi-timeframe
async function getMultiTimeframe(symbol) {
  try {
    const response = await axios.get(
      `${API_BASE}/api/multi-timeframe/${symbol}`
    );
    return response.data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
(async () => {
  const btcPrediction = await getPrediction('BTC-USD', '1d');
  console.log('BTC Recommendation:', btcPrediction.recommendation);
  
  const ethMulti = await getMultiTimeframe('ETH-USD');
  console.log('ETH Multi-timeframe:', ethMulti.predictions);
})();
```

### Python

```python
import requests

API_BASE = 'https://your-app.railway.app'

def get_prediction(symbol, timeframe='1d'):
    """Get prediction for a cryptocurrency"""
    try:
        response = requests.get(
            f'{API_BASE}/api/prediction/{symbol}',
            params={'timeframe': timeframe}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        raise

def get_multi_timeframe(symbol):
    """Get multi-timeframe predictions"""
    try:
        response = requests.get(
            f'{API_BASE}/api/multi-timeframe/{symbol}'
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        raise

# Usage
if __name__ == '__main__':
    btc = get_prediction('BTC-USD', '1d')
    print(f"BTC Recommendation: {btc['recommendation']}")
    
    eth_multi = get_multi_timeframe('ETH-USD')
    print(f"ETH Predictions: {eth_multi['predictions']}")
```

### cURL

```bash
# Get daily Bitcoin prediction
curl -X GET "https://your-app.railway.app/api/prediction/BTC-USD?timeframe=1d"

# Get multi-timeframe Ethereum analysis
curl -X GET "https://your-app.railway.app/api/multi-timeframe/ETH-USD"

# Get supported coins
curl -X GET "https://your-app.railway.app/api/coins"

# Health check
curl -X GET "https://your-app.railway.app/api/health"
```

---

## Changelog

### v1.0.0 (Initial Release)
- Basic prediction API
- Multi-timeframe analysis
- Technical indicators
- 8 supported cryptocurrencies

---

## Support

For API issues or questions:
- GitHub Issues: https://github.com/Islamhassana3/EPICcrypto/issues
- Check deployment logs for errors
- Review this documentation

---

## Disclaimer

⚠️ **Important**: This API provides predictions based on technical analysis and machine learning models. It is NOT financial advice. Always:
- Do your own research
- Consult with financial advisors
- Understand the risks of cryptocurrency trading
- Never invest more than you can afford to lose

The predictions are probabilistic and may not always be accurate. Past performance does not guarantee future results.

---

Last Updated: 2024
