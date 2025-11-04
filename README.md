# Paprwall 🖼️

🎨 **Minimal CLI wallpaper manager for Linux** with multi-source support, local image management, and proper attribution.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Linux](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.org/)

> **Simple, fast, and fully functional CLI-only wallpaper manager. Free for personal use!**

## ✨ Features

### 🌐 Multiple Image Sources
- **Pixabay** - Free, high-quality images
- **Unsplash** - Professional photographer community
- **Pexels** - Curated stock photos
- **Local Images** - Use your own photos!

### 🎛️ User Control
- ✅ Choose which sources to use
- ✅ Set distribution (how many images from each source)
- ✅ **Select wallpaper themes** (nature, city, space, ocean, minimal, etc.)
- ✅ **Custom search queries** for specific wallpapers
- ✅ Upload and manage your own images
- ✅ Manual wallpaper selection
- ✅ Custom API keys support

### 🔄 Smart Rotation
- ✅ Auto-fetch new images daily
- ✅ **Automatic retry** if fetch fails (retries after 1 hour)
- ✅ Rotate wallpapers at custom intervals
- ✅ Pause/resume anytime
- ✅ Navigate through image history
- ✅ **Auto-starts on system boot** (enabled during installation)

### 📸 Proper Attribution
- ✅ Credits photographers automatically
- ✅ Complies with API terms of service
- ✅ Optional desktop overlay
- ✅ View attribution with --current command

### 🖥️ Desktop Environment Support
Supports all major Linux desktop environments:
- GNOME / Ubuntu
- KDE Plasma
- XFCE
- MATE
- Cinnamon
- LXDE / LXQt

---

## 🚀 Quick Start

### One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | sh
```

### Usage

```bash
# Fetch and set new wallpapers
paprwall --fetch

# Navigate wallpapers
paprwall --next
paprwall --prev

# Show current wallpaper info
paprwall --current

# Set a theme
paprwall --set-theme nature
paprwall --set-theme space

# Custom search
paprwall --custom-query "mountain sunset"

# Enable/disable sources
paprwall --enable pixabay
paprwall --disable unsplash

# Test API connection
paprwall --test pixabay
```

---

## �� Installation

### Prerequisites
- Python 3.8+
- pip
- One of: `gsettings` (GNOME), `qdbus` (KDE), `xfconf-query` (XFCE), or `feh`/`nitrogen` (fallback)

### Automated Installation (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | sh
```

This will:
- Create a virtual environment at `~/.paprwall/.venv`
- Install all dependencies
- Set up command wrappers in `~/.local/bin`
- Enable auto-start service

### Manual Installation

```bash
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 🔧 Configuration

### API Keys

Get free API keys:
- **Pixabay**: https://pixabay.com/api/docs/
- **Unsplash**: https://unsplash.com/developers
- **Pexels**: https://www.pexels.com/api/

**Method 1: Environment Variables (.env file)**

Create `.env` in project root or `~/.config/paprwall/`:

```bash
PIXABAY_API_KEY=your_key_here
UNSPLASH_ACCESS_KEY=your_key_here
PEXELS_API_KEY=your_key_here
```

**Method 2: Config File**

Edit `~/.config/paprwall/api_keys.json`:

```json
{
  "pixabay": {
    "api_key": "your_key_here"
  },
  "unsplash": {
    "access_key": "your_key_here"
  },
  "pexels": {
    "api_key": "your_key_here"
  }
}
```

### Enable/Disable Sources

```bash
# Enable a source
paprwall --enable pixabay
paprwall --enable pexels
paprwall --enable local

# Disable a source
paprwall --disable unsplash

# List enabled sources
paprwall --sources
```

Or edit `~/.config/paprwall/sources.json`:

```json
{
  "enabled": ["pixabay", "pexels"],
  "weights": {
    "pixabay": 50,
    "pexels": 50
  }
}
```

### Themes

List available themes:

```bash
paprwall --themes
```

Set a theme:

```bash
paprwall --set-theme nature
paprwall --set-theme city
paprwall --set-theme space
paprwall --set-theme minimal
```

Custom search query (overrides theme):

```bash
paprwall --custom-query "sunset mountains"
```

---

## 💻 CLI Commands

### Basic Operations

```bash
# Fetch new wallpapers
paprwall --fetch

# Navigate
paprwall --next
paprwall --prev

# Show current wallpaper info
paprwall --current

# Set specific image
paprwall --set /path/to/image.jpg
```

### Source Management

```bash
# List enabled sources
paprwall --sources

# Test API connection
paprwall --test pixabay
paprwall --test pexels

