# 🚀 Paprwall - Ready for Shipment!

Your wallpaper application is now fully prepared for distribution!

## ✅ What's Been Set Up

### 📁 Directory Structure
```
wallpaper-app/
├── 📦 Core Application
│   ├── src/paprwall/          # Source code
│   ├── setup.py               # Package setup
│   ├── pyproject.toml         # Modern packaging
│   └── requirements.txt       # Dependencies
│
├── 🚀 Installation Scripts
│   ├── install.sh            # One-line installer for users
│   ├── uninstall.sh          # Complete removal
│   └── setup_venv.sh         # Development setup
│
├── 🏗️  Build Scripts
│   ├── build.sh              # Build Python packages
│   ├── build_binaries.sh     # Build standalone binaries
│   ├── test.sh               # Test suite
│   └── prepare_release.sh    # Pre-release checks
│
└── 📚 Documentation
    ├── README.md             # Main documentation
    ├── INSTALL.md            # Installation guide
    ├── DISTRIBUTION.md       # Distribution summary
    ├── SHIPMENT_CHECKLIST.md # Release checklist
    └── LICENSE               # CC BY-NC 4.0
```

## 🎯 Quick Start for Users

### Method 1: One-Line Install (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash
```

This automatically:
- ✅ Detects their Linux distro
- ✅ Installs system dependencies
- ✅ Creates virtual environment
- ✅ Installs paprwall
- ✅ Sets up commands
- ✅ Enables auto-start

### Method 2: Manual Install
```bash
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall
./setup_venv.sh
```

## 🏗️  Building & Releasing

### 1. Prepare for Release
```bash
./prepare_release.sh
```
This checks everything is ready.

### 2. Build Python Packages
```bash
./build.sh
```
Creates:
- `dist/paprwall-1.0.0-py3-none-any.whl`
- `dist/paprwall-1.0.0.tar.gz`

### 3. Build Standalone Binaries (Optional)
```bash
./build_binaries.sh
```
Creates:
- `dist/wallpaper-manager` (CLI binary)
- `dist/wallpaper-gui` (GUI binary)
- `paprwall-v1.0.0-linux-x64.tar.gz` (archive)

### 4. Test Everything
```bash
./test.sh
```

### 5. Create GitHub Release
```bash
# Tag the release
git add .
git commit -m "Release v1.0.0"
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main
git push origin v1.0.0

# Then create release on GitHub:
# https://github.com/riturajprofile/paprwall/releases/new
```

## 📦 Distribution Options

### Option A: GitHub + Install Script (Easiest)
Users run:
```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash
```

**Pros:**
- ✅ Simple one-liner
- ✅ Works on all distros
- ✅ Includes GUI support
- ✅ Auto-updates possible

### Option B: GitHub Releases + Binaries
1. Build binaries: `./build_binaries.sh`
2. Upload to GitHub Releases
3. Users download and extract

**Pros:**
- ✅ No Python required
- ✅ Standalone executables
- ✅ Fast to install

**Cons:**
- ⚠️  Larger file sizes (~15-20 MB)
- ⚠️  Need separate builds per distro

### Option C: PyPI (Future)
```bash
# After setting up PyPI account
pip install twine
twine upload dist/*
```

Users install:
```bash
pip install paprwall
```

**Pros:**
- ✅ Standard Python installation
- ✅ Easy updates with pip

**Cons:**
- ⚠️  tkinter issues with pip/pipx
- ⚠️  Requires Python knowledge

## 🎨 Usage Examples

Once installed, users can:

```bash
# Fetch new wallpapers
paprwall --fetch

# Navigate wallpapers
paprwall --next
paprwall --prev

# Set theme
paprwall --set-theme nature
paprwall --set-theme space

# Custom search
paprwall --custom-query "mountain sunset"

# Launch GUI
wallpaper-gui

# Simple CLI
wallpaper-manager --help
```

## 📋 Pre-Release Checklist

Use `SHIPMENT_CHECKLIST.md` for complete checklist. Quick version:

- [x] Install script created and tested
- [x] Uninstall script created
- [x] Build scripts created
- [x] Test script created
- [x] Documentation complete
- [ ] Test on fresh Ubuntu system
- [ ] Create git tag
- [ ] Create GitHub release
- [ ] Update README with release info

## 🔧 Fixing the tkinter Issue

The original error was caused by using **pipx** which creates isolated environments without system packages.

**Solutions provided:**

1. **Use virtual environment** (Recommended)
   - Our `install.sh` creates proper venv
   - Has access to system tkinter
   - Works with GUI

2. **Use development setup**
   - `./setup_venv.sh` for dev work
   - Creates `.venv` in project
   - Editable install

3. **Install system tkinter**
   - Done automatically by install.sh
   - Manual: `sudo apt install python3-tk`

## 🌟 Key Features for Users

- 🖼️  **Multi-source support**: Pixabay, Unsplash, Pexels, Local
- 🎨 **Themes**: nature, city, space, ocean, minimal, etc.
- 🔄 **Auto-rotation**: Set custom intervals
- 📸 **Attribution**: Proper photographer credits
- 🖥️  **Desktop support**: GNOME, KDE, XFCE, MATE, etc.
- ⚙️  **Service**: Auto-starts on boot
- 💻 **Dual interface**: CLI + GUI

## 📞 Support Resources

**For End Users:**
- Quick install: One-line command
- Detailed help: `INSTALL.md`
- Usage guide: `README.md`
- Issues: GitHub Issues

**For Developers:**
- Dev setup: `./setup_venv.sh`
- Build guide: `DISTRIBUTION.md`
- Release process: `SHIPMENT_CHECKLIST.md`

## 🚢 Ready to Ship!

Your application is fully prepared for distribution. Next steps:

1. **Test locally:** `./test.sh`
2. **Build packages:** `./build.sh`
3. **Test installation:** On fresh VM/container
4. **Commit everything:**
   ```bash
   git add .
   git commit -m "Prepare for release v1.0.0"
   ```
5. **Create release:** Follow steps in `DISTRIBUTION.md`
6. **Share:** Post installation link

## 📣 Installation Link for Users

Once pushed to GitHub, users can install with:

```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash
```

That's it! Your wallpaper manager is ready to ship! 🎉

---

**Need help?** Check:
- `INSTALL.md` - Installation guide
- `DISTRIBUTION.md` - Distribution details
- `SHIPMENT_CHECKLIST.md` - Release checklist
- `README.md` - Full documentation
