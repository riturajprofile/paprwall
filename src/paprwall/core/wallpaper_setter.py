"""
Wallpaper setter for different Linux desktop environments.
"""
import subprocess
from pathlib import Path
import logging
import os
import shutil

logger = logging.getLogger(__name__)


class WallpaperSetter:
    """Sets wallpaper across different Linux desktop environments"""
    
    def __init__(self):
        self.de = self._detect_desktop_environment()
        logger.info(f"Detected desktop environment: {self.de}")
    
    def _detect_desktop_environment(self) -> str:
        """Detect the current desktop environment"""
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
        elif 'unity' in desktop:
            return 'gnome'  # Unity uses GNOME settings
        
        # Fallback detection
        session = os.environ.get('DESKTOP_SESSION', '').lower()
        if 'gnome' in session or 'ubuntu' in session:
            return 'gnome'
        elif 'kde' in session or 'plasma' in session:
            return 'kde'
        elif 'xfce' in session:
            return 'xfce'
        elif 'mate' in session:
            return 'mate'
        elif 'cinnamon' in session:
            return 'cinnamon'

        # Probe for known tools even if env vars are missing (common in minimal shells)
        try:
            if shutil.which('gsettings'):
                return 'gnome'
            if shutil.which('qdbus'):
                return 'kde'
            if shutil.which('xfconf-query'):
                return 'xfce'
            if shutil.which('pcmanfm') or shutil.which('pcmanfm-qt'):
                return 'lxde'
        except Exception:
            pass
        
        logger.warning("Could not detect desktop environment")
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
        
        if not image_path.is_file():
            logger.error(f"Not a file: {image_path}")
            return False
        
        logger.info(f"Setting wallpaper: {image_path.name} (DE: {self.de})")
        
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
        try:
            uri = f"file://{image_path.absolute()}"
            
            # Set light mode wallpaper
            subprocess.run([
                'gsettings', 'set',
                'org.gnome.desktop.background', 'picture-uri',
                uri
            ], check=True, capture_output=True)
            
            # Also set dark mode URI (may not exist on older systems)
            try:
                subprocess.run([
                    'gsettings', 'set',
                    'org.gnome.desktop.background', 'picture-uri-dark',
                    uri
                ], check=True, capture_output=True, timeout=5)
            except:
                logger.debug("Dark mode wallpaper setting not available")
            
            # Set picture options for better display
            try:
                subprocess.run([
                    'gsettings', 'set',
                    'org.gnome.desktop.background', 'picture-options',
                    'zoom'
                ], check=False, capture_output=True, timeout=5)
            except:
                pass
            
            logger.info("GNOME wallpaper set successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"GNOME wallpaper setting failed: {e}")
            return False
    
    def _set_kde(self, image_path: Path) -> bool:
        """Set wallpaper for KDE Plasma"""
        try:
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
            ], check=True, capture_output=True, timeout=10)
            
            logger.info("KDE wallpaper set successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"KDE wallpaper setting failed: {e}")
            return False
        except FileNotFoundError:
            logger.error("qdbus not found, KDE wallpaper setting not available")
            return False
    
    def _set_xfce(self, image_path: Path) -> bool:
        """Set wallpaper for XFCE"""
        try:
            # Get list of monitors/screens
            result = subprocess.run(
                ['xfconf-query', '-c', 'xfce4-desktop', '-l'],
                capture_output=True, text=True, timeout=10
            )
            
            success = False
            # Set for each monitor that has a last-image property
            for line in result.stdout.split('\n'):
                if '/last-image' in line or '/backdrop/screen' in line:
                    try:
                        subprocess.run([
                            'xfconf-query', '-c', 'xfce4-desktop',
                            '-p', line.strip(),
                            '-s', str(image_path.absolute())
                        ], check=True, capture_output=True, timeout=5)
                        success = True
                    except:
                        continue
            
            if success:
                logger.info("XFCE wallpaper set successfully")
            else:
                logger.warning("XFCE wallpaper setting may have failed")
            
            return success
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"XFCE wallpaper setting failed: {e}")
            return False
    
    def _set_mate(self, image_path: Path) -> bool:
        """Set wallpaper for MATE"""
        try:
            subprocess.run([
                'gsettings', 'set',
                'org.mate.background', 'picture-filename',
                str(image_path.absolute())
            ], check=True, capture_output=True, timeout=10)
            
            logger.info("MATE wallpaper set successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"MATE wallpaper setting failed: {e}")
            return False
    
    def _set_cinnamon(self, image_path: Path) -> bool:
        """Set wallpaper for Cinnamon"""
        try:
            uri = f"file://{image_path.absolute()}"
            
            subprocess.run([
                'gsettings', 'set',
                'org.cinnamon.desktop.background', 'picture-uri',
                uri
            ], check=True, capture_output=True, timeout=10)
            
            logger.info("Cinnamon wallpaper set successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Cinnamon wallpaper setting failed: {e}")
            return False
    
    def _set_lxde(self, image_path: Path) -> bool:
        """Set wallpaper for LXDE/LXQt"""
        try:
            subprocess.run([
                'pcmanfm', '--set-wallpaper',
                str(image_path.absolute())
            ], check=True, capture_output=True, timeout=10)
            
            logger.info("LXDE wallpaper set successfully")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try LXQt method
            try:
                subprocess.run([
                    'pcmanfm-qt', '--set-wallpaper',
                    str(image_path.absolute())
                ], check=True, capture_output=True, timeout=10)
                
                logger.info("LXQt wallpaper set successfully")
                return True
            except:
                logger.error("LXDE/LXQt wallpaper setting failed")
                return False
    
    def _set_generic(self, image_path: Path) -> bool:
        """Try generic wallpaper setting methods"""
        # Try feh as fallback
        try:
            subprocess.run(
                ['feh', '--bg-scale', str(image_path.absolute())],
                check=True, capture_output=True, timeout=10
            )
            logger.info("Set wallpaper using feh")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Try nitrogen
        try:
            subprocess.run(
                ['nitrogen', '--set-scaled', str(image_path.absolute())],
                check=True, capture_output=True, timeout=10
            )
            logger.info("Set wallpaper using nitrogen")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Try hsetroot
        try:
            subprocess.run(
                ['hsetroot', '-fill', str(image_path.absolute())],
                check=True, capture_output=True, timeout=10
            )
            logger.info("Set wallpaper using hsetroot")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        logger.error("All generic wallpaper setting methods failed")
        return False