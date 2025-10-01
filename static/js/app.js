// EPICcrypto Frontend JavaScript

let currentCoin = 'BTC-USD';

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    loadSupportedCoins();
    setupEventListeners();
});

// Load supported cryptocurrencies
async function loadSupportedCoins() {
    try {
        const response = await fetch('/api/coins');
        const coins = await response.json();
        
        const select = document.getElementById('coinSelect');
        select.innerHTML = '';
        
        coins.forEach(coin => {
            const option = document.createElement('option');
            option.value = coin.symbol;
            option.textContent = `${coin.name} (${coin.symbol})`;
            select.appendChild(option);
        });
        
        currentCoin = coins[0].symbol;
    } catch (error) {
        console.error('Error loading coins:', error);
        alert('Failed to load cryptocurrencies. Please refresh the page.');
    }
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('coinSelect').addEventListener('change', function(e) {
        currentCoin = e.target.value;
    });
    
    document.getElementById('analyzeBtn').addEventListener('click', analyzeCoin);
    document.getElementById('multiTimeframeBtn').addEventListener('click', analyzeMultiTimeframe);
}

// Analyze selected coin
async function analyzeCoin() {
    const timeframe = document.getElementById('timeframeSelect').value;
    
    showLoading();
    hideResults();
    hideMultiTimeframe();
    
    try {
        const response = await fetch(`/api/prediction/${currentCoin}?timeframe=${timeframe}`);
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error analyzing coin:', error);
        alert('Failed to analyze cryptocurrency. Please try again.');
    } finally {
        hideLoading();
    }
}

// Analyze across multiple timeframes
async function analyzeMultiTimeframe() {
    showLoading();
    hideResults();
    hideMultiTimeframe();
    
    try {
        const response = await fetch(`/api/multi-timeframe/${currentCoin}`);
        const data = await response.json();
        
        if (response.ok) {
            displayMultiTimeframeResults(data);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error analyzing coin:', error);
        alert('Failed to analyze cryptocurrency. Please try again.');
    } finally {
        hideLoading();
    }
}

// Display single timeframe results
function displayResults(data) {
    // Update coin name
    document.getElementById('coinName').textContent = data.symbol.replace('-USD', '');
    
    // Update prices
    document.getElementById('currentPrice').textContent = `$${data.current_price.toFixed(2)}`;
    document.getElementById('predictedPrice').textContent = `$${data.predicted_price.toFixed(2)}`;
    
    // Update recommendation
    const badge = document.getElementById('recommendationBadge');
    badge.textContent = data.recommendation;
    badge.className = `recommendation-badge ${data.recommendation}`;
    
    // Update confidence
    document.getElementById('confidence').textContent = `${(data.confidence * 100).toFixed(1)}%`;
    
    // Update price change
    const changeElement = document.getElementById('priceChange');
    const changeValue = data.price_change_percent.toFixed(2);
    changeElement.textContent = `${changeValue > 0 ? '+' : ''}${changeValue}%`;
    changeElement.className = `value ${changeValue >= 0 ? 'positive' : 'negative'}`;
    
    // Update technical indicators
    const indicatorsDiv = document.getElementById('indicators');
    indicatorsDiv.innerHTML = '';
    
    if (data.technical_indicators && Object.keys(data.technical_indicators).length > 0) {
        for (const [key, value] of Object.entries(data.technical_indicators)) {
            const indicatorDiv = document.createElement('div');
            indicatorDiv.className = 'indicator';
            
            const name = document.createElement('div');
            name.className = 'indicator-name';
            name.textContent = formatIndicatorName(key);
            
            const valueDiv = document.createElement('div');
            valueDiv.className = 'indicator-value';
            valueDiv.textContent = typeof value === 'number' ? value.toFixed(2) : value;
            
            indicatorDiv.appendChild(name);
            indicatorDiv.appendChild(valueDiv);
            indicatorsDiv.appendChild(indicatorDiv);
        }
    } else {
        indicatorsDiv.innerHTML = '<p>No technical indicators available</p>';
    }
    
    showResults();
}

// Display multi-timeframe results
function displayMultiTimeframeResults(data) {
    const grid = document.getElementById('timeframeGrid');
    grid.innerHTML = '';
    
    const timeframeNames = {
        '1m': '1 Minute',
        '5m': '5 Minutes',
        '15m': '15 Minutes',
        '1h': '1 Hour',
        '4h': '4 Hours',
        '1d': '1 Day',
        '1wk': '1 Week',
        '1mo': '1 Month'
    };
    
    for (const [timeframe, prediction] of Object.entries(data.predictions)) {
        const card = document.createElement('div');
        card.className = 'timeframe-card';
        
        const title = document.createElement('h3');
        title.textContent = timeframeNames[timeframe] || timeframe;
        
        const recommendation = document.createElement('div');
        recommendation.className = `timeframe-recommendation ${prediction.recommendation}`;
        recommendation.textContent = prediction.recommendation;
        
        const details = document.createElement('div');
        details.className = 'timeframe-details';
        details.innerHTML = `
            <p><strong>Confidence:</strong> ${(prediction.confidence * 100).toFixed(1)}%</p>
            <p><strong>Predicted Price:</strong> $${prediction.predicted_price.toFixed(2)}</p>
            <p><strong>Change:</strong> <span class="${prediction.price_change_percent >= 0 ? 'positive' : 'negative'}">${prediction.price_change_percent > 0 ? '+' : ''}${prediction.price_change_percent.toFixed(2)}%</span></p>
        `;
        
        card.appendChild(title);
        card.appendChild(recommendation);
        card.appendChild(details);
        grid.appendChild(card);
    }
    
    showMultiTimeframe();
}

// Helper functions
function formatIndicatorName(key) {
    const names = {
        'sma_20': 'SMA 20',
        'sma_50': 'SMA 50',
        'rsi': 'RSI',
        'macd': 'MACD',
        'macd_signal': 'MACD Signal',
        'bb_upper': 'BB Upper',
        'bb_lower': 'BB Lower'
    };
    return names[key] || key.toUpperCase();
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showResults() {
    document.getElementById('results').style.display = 'block';
}

function hideResults() {
    document.getElementById('results').style.display = 'none';
}

function showMultiTimeframe() {
    document.getElementById('multiTimeframeResults').style.display = 'block';
}

function hideMultiTimeframe() {
    document.getElementById('multiTimeframeResults').style.display = 'none';
}
