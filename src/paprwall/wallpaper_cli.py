"""
Deprecated legacy CLI (wallpaper_cli).

This module remains to avoid import errors in older environments.
Use the new entry points instead:
- CLI: `paprwall` -> paprwall.cli:main
- GUI: `paprwall-gui` -> paprwall.gui.wallpaper_manager_gui:main
"""

def main():  # pragma: no cover - deprecated
    raise RuntimeError(
        "'wallpaper-manager' is deprecated. Use 'paprwall' or 'paprwall-gui' instead."
    )

__all__ = ["main"]
