// AI Crypto Prediction App
const API_BASE = '/api';

// State
let state = {
    selectedCoin: 'bitcoin',
    selectedTimeframe: '1h',
    currentPrice: null,
    prediction: null
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeCoinButtons();
    initializeTimeframeButtons();
    initializeLoadAllButton();
    
    // Load initial data
    loadCurrentPrice();
    loadPrediction();
    loadTechnicalAnalysis();
});

// Coin selection
function initializeCoinButtons() {
    const coinButtons = document.querySelectorAll('.coin-btn');
    coinButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            coinButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update selected coin
            state.selectedCoin = btn.dataset.coin;
            
            // Reload data
            loadCurrentPrice();
            loadPrediction();
            loadTechnicalAnalysis();
        });
    });
}

// Timeframe selection
function initializeTimeframeButtons() {
    const timeframeButtons = document.querySelectorAll('.timeframe-btn');
    timeframeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            timeframeButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update selected timeframe
            state.selectedTimeframe = btn.dataset.timeframe;
            
            // Reload prediction
            loadPrediction();
        });
    });
}

// Load all timeframes button
function initializeLoadAllButton() {
    const loadAllBtn = document.getElementById('loadAllBtn');
    if (loadAllBtn) {
        loadAllBtn.addEventListener('click', loadAllTimeframes);
    }
}

// Load current price
async function loadCurrentPrice() {
    const priceCard = document.getElementById('priceCard');
    priceCard.innerHTML = '<div class="loading">Loading price data...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/price/${state.selectedCoin}`);
        const data = await response.json();
        
        if (data.error) {
            priceCard.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            return;
        }
        
        state.currentPrice = data;
        displayCurrentPrice(data);
    } catch (error) {
        priceCard.innerHTML = `<div class="error">Failed to load price data: ${error.message}</div>`;
    }
}

// Display current price
function displayCurrentPrice(data) {
    const priceCard = document.getElementById('priceCard');
    const changeClass = data.change_24h >= 0 ? 'positive' : 'negative';
    const changeSymbol = data.change_24h >= 0 ? '▲' : '▼';
    
    priceCard.innerHTML = `
        <div class="price-info">
            <div class="price-item">
                <div class="price-label">Current Price</div>
                <div class="price-value">$${formatNumber(data.price)}</div>
            </div>
            <div class="price-item">
                <div class="price-label">24h Change</div>
                <div class="price-value">
                    <span class="price-change ${changeClass}">
                        ${changeSymbol} ${Math.abs(data.change_24h).toFixed(2)}%
                    </span>
                </div>
            </div>
            <div class="price-item">
                <div class="price-label">24h Volume</div>
                <div class="price-value">$${formatNumber(data.volume_24h)}</div>
            </div>
            <div class="price-item">
                <div class="price-label">Market Cap</div>
                <div class="price-value">$${formatNumber(data.market_cap)}</div>
            </div>
        </div>
    `;
}

// Load prediction
async function loadPrediction() {
    const predictionSection = document.getElementById('predictionSection');
    const contentDiv = predictionSection.querySelector('.loading') || predictionSection;
    contentDiv.innerHTML = '<div class="loading">Generating AI prediction...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/predict/${state.selectedCoin}?timeframe=${state.selectedTimeframe}`);
        const data = await response.json();
        
        if (data.error) {
            contentDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            return;
        }
        
        state.prediction = data.prediction;
        displayPrediction(data.prediction);
    } catch (error) {
        contentDiv.innerHTML = `<div class="error">Failed to load prediction: ${error.message}</div>`;
    }
}

