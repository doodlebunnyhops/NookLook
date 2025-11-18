"""
Nookipedia API client for fetching URLs and data.
Includes rate limiting to be respectful to the API.
"""

import requests
import time
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NookipediaClient:
    """
    Client for fetching data from the Nookipedia API with rate limiting.
    """
    
    def __init__(self, api_key: str, rate_limit_seconds: float = 1.0):
        """
        Initialize the Nookipedia client.
        
        Args:
            api_key: Your Nookipedia API key
            rate_limit_seconds: Seconds to wait between requests (default: 1.0)
        """
        self.api_key = api_key
        self.rate_limit = rate_limit_seconds
        self.base_url = "https://api.nookipedia.com"
        self.last_request_time = 0
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'X-API-KEY': api_key,
            'Accept-Version': '1.7.0',
            'User-Agent': 'NookLook-Bot/1.0'
        })
    
    def _wait_for_rate_limit(self):
        """Ensure we don't exceed the rate limit."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict]:
        """
        Make a request to the Nookipedia API with rate limiting.
        
        Args:
            endpoint: API endpoint (e.g., '/nh/clothing')
            params: Query parameters
            
        Returns:
            JSON response data or None if error
        """
        self._wait_for_rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.get(url, params=params or {})
            self.last_request_time = time.time()
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
    
    def get_clothing_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all clothing items with full data.
        
        Returns:
            List of dicts with full clothing item data
        """
        logger.info("Fetching clothing data...")
        data = self._make_request('/nh/clothing', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_furniture_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all furniture items with full data.
        
        Returns:
            List of dicts with full furniture item data
        """
        logger.info("Fetching furniture data...")
        data = self._make_request('/nh/furniture', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_tools_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all tools with full data.
        
        Returns:
            List of dicts with full tool data
        """
        logger.info("Fetching tools data...")
        data = self._make_request('/nh/tools', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_items_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all miscellaneous items with full data.
        
        Returns:
            List of dicts with full miscellaneous item data
        """
        logger.info("Fetching miscellaneous items data...")
        data = self._make_request('/nh/items', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_interior_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all interior items (flooring, wallpaper, rugs) with full data.
        
        Returns:
            List of dicts with full interior item data
        """
        logger.info("Fetching interior items data...")
        data = self._make_request('/nh/interior', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_photos_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all photos and posters with full data.
        
        Returns:
            List of dicts with full photo/poster data
        """
        logger.info("Fetching photos and posters data...")
        data = self._make_request('/nh/photos', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_gyroids_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all gyroids with full data.
        
        Returns:
            List of dicts with full gyroid data
        """
        logger.info("Fetching gyroids data...")
        data = self._make_request('/nh/gyroids', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_events_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all events with full data.
        
        Returns:
            List of dicts with full event data
        """
        logger.info("Fetching events data...")
        data = self._make_request('/nh/events', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_recipes_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all recipes with full data.
        
        Returns:
            List of dicts with full recipe data
        """
        logger.info("Fetching recipes data...")
        data = self._make_request('/nh/recipes', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_fish_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all fish with full data.
        
        Returns:
            List of dicts with full fish data
        """
        logger.info("Fetching fish data...")
        data = self._make_request('/nh/fish', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_bugs_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all bugs with full data.
        
        Returns:
            List of dicts with full bug data
        """
        logger.info("Fetching bugs data...")
        data = self._make_request('/nh/bugs', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_sea_creatures_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all sea creatures with full data.
        
        Returns:
            List of dicts with full sea creature data
        """
        logger.info("Fetching sea creatures data...")
        data = self._make_request('/nh/sea', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_fossils_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all individual fossils with full data.
        
        Returns:
            List of dicts with full fossil data
        """
        logger.info("Fetching fossils data...")
        data = self._make_request('/nh/fossils/individuals', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_art_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all artwork with full data.
        
        Returns:
            List of dicts with full artwork data
        """
        logger.info("Fetching art data...")
        data = self._make_request('/nh/art', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data
    
    def get_villagers_urls(self) -> List[Dict[str, Any]]:
        """
        Fetch all villagers with full data.
        
        Returns:
            List of dicts with full villager data
        """
        logger.info("Fetching villagers data...")
        data = self._make_request('/villagers', {'excludedetails': 'false'})
        
        if not data:
            return []
        
        return data


def save_urls_to_json(data: List[Dict[str, Any]], filename: str, data_dir: str = "data"):
    """
    Save data to a JSON file.
    
    Args:
        data: List of dicts with full item data
        filename: Name of the JSON file to save
        data_dir: Directory to save the file in
    """
    data_path = Path(data_dir)
    data_path.mkdir(exist_ok=True)
    
    file_path = data_path / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(data)} items to {file_path}")


def load_urls_from_json(filename: str, data_dir: str = "data") -> List[Dict[str, Any]]:
    """
    Load data from a JSON file.
    
    Args:
        filename: Name of the JSON file to load
        data_dir: Directory to load the file from
        
    Returns:
        List of dicts with full item data
    """
    file_path = Path(data_dir) / filename
    
    if not file_path.exists():
        logger.warning(f"File {file_path} does not exist")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.info(f"Loaded {len(data)} items from {file_path}")
    return data