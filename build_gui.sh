#!/usr/bin/env bash
#
# Build standalone GUI and CLI binaries with PyInstaller
#
set -euo pipefail

echo "🔨 Building Paprwall binaries..."
echo ""

# Check if PyInstaller is installed
if ! python -m PyInstaller --version &>/dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Build CLI
echo ""
echo "🔨 Building CLI binary..."
pyinstaller -F -n paprwall src/paprwall/cli.py

# Build GUI
echo ""
echo "🔨 Building GUI binary..."
pyinstaller -F -n paprwall-gui \
    --add-data "src/paprwall:paprwall" \
    src/paprwall/gui/wallpaper_manager_gui.py

echo ""
echo "✅ Build complete!"
echo ""
echo "📦 Binaries created in dist/:"
ls -lh dist/

echo ""
echo "🚀 Test the binaries:"
echo "   ./dist/paprwall --help"
echo "   ./dist/paprwall-gui"
echo ""
