"""
System tray icon support for PaprWall.
Allows running in background with minimize to tray.
"""

import os
import sys
import platform
from pathlib import Path
from typing import Optional, Callable

try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    pystray = None
    item = None


class SystemTray:
    """System tray icon manager."""
    
    def __init__(self, app_name: str = "PaprWall", on_show: Optional[Callable] = None, on_quit: Optional[Callable] = None):
        """Initialize system tray icon."""
        self.app_name = app_name
        self.icon = None
        self.on_show_callback = on_show
        self.on_quit_callback = on_quit
        
        if not TRAY_AVAILABLE:
            print("Warning: pystray not available. System tray functionality disabled.")
            print("Install with: pip install pystray")
    
    def create_icon_image(self) -> Optional[Image.Image]:
        """Create a simple icon image for the system tray."""
        try:
            # Try to load app icon
            icon_paths = [
                Path(__file__).parent.parent.parent / "assets" / "paprwall-icon.png",
                Path(__file__).parent.parent.parent / "assets" / "paprwall-icon-64.png",
                Path(__file__).parent.parent.parent / "assets" / "paprwall-icon-32.png",
            ]
            
            for icon_path in icon_paths:
                if icon_path.exists():
                    img = Image.open(icon_path)
                    # Resize to appropriate tray icon size
                    img = img.resize((64, 64), Image.Resampling.LANCZOS)
                    return img
        except Exception as e:
            print(f"Failed to load icon: {e}")
        
        # Fallback: create simple icon
        return self._create_fallback_icon()
    
    def _create_fallback_icon(self) -> Image.Image:
        """Create a simple fallback icon."""
        # Create a 64x64 icon with "PW" text
        size = 64
        image = Image.new('RGB', (size, size), color=(60, 130, 246))
        draw = ImageDraw.Draw(image)
        
        # Draw "PW" text
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = None
        
        text = "PW"
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = 30
            text_height = 20
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        return image
    
    def create_menu(self):
        """Create the system tray menu."""
        if not TRAY_AVAILABLE or not pystray or not item:
            return None
        
        return pystray.Menu(
            item('Show Window', self.on_show, default=True),
            item('Quit', self.on_quit)
        )
    
    def on_show(self, icon, item):
        """Handle show window action."""
        if self.on_show_callback:
            self.on_show_callback()
    
    def on_quit(self, icon, item):
        """Handle quit action."""
        if self.on_quit_callback:
            self.on_quit_callback()
        if self.icon:
            self.icon.stop()
    
    def start(self):
        """Start the system tray icon."""
        if not TRAY_AVAILABLE or not pystray:
            return False
        
        try:
            image = self.create_icon_image()
            if not image:
                return False
            
            self.icon = pystray.Icon(
                self.app_name,
                image,
                self.app_name,
                self.create_menu()
            )
            
            # Run in separate thread
            import threading
            thread = threading.Thread(target=self.icon.run, daemon=True)
            thread.start()
            
            return True
        except Exception as e:
            print(f"Failed to start system tray: {e}")
            return False
    
    def stop(self):
        """Stop the system tray icon."""
        if self.icon:
            try:
                self.icon.stop()
            except:
                pass
    
    def is_available(self) -> bool:
        """Check if system tray is available."""
        return TRAY_AVAILABLE


def install_pystray():
    """Install pystray if not available."""
    if TRAY_AVAILABLE:
        print("pystray is already installed")
        return True
    
    try:
        import subprocess
        print("Installing pystray...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray"])
        print("✓ pystray installed successfully!")
        print("Please restart PaprWall to use system tray functionality.")
        return True
    except Exception as e:
        print(f"Failed to install pystray: {e}")
        print("You can install it manually with: pip install pystray")
        return False


if __name__ == "__main__":
    # Test the system tray
    import time
    
    def on_show():
        print("Show window clicked")
    
    def on_quit():
        print("Quit clicked")
    
    tray = SystemTray(on_show=on_show, on_quit=on_quit)
    
    if not tray.is_available():
        print("Installing pystray...")
        install_pystray()
    else:
        print("Starting system tray...")
        if tray.start():
            print("System tray started. Press Ctrl+C to exit.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping...")
                tray.stop()
        else:
            print("Failed to start system tray")