# Enable/disable sources
paprwall --enable pixabay
paprwall --disable local
```

### Theme Configuration

```bash
# List available themes
paprwall --themes

# Show current theme
paprwall --current-theme

# Set theme
paprwall --set-theme nature

# Custom search
paprwall --custom-query "ocean waves"
```

### Service Management

```bash
# Check service status
systemctl --user status paprwall

# Start service
systemctl --user start paprwall

# Stop service
systemctl --user stop paprwall

# Enable auto-start
systemctl --user enable paprwall

# Disable auto-start
systemctl --user disable paprwall
```

---

## 📸 Attribution

Paprwall respects photographers and API terms by:
- Displaying photographer credits on wallpapers (optional overlay)
- Including attribution in metadata
- Complying with all source API requirements

### Desktop Overlay

By default, wallpapers include a subtle overlay with photographer credit. To disable:

Edit `~/.config/paprwall/attribution.json`:

```json
{
  "attribution_disabled": true
}
```

---

## 🗂️ File Structure

```
~/.config/paprwall/          # Configuration
├── api_keys.json            # API keys
├── sources.json             # Enabled sources & weights
├── preferences.json         # General preferences
└── attribution.json         # Attribution settings

~/.local/share/paprwall/     # Data
├── images/                  # Downloaded wallpapers
│   └── 2025-11-03/         # Organized by date
│       ├── pixabay_1.jpg
│       └── pexels_1.jpg
└── logs/                    # Application logs
    └── app.log

~/.paprwall/                 # Installation
└── .venv/                   # Virtual environment
```

---

## � Ship it: builds and releases

You can distribute Paprwall in two ways: as a Python package or as standalone binaries.

### Option A: Python package (pip)

Build and install locally:

```bash
python -m pip install --upgrade pip build
python -m build
pip install dist/paprwall-*.whl
```

Publish to PyPI (optional):

```bash
python -m pip install twine
twine upload dist/*
```

### Option B: Standalone binaries (no Python required)

Create single-file executables with PyInstaller:

```bash
pip install pyinstaller

# CLI build
pyinstaller -F -n wallpaper-manager src/paprwall/wallpaper_cli.py

# GUI build
# On macOS/Windows, add -w to hide console: pyinstaller -F -w -n wallpaper-gui ...
pyinstaller -F -n wallpaper-gui src/paprwall/gui/wallpaper_manager_gui.py

# Artifacts will be in ./dist/
```

### Continuous builds with GitHub Actions

This repo includes a workflow at `.github/workflows/release.yml` that:
- Builds Windows, macOS, and Linux binaries with PyInstaller
- Runs automatically when you push a tag like `v1.2.3`
- Uploads the binaries as a GitHub Release

Usage:

```bash
git tag v1.0.0
git push origin v1.0.0
```

When the workflow finishes, download the binaries from the Release page.

---

## �🛠️ Troubleshooting

### Wallpaper not changing

Check desktop environment detection:

```bash
echo $XDG_CURRENT_DESKTOP
echo $DESKTOP_SESSION
```

Install the appropriate tool:
- GNOME: `gsettings` (usually pre-installed)
- KDE: `qdbus`
- XFCE: `xfconf-query`
- Fallback: `feh` or `nitrogen`

### API errors

```bash
# Test each source
paprwall --test pixabay
paprwall --test pexels
paprwall --test unsplash
```

Common issues:
- Invalid API key → Get new key from provider
- Rate limit exceeded → Wait 1 hour
- No results → Try different theme/query

### Check logs

```bash
tail -f ~/.local/share/paprwall/logs/app.log
```

---

## 📄 License

**CC BY-NC 4.0** (Creative Commons Attribution-NonCommercial 4.0 International)

✅ **Allowed:**
- ✅ Personal use
- ✅ Modification
- ✅ Distribution (non-commercial)

❌ **Not Allowed:**
- ❌ Commercial use
- ❌ Selling this software
- ❌ Using in commercial products

**Attribution Required:** Must credit riturajprofile

See [LICENSE](LICENSE) for full details.

---

## 🤝 Contributing

Contributions welcome! This project is non-commercial and open to community improvements.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 🙏 Credits

- **Image Sources**: Pixabay, Unsplash, Pexels
- **API Providers**: Thank you for free API access!
- **Photographers**: Credits displayed with each wallpaper

---

## 📞 Support

- **Issues**: https://github.com/riturajprofile/paprwall/issues
- **Discussions**: https://github.com/riturajprofile/paprwall/discussions

---

**Made with ❤️ by riturajprofile**
