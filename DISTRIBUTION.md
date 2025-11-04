# Paprwall - Distribution Summary

## Quick Reference for Shipment

### 🚀 Installation Methods

1. **One-Line Install (Recommended)**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash
   ```

2. **Manual Install**
   ```bash
   git clone https://github.com/riturajprofile/paprwall.git
   cd paprwall
   ./setup_venv.sh
   ```

3. **From PyPI** (when published)
   ```bash
   pip install paprwall  # System-wide
   pipx install paprwall # Isolated (CLI only, GUI may not work)
   ```

### 📦 What's Included

#### Scripts
- `install.sh` - Automated installer for end users
- `uninstall.sh` - Complete removal script
- `setup_venv.sh` - Development environment setup
- `build.sh` - Build Python packages (wheel/sdist)
- `build_binaries.sh` - Build standalone executables
- `test.sh` - Test suite for verification
- `prepare_release.sh` - Pre-release checks

#### Documentation
- `README.md` - Main documentation
- `INSTALL.md` - Detailed installation guide
- `SHIPMENT_CHECKLIST.md` - Release checklist
- `DISTRIBUTION.md` - This file
- `LICENSE` - CC BY-NC 4.0 license

#### Package Files
- `setup.py` - Python package setup
- `pyproject.toml` - Modern Python packaging
- `requirements.txt` - Dependencies
- `MANIFEST.in` - Package manifest

### 🛠️ Building for Distribution

#### 1. Prepare Release
```bash
./prepare_release.sh
```
This checks:
- ✅ Version consistency
- ✅ Required files present
- ✅ Python syntax valid
- ✅ Git status clean
- ✅ Dependencies available

#### 2. Build Python Package
```bash
./build.sh
```
Creates in `dist/`:
- `paprwall-1.0.0-py3-none-any.whl` - Wheel distribution
- `paprwall-1.0.0.tar.gz` - Source distribution

#### 3. Build Binaries (Optional)
```bash
./build_binaries.sh
```
Creates in `dist/`:
- `wallpaper-manager` - CLI binary
- `wallpaper-gui` - GUI binary
- `paprwall-v1.0.0-linux-x64.tar.gz` - Binary archive

#### 4. Test
```bash
./test.sh
```
Verifies:
- Installation successful
- Commands available
- Imports working
- Desktop environment compatible

### 📤 Publishing

#### GitHub Release

1. **Tag version:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Create release on GitHub:**
   - Go to https://github.com/riturajprofile/paprwall/releases/new
   - Select tag: `v1.0.0`
   - Title: `Paprwall v1.0.0`
   - Attach files from `dist/`

#### PyPI (Optional)

```bash
pip install twine

# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Then upload to PyPI
twine upload dist/*
```

### 📋 Pre-Shipment Checklist

- [ ] Update version in `setup.py` and `pyproject.toml`
- [ ] Update CHANGELOG (if exists)
- [ ] Run `./prepare_release.sh` - all checks pass
- [ ] Run `./build.sh` - builds successfully
- [ ] Test installation on clean system
- [ ] Run `./test.sh` - all tests pass
- [ ] Review documentation for accuracy
- [ ] Check all URLs work
- [ ] Verify install.sh works via curl
- [ ] Tag release in git
- [ ] Create GitHub release
- [ ] Update README badges if publishing to PyPI

### 🎯 Distribution Targets

#### Primary: Virtual Environment Install
Best for most users - full features including GUI.

**Install command:**
```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash
```

**Installed to:** `~/.paprwall/.venv`
**Commands:** `paprwall`, `wallpaper-manager`, `wallpaper-gui`

#### Alternative: Binary Distribution
For users who can't install Python packages.

**Install command:**
```bash
wget https://github.com/riturajprofile/paprwall/releases/download/v1.0.0/paprwall-v1.0.0-linux-x64.tar.gz
tar xzf paprwall-v1.0.0-linux-x64.tar.gz
cd paprwall-v1.0.0-linux-x64
./install.sh
```

#### Future: PyPI
For Python developers familiar with pip.

**Install command:**
```bash
pip install paprwall
```

### 🔧 System Requirements

**Minimum:**
- Linux (any distro)
- Python 3.8+
- 256 MB RAM
- 100 MB disk space

**Recommended:**
- Ubuntu 20.04+ or equivalent
- Python 3.10+
- 512 MB RAM
- 500 MB disk space

**Desktop Environments:**
- GNOME / Ubuntu (gsettings)
- KDE Plasma (qdbus)
- XFCE (xfconf-query)
- Others (feh/nitrogen fallback)

### ⚠️ Known Limitations

1. **Python 3.13 + tkinter:** 
   - Ubuntu doesn't have python3.13-tk package yet
   - Workaround: Use Python 3.12 or earlier

2. **pipx + GUI:**
   - tkinter not available in isolated pipx environment
   - Workaround: Use standard venv install

3. **Wayland + some tools:**
   - Some wallpaper setters work better on X11
   - Most tools now support Wayland

### 📊 File Sizes

Approximate sizes:
- Python wheel: ~50 KB (code only)
- Source dist: ~100 KB (includes docs)
- CLI binary: ~15 MB (with dependencies)
- GUI binary: ~20 MB (with tkinter)
- Full install: ~30 MB (venv + deps)

### 🆘 Support Resources

**For Users:**
- Installation: `INSTALL.md`
- Usage: `README.md`
- Issues: https://github.com/riturajprofile/paprwall/issues

**For Developers:**
- Setup: `setup_venv.sh`
- Build: `build.sh`
- Release: `prepare_release.sh`

### 📞 Contact

- **GitHub:** https://github.com/riturajprofile/paprwall
- **Issues:** https://github.com/riturajprofile/paprwall/issues
- **Email:** riturajprofile.me@gmail.com

### 📜 License

CC BY-NC 4.0 - Free for personal use, attribution required.

---

**Ready to ship! 🚢**

Use `./prepare_release.sh` to verify everything is ready.
