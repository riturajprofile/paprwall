"""
Attribution manager (simplified, no secret key).
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict
import logging
from PIL import Image, ImageDraw, ImageFont
from paprwall import CONFIG_DIR

logger = logging.getLogger(__name__)


class AttributionManager:
    """Manages attribution overlay rendering."""

    def __init__(self, config_manager):
        self.config = config_manager
        self.config_dir = CONFIG_DIR
    
    def should_show_attribution(self) -> bool:
        """Check if attribution should be shown on desktop."""
        config = self.config.get_attribution_config()
        return bool(config.get('overlay_enabled', True))
    
    def create_attribution_text(self, image_data: Dict) -> str:
        """
        Create attribution text for image.
        Format: "Photo by [Author] from [Source] | Wallpaper by Paprwall"
        """
        source = image_data.get('source', 'unknown')
        
        if source == 'local':
            return "Paprwall • Your Personal Wallpaper"
        
        photographer = image_data.get('photographer', 'Unknown')
        source_name = source.capitalize()
        
        # Always credit Paprwall
        return f"Photo by {photographer} from {source_name} • Paprwall"
    
    def create_desktop_overlay(self, image_path: Path, image_data: Dict) -> Path:
        """
        Add attribution text overlay to wallpaper image.
        Skip if secret key has been entered.
        
        Args:
            image_path: Path to the original image
            image_data: Image metadata
            
        Returns:
            Path to image (with or without overlay)
        """
        if not self.should_show_attribution():
            logger.debug("Attribution disabled, skipping overlay")
            return image_path  # Return original without overlay
        
        try:
            # Open image
            img = Image.open(image_path)
            
            # Convert to RGBA for transparency support
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Get attribution text
            attribution_text = self.create_attribution_text(image_data)
            
            # Load font
            font_size = 14
            font = None
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                '/usr/share/fonts/TTF/DejaVuSans.ttf',
            ]
            
            for font_path in font_paths:
                try:
                    if Path(font_path).exists():
                        font = ImageFont.truetype(font_path, font_size)
                        break
                except:
                    continue
            
            if font is None:
                logger.warning("Could not load TrueType font, using default")
                font = ImageFont.load_default()
            
            # Get config preferences
            config = self.config.get_attribution_config()
            position_type = config.get('position', 'bottom-right')
            opacity = config.get('opacity', 0.7)
            
            # Create drawing context for text measurement
            draw = ImageDraw.Draw(img)
            
            # Get text bounding box
            bbox = draw.textbbox((0, 0), attribution_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            padding = 12
            img_width, img_height = img.size
            
            # Calculate position based on preference
            if position_type == 'bottom-right':
                x = img_width - text_width - padding * 2
                y = img_height - text_height - padding * 2
            elif position_type == 'bottom-left':
                x = padding
                y = img_height - text_height - padding * 2
            elif position_type == 'top-right':
                x = img_width - text_width - padding * 2
                y = padding
            else:  # top-left
                x = padding
                y = padding
            
            # Create overlay with semi-transparent background
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Draw semi-transparent background rectangle
            background_coords = [
                x - padding,
                y - padding,
                x + text_width + padding,
                y + text_height + padding
            ]
            overlay_draw.rectangle(
                background_coords,
                fill=(0, 0, 0, int(255 * opacity))
            )
            
            # Composite overlay with image
            img = Image.alpha_composite(img, overlay)
            
            # Draw white text on top
            final_draw = ImageDraw.Draw(img)
            final_draw.text((x, y), attribution_text, fill=(255, 255, 255, 255), font=font)
            
            # Save with overlay
            overlay_path = image_path.with_stem(image_path.stem + '_overlay')
            
            # Convert back to RGB for JPEG
            img = img.convert('RGB')
            img.save(overlay_path, 'JPEG', quality=95, optimize=True)
            
            logger.debug(f"Created overlay: {overlay_path.name}")
            return overlay_path
            
        except Exception as e:
            logger.error(f"Failed to create overlay: {e}")
            return image_path
    
    def get_gui_attribution_html(self, image_data: Dict) -> str:
        """
        Generate HTML for image info panel in GUI.
        Always shown regardless of secret key.
        """
        source = image_data.get('source', 'unknown')
        
        if source == 'local':
            return """
            <div style="padding: 10px;">
                <h3 style="margin: 5px 0;">Your Image</h3>
                <p style="margin: 5px 0;">From: Local Collection</p>
                <p style="margin: 5px 0; font-style: italic; color: #666;">Paprwall • Personal Wallpaper Manager</p>
            </div>
            """
        
        photographer = image_data.get('photographer', 'Unknown')
        source_name = source.capitalize()
        source_url = image_data.get('image_url', '#')
        photographer_url = image_data.get('photographer_url', '#')
        
        return f"""
        <div style="padding: 10px;">
            <h3 style="margin: 5px 0;">Photo by <a href="{photographer_url}">{photographer}</a></h3>
            <p style="margin: 5px 0;">Source: <a href="{source_url}">{source_name}</a></p>
            <p style="margin: 5px 0; font-style: italic; color: #666;">Paprwall • Wallpaper Manager</p>
        </div>
        """