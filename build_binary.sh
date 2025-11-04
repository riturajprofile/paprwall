#!/usr/bin/env bash
#
# Build single-file binary for Paprwall with PyInstaller
#
set -euo pipefail

echo "🔨 Building Paprwall single-file binary with PyInstaller..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

# Create/activate venv for building
VENV_DIR=".venv-build"
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating build virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Install build dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip -q
pip install pyinstaller -q

# Install package in editable mode
pip install -e . -q

# Build single-file binary
echo "🚀 Building single binary (this may take a minute)..."
pyinstaller --onefile \
    --name paprwall \
    --hidden-import PIL._tkinter_finder \
    --collect-all PIL \
    --collect-all requests \
    --add-data "src/paprwall:paprwall" \
    src/paprwall/__main__.py

echo ""
echo "✅ Build complete!"
echo ""
echo "📁 Binary location: dist/paprwall"
echo ""
echo "📝 To install:"
echo "   sudo cp dist/paprwall /usr/local/bin/"
echo "   # or"
echo "   cp dist/paprwall ~/.local/bin/"
echo ""
echo "📝 To run:"
echo "   ./dist/paprwall --help"
echo ""
