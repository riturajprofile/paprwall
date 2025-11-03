"""
Unsplash API client.
"""
from typing import List, Dict, Any
from riturajprofile_wallpaper.api.base_client import BaseAPIClient


class UnsplashClient(BaseAPIClient):
    """Client for Unsplash API"""
    
    API_BASE = "https://api.unsplash.com"
    
    def get_api_key(self) -> str:
        """Get Unsplash access key from config"""
        return self.config.get_api_key('unsplash')
    
    def fetch_images(self, count: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch images from Unsplash.
        
        Args:
            count: Number of images to fetch
            
        Returns:
            List of normalized image metadata
        """
        try:
            access_key = self.get_api_key()
            preferences = self.config.get_source_preferences('unsplash')
            
            headers = {
                'Authorization': f'Client-ID {access_key}'
            }
            
            # Use search or random endpoint
            collections = preferences.get('collections', [])
            orientation = preferences.get('orientation', 'landscape')
            theme = preferences.get('theme', 'nature')
            custom_query = self.config.get_preference('custom_query', '')
            
            # Determine search query
            if custom_query:
                search_query = custom_query
            elif theme:
                search_query = f"{theme} wallpaper"
            else:
                search_query = 'wallpaper nature landscape'
            
            if collections:
                # Search in specific collections
                endpoint = f"{self.API_BASE}/photos/random"
                params = {
                    'collections': ','.join(collections),
                    'orientation': orientation,
                    'count': count
                }
            else:
                # Random photos with theme query
                endpoint = f"{self.API_BASE}/photos/random"
                params = {
                    'query': search_query,
                    'orientation': orientation,
                    'count': count
                }
            
            response = self.session.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            # Handle both single photo and array response
            photos = data if isinstance(data, list) else [data]
            
            for photo in photos[:count]:
                images.append(self.normalize_image_data(photo))
            
            return images
            
        except Exception as e:
            raise Exception(f"Unsplash API error: {e}")
    
    def normalize_image_data(self, raw_data: Dict) -> Dict[str, Any]:
        """Normalize Unsplash response to standard format"""
        user = raw_data.get('user', {})
        urls = raw_data.get('urls', {})
        
        return {
            'id': raw_data.get('id', ''),
            'source': 'unsplash',
            'photographer': user.get('name', 'Unknown'),
            'photographer_url': user.get('links', {}).get('html', ''),
            'image_url': raw_data.get('links', {}).get('html', ''),
            'download_url': urls.get('raw', urls.get('full', '')),
            'description': raw_data.get('description', raw_data.get('alt_description', '')),
            'width': raw_data.get('width', 0),
            'height': raw_data.get('height', 0),
            'tags': [tag.get('title', '') for tag in raw_data.get('tags', [])]
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Unsplash API connection"""
        try:
            images = self.fetch_images(count=1)
            return {
                'success': True,
                'message': 'Unsplash API is working',
                'details': images[0] if images else {}
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'details': {}
            }