// Display prediction
function displayPrediction(prediction) {
    const predictionSection = document.getElementById('predictionSection');
    const recommendation = prediction.recommendation || {};
    const trendPred = prediction.trend_prediction || {};
    const momentum = prediction.momentum_analysis || {};
    
    let html = '<div class="recommendation-card">';
    
    // Recommendation
    html += `
        <div class="recommendation-item">
            <h3>📊 Recommendation</h3>
            <div class="action-badge action-${recommendation.action || 'hold'}">
                ${(recommendation.action || 'hold').toUpperCase().replace('_', ' ')}
            </div>
            <div style="margin-top: 15px;">
                <strong>Confidence:</strong> ${(recommendation.confidence * 100).toFixed(0)}%
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${(recommendation.confidence * 100)}%"></div>
                </div>
            </div>
            <div style="margin-top: 10px; color: #6b7280;">
                ${recommendation.reason || 'Analysis in progress'}
            </div>
        </div>
    `;
    
    // Trend
    if (trendPred.trend) {
        const trendClass = trendPred.trend === 'bullish' ? 'trend-bullish' : 
                          trendPred.trend === 'bearish' ? 'trend-bearish' : 'trend-neutral';
        html += `
            <div class="recommendation-item">
                <h3>📈 Trend Analysis</h3>
                <div class="trend ${trendClass}">
                    ${trendPred.trend.toUpperCase()}
                </div>
                ${trendPred.predictions ? `
                    <div style="margin-top: 10px;">
                        <strong>Predicted Price:</strong> 
                        $${formatNumber(trendPred.predictions[0])}
                    </div>
                ` : ''}
                <div style="margin-top: 10px; color: #6b7280; font-size: 0.9em;">
                    Model confidence: ${(trendPred.confidence * 100).toFixed(0)}%
                </div>
            </div>
        `;
    }
    
    // Momentum
    if (momentum.momentum !== undefined) {
        html += `
            <div class="recommendation-item">
                <h3>⚡ Momentum</h3>
                <div class="indicator-value">${momentum.momentum.toFixed(2)}%</div>
                <div style="margin-top: 10px;">
                    <strong>Signal:</strong> 
                    <span class="action-badge action-${momentum.signal.includes('buy') ? 'buy' : momentum.signal.includes('sell') ? 'sell' : 'hold'}">
                        ${momentum.signal.toUpperCase().replace('_', ' ')}
                    </span>
                </div>
                <div style="margin-top: 10px; color: #6b7280; font-size: 0.9em;">
                    Volatility: ${momentum.volatility.toFixed(2)}
                </div>
            </div>
        `;
    }
    
    html += '</div>';
    
    predictionSection.innerHTML = `
        <h2>AI Prediction & Recommendation</h2>
        ${html}
    `;
}

// Load all timeframes
async function loadAllTimeframes() {
    const grid = document.getElementById('timeframesGrid');
    const loadAllBtn = document.getElementById('loadAllBtn');
    
    loadAllBtn.disabled = true;
    loadAllBtn.textContent = 'Loading...';
    grid.innerHTML = '<div class="loading">Loading all timeframes...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/predict/${state.selectedCoin}/all`);
        const data = await response.json();
        
        if (data.error) {
            grid.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            return;
        }
        
        displayAllTimeframes(data.predictions);
    } catch (error) {
        grid.innerHTML = `<div class="error">Failed to load timeframes: ${error.message}</div>`;
    } finally {
        loadAllBtn.disabled = false;
        loadAllBtn.textContent = 'Reload All Timeframes';
    }
}

// Display all timeframes
function displayAllTimeframes(predictions) {
    const grid = document.getElementById('timeframesGrid');
    let html = '';
    
    const timeframes = ['1m', '5m', '10m', '30m', '1h', 'daily', 'monthly', 'yearly'];
    
    for (const tf of timeframes) {
        const pred = predictions[tf];
        if (!pred || pred.error) {
            html += `
                <div class="timeframe-card">
                    <h3>${tf.toUpperCase()}</h3>
                    <div class="error" style="font-size: 0.9em;">${pred?.error || 'No data'}</div>
                </div>
            `;
            continue;
        }
        
        const rec = pred.recommendation || {};
        const trendPred = pred.trend_prediction || {};
        const trendClass = trendPred.trend === 'bullish' ? 'trend-bullish' : 
                          trendPred.trend === 'bearish' ? 'trend-bearish' : 'trend-neutral';
        
        html += `
            <div class="timeframe-card">
                <h3>${tf.toUpperCase()}</h3>
                ${trendPred.trend ? `
                    <div class="trend ${trendClass}">
                        Trend: ${trendPred.trend.toUpperCase()}
                    </div>
                ` : ''}
                <div style="margin-top: 15px;">
                    <div class="action-badge action-${rec.action || 'hold'}">
                        ${(rec.action || 'hold').toUpperCase().replace('_', ' ')}
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 0.9em; color: #6b7280;">
                    Confidence: ${((rec.confidence || 0) * 100).toFixed(0)}%
                </div>
            </div>
        `;
    }
    
    grid.innerHTML = html;
}

