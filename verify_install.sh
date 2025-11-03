#!/bin/bash
# Verification script for riturajprofile-wallpaper installation

echo "=================================="
echo "riturajprofile-wallpaper Verification"
echo "=================================="
echo ""

# Check if package is installed
echo "1. Checking package installation..."
if python3 -c "import riturajprofile_wallpaper" 2>/dev/null; then
    VERSION=$(python3 -c "import riturajprofile_wallpaper; print(riturajprofile_wallpaper.__version__)")
    echo "   ✓ Package installed (version $VERSION)"
else
    echo "   ✗ Package not found"
    echo "   Run: pip install -e . (from project directory)"
    exit 1
fi

# Check CLI command
echo ""
echo "2. Checking CLI command..."
if command -v riturajprofile-wallpaper &> /dev/null; then
    echo "   ✓ CLI command available"
    riturajprofile-wallpaper --version
else
    echo "   ✗ CLI command not found"
    echo "   Make sure ~/.local/bin is in your PATH"
fi

# Check GUI command
echo ""
echo "3. Checking GUI command..."
if command -v riturajprofile-wallpaper-gui &> /dev/null; then
    echo "   ✓ GUI command available"
else
    echo "   ✗ GUI command not found"
fi

# Check configuration directories
echo ""
echo "4. Checking configuration directories..."
CONFIG_DIR="$HOME/.config/riturajprofile-wallpaper"
DATA_DIR="$HOME/.local/share/riturajprofile-wallpaper"

if [ -d "$CONFIG_DIR" ]; then
    echo "   ✓ Config directory exists: $CONFIG_DIR"
    echo "     Files:"
    ls -1 "$CONFIG_DIR" 2>/dev/null | sed 's/^/       - /'
else
    echo "   ⚠️  Config directory will be created on first run"
fi

if [ -d "$DATA_DIR" ]; then
    echo "   ✓ Data directory exists: $DATA_DIR"
else
    echo "   ⚠️  Data directory will be created on first run"
fi

# Check system dependencies
echo ""
echo "5. Checking system dependencies..."

# Check Python GTK
if python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo "   ✓ PyGObject (GTK3) available"
else
    echo "   ✗ PyGObject not found"
    echo "   Install: sudo apt-get install python3-gi gir1.2-gtk-3.0"
fi

# Check Pillow
if python3 -c "import PIL" 2>/dev/null; then
    echo "   ✓ Pillow (PIL) available"
else
    echo "   ✗ Pillow not found"
fi

# Check requests
if python3 -c "import requests" 2>/dev/null; then
    echo "   ✓ requests library available"
else
    echo "   ✗ requests not found"
fi

# Check APScheduler
if python3 -c "import apscheduler" 2>/dev/null; then
    echo "   ✓ APScheduler available"
else
    echo "   ✗ APScheduler not found"
fi

# Check desktop environment
echo ""
echo "6. Checking desktop environment..."
if [ -n "$XDG_CURRENT_DESKTOP" ]; then
    echo "   ✓ Desktop environment: $XDG_CURRENT_DESKTOP"
else
    echo "   ⚠️  Desktop environment not detected"
fi

# Summary
echo ""
echo "=================================="
echo "Verification complete!"
echo ""
echo "Next steps:"
echo "  1. Test CLI:   riturajprofile-wallpaper --help"
echo "  2. Fetch test: riturajprofile-wallpaper --fetch"
echo "  3. Launch GUI: riturajprofile-wallpaper-gui"
echo ""
echo "Need help? Check README.md or QUICKSTART.md"
echo "=================================="
