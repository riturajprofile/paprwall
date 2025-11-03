"""
Wallpaper setter for different Linux desktop environments.
"""
import subprocess
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class WallpaperSetter:
    """Sets wallpaper across different Linux desktop environments"""
    
    def __init__(self):
        self.de = self._detect_desktop_environment()
    
    def _detect_desktop_environment(self) -> str:
        """Detect the current desktop environment"""
        import os
        
        # Check XDG_CURRENT_DESKTOP
        desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        
        if 'gnome' in desktop:
            return 'gnome'
        elif 'kde' in desktop or 'plasma' in desktop:
            return 'kde'
        elif 'xfce' in desktop:
            return 'xfce'
        elif 'mate' in desktop:
            return 'mate'
        elif 'cinnamon' in desktop:
            return 'cinnamon'
        elif 'lxde' in desktop or 'lxqt' in desktop:
            return 'lxde'
        
        # Fallback detection
        session = os.environ.get('DESKTOP_SESSION', '').lower()
        if 'gnome' in session:
            return 'gnome'
        elif 'kde' in session:
            return 'kde'
        elif 'xfce' in session:
            return 'xfce'
        
        return 'unknown'
    
    def set_wallpaper(self, image_path: Path) -> bool:
        """
        Set wallpaper for detected desktop environment.
        
        Args:
            image_path: Path to wallpaper image
            
        Returns:
            True if successful
        """
        if not image_path.exists():
            logger.error(f"Image not found: {image_path}")
            return False
        
        image_uri = f"file://{image_path.absolute()}"
        
        try:
            if self.de == 'gnome':
                return self._set_gnome(image_path)
            elif self.de == 'kde':
                return self._set_kde(image_path)
            elif self.de == 'xfce':
                return self._set_xfce(image_path)
            elif self.de == 'mate':
                return self._set_mate(image_path)
            elif self.de == 'cinnamon':
                return self._set_cinnamon(image_path)
            elif self.de == 'lxde':
                return self._set_lxde(image_path)
            else:
                logger.warning(f"Unknown DE: {self.de}, trying generic methods")
                return self._set_generic(image_path)
        except Exception as e:
            logger.error(f"Failed to set wallpaper: {e}")
            return False
    
    def _set_gnome(self, image_path: Path) -> bool:
        """Set wallpaper for GNOME/Ubuntu"""
        subprocess.run([
            'gsettings', 'set',
            'org.gnome.desktop.background', 'picture-uri',
            f"file://{image_path.absolute()}"
        ], check=True)
        
        # Also set dark mode URI
        subprocess.run([
            'gsettings', 'set',
            'org.gnome.desktop.background', 'picture-uri-dark',
            f"file://{image_path.absolute()}"
        ], check=False)  # Don't fail if dark mode not supported
        
        return True
    
    def _set_kde(self, image_path: Path) -> bool:
        """Set wallpaper for KDE Plasma"""
        script = f"""
        var allDesktops = desktops();
        for (var i = 0; i < allDesktops.length; i++) {{
            var desktop = allDesktops[i];
            desktop.wallpaperPlugin = "org.kde.image";
            desktop.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
            desktop.writeConfig("Image", "file://{image_path.absolute()}");
        }}
        """
        
        subprocess.run([
            'qdbus', 'org.kde.plasmashell', '/PlasmaShell',
            'org.kde.PlasmaShell.evaluateScript', script
        ], check=True)
        
        return True
    
    def _set_xfce(self, image_path: Path) -> bool:
        """Set wallpaper for XFCE"""
        # Get list of monitors
        result = subprocess.run(
            ['xfconf-query', '-c', 'xfce4-desktop', '-l'],
            capture_output=True, text=True
        )
        
        # Set for each monitor
        for line in result.stdout.split('\n'):
            if '/last-image' in line:
                subprocess.run([
                    'xfconf-query', '-c', 'xfce4-desktop',
                    '-p', line.strip(),
                    '-s', str(image_path.absolute())
                ], check=False)
        
        return True
    
    def _set_mate(self, image_path: Path) -> bool:
        """Set wallpaper for MATE"""
        subprocess.run([
            'gsettings', 'set',
            'org.mate.background', 'picture-filename',
            str(image_path.absolute())
        ], check=True)
        
        return True
    
    def _set_cinnamon(self, image_path: Path) -> bool:
        """Set wallpaper for Cinnamon"""
        subprocess.run([
            'gsettings', 'set',
            'org.cinnamon.desktop.background', 'picture-uri',
            f"file://{image_path.absolute()}"
        ], check=True)
        
        return True
    
    def _set_lxde(self, image_path: Path) -> bool:
        """Set wallpaper for LXDE/LXQt"""
        subprocess.run([
            'pcmanfm', '--set-wallpaper',
            str(image_path.absolute())
        ], check=True)
        
        return True
    
    def _set_generic(self, image_path: Path) -> bool:
        """Try generic wallpaper setting methods"""
        # Try feh as fallback
        try:
            subprocess.run(['feh', '--bg-scale', str(image_path.absolute())], check=True)
            return True
        except:
            pass
        
        # Try nitrogen
        try:
            subprocess.run(['nitrogen', '--set-scaled', str(image_path.absolute())], check=True)
            return True
        except:
            pass
        
        return False
