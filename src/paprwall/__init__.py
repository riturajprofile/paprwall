"""
paprwall: Auto-rotating wallpaper app for Linux
with multi-source support and local images.
"""

from .__version__ import __version__, __author__, __description__

__email__ = "riturajprofile@gmail.com"

from pathlib import Path
import os

# Package information
PACKAGE_NAME = "paprwall"
APP_NAME = "paprwall"

# User directories
CONFIG_DIR = Path.home() / ".config" / "paprwall"
DATA_DIR = Path.home() / ".local" / "share" / "paprwall"
CACHE_DIR = DATA_DIR / "cache"
IMAGES_DIR = DATA_DIR / "images"
LOGS_DIR = DATA_DIR / "logs"

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    for directory in [CONFIG_DIR, DATA_DIR, CACHE_DIR, IMAGES_DIR, LOGS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

# Create directories on import
ensure_directories()
