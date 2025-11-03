"""
Base client for API image sources.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from pathlib import Path


class BaseAPIClient(ABC):
    """Abstract base class for all API clients"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'paprwall/1.0.0'
        })
    
    @abstractmethod
    def fetch_images(self, count: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch images from the API.
        
        Args:
            count: Number of images to fetch
            
        Returns:
            List of image metadata dictionaries
        """
        pass
    
    @abstractmethod
    def get_api_key(self) -> str:
        """Get API key from config"""
        pass
    
    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """Test if API is accessible and key is valid"""
        pass
    
    def download_image(self, url: str, save_path: Path) -> bool:
        """
        Download image from URL to local path.
        
        Args:
            url: Image URL
            save_path: Path to save image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            print(f"Failed to download image: {e}")
            return False
    
    def normalize_image_data(self, raw_data: Dict) -> Dict[str, Any]:
        """
        Normalize API response to standard format.
        
        Returns:
            {
                'id': str,
                'source': str,
                'photographer': str,
                'photographer_url': str,
                'image_url': str,
                'download_url': str,
                'description': str,
                'width': int,
                'height': int,
                'tags': List[str]
            }
        """
        pass