// Load technical analysis
async function loadTechnicalAnalysis() {
    const analysisSection = document.getElementById('technicalAnalysis');
    analysisSection.innerHTML = '<h2>Technical Analysis</h2><div class="loading">Loading technical indicators...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/analyze/${state.selectedCoin}`);
        const data = await response.json();
        
        if (data.error) {
            analysisSection.innerHTML += `<div class="error">Error: ${data.error}</div>`;
            return;
        }
        
        displayTechnicalAnalysis(data);
    } catch (error) {
        analysisSection.innerHTML += `<div class="error">Failed to load technical analysis: ${error.message}</div>`;
    }
}

// Display technical analysis
function displayTechnicalAnalysis(data) {
    const analysisSection = document.getElementById('technicalAnalysis');
    const indicators = data.indicators || {};
    const interpretation = data.technical_analysis || {};
    
    let html = '<div class="indicators-grid">';
    
    // RSI
    if (indicators.RSI !== null) {
        const rsiValue = indicators.RSI;
        const rsiColor = rsiValue > 70 ? '#ef4444' : rsiValue < 30 ? '#10b981' : '#667eea';
        html += `
            <div class="indicator-card">
                <h4>RSI (14)</h4>
                <div class="indicator-value" style="color: ${rsiColor};">${rsiValue.toFixed(2)}</div>
                <div class="indicator-interpretation">${interpretation.RSI || 'Calculating...'}</div>
            </div>
        `;
    }
    
    // MACD
    if (indicators.MACD !== null) {
        html += `
            <div class="indicator-card">
                <h4>MACD</h4>
                <div class="indicator-value">${indicators.MACD.toFixed(4)}</div>
                <div class="indicator-interpretation">${interpretation.MACD || 'Calculating...'}</div>
            </div>
        `;
    }
    
    // Moving Averages
    if (indicators.MA_7 !== null && indicators.MA_25 !== null) {
        html += `
            <div class="indicator-card">
                <h4>Moving Averages</h4>
                <div style="margin: 10px 0;">
                    <strong>MA(7):</strong> $${formatNumber(indicators.MA_7)}<br>
                    <strong>MA(25):</strong> $${formatNumber(indicators.MA_25)}
                </div>
                <div class="indicator-interpretation">${interpretation.MA_Cross || 'Calculating...'}</div>
            </div>
        `;
    }
    
    // Volatility
    if (indicators.Volatility !== null) {
        html += `
            <div class="indicator-card">
                <h4>Volatility</h4>
                <div class="indicator-value">${(indicators.Volatility * 100).toFixed(2)}%</div>
                <div class="indicator-interpretation">
                    ${indicators.Volatility > 0.05 ? 'High volatility' : 
                      indicators.Volatility > 0.02 ? 'Moderate volatility' : 'Low volatility'}
                </div>
            </div>
        `;
    }
    
    html += '</div>';
    
    analysisSection.innerHTML = `
        <h2>Technical Analysis</h2>
        ${html}
    `;
}

// Utility: Format number
function formatNumber(num) {
    if (num === null || num === undefined) return '0';
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
    if (num >= 1) return num.toFixed(2);
    if (num >= 0.01) return num.toFixed(4);
    return num.toFixed(8);
}
