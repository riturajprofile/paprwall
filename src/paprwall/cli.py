"""
CLI interface for paprwall.
"""
import argparse
import sys
from pathlib import Path
from paprwall import __version__
from paprwall.config.config_manager import ConfigManager
from paprwall.core.rotator import WallpaperRotator
from paprwall.api.source_manager import SourceManager
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
    
    # Sources
    parser.add_argument('--sources', action='store_true', help='List enabled sources')
    parser.add_argument('--test', metavar='SOURCE', help='Test specific source (pixabay, unsplash, pexels)')
    parser.add_argument('--enable', metavar='SOURCE', help='Enable a source')
    parser.add_argument('--disable', metavar='SOURCE', help='Disable a source')
    
    # Themes
    parser.add_argument('--themes', action='store_true', help='List available themes')
    parser.add_argument('--set-theme', metavar='THEME', help='Set wallpaper theme (nature, city, space, etc.)')
    parser.add_argument('--custom-query', metavar='QUERY', help='Set custom search query for all sources')
    parser.add_argument('--current-theme', action='store_true', help='Show current theme')
    
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
            from paprwall.gui.main_window import main as gui_main
            return gui_main()
        except ImportError as e:
            logger.error(f"Failed to launch GUI: {e}")
            logger.error("Make sure PyGObject is installed: pip install PyGObject")
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
    
    # Handle sources
    if args.sources:
        enabled = config.get_enabled_sources()
        weights = config.get_source_weights()
        
        print("\nEnabled Sources:")
        for source in enabled:
            weight = weights.get(source, 0)
            print(f"  ✓ {source.capitalize()} (weight: {weight})")
        
        all_sources = ['pixabay', 'unsplash', 'pexels', 'local']
        disabled = [s for s in all_sources if s not in enabled]
        
        if disabled:
            print("\nDisabled Sources:")
            for source in disabled:
                print(f"  ✗ {source.capitalize()}")
        
        return 0
    
    # Handle test source
    if args.test:
        source_name = args.test.lower()
        logger.info(f"Testing {source_name}...")
        
        source_manager = SourceManager(config)
        result = source_manager.test_source(source_name)
        
        if result['success']:
            logger.info(f"✓ {result['message']}")
            return 0
        else:
            logger.error(f"✗ {result['message']}")
            return 1
    
    # Handle enable/disable sources
    if args.enable:
        source_name = args.enable.lower()
        enabled = config.get_enabled_sources()
        
        if source_name not in enabled:
            enabled.append(source_name)
            config.set_enabled_sources(enabled)
            logger.info(f"✓ Enabled {source_name}")
        else:
            logger.info(f"{source_name} is already enabled")
        return 0
    
    if args.disable:
        source_name = args.disable.lower()
        enabled = config.get_enabled_sources()
        
        if source_name in enabled:
            enabled.remove(source_name)
            config.set_enabled_sources(enabled)
            logger.info(f"✓ Disabled {source_name}")
        else:
            logger.info(f"{source_name} is not enabled")
        return 0
    
    # Handle themes
    if args.themes:
        from paprwall.config.default_keys import AVAILABLE_THEMES
        
        print("\nAvailable Themes:")
        print("=" * 60)
        for theme_name, theme_data in AVAILABLE_THEMES.items():
            print(f"\n  {theme_name.upper()}")
            print(f"  {theme_data['description']}")
            print(f"  Searches: {', '.join(theme_data['search_queries'][:3])}")
        
        print("\n" + "=" * 60)
        print("\nSet theme with: paprwall --set-theme THEME_NAME")
        return 0
    
    if args.current_theme:
        current = config.get_preference('theme', 'nature')
        custom = config.get_preference('custom_query', '')
        
        print("\nCurrent Theme Configuration:")
        print(f"  Theme: {current}")
        if custom:
            print(f"  Custom Query: {custom}")
        else:
            print(f"  Custom Query: (none)")
        return 0
    
    if args.set_theme:
        theme_name = args.set_theme.lower()
        from paprwall.config.default_keys import AVAILABLE_THEMES
        
        if theme_name in AVAILABLE_THEMES:
            config.set_preference('theme', theme_name)
            
            # Update all source preferences
            for source in ['pixabay', 'pexels', 'unsplash']:
                prefs = config.get_source_preferences(source)
                prefs['theme'] = theme_name
                config.set_source_preferences(source, prefs)
            
            logger.info(f"✓ Theme set to: {theme_name}")
            logger.info(f"  {AVAILABLE_THEMES[theme_name]['description']}")
            logger.info(f"\nFetch new images with: paprwall --fetch")
            return 0
        else:
            logger.error(f"✗ Unknown theme: {theme_name}")
            logger.info(f"Available themes: {', '.join(AVAILABLE_THEMES.keys())}")
            logger.info(f"Or run: paprwall --themes")
            return 1
    
    if args.custom_query:
        query = args.custom_query
        config.set_preference('custom_query', query)
        logger.info(f"✓ Custom query set to: {query}")
        logger.info(f"\nFetch new images with: paprwall --fetch")
        return 0
    
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
