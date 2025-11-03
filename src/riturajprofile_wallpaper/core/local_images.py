"""
Local image manager for user's own images.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import random
from PIL import Image
from riturajprofile_wallpaper import CONFIG_DIR


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
    
    def scan_local_images(self) -> List[Dict]:
        """
        Scan local folder for valid wallpaper images.
        Returns list of image metadata.
        """
        valid_images = []
        
        if not self.local_folder.exists():
            return valid_images
        
        for img_path in self.local_folder.glob('**/*'):
            if img_path.is_file() and img_path.suffix.lower() in self.SUPPORTED_FORMATS:
                if self.is_valid_wallpaper(img_path):
                    valid_images.append({
                        'path': str(img_path),
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
                    return False
                
                # Check aspect ratio
                ratio = width / height
                return self.MIN_RATIO <= ratio <= self.MAX_RATIO
                
        except Exception:
            return False
    
    def get_random_images(self, count: int = 1) -> List[Dict]:
        """Get random images from local collection"""
        images = self.scan_local_images()
        
        if not images:
            return []
        
        # Return random selection
        return random.sample(images, min(count, len(images)))
    
    def add_image(self, source_path: Path) -> bool:
        """
        Copy image to managed local folder.
        
        Args:
            source_path: Path to image file to add
            
        Returns:
            True if successful
        """
        try:
            if not self.is_valid_wallpaper(source_path):
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
            
            # Rescan to update metadata
            self.scan_local_images()
            
            return True
            
        except Exception as e:
            print(f"Failed to add image: {e}")
            return False
    
    def remove_image(self, filename: str) -> bool:
        """Remove image from local collection"""
        try:
            img_path = self.local_folder / filename
            if img_path.exists():
                img_path.unlink()
                self.scan_local_images()
                return True
            return False
        except Exception:
            return False
    
    def get_image_count(self) -> int:
        """Get count of valid local images"""
        return len(self.scan_local_images())
    
    def _save_metadata(self, images: List[Dict]):
        """Save local images metadata"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(images, f, indent=2)
        except Exception:
            pass
    
    def _load_metadata(self) -> List[Dict]:
        """Load local images metadata"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
