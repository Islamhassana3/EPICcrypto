"""
Crypto API client for fetching real-time and historical data
Supports CoinGecko and Binance APIs
"""
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from pycoingecko import CoinGeckoAPI


class CryptoDataFetcher:
    """Fetch crypto data from multiple sources"""
    
    def __init__(self):
        self.coingecko = CoinGeckoAPI()
        self.binance_base_url = "https://api.binance.com/api/v3"
        
    def get_current_price(self, symbol: str = "bitcoin") -> Dict:
        """Get current price for a cryptocurrency"""
        try:
            data = self.coingecko.get_price(
                ids=symbol,
                vs_currencies='usd',
                include_24hr_change=True,
                include_24hr_vol=True,
                include_market_cap=True
            )
            return {
                'symbol': symbol,
                'price': data[symbol]['usd'],
                'change_24h': data[symbol].get('usd_24h_change', 0),
                'volume_24h': data[symbol].get('usd_24h_vol', 0),
                'market_cap': data[symbol].get('usd_market_cap', 0),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error fetching current price: {e}")
            return None
    
    def get_historical_data(self, symbol: str = "bitcoin", days: int = 30) -> List[Dict]:
        """Get historical price data"""
        try:
            data = self.coingecko.get_coin_market_chart_by_id(
                id=symbol,
                vs_currency='usd',
                days=days
            )
            
            prices = data['prices']
            volumes = data['total_volumes']
            market_caps = data['market_caps']
            
            historical_data = []
            for i in range(len(prices)):
                historical_data.append({
                    'timestamp': datetime.fromtimestamp(prices[i][0] / 1000).isoformat(),
                    'price': prices[i][1],
                    'volume': volumes[i][1] if i < len(volumes) else 0,
                    'market_cap': market_caps[i][1] if i < len(market_caps) else 0
                })
            
            return historical_data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return []
    
    def get_binance_klines(self, symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 100) -> List[Dict]:
        """Get candlestick data from Binance"""
        try:
            url = f"{self.binance_base_url}/klines"
            params = {
                'symbol': symbol.upper(),
                'interval': interval,
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            klines = response.json()
            formatted_data = []
            
            for kline in klines:
                formatted_data.append({
                    'timestamp': datetime.fromtimestamp(kline[0] / 1000).isoformat(),
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5]),
                })
            
            return formatted_data
        except Exception as e:
            print(f"Error fetching Binance klines: {e}")
            return []
    
    def get_supported_coins(self) -> List[Dict]:
        """Get list of supported cryptocurrencies"""
        try:
            coins = self.coingecko.get_coins_list()
            # Return top coins only
            return [
                {'id': coin['id'], 'symbol': coin['symbol'], 'name': coin['name']}
                for coin in coins[:100]
            ]
        except Exception as e:
            print(f"Error fetching supported coins: {e}")
            return []
    
    def get_multi_coin_data(self, symbols: List[str]) -> Dict:
        """Get data for multiple cryptocurrencies"""
        result = {}
        for symbol in symbols:
            data = self.get_current_price(symbol)
            if data:
                result[symbol] = data
            time.sleep(0.5)  # Rate limiting
        return result
