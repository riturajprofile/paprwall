"""
Local image manager for user's own images.
"""
import json
from pathlib import Path
from typing import List, Dict
import random
import logging
from datetime import datetime
from PIL import Image
from paprwall import CONFIG_DIR

logger = logging.getLogger(__name__)


class LocalImageManager:
    """
    Manages user's local images for wallpapers.
    Supports: JPG, PNG, WebP
    Filters: Only 16:9 or similar ratios
    """
    
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']
    MIN_WIDTH = 1920
    MIN_RATIO = 1.5  # 16:10
    MAX_RATIO = 1.9  # wider than 16:9
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.local_folder = Path(self.config.get_local_folder())
        self.metadata_file = CONFIG_DIR / "local_images.json"
        
        # Ensure local folder exists
        self.local_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Local images folder: {self.local_folder}")
    
    def scan_local_images(self) -> List[Dict]:
        """
        Scan local folder for valid wallpaper images.
        Returns list of image metadata.
        """
        valid_images = []
        
        if not self.local_folder.exists():
            logger.warning(f"Local folder does not exist: {self.local_folder}")
            return valid_images
        
        scanned_count = 0
        for img_path in self.local_folder.glob('**/*'):
            if img_path.is_file() and img_path.suffix.lower() in self.SUPPORTED_FORMATS:
                scanned_count += 1
                if self.is_valid_wallpaper(img_path):
                    valid_images.append({
                        'path': str(img_path),
                        'local_path': str(img_path),  # Add local_path for consistency
                        'filename': img_path.name,
                        'source': 'local',
                        'photographer': 'You',
                        'photographer_url': '',
                        'image_url': '',
                        'download_url': str(img_path),
                        'description': img_path.stem,
                        'added_date': img_path.stat().st_mtime,
                        'id': img_path.stem
                    })
        
        logger.info(f"Scanned {scanned_count} images, {len(valid_images)} valid wallpapers")
        
        # Save metadata
        self._save_metadata(valid_images)
        
        return valid_images
    
    def is_valid_wallpaper(self, img_path: Path) -> bool:
        """Check if image has acceptable aspect ratio and resolution"""
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                
                # Check minimum width
                if width < self.MIN_WIDTH:
                    logger.debug(f"Image too small: {img_path.name} ({width}x{height})")
                    return False
                
                # Check aspect ratio
                ratio = width / height
                if not (self.MIN_RATIO <= ratio <= self.MAX_RATIO):
                    logger.debug(f"Invalid aspect ratio: {img_path.name} ({ratio:.2f})")
                    return False
                
                return True
                
        except Exception as e:
            logger.error(f"Failed to check image {img_path.name}: {e}")
            return False
    
    def get_random_images(self, count: int = 1) -> List[Dict]:
        """Get random images from local collection"""
        images = self.scan_local_images()
        
        if not images:
            logger.warning("No valid local images found")
            return []
        
        # Return random selection
        selected = random.sample(images, min(count, len(images)))
        logger.info(f"Selected {len(selected)} random local images")
        return selected
    
    def add_image(self, source_path: Path) -> bool:
        """
        Copy image to managed local folder.
        
        Args:
            source_path: Path to image file to add
            
        Returns:
            True if successful
        """
        try:
            if not source_path.exists():
                logger.error(f"Source image not found: {source_path}")
                return False
            
            if not self.is_valid_wallpaper(source_path):
                logger.warning(f"Image does not meet wallpaper requirements: {source_path.name}")
                return False
            
            # Copy to local folder
            dest_path = self.local_folder / source_path.name
            
            # Handle name conflicts
            counter = 1
            while dest_path.exists():
                dest_path = self.local_folder / f"{source_path.stem}_{counter}{source_path.suffix}"
                counter += 1
            
            # Copy file
            import shutil
            shutil.copy2(source_path, dest_path)
            logger.info(f"Added image to local collection: {dest_path.name}")
            
            # Rescan to update metadata
            self.scan_local_images()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to add image: {e}")
            return False
    
    def remove_image(self, filename: str) -> bool:
        """Remove image from local collection"""
        try:
            img_path = self.local_folder / filename
            if img_path.exists():
                img_path.unlink()
                logger.info(f"Removed image: {filename}")
                self.scan_local_images()
                return True
            logger.warning(f"Image not found: {filename}")
            return False
        except Exception as e:
            logger.error(f"Failed to remove image: {e}")
            return False
    
    def get_image_count(self) -> int:
        """Get count of valid local images"""
        count = len(self.scan_local_images())
        logger.debug(f"Local image count: {count}")
        return count
    
    def _save_metadata(self, images: List[Dict]):
        """Save local images metadata"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump({
                    'images': images,
                    'last_scan': datetime.now().isoformat(),
                    'count': len(images)
                }, f, indent=2)
            logger.debug(f"Saved metadata for {len(images)} images")
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
    
    def _load_metadata(self) -> List[Dict]:
        """Load local images metadata"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    data = json.load(f)
                    return data.get('images', [])
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")
        return []