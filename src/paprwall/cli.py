"""
Command-line interface for PaprWall.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from . import __version__
from .gui.wallpaper_manager_gui import WallpaperManagerGUI


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="paprwall",
        description="Modern Desktop Wallpaper Manager with Motivational Quotes",
        epilog="For more information, visit: https://github.com/riturajprofile/paprwall"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"PaprWall {__version__}"
    )

    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the GUI interface (default)"
    )

    parser.add_argument(
        "--install",
        action="store_true",
        help="Install PaprWall to system (creates desktop entry, shortcuts)"
    )

    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninstall PaprWall from system"
    )

    parser.add_argument(
        "--set-wallpaper",
        metavar="PATH",
        help="Set wallpaper from local file path"
    )

    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch and set a random wallpaper"
    )

    parser.add_argument(
        "--category",
        choices=["motivational", "mathematics", "science", "famous", "technology", "philosophy"],
        default="motivational",
        help="Quote category for wallpaper (default: motivational)"
    )

    parser.add_argument(
        "--no-quote",
        action="store_true",
        help="Don't add quote to wallpaper"
    )

    parser.add_argument(
        "--config-dir",
        type=Path,
        help="Override default config directory"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    return parser


def main(args: Optional[list] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    try:
        # Handle installation/uninstallation
        if parsed_args.install:
            from .installer import install_system
            return install_system()

        if parsed_args.uninstall:
            from .installer import uninstall_system
            return uninstall_system()

        # Handle wallpaper operations
        if parsed_args.set_wallpaper:
            from .core import set_wallpaper_from_file
            return set_wallpaper_from_file(
                parsed_args.set_wallpaper,
                add_quote=not parsed_args.no_quote,
                category=parsed_args.category
            )

        if parsed_args.fetch:
            from .core import fetch_and_set_wallpaper
            return fetch_and_set_wallpaper(
                category=parsed_args.category,
                add_quote=not parsed_args.no_quote
            )

        # Default: launch GUI
        import tkinter as tk
        root = tk.Tk()
        app = WallpaperManagerGUI(root)

        # Pass CLI arguments to GUI if needed
        if hasattr(app, 'set_cli_args'):
            app.set_cli_args(parsed_args)

        root.mainloop()
        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
