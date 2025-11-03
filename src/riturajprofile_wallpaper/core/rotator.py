"""
Wallpaper rotator - handles automatic rotation of wallpapers.
"""
import json
from pathlib import Path
from typing import Optional, List, Dict
import logging
from datetime import datetime, timedelta
from paprwall.core.wallpaper_setter import WallpaperSetter
from paprwall.core.fetcher import ImageFetcher
from paprwall import DATA_DIR

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
        
        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        self._load_state()
        logger.info(f"Rotator initialized with {len(self.images)} images")
    
    def _load_state(self):
        """Load rotation state from file"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.current_index = state.get('current_index', 0)
                    self.images = state.get('images', [])
                    
                    # Validate current index
                    if self.images and self.current_index >= len(self.images):
                        logger.warning(f"Invalid index {self.current_index}, resetting to 0")
                        self.current_index = 0
                    
                    # Load retry tracking
                    if 'last_fetch_attempt' in state:
                        self.last_fetch_attempt = datetime.fromisoformat(state['last_fetch_attempt'])
                    self.fetch_retry_count = state.get('fetch_retry_count', 0)
                    
                    logger.info(f"Loaded state: {len(self.images)} images, index={self.current_index}")
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            self.current_index = 0
            self.images = []
    
    def _save_state(self):
        """Save rotation state to file"""
        try:
            state_data = {
                'current_index': self.current_index,
                'images': self.images,
                'fetch_retry_count': self.fetch_retry_count,
                'image_count': len(self.images),
                'last_updated': datetime.now().isoformat()
            }
            
            if self.last_fetch_attempt:
                state_data['last_fetch_attempt'] = self.last_fetch_attempt.isoformat()
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
            logger.debug("Saved rotation state")
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
            logger.info("Fetching new wallpapers...")
            
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
            else:
                logger.error("Failed to set wallpaper after fetch")
            
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
            logger.info("No images in memory, loading today's images")
            self.images = self.fetcher.get_today_images()
            
            if not self.images:
                logger.warning("No images available for next")
                return False
        
        self.current_index = (self.current_index + 1) % len(self.images)
        logger.info(f"Moving to next wallpaper: index {self.current_index}/{len(self.images)}")
        result = self.set_current()
        self._save_state()
        return result
    
    def previous(self) -> bool:
        """Switch to previous wallpaper"""
        if not self.images:
            logger.info("No images in memory, loading today's images")
            self.images = self.fetcher.get_today_images()
            
            if not self.images:
                logger.warning("No images available for previous")
                return False
        
        self.current_index = (self.current_index - 1) % len(self.images)
        logger.info(f"Moving to previous wallpaper: index {self.current_index}/{len(self.images)}")
        result = self.set_current()
        self._save_state()
        return result
    
    def set_current(self) -> bool:
        """Set current indexed wallpaper"""
        if not self.images:
            logger.error("No images available to set")
            return False
        
        if self.current_index >= len(self.images):
            logger.error(f"Invalid index {self.current_index} for {len(self.images)} images")
            self.current_index = 0
        
        current_image = self.images[self.current_index]
        
        # Get local path
        if 'local_path' in current_image:
            image_path = Path(current_image['local_path'])
        elif 'path' in current_image:
            image_path = Path(current_image['path'])
        else:
            logger.error("No path found in image data")
            return False
        
        if not image_path.exists():
            logger.error(f"Image file not found: {image_path}")
            return False
        
        # Set wallpaper
        logger.info(f"Setting wallpaper: {image_path.name}")
        result = self.setter.set_wallpaper(image_path)
        
        if result:
            logger.info("Wallpaper set successfully")
        else:
            logger.error("Failed to set wallpaper")
        
        return result
    
    def set_specific(self, image_path: Path) -> bool:
        """Set a specific image as wallpaper"""
        if not image_path.exists():
            logger.error(f"Image file not found: {image_path}")
            return False
        
        logger.info(f"Setting specific wallpaper: {image_path.name}")
        return self.setter.set_wallpaper(image_path)
    
    def get_current_image(self) -> Optional[Dict]:
        """Get current image metadata"""
        if self.images and 0 <= self.current_index < len(self.images):
            return self.images[self.current_index]
        logger.debug("No current image available")
        return None
    
    def get_all_images(self) -> List[Dict]:
        """Get all available images"""
        if not self.images:
            logger.info("Loading today's images")
            self.images = self.fetcher.get_today_images()
        return self.images
    
    def get_status(self) -> Dict:
        """Get current rotation status"""
        return {
            'image_count': len(self.images),
            'current_index': self.current_index,
            'current_image': self.get_current_image(),
            'fetch_retry_count': self.fetch_retry_count,
            'last_fetch': self.last_fetch_attempt.isoformat() if self.last_fetch_attempt else None
        }