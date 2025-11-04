# Changelog

All notable changes to Paprwall will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-04

### Added
- 🚀 **Complete distribution system** for easy deployment
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

- [1.1.0](https://github.com/riturajprofile/paprwall/releases/tag/v1.1.0) - Distribution Ready
- [1.0.0](https://github.com/riturajprofile/paprwall/releases/tag/v1.0.0) - Initial Release

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
