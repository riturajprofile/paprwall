"""
Source manager - coordinates all image sources.
"""
from typing import List, Dict, Any
import logging
from riturajprofile_wallpaper.api.pixabay_client import PixabayClient
from riturajprofile_wallpaper.api.unsplash_client import UnsplashClient
from riturajprofile_wallpaper.api.pexels_client import PexelsClient

logger = logging.getLogger(__name__)


class SourceManager:
    """
    Manages all image sources (API + Local).
    Distributes fetch requests based on user preferences.
    """
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.clients = {
            'pixabay': PixabayClient(config_manager),
            'unsplash': UnsplashClient(config_manager),
            'pexels': PexelsClient(config_manager),
        }
    
    def fetch_daily_images(self, total_count: int = 5) -> List[Dict]:
        """
        Fetch images from enabled sources.
        Distributes count based on source_weights.
        
        Args:
            total_count: Total number of images to fetch
            
        Returns:
            List of image metadata dictionaries
        """
        enabled_sources = self.config.get_enabled_sources()
        weights = self.config.get_source_weights()
        
        # Calculate distribution
        distribution = self.calculate_distribution(total_count, enabled_sources, weights)
        
        all_images = []
        for source, count in distribution.items():
            if count > 0 and source in self.clients:
                try:
                    logger.info(f"Fetching {count} images from {source}")
                    images = self.clients[source].fetch_images(count)
                    all_images.extend(images)
                except Exception as e:
                    logger.error(f"Failed to fetch from {source}: {e}")
        
        return all_images
    
    def calculate_distribution(self, total: int, sources: List[str], 
                               weights: Dict[str, int]) -> Dict[str, int]:
        """
        Calculate how many images to fetch from each source.
        
        Args:
            total: Total number of images needed
            sources: List of enabled source names
            weights: Dictionary of source weights
            
        Returns:
            Dictionary mapping source name to image count
        """
        if not sources:
            return {}
        
        # Filter out local source for API distribution
        api_sources = [s for s in sources if s != 'local' and s in self.clients]
        
        if not api_sources:
            return {}
        
        # Calculate total weight
        total_weight = sum(weights.get(s, 0) for s in api_sources if weights.get(s, 0) > 0)
        
        if total_weight == 0:
            # Equal distribution if no weights specified
            base_count = total // len(api_sources)
            remainder = total % len(api_sources)
            distribution = {s: base_count for s in api_sources}
            
            # Distribute remainder
            for i, source in enumerate(api_sources):
                if i < remainder:
                    distribution[source] += 1
            
            return distribution
        
        # Weighted distribution
        distribution = {}
        remaining = total
        
        for source in api_sources:
            weight = weights.get(source, 0)
            count = round((weight / total_weight) * total)
            distribution[source] = min(count, remaining)
            remaining -= distribution[source]
        
        # Distribute any remainder
        if remaining > 0:
            for source in api_sources:
                if remaining > 0:
                    distribution[source] += 1
                    remaining -= 1
        
        return distribution
    
    def test_source(self, source_name: str) -> Dict[str, Any]:
        """
        Test if source is working (API key valid, etc.).
        
        Args:
            source_name: Name of the source to test
            
        Returns:
            Dictionary with success status and message
        """
        if source_name not in self.clients:
            return {
                'success': False,
                'message': f'Unknown source: {source_name}',
                'details': {}
            }
        
        try:
            return self.clients[source_name].test_connection()
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'details': {}
            }
    
    def get_available_sources(self) -> List[str]:
        """Get list of available source names"""
        return list(self.clients.keys()) + ['local']
