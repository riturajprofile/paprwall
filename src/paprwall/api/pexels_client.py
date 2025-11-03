"""
Pexels API client.
"""
from typing import List, Dict, Any
from paprwall.api.base_client import BaseAPIClient


class PexelsClient(BaseAPIClient):
    """Client for Pexels API"""
    
    API_BASE = "https://api.pexels.com/v1"
    
    def get_api_key(self) -> str:
        """Get Pexels API key from config"""
        return self.config.get_api_key('pexels')
    
    def fetch_images(self, count: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch images from Pexels.
        
        Args:
            count: Number of images to fetch
            
        Returns:
            List of normalized image metadata
        """
        try:
            api_key = self.get_api_key()
            preferences = self.config.get_source_preferences('pexels')
            
            headers = {
                'Authorization': api_key
            }
            
            # Get theme-based query
            theme = preferences.get('theme', 'nature')
            custom_query = self.config.get_preference('custom_query', '')
            
            if custom_query:
                query = custom_query
            elif theme:
                query = f"{theme} wallpaper"
            else:
                query = preferences.get('query', 'nature landscape')
            
            orientation = preferences.get('orientation', 'landscape')
            
            params = {
                'query': query,
                'orientation': orientation,
                'per_page': count,
                'size': 'large'
            }
            
            endpoint = f"{self.API_BASE}/search"
            response = self.session.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for photo in data.get('photos', [])[:count]:
                images.append(self.normalize_image_data(photo))
            
            return images
            
        except Exception as e:
            raise Exception(f"Pexels API error: {e}")
    
    def normalize_image_data(self, raw_data: Dict) -> Dict[str, Any]:
        """Normalize Pexels response to standard format"""
        src = raw_data.get('src', {})
        
        return {
            'id': str(raw_data.get('id', '')),
            'source': 'pexels',
            'photographer': raw_data.get('photographer', 'Unknown'),
            'photographer_url': raw_data.get('photographer_url', ''),
            'image_url': raw_data.get('url', ''),
            'download_url': src.get('original', src.get('large2x', src.get('large', ''))),
            'description': raw_data.get('alt', 'Pexels Photo'),
            'width': raw_data.get('width', 0),
            'height': raw_data.get('height', 0),
            'tags': []  # Pexels doesn't provide tags in search results
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Pexels API connection"""
        try:
            images = self.fetch_images(count=1)
            return {
                'success': True,
                'message': 'Pexels API is working',
                'details': images[0] if images else {}
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'details': {}
            }
