# CHANGELOG for PaprWall

## [2.1.1] - 2025-11-05
### Changed
- Updated author contact information and links
- Updated email to riturajprofile.me@gmail.com
- Added portfolio link: www.riturajprofile.me
- Added LinkedIn profile link

## [2.1.0] - 2025-11-05
### Changed
- **Simplified Service Controls**: Replaced 3-button service UI (Enable/Disable/Status) with single smart toggle button
- **Enhanced Status Display**: Added color-coded status icons (🟢 Running, 🔴 Disabled, 🟡 Enabled but Stopped, ⚪ Not Installed)
- **Improved UX**: Toggle button automatically shows correct action ("Enable Service" or "Disable Service") based on current state
- **Better Visual Feedback**: Service status now displayed with icon + text for at-a-glance understanding

### Fixed
- Service status checking now has proper timeout handling to prevent UI freezes
- Improved error messages for service-related operations

## [2.0.1] - 2025-11-05
### Changed
- **Simplified Service Controls**: Replaced 3-button service UI (Enable/Disable/Status) with single smart toggle button
- **Enhanced Status Display**: Added color-coded status icons (🟢 Running, 🔴 Disabled, 🟡 Enabled but Stopped, ⚪ Not Installed)
- **Improved UX**: Toggle button automatically shows correct action ("Enable Service" or "Disable Service") based on current state
- **Better Visual Feedback**: Service status now displayed with icon + text for at-a-glance understanding

### Fixed
- Service status checking now has proper timeout handling to prevent UI freezes
- Improved error messages for service-related operations

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