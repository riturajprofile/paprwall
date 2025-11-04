# Changelog

All notable changes to Paprwall will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-11-04

### Added
- 🚀 **First-Run Auto-Install Prompt**: Binary automatically detects if not installed and prompts user
  - "Yes" button installs desktop entry, icon, and shortcuts
  - "No" button skips this time (asks again next run)
  - "Cancel" button permanently dismisses prompt (portable mode)
- 🔧 **Command-Line Installation**: `paprwall-gui --install` for manual installation
- 🗑️ **Command-Line Uninstallation**: `paprwall-gui --uninstall` for removal
- 🗑️ **GUI Uninstall Button**: Red uninstall button in left control panel
- 🎯 **Automatic Desktop Integration**: Creates desktop entries, shortcuts, and icons

### Changed
- 📦 Binary now includes installation/uninstallation functionality
- 🖥️ Improved user experience for first-time users
- 📝 Updated README with installation options documentation

### Technical
- Added `install_app()` function for cross-platform installation
- Added `uninstall_app_cli()` and GUI `uninstall_app()` methods
- Added `check_first_run_install()` to detect and prompt on first run
- Cross-platform support for Linux and Windows installation paths
- Creates `.no_install_prompt` file to remember user preference

---

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

## [1.0.0] - 2025-11-04

### 🎉 Major Release - Complete Redesign

#### 🎨 Modern GUI Interface
- **Full-screen responsive layout** - Maximized by default, efficient space usage
- **Large wallpaper preview** (480px sidebar) with embedded quotes
- **Dark theme** with professional color palette
- **Compact header** with quick actions
- **Dynamic content panels** that expand to fill available space

#### 💭 Quote System
- **6 Quote Categories**: Motivational, Mathematics, Science, Famous People, Technology, Philosophy
- **Category-specific quotes** with curated fallbacks
- **Quote embedding** directly on wallpaper images (top-right corner)
- **Semi-transparent overlay** for better readability
- **Custom quote support** - Add your own inspirational text
- **API integration** (quotable.io, zenquotes.io)

#### 🔄 Auto-Rotation
- **Enabled by default** with 60-minute interval
- **Real-time countdown timer** (MM:SS format)
- **Auto-fetch on startup** - 2 images fetched automatically
- **Configurable intervals** - Adjust rotation time
- **Smart timer reset** - Resets when manually changing wallpapers

#### � Enhanced History
- **Recent History Gallery** with large thumbnails (120x75px)
- **Preview & Set buttons** for each history item
- **Click to preview** without setting wallpaper
- **Direct set** from history gallery
- **Removed sidebar history** for cleaner layout
- **No favorites clutter** - History is the main feature

#### 🖼️ Wallpaper Management
- **Picsum Photos integration** (https://picsum.photos)
- **URL-based fetching** with progress indicators
- **Local file browser** support
- **Quote embedded on save** - Permanent quote on wallpaper file
- **High-quality exports** (JPEG quality=95)
- **Auto-fetch on launch** - Immediate wallpaper preview

#### 🎯 User Experience
- **Responsive design** - Works on 720p, 1080p, and higher
- **Clean typography** - Segoe UI, Poppins, Georgia fonts
- **Hover effects** - Visual feedback on interactive elements
- **Status bar updates** - Real-time operation feedback
- **Toast notifications** - Non-intrusive alerts
- **Smooth scrolling** - Scrollbars appear only when needed

#### 🛠️ Technical Improvements
- **Thread-safe operations** - Non-blocking UI
- **Smart image resizing** - Maintains aspect ratios
- **Font fallback system** - DejaVu → Liberation → default
- **Error handling** - Graceful degradation
- **Memory efficient** - Proper cleanup of images
- **Cross-platform** - Linux (GNOME, KDE, XFCE) support

#### 🚫 Removed Features
- Multi-source API support (simplified to Picsum)
- Theme selector (removed for simplicity)
- Favorites system (replaced with enhanced history)
- Sidebar recent history (moved to main gallery)
- Complex configuration options

### Added
- 🎨 Modern full-screen GUI with dark theme
- � Motivational quote embedding on wallpapers
- 🔄 Auto-rotation with countdown timer
- 📜 Enhanced history gallery with preview
- 🎯 6 quote categories to choose from
- 🖼️ Top-right corner quote positioning
- 📊 Real-time status updates
- � Custom quote input support
- 🎨 Professional color scheme
- ✨ Hover effects and visual feedback

### Changed
- 🌐 Simplified to Picsum Photos only
- 📐 Full-screen maximized window by default
- 🎨 Complete UI redesign with web-inspired layout
- 💾 Quote embedded permanently on wallpaper images
- 📜 History moved from sidebar to main panel
- 🔄 Auto-rotation enabled by default

### Removed
- ❌ Multi-API support (Pixabay, Unsplash, Pexels)
- ❌ Favorites feature
- ❌ Wallpaper theme selector
- ❌ Sidebar recent history thumbnails
- ❌ Favorite button from actions

### Fixed
- � Layout responsiveness issues
- 🐛 Quote overlay visibility
- 🐛 Timer thread cleanup
- 🐛 Button enable/disable states
- 🐛 History gallery refresh

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
