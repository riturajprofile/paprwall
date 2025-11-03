"""
Image fetcher - coordinates downloading and storing images.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import logging
from riturajprofile_wallpaper import IMAGES_DIR
from riturajprofile_wallpaper.api.source_manager import SourceManager
from riturajprofile_wallpaper.core.local_images import LocalImageManager
from riturajprofile_wallpaper.core.attribution import AttributionManager

logger = logging.getLogger(__name__)


class ImageFetcher:
    """Fetches and stores wallpaper images"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.source_manager = SourceManager(config_manager)
        self.local_manager = LocalImageManager(config_manager)
        self.attribution_manager = AttributionManager(config_manager)
        self.images_dir = IMAGES_DIR
    
    def fetch_daily_images(self) -> List[Dict]:
        """
        Fetch today's wallpaper collection from all enabled sources.
        
        Returns:
            List of image metadata with local paths
        """
        # Get today's folder
        today = datetime.now().strftime('%Y-%m-%d')
        today_dir = self.images_dir / today
        today_dir.mkdir(parents=True, exist_ok=True)
        
        # Get configured image count
        total_images = self.config.get_preference('images_per_day', 5)
        
        # Calculate how many from APIs vs local
        enabled_sources = self.config.get_enabled_sources()
        local_enabled = 'local' in enabled_sources
        
        if local_enabled:
            weights = self.config.get_source_weights()
            local_weight = weights.get('local', 0)
            total_weight = sum(weights.values())
            
            if total_weight > 0:
                local_count = int((local_weight / total_weight) * total_images)
                api_count = total_images - local_count
            else:
                local_count = 0
                api_count = total_images
        else:
            local_count = 0
            api_count = total_images
        
        all_images = []
        
        # Fetch from APIs
        if api_count > 0:
            try:
                api_images = self.source_manager.fetch_daily_images(api_count)
                
                # Download each image
                for idx, img_data in enumerate(api_images):
                    try:
                        # Generate filename
                        source = img_data['source']
                        filename = f"{source}_{idx + 1}.jpg"
                        local_path = today_dir / filename
                        
                        # Download image
                        client = self.source_manager.clients[source]
                        if client.download_image(img_data['download_url'], local_path):
                            # Add attribution overlay if enabled
                            final_path = self.attribution_manager.create_desktop_overlay(
                                local_path, img_data
                            )
                            
                            # Update image data with local path
                            img_data['local_path'] = str(final_path)
                            
                            # Save metadata
                            metadata_path = local_path.with_suffix('.json')
                            with open(metadata_path, 'w') as f:
                                json.dump(img_data, f, indent=2)
                            
                            all_images.append(img_data)
                            logger.info(f"Downloaded: {filename}")
                    
                    except Exception as e:
                        logger.error(f"Failed to download image: {e}")
            
            except Exception as e:
                logger.error(f"Failed to fetch API images: {e}")
        
        # Add local images
        if local_count > 0 and local_enabled:
            try:
                local_images = self.local_manager.get_random_images(local_count)
                all_images.extend(local_images)
                logger.info(f"Added {len(local_images)} local images")
            except Exception as e:
                logger.error(f"Failed to get local images: {e}")
        
        return all_images
    
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
                    images.append(img_data)
            except Exception:
                pass
        
        return images
    
    def cleanup_old_images(self):
        """Remove images older than configured keep_days"""
        keep_days = self.config.get_preference('keep_days', 7)
        
        if not self.config.get_preference('auto_delete_old', True):
            return
        
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        for date_dir in self.images_dir.iterdir():
            if date_dir.is_dir():
                try:
                    dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d')
                    if dir_date < cutoff_date:
                        import shutil
                        shutil.rmtree(date_dir)
                        logger.info(f"Cleaned up old images: {date_dir.name}")
                except Exception as e:
                    logger.error(f"Failed to cleanup {date_dir}: {e}")
