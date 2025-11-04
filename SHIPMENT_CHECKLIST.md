# Paprwall Shipment Checklist

This document ensures all aspects are ready before shipping/releasing.

## Pre-Release Checklist

### 📋 Code Quality

- [ ] All Python files follow PEP 8
- [ ] No syntax errors (`python -m py_compile src/**/*.py`)
- [ ] All imports are correct
- [ ] No hardcoded paths (use Path objects)
- [ ] Logging is properly configured
- [ ] Error handling is comprehensive

### 🧪 Testing

- [ ] Manual testing on Ubuntu/Debian
- [ ] Manual testing on Fedora/RHEL (if possible)
- [ ] Manual testing on Arch Linux (if possible)
- [ ] Test all CLI commands work
- [ ] Test GUI launches and works
- [ ] Test auto-start service
- [ ] Test API connections (all sources)
- [ ] Test offline mode (local images)
- [ ] Test wallpaper rotation
- [ ] Test theme changes
- [ ] Test navigation (next/prev)

### 📦 Package Structure

- [ ] `setup.py` is correct
- [ ] `pyproject.toml` is correct
- [ ] `requirements.txt` matches dependencies
- [ ] `MANIFEST.in` includes all necessary files
- [ ] Version numbers are consistent across files
- [ ] Entry points are correctly defined

### 📝 Documentation

- [ ] README.md is complete and accurate
- [ ] INSTALL.md has all installation methods
- [ ] LICENSE file is present and correct
- [ ] Code comments are clear
- [ ] API keys documentation is clear
- [ ] Troubleshooting section is comprehensive

### 🔧 Scripts

- [ ] `install.sh` works on all supported distros
- [ ] `uninstall.sh` completely removes everything
- [ ] `setup_venv.sh` works for development
- [ ] All scripts are executable (`chmod +x`)
- [ ] Scripts have proper shebang lines
- [ ] Error handling in scripts is robust

### 🎨 User Experience

- [ ] Installation is straightforward
- [ ] First-time user experience is smooth
- [ ] Error messages are helpful
- [ ] Success messages are clear
- [ ] GUI is intuitive
- [ ] CLI help text is comprehensive

### 🔐 Security

- [ ] No API keys in code
- [ ] No sensitive data in logs
- [ ] File permissions are correct
- [ ] No shell injection vulnerabilities
- [ ] Dependencies are from trusted sources

### 🌐 Repository

- [ ] `.gitignore` excludes venvs, caches, etc.
- [ ] README badges are working
- [ ] Repository description is accurate
- [ ] Topics/tags are added
- [ ] LICENSE is visible on GitHub

## Build & Distribution

### 🏗️ Building

#### Python Package (PyPI)

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build source and wheel distributions
python -m pip install --upgrade build
python -m build

# Verify contents
tar tzf dist/paprwall-*.tar.gz
unzip -l dist/paprwall-*.whl
```

- [ ] Source distribution builds without errors
- [ ] Wheel builds without errors
- [ ] Package includes all necessary files
- [ ] Package size is reasonable (<5MB without images)

#### Standalone Binaries (PyInstaller)

```bash
# Install PyInstaller
pip install pyinstaller

# Build CLI
pyinstaller wallpaper-manager.spec

# Build GUI
pyinstaller wallpaper-gui.spec

# Test binaries
./dist/wallpaper-manager --help
./dist/wallpaper-gui
```

- [ ] CLI binary works standalone
- [ ] GUI binary works standalone
- [ ] Binaries are reasonably sized
- [ ] No missing dependencies

### 📤 Publishing

#### GitHub Release

- [ ] Create git tag with version (e.g., `v1.0.0`)
- [ ] Push tag to GitHub
- [ ] Create GitHub Release
- [ ] Upload binaries to release
- [ ] Write release notes
- [ ] Include changelog

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

#### PyPI (Optional)

```bash
# Install twine
pip install twine

# Check package
twine check dist/*

# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ paprwall

# If everything works, upload to real PyPI
twine upload dist/*
```

- [ ] TestPyPI upload successful
- [ ] Test installation from TestPyPI works
- [ ] PyPI upload successful
- [ ] PyPI page looks correct

### 🔗 Links & Integration

- [ ] Update README with correct PyPI badge
- [ ] Update install script URL
- [ ] Update documentation links
- [ ] Test one-line installer
- [ ] Verify all URLs in documentation work

## Post-Release

### 📢 Announcement

- [ ] Post on GitHub Discussions
- [ ] Update project description
- [ ] Share on relevant communities (r/linux, etc.)
- [ ] Update personal portfolio/website

### 📊 Monitoring

- [ ] Watch for issues on GitHub
- [ ] Monitor PyPI download stats
- [ ] Check for user feedback
- [ ] Track installation success rate

### 🐛 Support

- [ ] Respond to issues promptly
- [ ] Help users with installation problems
- [ ] Document common issues
- [ ] Update troubleshooting guide

## Version Checklist

Current version: **1.0.0**

Update version in:
- [ ] `setup.py` → `version="1.0.0"`
- [ ] `pyproject.toml` → `version = "1.0.0"`
- [ ] `src/paprwall/__init__.py` → `__version__ = "1.0.0"`
- [ ] README.md → badges and references
- [ ] Git tag → `v1.0.0`

## Testing Matrix

| OS/Distro | Python | venv | GUI | CLI | Service | Status |
|-----------|--------|------|-----|-----|---------|--------|
| Ubuntu 24.04 | 3.12 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ubuntu 22.04 | 3.10 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Debian 12 | 3.11 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Fedora 39 | 3.12 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Arch Linux | 3.12 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Pop!_OS 22.04 | 3.10 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

Legend: ✅ Tested & Working | ❌ Failed | ⏳ Not Tested | ⚠️ Issues

## Known Issues

Document any known issues here:

1. **Python 3.13 + tkinter on Ubuntu:**
   - Issue: `python3.13-tk` package not available
   - Workaround: Use Python 3.12 or install tkinter manually
   - Status: Documented in INSTALL.md

2. **pipx installation + GUI:**
   - Issue: tkinter not available in pipx venv
   - Workaround: Use standard venv installation
   - Status: Documented in README.md

## Release Commands

Quick reference for releasing:

```bash
# 1. Update version numbers
# Edit: setup.py, pyproject.toml, __init__.py

# 2. Commit changes
git add .
git commit -m "Release v1.0.0"

# 3. Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main
git push origin v1.0.0

# 4. Build distributions
python -m build

# 5. Test locally
pip install dist/paprwall-1.0.0-py3-none-any.whl

# 6. Upload to PyPI (if applicable)
twine upload dist/*

# 7. Create GitHub Release
# Go to: https://github.com/riturajprofile/paprwall/releases/new
# - Tag: v1.0.0
# - Title: Paprwall v1.0.0
# - Description: Release notes
# - Attach: binaries if built
```

## Emergency Rollback

If something goes wrong:

```bash
# Delete tag locally and remotely
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# Delete release on GitHub
# (use GitHub web interface)

# Yank from PyPI (doesn't delete, marks as broken)
# (use PyPI web interface)

# Fix issues, increment version, re-release
```

---

## Sign-Off

Before shipping, confirm:

- [ ] I have tested the installation on a fresh system
- [ ] I have read all documentation
- [ ] I have verified all scripts work
- [ ] I have checked all URLs
- [ ] I have updated version numbers everywhere
- [ ] I am ready to support users
- [ ] I have backed up the repository

**Signed:** _______________ **Date:** _______________

---

**Ready to ship? Let's go! 🚀**
