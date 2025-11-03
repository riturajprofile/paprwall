"""
Wallpaper rotator - handles automatic rotation of wallpapers.
"""
import json
from pathlib import Path
from typing import Optional, List, Dict
import logging
from datetime import datetime, timedelta
from riturajprofile_wallpaper.core.wallpaper_setter import WallpaperSetter
from riturajprofile_wallpaper.core.fetcher import ImageFetcher
from riturajprofile_wallpaper import DATA_DIR

logger = logging.getLogger(__name__)


class WallpaperRotator:
    """Manages wallpaper rotation"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.setter = WallpaperSetter()
        self.fetcher = ImageFetcher(config_manager)
        self.state_file = DATA_DIR / 'rotation_state.json'
        self.current_index = 0
        self.images = []
        self.last_fetch_attempt = None
        self.fetch_retry_count = 0
        
        self._load_state()
    
    def _load_state(self):
        """Load rotation state from file"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.current_index = state.get('current_index', 0)
                    self.images = state.get('images', [])
                    
                    # Load retry tracking
                    if 'last_fetch_attempt' in state:
                        self.last_fetch_attempt = datetime.fromisoformat(state['last_fetch_attempt'])
                    self.fetch_retry_count = state.get('fetch_retry_count', 0)
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
    
    def _save_state(self):
        """Save rotation state to file"""
        try:
            state_data = {
                'current_index': self.current_index,
                'images': self.images,
                'fetch_retry_count': self.fetch_retry_count
            }
            
            if self.last_fetch_attempt:
                state_data['last_fetch_attempt'] = self.last_fetch_attempt.isoformat()
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def fetch_and_rotate(self, is_retry: bool = False) -> bool:
        """Fetch new images and set first one
        
        Args:
            is_retry: Whether this is a retry attempt
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Record attempt time
            self.last_fetch_attempt = datetime.now()
            
            # Fetch new images
            self.images = self.fetcher.fetch_daily_images()
            
            if not self.images:
                logger.warning("No images fetched")
                self.fetch_retry_count += 1
                self._save_state()
                return False
            
            # Success! Reset retry count
            self.fetch_retry_count = 0
            
            # Reset index and set first image
            self.current_index = 0
            result = self.set_current()
            
            self._save_state()
            
            if result and not is_retry:
                logger.info(f"Successfully fetched and set {len(self.images)} new wallpapers")
            elif result and is_retry:
                logger.info(f"Retry successful! Fetched {len(self.images)} wallpapers")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch and rotate: {e}")
            self.fetch_retry_count += 1
            self._save_state()
            return False
    
    def should_retry_fetch(self) -> bool:
        """Check if we should retry a failed fetch
        
        Returns:
            bool: True if enough time has passed since last attempt
        """
        if not self.last_fetch_attempt:
            return True
        
        # If we have recent images, don't retry
        if self.images and self.fetch_retry_count == 0:
            return False
        
        # Retry after 1 hour
        time_since_last = datetime.now() - self.last_fetch_attempt
        retry_interval = timedelta(hours=1)
        
        should_retry = time_since_last >= retry_interval
        
        if should_retry and self.fetch_retry_count > 0:
            logger.info(f"Retry attempt #{self.fetch_retry_count + 1} - Last attempt was {time_since_last.total_seconds() / 3600:.1f} hours ago")
        
        return should_retry
    
    def next(self) -> bool:
        """Switch to next wallpaper"""
        if not self.images:
            # Try to load today's images
            self.images = self.fetcher.get_today_images()
            
            if not self.images:
                logger.warning("No images available")
                return False
        
        self.current_index = (self.current_index + 1) % len(self.images)
        result = self.set_current()
        self._save_state()
        return result
    
    def previous(self) -> bool:
        """Switch to previous wallpaper"""
        if not self.images:
            self.images = self.fetcher.get_today_images()
            
            if not self.images:
                return False
        
        self.current_index = (self.current_index - 1) % len(self.images)
        result = self.set_current()
        self._save_state()
        return result
    
    def set_current(self) -> bool:
        """Set current indexed wallpaper"""
        if not self.images or self.current_index >= len(self.images):
            return False
        
        current_image = self.images[self.current_index]
        
        # Get local path
        if 'local_path' in current_image:
            image_path = Path(current_image['local_path'])
        elif 'path' in current_image:
            image_path = Path(current_image['path'])
        else:
            logger.error("No path found in image data")
            return False
        
        # Set wallpaper
        return self.setter.set_wallpaper(image_path)
    
    def set_specific(self, image_path: Path) -> bool:
        """Set a specific image as wallpaper"""
        return self.setter.set_wallpaper(image_path)
    
    def get_current_image(self) -> Optional[Dict]:
        """Get current image metadata"""
        if self.images and 0 <= self.current_index < len(self.images):
            return self.images[self.current_index]
        return None
    
    def get_all_images(self) -> List[Dict]:
        """Get all available images"""
        if not self.images:
            self.images = self.fetcher.get_today_images()
        return self.images
