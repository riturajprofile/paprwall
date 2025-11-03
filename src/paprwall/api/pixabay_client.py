"""
Pixabay API client.
"""
from typing import List, Dict, Any
from paprwall.api.base_client import BaseAPIClient


class PixabayClient(BaseAPIClient):
    """Client for Pixabay API"""
    
    API_BASE = "https://pixabay.com/api/"
    
    def get_api_key(self) -> str:
        """Get Pixabay API key from config"""
        return self.config.get_api_key('pixabay')
    
    def fetch_images(self, count: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch images from Pixabay.
        
        Args:
            count: Number of images to fetch
            
        Returns:
            List of normalized image metadata
        """
        try:
            api_key = self.get_api_key()
            preferences = self.config.get_source_preferences('pixabay')
            
            params = {
                'key': api_key,
                'image_type': 'photo',
                'orientation': 'horizontal',
                'min_width': 1920,
                'min_height': 1080,
                'per_page': count,
                'safesearch': preferences.get('safe_search', True),
                'order': 'popular'
            }
            
            # Add theme-based search query
            theme = preferences.get('theme', 'nature')
            custom_query = self.config.get_preference('custom_query', '')
            
            if custom_query:
                params['q'] = custom_query
            elif theme:
                # Use theme as search query
                params['q'] = theme
            
            # Add categories if specified
            categories = preferences.get('categories', [])
            if categories:
                params['category'] = ','.join(categories)
            
            response = self.session.get(self.API_BASE, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for hit in data.get('hits', [])[:count]:
                images.append(self.normalize_image_data(hit))
            
            return images
            
        except Exception as e:
            raise Exception(f"Pixabay API error: {e}")
    
    def normalize_image_data(self, raw_data: Dict) -> Dict[str, Any]:
        """Normalize Pixabay response to standard format"""
        return {
            'id': str(raw_data['id']),
            'source': 'pixabay',
            'photographer': raw_data.get('user', 'Unknown'),
            'photographer_url': f"https://pixabay.com/users/{raw_data.get('user', '')}-{raw_data.get('user_id', '')}",
            'image_url': raw_data.get('pageURL', ''),
            'download_url': raw_data.get('largeImageURL', raw_data.get('webformatURL', '')),
            'description': raw_data.get('tags', ''),
            'width': raw_data.get('imageWidth', 0),
            'height': raw_data.get('imageHeight', 0),
            'tags': raw_data.get('tags', '').split(', ')
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Pixabay API connection"""
        try:
            images = self.fetch_images(count=1)
            return {
                'success': True,
                'message': 'Pixabay API is working',
                'details': images[0] if images else {}
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'details': {}
            }
