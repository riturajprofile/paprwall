"""
Image fetcher - simplified to download wallpapers from Picsum only.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import logging
from paprwall import IMAGES_DIR
import requests
import time
from paprwall.core.attribution import AttributionManager

logger = logging.getLogger(__name__)


class ImageFetcher:
    """Fetches and stores wallpaper images"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.attribution_manager = AttributionManager(config_manager)
        self.images_dir = IMAGES_DIR
    
    def fetch_daily_images(self) -> List[Dict]:
        """
        Fetch today's wallpapers exclusively from Picsum.

        Returns:
            List of image metadata with local paths
        """
        # Get today's folder
        today = datetime.now().strftime('%Y-%m-%d')
        today_dir = self.images_dir / today
        today_dir.mkdir(parents=True, exist_ok=True)
        
        # Get configured image count (default to 1 for interval-based fetching)
        total_images = int(self.config.get_preference('images_per_day', 1) or 1)

        # Always download from Picsum
        images = self._download_picsum_images(total_images, today_dir)
        return images

    def _download_picsum_images(self, count: int, dest_dir: Path) -> List[Dict]:
        """Download random images from Picsum as a fallback.

        Args:
            count: number of images to download
            dest_dir: destination directory for images

        Returns:
            List of image metadata dictionaries similar to API results
        """
        results: List[Dict] = []
        for i in range(count):
            # Add a cache-busting query param so each request returns a new image
            ts = int(time.time() * 1000)
            url = f"https://picsum.photos/1920/1080?random={ts}-{i}"
            filename = f"picsum_{i + 1}.jpg"
            local_path = dest_dir / filename
            try:
                r = requests.get(url, timeout=30)
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    f.write(r.content)

                # Build minimal metadata and apply optional overlay
                img_data: Dict = {
                    'source': 'picsum',
                    'download_url': url,
                    'width': 1920,
                    'height': 1080,
                    'attribution': {
                        'provider': 'Picsum',
                        'url': 'https://picsum.photos',
                        'author': 'Random'
                    }
                }

                final_path = self.attribution_manager.create_desktop_overlay(local_path, img_data)
                img_data['local_path'] = str(final_path)

                # Save metadata JSON next to the file
                metadata_path = local_path.with_suffix('.json')
                with open(metadata_path, 'w') as f:
                    json.dump(img_data, f, indent=2)

                results.append(img_data)
                logger.info(f"Downloaded fallback image: {filename}")
            except Exception as e:
                logger.error(f"Failed to download Picsum fallback image {i + 1}/{count}: {e}")
                # Continue to next; partial results are acceptable
                continue

        return results
    
    def get_today_images(self) -> List[Dict]:
        """Get list of today's downloaded images"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_dir = self.images_dir / today
        
        if not today_dir.exists():
            return []
        
        images = []
        for json_file in today_dir.glob('*.json'):
            try:
                with open(json_file, 'r') as f:
                    img_data = json.load(f)
                    # Verify image file exists
                    img_path = img_data.get('local_path') or img_data.get('path')
                    if img_path and Path(img_path).exists():
                        images.append(img_data)
            except Exception as e:
                logger.error(f"Failed to load image metadata from {json_file}: {e}")
        
        return images
    
    def cleanup_old_images(self):
        """Remove images older than configured keep_days"""
        keep_days = self.config.get_preference('keep_days', 7)
        
        if not self.config.get_preference('auto_delete_old', True):
            logger.info("Auto-delete is disabled, skipping cleanup")
            return
        
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        cleaned_count = 0
        for date_dir in self.images_dir.iterdir():
            if date_dir.is_dir():
                try:
                    # Only process date-formatted directories
                    dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d')
                    if dir_date < cutoff_date:
                        import shutil
                        shutil.rmtree(date_dir)
                        cleaned_count += 1
                        logger.info(f"Cleaned up old images: {date_dir.name}")
                except ValueError:
                    # Not a date directory, skip
                    continue
                except Exception as e:
                    logger.error(f"Failed to cleanup {date_dir}: {e}")
        
        if cleaned_count > 0:
            logger.info(f"Cleanup complete: removed {cleaned_count} old date folder(s)")