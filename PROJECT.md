# PaprWall Project Overview

<div align="center">

![PaprWall Logo](https://via.placeholder.com/200x200/0f1419/3b82f6?text=PW)

**Modern Desktop Wallpaper Manager with Motivational Quotes**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/riturajprofile/paprwall/releases)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.linux.org/)

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Development](#-development) • [Contributing](#-contributing)

</div>

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Version** | 1.0.0 |
| **Release Date** | November 4, 2025 |
| **Codebase Size** | 67KB (single module) |
| **Dependencies** | 2 (requests, Pillow) |
| **Lines of Code** | ~1,700 |
| **Language** | Python 3.8+ |
| **GUI Framework** | Tkinter |
| **License** | MIT |

## 🎯 Project Goals

### Primary Objectives
1. **Simplicity** - Easy to use, no complex configuration
2. **Beauty** - Stunning wallpapers with inspirational quotes
3. **Reliability** - Stable, production-ready application
4. **Performance** - Fast, responsive, non-blocking UI

### Target Audience
- Linux desktop users (GNOME, KDE, XFCE, MATE)
- Productivity enthusiasts seeking daily motivation
- Users who love beautiful, customized desktops
- Anyone wanting automatic wallpaper rotation

## 🏗️ Architecture

### Project Structure
```
paprwall/
├── src/paprwall/
│   ├── __init__.py           # Package initialization
│   ├── __version__.py        # Version info
│   └── gui/
│       ├── __init__.py       # GUI module init
│       └── wallpaper_manager_gui.py  # Main GUI (67KB, 1700 lines)
├── CHANGELOG.md              # Version history
├── LICENSE                   # MIT License
├── README.md                 # User documentation
├── MANIFEST.in              # Package manifest
├── pyproject.toml           # Modern build config
├── setup.py                 # Package setup
├── requirements.txt         # Runtime dependencies
├── build_release.sh         # Release build script
└── publish_to_pypi.sh       # PyPI publishing script
```

### Technology Stack

**Core Technologies:**
- **Python 3.8+** - Main language
- **Tkinter** - GUI framework (included with Python)
- **Pillow (PIL)** - Image processing and quote embedding
- **Requests** - HTTP client for API calls

**APIs:**
- **Picsum Photos** - Random wallpaper images
- **Quotable.io** - Quote API (primary)
- **ZenQuotes.io** - Quote API (fallback)

**Build Tools:**
- **setuptools** - Package distribution
- **PyInstaller** - Binary compilation
- **build** - PEP 517 builder
- **twine** - PyPI uploader

### Design Patterns

1. **Single-Class Architecture**
   - `WallpaperManagerGUI` class handles everything
   - Modular methods for different features
   - Clean separation of concerns

2. **Threaded Operations**
   - Non-blocking image fetching
   - Background auto-rotation timer
   - Smooth UI responsiveness

3. **Event-Driven GUI**
   - Tkinter event loop
   - Button callbacks
   - Canvas resize handlers

4. **API Integration**
   - Fallback quote sources
   - Error handling and retries
   - Cached default quotes

## 🎨 Features

### Implemented (v1.0.0)
- ✅ Full-screen responsive GUI
- ✅ 6 quote categories (Motivational, Math, Science, Famous People, Tech, Philosophy)
- ✅ Quote embedding on wallpapers (top-right corner)
- ✅ Auto-rotation with countdown timer
- ✅ History gallery with preview/set buttons
- ✅ Local file support
- ✅ Cross-desktop environment support (GNOME, KDE, XFCE, MATE, Cinnamon)
- ✅ Dark theme UI
- ✅ Standalone binary distribution

### Planned (v1.1.0)
- [ ] Multi-monitor support
- [ ] Custom font selection for quotes
- [ ] Color theme customization
- [ ] Image filters (blur, brightness, contrast)
- [ ] Slideshow mode

### Future (v1.2.0+)
- [ ] Cloud sync for favorites
- [ ] Time-based wallpaper scheduling
- [ ] Unsplash API integration
- [ ] System tray widget
- [ ] Wayland support

## 💻 Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

### Running from Source

```bash
# Run GUI directly
python -m src.paprwall.gui.wallpaper_manager_gui

# Or use installed entry point
python -m pip install -e .
paprwall-gui
```

### Code Structure

**Main GUI Class** (`wallpaper_manager_gui.py`):
- `WallpaperManagerGUI.__init__()` - Initialize application
- `setup_ui()` - Build UI components
- `fetch_from_url()` - Download wallpaper from URL
- `fetch_random_quote()` - Get quote from API
- `embed_quote_on_image()` - Add quote to image using PIL
- `set_wallpaper()` - Apply wallpaper to desktop
- `toggle_auto_rotate()` - Enable/disable auto-rotation
- `display_history_gallery()` - Show recent wallpapers

### Testing

```bash
# Run tests (when implemented)
pytest tests/

# Lint code
flake8 src/

# Format code
black src/
```

### Building Release

```bash
# Build standalone binaries
./build_release.sh

# Creates:
# - release-v1.0.0/paprwall-gui (40MB)
# - paprwall-v1.0.0-linux-x64.tar.gz (80MB)
```

### Publishing to PyPI

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI
./publish_to_pypi.sh
```

## 🤝 Contributing

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** (`git commit -m 'Add amazing feature'`)
6. **Push** (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Write clear commit messages
- Test on multiple desktop environments
- Update CHANGELOG.md
- Add yourself to contributors list

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes
vim src/paprwall/gui/wallpaper_manager_gui.py

# 3. Test changes
python -m src.paprwall.gui.wallpaper_manager_gui

# 4. Commit
git add .
git commit -m "feat: Add my amazing feature"

# 5. Push
git push origin feature/my-feature

# 6. Create Pull Request on GitHub
```

### Code Review Process

1. Automated checks run (linting, tests)
2. Maintainer reviews code
3. Feedback addressed
4. Approved and merged
5. Released in next version

## 📝 Documentation

### For Users
- **README.md** - Complete user guide
- **CHANGELOG.md** - Version history
- **PYPI_QUICKSTART.md** - Quick PyPI setup

### For Developers
- **PROJECT.md** - This file (project overview)
- **PYPI_PUBLISHING.md** - Publishing guide
- **Code comments** - Inline documentation

## 🔧 Configuration

### User Data Locations

```bash
# Wallpapers
~/.local/share/paprwall/wallpapers/

# History
~/.local/share/paprwall/history.json

# Logs
~/.local/share/paprwall/paprwall.log

# Config (future)
~/.config/paprwall/config.json
```

### Environment Variables (Future)

```bash
PAPRWALL_CACHE_DIR=/custom/cache/dir
PAPRWALL_LOG_LEVEL=DEBUG
PAPRWALL_API_KEY=custom-api-key
```

## 🐛 Known Issues

### Current Limitations
- ❌ No Wayland support (X11 only)
- ❌ Single monitor only
- ❌ No CLI interface (GUI only)
- ❌ Limited quote customization

### Bug Fixes in v1.0.0
- ✅ Fixed layout responsiveness
- ✅ Fixed quote visibility on light images
- ✅ Fixed timer thread cleanup
- ✅ Fixed history refresh issues

## 🎯 Roadmap

### v1.0.x (Maintenance)
- Bug fixes
- Performance improvements
- Documentation updates

### v1.1.0 (Feature Release)
- Multi-monitor support
- Custom fonts for quotes
- Image filters
- Theme customization

### v1.2.0 (Major Update)
- Wayland support
- Cloud sync
- Additional image sources
- Mobile companion app

### v2.0.0 (Future)
- Complete rewrite in Qt?
- Plugin system
- Advanced scheduling
- AI-generated quotes

## 📊 Metrics & Analytics

### Development Stats
- **Development Time**: ~40 hours
- **Commits**: 50+
- **Contributors**: 1 (riturajprofile)
- **Stars**: TBD
- **Forks**: TBD

### Code Quality
- **Code Coverage**: TBD
- **Technical Debt**: Low
- **Maintainability Index**: High
- **Complexity**: Low-Medium

## 📞 Support

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/riturajprofile/paprwall/issues)
- **Discussions**: [GitHub Discussions](https://github.com/riturajprofile/paprwall/discussions)
- **Email**: riturajprofile@example.com

### Reporting Bugs
1. Check existing issues
2. Create new issue with:
   - OS and version
   - Desktop environment
   - Python version
   - Error messages
   - Steps to reproduce

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

### What This Means
- ✅ Use commercially
- ✅ Modify freely
- ✅ Distribute
- ✅ Private use
- ❌ No warranty
- ❌ No liability

## 🙏 Acknowledgments

### APIs & Services
- [Picsum Photos](https://picsum.photos) - Random images
- [Quotable.io](https://quotable.io) - Quote API
- [ZenQuotes.io](https://zenquotes.io) - Fallback quotes

### Fonts
- DejaVu Serif Italic
- Liberation Serif Italic

### Inspiration
- Desktop customization community
- Linux enthusiasts
- Productivity tools

## 👥 Team

### Maintainer
- **riturajprofile** - Creator & Lead Developer
  - GitHub: [@riturajprofile](https://github.com/riturajprofile)
  - Email: riturajprofile@example.com

### Contributors
- Your name here! - See [Contributing](#-contributing)

## 🌟 Show Your Support

If you find PaprWall useful, please:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code
- 📢 Share with friends

---

<div align="center">

**Made with ❤️ by [riturajprofile](https://github.com/riturajprofile)**

*Change your wallpaper, change your mood* 🎨💭

[⬆ Back to Top](#paprwall-project-overview)

</div>
