#!/usr/bin/env bash
#
# Build script for Paprwall
# Creates Python packages (wheel and source distribution)
#
set -euo pipefail

echo "╔═══════════════════════════════════════════╗"
echo "║     Paprwall Build Script                 ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_info() { echo -e "${BLUE}ℹ${NC} $1"; }
echo_success() { echo -e "${GREEN}✓${NC} $1"; }
echo_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
echo_error() { echo -e "${RED}✗${NC} $1"; }

# Get version from setup.py
VERSION=$(grep -E "version=\"[0-9.]+\"" setup.py | sed -E 's/.*version="([0-9.]+)".*/\1/')
echo_info "Building Paprwall v$VERSION"
echo ""

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo_error "setup.py not found. Please run this script from the project root."
    exit 1
fi

# Clean previous builds
echo_info "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/ src/*.egg-info/
echo_success "Cleaned build artifacts"
echo ""

# Check if build module is installed
if ! python3 -c "import build" 2>/dev/null; then
    echo_info "Installing build tools..."
    python3 -m pip install --upgrade pip build wheel
    echo_success "Build tools installed"
    echo ""
fi

# Build source distribution and wheel
echo_info "Building Python packages..."
python3 -m build

if [ $? -eq 0 ]; then
    echo_success "Build successful!"
    echo ""
else
    echo_error "Build failed!"
    exit 1
fi

# List created files
echo_info "Created packages:"
ls -lh dist/
echo ""

# Verify package contents
echo_info "Verifying package contents..."
echo ""

# Check source distribution
SDIST=$(ls dist/*.tar.gz 2>/dev/null | head -n1)
if [ -n "$SDIST" ]; then
    echo "📦 Source distribution contents:"
    tar tzf "$SDIST" | head -20
    echo "   ... (showing first 20 files)"
    echo ""
fi

# Check wheel
WHEEL=$(ls dist/*.whl 2>/dev/null | head -n1)
if [ -n "$WHEEL" ]; then
    echo "📦 Wheel contents:"
    python3 -m zipfile -l "$WHEEL" | head -20
    echo "   ... (showing first 20 files)"
    echo ""
fi

# Verify with twine if available
if command -v twine &> /dev/null; then
    echo_info "Running twine check..."
    twine check dist/*
    echo ""
else
    echo_warning "twine not installed, skipping validation"
    echo "Install with: pip install twine"
    echo ""
fi

# Summary
echo "╔═══════════════════════════════════════════╗"
echo "║     Build Complete! 🎉                    ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo_success "Packages built successfully in dist/"
echo ""
echo "📝 Next steps:"
echo ""
echo "  1. Test installation locally:"
echo "     pip install dist/paprwall-$VERSION-py3-none-any.whl"
echo ""
echo "  2. Test in a clean environment:"
echo "     python3 -m venv test_env"
echo "     source test_env/bin/activate"
echo "     pip install dist/paprwall-$VERSION-py3-none-any.whl"
echo "     paprwall --help"
echo ""
echo "  3. Upload to TestPyPI (optional):"
echo "     pip install twine"
echo "     twine upload --repository testpypi dist/*"
echo ""
echo "  4. Upload to PyPI (when ready):"
echo "     twine upload dist/*"
echo ""
echo "  5. Create GitHub release:"
echo "     git tag -a v$VERSION -m \"Release version $VERSION\""
echo "     git push origin v$VERSION"
echo ""
