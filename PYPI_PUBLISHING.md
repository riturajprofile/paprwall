# PyPI Publishing Guide for PaprWall

This guide explains how to publish PaprWall to PyPI (Python Package Index).

## Prerequisites

### 1. Create PyPI Account
- Register at [PyPI.org](https://pypi.org/account/register/)
- Register at [TestPyPI.org](https://test.pypi.org/account/register/) (for testing)

### 2. Install Publishing Tools
```bash
pip install --upgrade build twine
```

### 3. Configure PyPI Credentials

Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TEST-API-TOKEN-HERE
```

**Get API Tokens:**
- PyPI: https://pypi.org/manage/account/token/
- TestPyPI: https://test.pypi.org/manage/account/token/

Set permissions:
```bash
chmod 600 ~/.pypirc
```

## Building the Package

### 1. Clean Previous Builds
```bash
cd /home/riturajprofile/wallpaper-app
rm -rf dist/ build/ src/*.egg-info/
```

### 2. Build Distribution
```bash
python -m build
```

This creates:
- `dist/paprwall-1.0.0.tar.gz` (source distribution)
- `dist/paprwall-1.0.0-py3-none-any.whl` (wheel distribution)

### 3. Verify Build
```bash
twine check dist/*
```

Expected output:
```
Checking dist/paprwall-1.0.0.tar.gz: PASSED
Checking dist/paprwall-1.0.0-py3-none-any.whl: PASSED
```

## Testing on TestPyPI

### 1. Upload to TestPyPI
```bash
twine upload --repository testpypi dist/*
```

### 2. Test Installation
```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    paprwall

# Test the package
paprwall-gui

# Cleanup
deactivate
rm -rf test_env
```

## Publishing to PyPI

### 1. Upload to PyPI
```bash
twine upload dist/*
```

You'll see:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading paprwall-1.0.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Uploading paprwall-1.0.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View at:
https://pypi.org/project/paprwall/1.0.0/
```

### 2. Verify Installation
```bash
pip install paprwall
paprwall-gui
```

## Complete Release Script

Create `publish_to_pypi.sh`:

```bash
#!/bin/bash

set -e

VERSION="1.0.0"

echo "=========================================="
echo "  Publishing PaprWall v${VERSION} to PyPI"
echo "=========================================="
echo ""

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
twine check dist/*
echo "✓ Checked"
echo ""

# Step 4: Test on TestPyPI (optional)
read -p "Upload to TestPyPI first? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "4. Uploading to TestPyPI..."
    twine upload --repository testpypi dist/*
    echo "✓ Uploaded to TestPyPI"
    echo ""
    echo "Test with:"
    echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple paprwall"
    echo ""
    read -p "Continue to PyPI? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Step 5: Upload to PyPI
echo "5. Uploading to PyPI..."
twine upload dist/*
echo "✓ Uploaded to PyPI"
echo ""

echo "=========================================="
echo "  ✨ Published Successfully!"
echo "=========================================="
echo ""
echo "Package URL: https://pypi.org/project/paprwall/${VERSION}/"
echo ""
echo "Users can now install with:"
echo "  pip install paprwall"
echo ""
```

Make it executable:
```bash
chmod +x publish_to_pypi.sh
```

## Post-Publication Steps

### 1. Update README Badge
Add to README.md:
```markdown
[![PyPI](https://img.shields.io/pypi/v/paprwall.svg)](https://pypi.org/project/paprwall/)
[![Downloads](https://pepy.tech/badge/paprwall)](https://pepy.tech/project/paprwall)
```

### 2. Announce Release
- Create GitHub Release
- Post on social media
- Update project homepage

### 3. Monitor
- Check PyPI project page: https://pypi.org/project/paprwall/
- Monitor download stats: https://pepy.tech/project/paprwall
- Watch for issues/feedback

## Version Updates

For future releases:

1. Update version in:
   - `src/paprwall/__version__.py`
   - `setup.py`
   - `pyproject.toml`

2. Update `CHANGELOG.md`

3. Create git tag:
   ```bash
   git tag -a v1.0.1 -m "Release v1.0.1"
   git push origin v1.0.1
   ```

4. Build and publish:
   ```bash
   ./publish_to_pypi.sh
   ```

## Troubleshooting

### Issue: "File already exists"
**Solution**: You cannot overwrite releases. Increment version number.

### Issue: "Invalid distribution"
**Solution**: Run `twine check dist/*` to see specific errors.

### Issue: "Authentication failed"
**Solution**: 
- Verify API token is correct in `~/.pypirc`
- Use `__token__` as username
- Token must have upload permissions

### Issue: "Package name already taken"
**Solution**: Choose a different name in `setup.py` and `pyproject.toml`.

## Security Best Practices

1. **Never commit** `.pypirc` or API tokens
2. **Use API tokens** instead of passwords
3. **Limit token scope** to upload only
4. **Rotate tokens** periodically
5. **Use 2FA** on PyPI account

## Resources

- PyPI Documentation: https://packaging.python.org/
- Twine Documentation: https://twine.readthedocs.io/
- PEP 517/518: https://peps.python.org/pep-0517/
- setuptools Guide: https://setuptools.pypa.io/

---

**Ready to publish PaprWall to the world! 🚀**
