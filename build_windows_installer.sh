#!/bin/bash
# Script to build Windows installer (requires NSIS on Windows or makensis on Linux)
# Install on Ubuntu: sudo apt install nsis
# Install on Windows: Download from https://nsis.sourceforge.io/

set -e

echo "=========================================="
echo "  Building PaprWall Windows Installer"
echo "=========================================="
echo ""

# Check if makensis is installed
if ! command -v makensis &> /dev/null; then
    echo "ERROR: makensis (NSIS) not found"
    echo ""
    echo "Install it with:"
    echo "  Ubuntu/Debian: sudo apt install nsis"
    echo "  Windows: Download from https://nsis.sourceforge.io/"
    echo ""
    echo "Note: You need to build the Windows .exe first with PyInstaller on Windows"
    exit 1
fi

# Check if Windows binary exists
if [ ! -f "dist/paprwall-gui.exe" ]; then
    echo "ERROR: Windows binary not found at dist/paprwall-gui.exe"
    echo ""
    echo "Please build the Windows binary first:"
    echo "  1. On Windows machine, run: build_release_windows.bat"
    echo "  2. Or manually: pyinstaller --name=paprwall-gui --onefile --windowed src/paprwall/gui/wallpaper_manager_gui.py"
    echo ""
    exit 1
fi

# Build the installer
cd "$(dirname "$0")"
makensis packaging/windows/paprwall-installer.nsi

if [ -f "paprwall-setup-1.0.2-win64.exe" ]; then
    echo ""
    echo "✓ Windows installer created successfully!"
    ls -lh paprwall-setup-1.0.2-win64.exe
else
    echo ""
    echo "ERROR: Installer build failed"
    exit 1
fi
