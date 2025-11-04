# Changelog

All notable changes to Paprwall will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-04

### Added
- ⏱️ **Real-time Countdown Timer**: Display showing MM:SS until next wallpaper rotation
- 🔄 **Auto Fetch Button**: One-click button to fetch and immediately apply new wallpaper (sync)
- 🎛️ **Auto-Rotation Controls**: Toggle checkbox with configurable interval (minutes)
- 🧵 **Background Timer Thread**: Non-blocking countdown updates every second
- 📊 **Timer Auto-Reset**: Timer resets automatically when manually changing wallpapers

### Features
- 🌐 Picsum-only image source (https://picsum.photos/1920/1080)
- 🖼️ Modern web-inspired GUI with large preview area
- 💻 CLI interface with fetch/next/prev/set/current commands
- 📦 Standalone binaries for Linux, Windows, macOS
- 🤖 Automated builds via GitHub Actions
- 📦 DEB and RPM packages for Linux
- 🔧 One-line installer for Linux

### Technical
- Thread-safe UI updates using root.after()
- Proper daemon thread cleanup with stop flags
- Non-blocking HTTP requests for downloads
- Comprehensive error handling
- Real-time status bar feedback

---

## [1.1.0] - 2025-11-04
## [2.0.0] - 2025-11-04

### Added
- 🖼️ GUI binaries for Linux, Windows (macOS builds available)
- 🤖 GitHub Actions workflow to build and publish CLI + GUI binaries and Linux packages (DEB/RPM)
- � `install-single.sh` now installs both CLI and GUI when binaries are available
- 🔁 `paprwall --gui` flag to launch the Tkinter GUI from CLI

### Changed
- 🌐 Simplified to Picsum-only source (no API keys required)
- 🧹 Removed unused API client codepaths and legacy options from CLI
- 📝 Clean, compact README focused on downloads and quick usage

### Fixed
- 🧰 Consistent versioning across `pyproject.toml`, `setup.py`, and `__init__.py`

### About this release
2.0.0 is a distribution-focused release: easy downloads for end-users (no Python needed) and a simpler app model using Picsum. It keeps both a lightweight CLI and a friendly GUI, with clear installers and automated release builds.

---


### Added
- �🚀 **Complete distribution system** for easy deployment
  - `install.sh` - One-line automated installer for all major Linux distros
  - `uninstall.sh` - Clean removal script
- 🔑 **Hardcoded API keys** - No setup required, works out of the box
- 📚 **Simplified documentation** - Just README and CHANGELOG

### Fixed
- 🐛 **tkinter module not found** error when using pipx
  - Install script creates proper venv with system package access
  - GUI works correctly after installation

### Improved
- ✨ **Installation experience**
  - Auto-detection of package manager (apt/dnf/pacman/zypper)
  - Automatic system dependency installation
  - Virtual environment setup at `~/.paprwall/.venv`
  - Command wrapper creation in `~/.local/bin`
  - Auto-start service
- 🎯 **Simplified setup** - No API key configuration needed

### Changed
- 🔄 Moved from pipx to virtual environment installation
- � Hardcoded API keys for instant use
- 🧹 Removed unnecessary build scripts

## [1.0.0] - 2025-11-03

### Added
- 🎨 Initial release of Paprwall
- 🌐 Multi-source wallpaper support (Pixabay, Unsplash, Pexels)
- 📁 Local image management
- 🔄 Automatic wallpaper rotation
- 🎛️ Theme support (nature, city, space, ocean, minimal, etc.)
- 🔍 Custom search queries
- 📸 Photographer attribution system
- 🖥️ Desktop environment support (GNOME, KDE, XFCE, MATE, etc.)
- 💻 Dual interface: CLI and GUI
- ⚙️ Systemd service for auto-start
- 📊 Wallpaper history navigation
- 🔑 Custom API key support
- 🎨 Source enable/disable functionality
- 📝 Comprehensive logging

---

## Release Links

- [0.1.0](https://github.com/riturajprofile/paprwall/releases/tag/v0.1.0) - First Release with Countdown Timer & Auto-Fetch

## Upgrade Instructions

### From 1.0.0 to 1.1.0

If you had 1.0.0 installed via pipx or other methods:

```bash
# Remove old installation
pipx uninstall paprwall 2>/dev/null || pip uninstall paprwall -y

# Install 1.1.0 with new method
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash
```

Your configuration and wallpapers will be preserved in `~/.config/paprwall` and `~/.local/share/paprwall`.

---

## Versioning Policy

- **Major version (X.0.0)**: Breaking changes, major features
- **Minor version (0.X.0)**: New features, non-breaking changes
- **Patch version (0.0.X)**: Bug fixes, minor improvements

---

**Legend:**
- 🚀 New features
- 🐛 Bug fixes
- ✨ Improvements
- 🔄 Changes
- ⚠️ Deprecations
- 🗑️ Removals
