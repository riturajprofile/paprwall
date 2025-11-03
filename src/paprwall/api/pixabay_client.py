"""
Pixabay API client.
Docs: https://pixabay.com/api/docs/
"""
from typing import List, Dict, Any
import logging
from paprwall.api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class PixabayClient(BaseAPIClient):
    """Client for Pixabay API"""
    
    API_BASE = "https://pixabay.com/api/"
    # Allowed categories per official Pixabay API docs
    ALLOWED_CATEGORIES = {
        'backgrounds', 'fashion', 'nature', 'science', 'education', 'feelings', 'health', 
        'people', 'religion', 'places', 'animals', 'industry', 'computer', 'food', 
        'sports', 'transportation', 'travel', 'buildings', 'business', 'music'
    }
    
    def get_api_key(self) -> str:
        """Get Pixabay API key from config"""
        return self.config.get_api_key('pixabay')
    
    def _build_params(self, count: int) -> Dict[str, Any]:
        """Build API request params according to official Pixabay docs"""
        prefs = self.config.get_source_preferences('pixabay')
        custom_query = self.config.get_preference('custom_query', '')
        theme = prefs.get('theme', 'nature')
        
        # Required parameter
        params: Dict[str, Any] = {
            'key': self.get_api_key(),
        }
        
        # Optional params per official docs
        # Search query (URL encoded by requests library)
        if custom_query:
            params['q'] = custom_query.strip()
        elif theme:
            params['q'] = theme.strip()
        
        # Image type filter
        params['image_type'] = 'photo'
        
        # Orientation filter
        params['orientation'] = 'horizontal'
        
        # Minimum dimensions
        params['min_width'] = 1920
        params['min_height'] = 1080
        
        # Results per page (3-200 allowed)
        params['per_page'] = max(3, min(int(count), 200))
        
        # Safe search
        params['safesearch'] = 'true' if prefs.get('safe_search', True) else 'false'
        
        # Order by popularity
        params['order'] = 'popular'
        
        # Language (default: en)
        params['lang'] = 'en'
        
        # Category: Pixabay accepts only ONE category, not comma-separated
        # If user config has multiple, pick first valid one
        categories = prefs.get('categories', [])
        if categories:
            valid_cat = next((c for c in categories if str(c).lower() in self.ALLOWED_CATEGORIES), None)
            if valid_cat:
                params['category'] = str(valid_cat).lower()
        
        return params
    
    def fetch_images(self, count: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch images from Pixabay API.
        
        Args:
            count: Number of images to fetch (will be clamped to 3-200)
            
        Returns:
            List of normalized image metadata
            
        Raises:
            Exception: On API errors with descriptive message
        """
        try:
            params = self._build_params(count)
            
            # Make request
            response = self.session.get(self.API_BASE, params=params, timeout=15)
            
            # Parse response
            try:
                data = response.json()
            except Exception:
                # If JSON parse fails, surface HTTP error
                response.raise_for_status()
                raise Exception(f"Invalid JSON response from Pixabay")
            
            # Check for HTTP errors
            if not response.ok:
                error_msg = data if isinstance(data, str) else data.get('error', response.text)
                if response.status_code == 400:
                    raise Exception(f"Bad Request (400): {error_msg}. Check your API key and params.")
                elif response.status_code == 429:
                    raise Exception(f"Rate limit exceeded (429). Wait before retrying.")
                else:
                    raise Exception(f"HTTP {response.status_code}: {error_msg}")
            
            # Check rate limit headers
            rate_limit = response.headers.get('X-RateLimit-Remaining')
            if rate_limit and int(rate_limit) < 10:
                logger.warning(f"Pixabay rate limit low: {rate_limit} requests remaining")
            
            # Extract images from response
            hits = data.get('hits', [])
            if not hits:
                logger.warning(f"Pixabay returned 0 images for query: {params.get('q', '(no query)')}")
                return []
            
            images = [self.normalize_image_data(hit) for hit in hits[:count]]
            logger.info(f"Fetched {len(images)} images from Pixabay")
            return images
            
        except Exception as e:
            # Re-raise with context
            raise Exception(f"Pixabay API error: {e}")
    
    def normalize_image_data(self, raw_data: Dict) -> Dict[str, Any]:
        """
        Normalize Pixabay API response to standard format.
        
        Pixabay response keys (per official docs):
        - id, pageURL, type, tags, previewURL, webformatURL, largeImageURL, fullHDURL, imageURL
        - imageWidth, imageHeight, imageSize, views, downloads, likes, comments
        - user_id, user, userImageURL
        """
        return {
            'id': str(raw_data.get('id', '')),
            'source': 'pixabay',
            'photographer': raw_data.get('user', 'Unknown'),
            'photographer_url': f"https://pixabay.com/users/{raw_data.get('user', '')}-{raw_data.get('user_id', '')}/",
            'image_url': raw_data.get('pageURL', ''),
            # Prefer largeImageURL (1280px) over webformatURL (640px)
            'download_url': raw_data.get('largeImageURL') or raw_data.get('webformatURL', ''),
            'description': raw_data.get('tags', ''),
            'width': raw_data.get('imageWidth', 0),
            'height': raw_data.get('imageHeight', 0),
            'tags': [t.strip() for t in raw_data.get('tags', '').split(',') if t.strip()],
            'views': raw_data.get('views', 0),
            'downloads': raw_data.get('downloads', 0),
            'likes': raw_data.get('likes', 0),
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
