# CHANGELOG for PaprWall

## [Unreleased]
### Added
- **Desktop Integration**: Added automatic desktop entry creation via `paprwall-setup-desktop` command
- Users can now launch PaprWall from their application menu (Linux) or Start Menu (Windows)
- Desktop entry template for consistent cross-platform integration
- Post-installation script for one-command desktop setup
- Comprehensive desktop integration documentation (DESKTOP_INTEGRATION.md, QUICKSTART.md)
- Icon installation to system icons directory
- Initial project setup with basic structure.
- Implemented the ModernWallpaperGUI class for managing the wallpaper application's GUI.
- Added functionality for fetching random wallpapers and displaying motivational quotes.

### Changed
- Updated installation process to include desktop integration setup step
- Enhanced README with desktop app installation instructions
- Updated the auto-rotation feature to allow user-defined intervals.
- Improved error handling for image fetching and quote retrieval.

### Fixed
- Desktop app now accessible without relying solely on terminal commands

## [0.1.0] - 2024-01-01
### Added
- First release of PaprWall.
- Included installation instructions in the documentation.
- Added unit tests for wallpaper manager functionality.

### Changed
- Enhanced the user interface for better usability.
- Optimized image loading and display performance.

### Fixed
- Resolved issues with wallpaper setting on different operating systems.
- Fixed bugs related to quote fetching from APIs.