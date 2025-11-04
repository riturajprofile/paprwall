"""
CLI interface for paprwall (Picsum-only, simplified).
"""
import argparse
import sys
from pathlib import Path
from paprwall import __version__
from paprwall.config.config_manager import ConfigManager
from paprwall.core.rotator import WallpaperRotator
from paprwall.utils.logger import setup_logger

logger = setup_logger()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='paprwall - Auto-rotating wallpaper app for Linux',
        prog='paprwall'
    )
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    # Actions
    parser.add_argument('--gui', action='store_true', help='Launch GUI')
    parser.add_argument('--fetch', action='store_true', help='Fetch new images now')
    parser.add_argument('--next', action='store_true', help='Switch to next wallpaper')
    parser.add_argument('--prev', '--previous', action='store_true', help='Switch to previous wallpaper')
    parser.add_argument('--set', metavar='IMAGE_PATH', help='Set specific image as wallpaper')
    parser.add_argument('--current', action='store_true', help='Show current wallpaper info')
    
    # Removed: sources and themes management (no longer applicable)
    
    # Service (simplified placeholders)
    parser.add_argument('--start', action='store_true', help='Start wallpaper rotation service')
    parser.add_argument('--stop', action='store_true', help='Stop wallpaper rotation service')
    parser.add_argument('--status', action='store_true', help='Show service status')
    
    args = parser.parse_args()
    
    # Initialize config
    config = ConfigManager()
    
    # Handle GUI launch
    if args.gui:
        try:
            from paprwall.gui.wallpaper_manager_gui import main as gui_main
            logger.info("Launching GUI...")
            gui_main()
            return 0
        except Exception as e:
            logger.error(f"Failed to launch GUI: {e}")
            return 1
    
    # Handle fetch
    if args.fetch:
        logger.info("Fetching new wallpapers...")
        rotator = WallpaperRotator(config)
        if rotator.fetch_and_rotate():
            logger.info("✓ Successfully fetched and set new wallpapers")
            return 0
        else:
            logger.error("✗ Failed to fetch wallpapers")
            return 1
    
    # Handle next/previous
    if args.next:
        logger.info("Switching to next wallpaper...")
        rotator = WallpaperRotator(config)
        if rotator.next():
            logger.info("✓ Switched to next wallpaper")
            return 0
        else:
            logger.error("✗ Failed to switch wallpaper")
            return 1
    
    if args.prev:
        logger.info("Switching to previous wallpaper...")
        rotator = WallpaperRotator(config)
        if rotator.previous():
            logger.info("✓ Switched to previous wallpaper")
            return 0
        else:
            logger.error("✗ Failed to switch wallpaper")
            return 1
    
    # Handle set specific image
    if args.set:
        image_path = Path(args.set)
        if not image_path.exists():
            logger.error(f"Image not found: {image_path}")
            return 1
        
        logger.info(f"Setting wallpaper: {image_path}")
        rotator = WallpaperRotator(config)
        if rotator.set_specific(image_path):
            logger.info("✓ Wallpaper set successfully")
            return 0
        else:
            logger.error("✗ Failed to set wallpaper")
            return 1
    
    # Handle current image info
    if args.current:
        rotator = WallpaperRotator(config)
        current = rotator.get_current_image()
        if current:
            print("\nCurrent Wallpaper:")
            print(f"  Source: {current.get('source', 'unknown')}")
            print(f"  Photographer: {current.get('photographer', 'Unknown')}")
            if 'description' in current:
                print(f"  Description: {current['description']}")
            if 'local_path' in current:
                print(f"  Path: {current['local_path']}")
            return 0
        else:
            logger.error("No current wallpaper found")
            return 1
    
    # Sources/themes commands removed
    
    # Handle service commands (basic implementation)
    if args.start:
        logger.info("Starting wallpaper rotation service...")
        logger.info("Service management is best done through systemd")
        logger.info("Run: systemctl --user enable paprwall")
        logger.info("     systemctl --user start paprwall")
        return 0
    
    if args.stop:
        logger.info("Stopping wallpaper rotation service...")
        logger.info("Run: systemctl --user stop paprwall")
        return 0
    
    if args.status:
        logger.info("Checking service status...")
        logger.info("Run: systemctl --user status paprwall")
        return 0
    
    # No arguments - show help
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
