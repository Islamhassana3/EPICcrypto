"""
Simple in-memory cache manager
"""
import time
from typing import Any, Optional


class CacheManager:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self):
        self.cache = {}
        
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self.cache:
            value, expiry = self.cache[key]
            if expiry is None or time.time() < expiry:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in cache with TTL in seconds"""
        expiry = time.time() + ttl if ttl else None
        self.cache[key] = (value, expiry)
    
    def delete(self, key: str):
        """Delete key from cache"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def cleanup(self):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if expiry is not None and current_time >= expiry
        ]
        for key in expired_keys:
            del self.cache[key]
