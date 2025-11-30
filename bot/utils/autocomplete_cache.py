"""Autocomplete caching utilities"""
import time
import logging

logger = logging.getLogger(__name__)

class AutocompleteCache:
    """Efficient cache for autocomplete results with smart optimizations"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 300, random_ttl: int = 60):  # 1 minute random TTL
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.random_ttl = random_ttl  # Shorter TTL for random results
        self.access_times = {}
        self.random_pools = {}  # Store multiple random result sets
        self.random_rotation_times = {}  # Track when to rotate random sets
        
        # Enhanced caching features
        self.prefix_cache = {}  # Cache for prefix-based lookups
        self.hit_counts = {}    # Track cache hit frequency
        self.query_patterns = {}  # Track common query patterns
    
    def _cleanup_expired(self):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.access_times.items()
            if current_time - timestamp > self._get_ttl_for_key(key)
        ]
        if expired_keys:
            logger.debug(f"Cache cleanup: removing {len(expired_keys)} expired entries")
        for key in expired_keys:
            self.cache.pop(key, None)
            self.access_times.pop(key, None)
            # Clean up random pool tracking
            if key in self.random_rotation_times:
                self.random_rotation_times.pop(key, None)
    
    def _get_ttl_for_key(self, key: str) -> int:
        """Get TTL based on key type"""
        return self.random_ttl if ':random' in key else self.ttl
    
    def _make_room(self):
        """Remove oldest entries if cache is full"""
        if len(self.cache) >= self.max_size:
            # Remove 20% of oldest entries
            to_remove = max(1, len(self.cache) // 5)
            oldest_keys = sorted(self.access_times.items(), key=lambda x: x[1])[:to_remove]
            logger.info(f"Cache full ({len(self.cache)} entries), evicting {to_remove} oldest entries")
            for key, _ in oldest_keys:
                self.cache.pop(key, None)
                self.access_times.pop(key, None)
    
    def get(self, key: str):
        """Get cached value if not expired with smart optimizations"""
        self._cleanup_expired()
        
        # Normalize key for consistent caching
        normalized_key = self._normalize_key(key)
        
        # Special handling for random keys
        if ':random' in normalized_key:
            return self._get_random_result(normalized_key)
        
        # Try exact match first
        if normalized_key in self.cache:
            self.access_times[normalized_key] = time.time()
            self.hit_counts[normalized_key] = self.hit_counts.get(normalized_key, 0) + 1
            logger.info(f"Cache HIT for key: {normalized_key} (hits: {self.hit_counts[normalized_key]})")
            return self.cache[normalized_key]
        
        # Try prefix matching for progressive typing
        prefix_result = self._try_prefix_match(normalized_key)
        if prefix_result:
            return prefix_result
            
        logger.debug(f"Cache MISS for key: {normalized_key}")
        return None
    
    def _normalize_key(self, key: str) -> str:
        """Normalize cache keys for consistency"""
        if ':' in key:
            prefix, query = key.split(':', 1)
            # Normalize the query part - trim whitespace, lowercase
            normalized_query = query.strip().lower()
            return f"{prefix}:{normalized_query}"
        return key.strip().lower()
    
    def _try_prefix_match(self, key: str) -> any:
        """Try to find results from cached longer queries"""
        if ':' not in key:
            return None
            
        prefix, query = key.split(':', 1)
        
        # Look for cached results from longer queries that start with this query
        for cached_key, cached_result in self.cache.items():
            if not cached_key.startswith(f"{prefix}:"):
                continue
                
            _, cached_query = cached_key.split(':', 1)
            
            # If cached query starts with our query and is longer
            if cached_query.startswith(query) and len(cached_query) > len(query):
                # Filter the cached results to match our shorter query
                filtered_results = self._filter_results_for_query(cached_result, query)
                if filtered_results:
                    logger.info(f"Cache PREFIX HIT: '{key}' found via '{cached_key}' ({len(filtered_results)} results)")
                    # Cache this result for future use
                    self.cache[key] = filtered_results
                    self.access_times[key] = time.time()
                    return filtered_results
        
        return None
    
    def _filter_results_for_query(self, results, query: str):
        """Filter autocomplete results to match a shorter query"""
        if not results or not query:
            return results
            
        # Filter choices that contain the query
        filtered = []
        for choice in results:
            if hasattr(choice, 'name') and query.lower() in choice.name.lower():
                filtered.append(choice)
            elif isinstance(choice, dict) and 'name' in choice and query.lower() in choice['name'].lower():
                filtered.append(choice)
                
        return filtered[:25]  # Maintain Discord's 25-item limit
    
    def _get_random_result(self, key: str):
        """Handle random result caching with rotation"""
        current_time = time.time()
        
        # Check if we have a fresh random result
        if key in self.cache and key in self.access_times:
            age = current_time - self.access_times[key]
            if age < self.random_ttl:
                logger.info(f"Cache HIT for random key: {key} (age: {age:.1f}s)")
                return self.cache[key]
            else:
                logger.debug(f"Random cache EXPIRED for key: {key} (age: {age:.1f}s)")
        
        logger.debug(f"Random cache MISS for key: {key}")
        return None
    
    def set(self, key: str, value):
        """Cache a value with normalization"""
        self._cleanup_expired()
        self._make_room()
        
        # Normalize the key
        normalized_key = self._normalize_key(key)
        
        self.cache[normalized_key] = value
        self.access_times[normalized_key] = time.time()
        self.hit_counts[normalized_key] = 0  # Initialize hit counter
        
        # Track query patterns for analytics
        if ':' in normalized_key:
            prefix, query = normalized_key.split(':', 1)
            if len(query) >= 2:  # Only track meaningful queries
                self.query_patterns[prefix] = self.query_patterns.get(prefix, 0) + 1
        
        ttl_type = "random" if ':random' in normalized_key else "regular"
        ttl_value = self._get_ttl_for_key(normalized_key)
        logger.debug(f"Cache SET for key: {normalized_key} ({ttl_type} TTL: {ttl_value}s, cache size: {len(self.cache)})")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.access_times.clear()
        self.random_pools.clear()
        self.random_rotation_times.clear()
        self.prefix_cache.clear()
        self.hit_counts.clear()
        self.query_patterns.clear()
    
    def get_cache_stats(self) -> dict:
        """Get comprehensive cache statistics"""
        total_hits = sum(self.hit_counts.values())
        cache_size = len(self.cache)
        
        # Find most popular queries
        popular_queries = sorted(self.hit_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Query pattern stats
        pattern_stats = dict(sorted(self.query_patterns.items(), key=lambda x: x[1], reverse=True))
        
        return {
            'cache_size': cache_size,
            'total_hits': total_hits,
            'hit_rate': f"{(total_hits / max(cache_size, 1)) * 100:.1f}%",
            'popular_queries': popular_queries,
            'query_patterns': pattern_stats,
            'max_size': self.max_size,
            'utilization': f"{(cache_size / self.max_size) * 100:.1f}%"
        }
    
autocomplete_cache = AutocompleteCache(max_size=1000, ttl=300, random_ttl=60)