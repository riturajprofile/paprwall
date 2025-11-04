# Quick Start Guide - PyPI Setup

## 🚀 Ready to Publish PaprWall to PyPI

### 📋 Checklist

- [x] README.md created with comprehensive documentation
- [x] setup.py configured with PyPI metadata
- [x] pyproject.toml updated for modern packaging
- [x] MANIFEST.in includes necessary files
- [x] .gitignore excludes sensitive files
- [x] Publishing scripts created

### 🔑 Next Steps

#### 1. Create PyPI Account (5 minutes)
```bash
# Register at PyPI
https://pypi.org/account/register/

# Register at TestPyPI (for testing)
https://test.pypi.org/account/register/
```

#### 2. Generate API Tokens (2 minutes)
```bash
# PyPI Token
https://pypi.org/manage/account/token/
Scope: "Entire account" or "paprwall project"

# TestPyPI Token
https://test.pypi.org/manage/account/token/
Scope: "Entire account"
```

#### 3. Configure Credentials (3 minutes)
Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-REAL-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TEST-TOKEN-HERE
```

Set permissions:
```bash
chmod 600 ~/.pypirc
```

#### 4. Install Publishing Tools (1 minute)
```bash
pip install --upgrade build twine
```

#### 5. Test Build Locally (2 minutes)
```bash
cd /home/riturajprofile/wallpaper-app

# Clean previous builds
rm -rf dist/ build/ src/*.egg-info/

# Build package
python -m build

# Check package
twine check dist/*
```

Expected output:
```
Checking dist/paprwall-1.0.0.tar.gz: PASSED
Checking dist/paprwall-1.0.0-py3-none-any.whl: PASSED
```

#### 6. Test on TestPyPI (5 minutes)
```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    paprwall

# Run GUI
paprwall-gui
```

#### 7. Publish to PyPI (2 minutes)
```bash
# Use the automated script
./publish_to_pypi.sh

# Or manually
twine upload dist/*
```

#### 8. Verify Installation (1 minute)
```bash
# Create clean environment
python -m venv test_install
source test_install/bin/activate

# Install from PyPI
pip install paprwall

# Test
paprwall-gui

# Cleanup
deactivate
rm -rf test_install
```

### 📦 What Gets Published

**Source Distribution** (`paprwall-1.0.0.tar.gz`):
- All Python source files
- README.md, LICENSE, CHANGELOG.md
- setup.py, pyproject.toml
- MANIFEST.in

**Wheel Distribution** (`paprwall-1.0.0-py3-none-any.whl`):
- Compiled Python bytecode
- Package metadata
- Faster installation

### 🎯 Total Time: ~20 minutes

### 📊 After Publishing

Users can install with:
```bash
pip install paprwall
```

Your package will be at:
```
https://pypi.org/project/paprwall/
```

### 🔍 Monitoring

- **PyPI Stats**: https://pypi.org/project/paprwall/
- **Download Stats**: https://pepy.tech/project/paprwall
- **GitHub Releases**: https://github.com/riturajprofile/paprwall/releases

### 📚 Full Documentation

See `PYPI_PUBLISHING.md` for complete details.

---

**Ready to ship PaprWall to 400k+ PyPI users! 🎉**
