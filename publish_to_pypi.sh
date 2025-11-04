#!/bin/bash

set -e

VERSION="1.0.0"

echo "=========================================="
echo "  Publishing PaprWall v${VERSION} to PyPI"
echo "=========================================="
echo ""

# Check requirements
command -v python >/dev/null 2>&1 || { echo "❌ Python not found"; exit 1; }
python -c "import build" 2>/dev/null || { echo "❌ 'build' module not found. Install: pip install build"; exit 1; }
python -c "import twine" 2>/dev/null || { echo "❌ 'twine' module not found. Install: pip install twine"; exit 1; }

# Step 1: Clean
echo "1. Cleaning previous builds..."
rm -rf dist/ build/ src/*.egg-info/
echo "✓ Cleaned"
echo ""

# Step 2: Build
echo "2. Building package..."
python -m build
echo "✓ Built"
echo ""

# Step 3: Check
echo "3. Checking package..."
if ! twine check dist/*; then
    echo "❌ Package check failed"
    exit 1
fi
echo "✓ Package validated"
echo ""

# List built files
echo "Built files:"
ls -lh dist/
echo ""

# Step 4: Test on TestPyPI (optional)
echo "─────────────────────────────────────────"
read -p "Upload to TestPyPI first? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "4. Uploading to TestPyPI..."
    twine upload --repository testpypi dist/*
    echo "✓ Uploaded to TestPyPI"
    echo ""
    echo "View at: https://test.pypi.org/project/paprwall/${VERSION}/"
    echo ""
    echo "Test installation:"
    echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple paprwall"
    echo ""
    echo "─────────────────────────────────────────"
    read -p "Continue to production PyPI? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Stopped. You can upload to PyPI later with:"
        echo "  twine upload dist/*"
        exit 0
    fi
fi

# Step 5: Upload to PyPI
echo ""
echo "5. Uploading to PyPI..."
echo "⚠️  This will publish to production PyPI!"
read -p "Are you sure? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Uploading..."
if twine upload dist/*; then
    echo ""
    echo "=========================================="
    echo "  ✨ Published Successfully!"
    echo "=========================================="
    echo ""
    echo "📦 Package: https://pypi.org/project/paprwall/${VERSION}/"
    echo ""
    echo "Install command:"
    echo "  pip install paprwall"
    echo ""
    echo "Next steps:"
    echo "  1. Create GitHub Release: https://github.com/riturajprofile/paprwall/releases/new"
    echo "  2. Update README badges"
    echo "  3. Announce on social media"
    echo "  4. Monitor: https://pepy.tech/project/paprwall"
    echo ""
else
    echo ""
    echo "❌ Upload failed!"
    echo "Check your credentials in ~/.pypirc"
    exit 1
fi
