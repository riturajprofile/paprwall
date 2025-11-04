"""
Tests for PaprWall - Modern Desktop Wallpaper Manager.
"""

# Test configuration
import sys
import os
from pathlib import Path

# Add src directory to Python path for testing
test_dir = Path(__file__).parent
src_dir = test_dir.parent / "src"
sys.path.insert(0, str(src_dir))

# Test constants
TEST_DATA_DIR = test_dir / "data"
SAMPLE_IMAGE_PATH = TEST_DATA_DIR / "sample_wallpaper.jpg"
SAMPLE_QUOTE = {
    "text": "The only way to do great work is to love what you do.",
    "author": "Steve Jobs",
}

# Ensure test data directory exists
TEST_DATA_DIR.mkdir(exist_ok=True)
