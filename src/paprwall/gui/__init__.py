"""
GUI module for PaprWall - Modern Desktop Wallpaper Manager.
"""

import sys
import tkinter as tk
from typing import Optional

from .wallpaper_manager_gui import WallpaperManagerGUI


def main(args: Optional[list] = None) -> int:
    """Main GUI entry point."""
    try:
        # Create the main window
        root = tk.Tk()

        # Initialize the application
        app = WallpaperManagerGUI(root)

        # Handle command line arguments if provided
        if args and hasattr(app, 'handle_args'):
            app.handle_args(args)

        # Start the GUI main loop
        root.mainloop()
        return 0

    except KeyboardInterrupt:
        print("\nGUI closed by user.")
        return 0
    except Exception as e:
        print(f"Error starting GUI: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
