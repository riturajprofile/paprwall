"""
System installer module for PaprWall desktop integration.
Handles installation and uninstallation of desktop entries, shortcuts, and system integration.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

from . import __version__, PACKAGE_NAME, APP_NAME


class SystemInstaller:
    """Handle system-level installation and uninstallation."""

    def __init__(self):
        """Initialize the system installer."""
        self.system = platform.system().lower()
        self.version = __version__
        self.app_name = APP_NAME
        self.package_name = PACKAGE_NAME

        # Define installation paths based on OS
        if self.system == "linux":
            self.home = Path.home()
            self.local_bin = self.home / ".local" / "bin"
            self.local_share = self.home / ".local" / "share"
            self.desktop_entries = self.local_share / "applications"
            self.icons_dir = self.local_share / "icons" / "hicolor" / "256x256" / "apps"
            self.executable_name = f"{self.app_name}-gui"

        elif self.system == "windows":
            self.appdata = Path(os.environ.get("APPDATA", ""))
            self.local_appdata = Path(os.environ.get("LOCALAPPDATA", ""))
            self.programs_dir = self.local_appdata / "Programs" / "PaprWall"
            self.start_menu = (
                self.appdata / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            )
            self.desktop = Path.home() / "Desktop"
            self.executable_name = f"{self.app_name}-gui.exe"

    def install_linux(self) -> bool:
        """Install PaprWall on Linux systems."""
        try:
            print("Installing PaprWall on Linux...")

            # Create necessary directories
            self.local_bin.mkdir(parents=True, exist_ok=True)
            self.desktop_entries.mkdir(parents=True, exist_ok=True)
            self.icons_dir.mkdir(parents=True, exist_ok=True)

            # Get the path to the current executable
            current_executable = Path(sys.executable)
            if getattr(sys, "frozen", False):
                # Running as PyInstaller bundle
                current_executable = Path(sys.argv[0]).resolve()

            # Copy executable to local bin
            target_executable = self.local_bin / self.executable_name
            if current_executable != target_executable:
                shutil.copy2(current_executable, target_executable)
                target_executable.chmod(0o755)

            # Create desktop entry
            desktop_content = f"""[Desktop Entry]
Version=1.0
Name=PaprWall
Comment=Modern Desktop Wallpaper Manager with Motivational Quotes
GenericName=Wallpaper Manager
Exec={target_executable}
Icon=paprwall
Terminal=false
Type=Application
Categories=Graphics;Photography;Viewer;
Keywords=wallpaper;background;desktop;quotes;
StartupNotify=true
StartupWMClass=PaprWall
"""

            desktop_file = self.desktop_entries / "paprwall.desktop"
            desktop_file.write_text(desktop_content)
            desktop_file.chmod(0o644)

            # Copy application icon from assets
            icon_file = self.icons_dir / "paprwall.png"
            self._copy_icon_from_assets(icon_file)

            # Create uninstall script
            uninstall_script = self.local_bin / f"uninstall-{self.app_name}"
            uninstall_content = f"""#!/bin/bash
# PaprWall Uninstaller v{self.version}

echo "PaprWall Uninstaller"
echo "==================="

# Ask for confirmation
read -p "Are you sure you want to uninstall PaprWall? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo "Removing PaprWall..."

# Remove executable
rm -f "{target_executable}"
echo "✓ Removed executable"

# Remove desktop entry
rm -f "{desktop_file}"
echo "✓ Removed desktop entry"

# Remove icon
rm -f "{icon_file}"
echo "✓ Removed icon"

# Remove uninstall script
rm -f "{uninstall_script}"
echo "✓ Removed uninstall script"

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "{self.desktop_entries}" 2>/dev/null || true
    echo "✓ Updated desktop database"
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -t "{self.local_share}/icons/hicolor" 2>/dev/null || true
    echo "✓ Updated icon cache"
fi

# Ask about data directory
echo
read -p "Remove data directory (~/.local/share/paprwall)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/.local/share/paprwall"
    echo "✓ Removed data directory"
else
    echo "✓ Kept data directory"
fi

echo
echo "PaprWall has been successfully uninstalled!"
"""

            with open(uninstall_script, "w") as f:
                f.write(uninstall_content)
            uninstall_script.chmod(0o755)

            # Update desktop database
            try:
                subprocess.run(
                    ["update-desktop-database", str(self.desktop_entries)],
                    capture_output=True,
                    timeout=10,
                )
            except:
                pass

            # Update icon cache
            try:
                subprocess.run(
                    [
                        "gtk-update-icon-cache",
                        "-t",
                        str(self.local_share / "icons" / "hicolor"),
                    ],
                    capture_output=True,
                    timeout=10,
                )
            except:
                pass

            print("✓ PaprWall installed successfully!")
            print(f"✓ Executable: {target_executable}")
            print(f"✓ Desktop entry: {desktop_file}")
            print(f"✓ Uninstaller: {uninstall_script}")
            print("\nYou can now find PaprWall in your application menu.")

            return True

        except Exception as e:
            print(f"Installation failed: {e}")
            return False

    def install_windows(self) -> bool:
        """Install PaprWall on Windows systems."""
        try:
            print("Installing PaprWall on Windows...")

            # Create necessary directories
            self.programs_dir.mkdir(parents=True, exist_ok=True)

            # Get the path to the current executable
            current_executable = Path(sys.executable)
            if getattr(sys, "frozen", False):
                # Running as PyInstaller bundle
                current_executable = Path(sys.argv[0]).resolve()

            # Copy executable to programs directory
            target_executable = self.programs_dir / self.executable_name
            if current_executable != target_executable:
                shutil.copy2(current_executable, target_executable)

            # Create Start Menu shortcut
            start_menu_folder = self.start_menu / "PaprWall"
            start_menu_folder.mkdir(exist_ok=True)

            # Create shortcut using PowerShell
            shortcut_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{start_menu_folder / "PaprWall.lnk"}")
$Shortcut.TargetPath = "{target_executable}"
$Shortcut.Description = "Modern Desktop Wallpaper Manager with Motivational Quotes"
$Shortcut.WorkingDirectory = "{target_executable.parent}"
$Shortcut.Save()
'''

            try:
                subprocess.run(
                    ["powershell", "-Command", shortcut_script],
                    capture_output=True,
                    timeout=30,
                )
            except:
                pass

            # Create Desktop shortcut
            desktop_shortcut_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{self.desktop / "PaprWall.lnk"}")
$Shortcut.TargetPath = "{target_executable}"
$Shortcut.Description = "Modern Desktop Wallpaper Manager with Motivational Quotes"
$Shortcut.WorkingDirectory = "{target_executable.parent}"
$Shortcut.Save()
'''

            try:
                subprocess.run(
                    ["powershell", "-Command", desktop_shortcut_script],
                    capture_output=True,
                    timeout=30,
                )
            except:
                pass

            # Create uninstall script
            uninstall_script = self.programs_dir / "UNINSTALL.bat"
            uninstall_content = f'''@echo off
REM PaprWall Uninstaller v{self.version}

echo PaprWall Uninstaller
echo ====================
echo.

set /p confirm="Are you sure you want to uninstall PaprWall? (y/N): "
if /i not "%confirm%"=="y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo Removing PaprWall...

REM Remove Start Menu shortcuts
rmdir /s /q "{start_menu_folder}" 2>nul
echo. Removed Start Menu shortcuts

REM Remove Desktop shortcut
del "{self.desktop / "PaprWall.lnk"}" 2>nul
echo. Removed Desktop shortcut

REM Remove program directory (except this script)
cd /d "%TEMP%"
rmdir /s /q "{self.programs_dir}" 2>nul
echo. Removed program files

echo.
set /p removedata="Remove data directory (%APPDATA%\\PaprWall)? (y/N): "
if /i "%removedata%"=="y" (
    rmdir /s /q "%APPDATA%\\PaprWall" 2>nul
    echo. Removed data directory
) else (
    echo. Kept data directory
)

echo.
echo PaprWall has been successfully uninstalled!
pause
'''

            with open(uninstall_script, "w") as f:
                f.write(uninstall_content)

            # Create uninstall shortcut in Start Menu
            uninstall_shortcut_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{start_menu_folder / "Uninstall PaprWall.lnk"}")
$Shortcut.TargetPath = "{uninstall_script}"
$Shortcut.Description = "Uninstall PaprWall"
$Shortcut.WorkingDirectory = "{uninstall_script.parent}"
$Shortcut.Save()
'''

            try:
                subprocess.run(
                    ["powershell", "-Command", uninstall_shortcut_script],
                    capture_output=True,
                    timeout=30,
                )
            except:
                pass

            print("✓ PaprWall installed successfully!")
            print(f"✓ Program files: {self.programs_dir}")
            print(f"✓ Start Menu: {start_menu_folder}")
            print("\nYou can now find PaprWall in your Start Menu.")

            return True

        except Exception as e:
            print(f"Installation failed: {e}")
            return False

    def uninstall_linux(self) -> bool:
        """Uninstall PaprWall from Linux systems."""
        try:
            print("Uninstalling PaprWall from Linux...")

            removed_items = []

            # Remove executable
            executable = self.local_bin / self.executable_name
            if executable.exists():
                executable.unlink()
                removed_items.append("executable")

            # Remove desktop entry
            desktop_file = self.desktop_entries / "paprwall.desktop"
            if desktop_file.exists():
                desktop_file.unlink()
                removed_items.append("desktop entry")

            # Remove icon
            icon_file = self.icons_dir / "paprwall.png"
            if icon_file.exists():
                icon_file.unlink()
                removed_items.append("icon")

            # Remove uninstall script
            uninstall_script = self.local_bin / f"uninstall-{self.app_name}"
            if uninstall_script.exists():
                uninstall_script.unlink()
                removed_items.append("uninstall script")

            # Update desktop database
            try:
                subprocess.run(
                    ["update-desktop-database", str(self.desktop_entries)],
                    capture_output=True,
                    timeout=10,
                )
                removed_items.append("updated desktop database")
            except:
                pass

            # Update icon cache
            try:
                subprocess.run(
                    [
                        "gtk-update-icon-cache",
                        "-t",
                        str(self.local_share / "icons" / "hicolor"),
                    ],
                    capture_output=True,
                    timeout=10,
                )
                removed_items.append("updated icon cache")
            except:
                pass

            if removed_items:
                print(f"✓ Removed: {', '.join(removed_items)}")
                print("PaprWall has been uninstalled successfully!")
                return True
            else:
                print("No PaprWall installation found.")
                return False

        except Exception as e:
            print(f"Uninstallation failed: {e}")
            return False

    def uninstall_windows(self) -> bool:
        """Uninstall PaprWall from Windows systems."""
        try:
            print("Uninstalling PaprWall from Windows...")

            removed_items = []

            # Remove Start Menu folder
            start_menu_folder = self.start_menu / "PaprWall"
            if start_menu_folder.exists():
                shutil.rmtree(start_menu_folder, ignore_errors=True)
                removed_items.append("Start Menu shortcuts")

            # Remove Desktop shortcut
            desktop_shortcut = self.desktop / "PaprWall.lnk"
            if desktop_shortcut.exists():
                desktop_shortcut.unlink()
                removed_items.append("Desktop shortcut")

            # Remove program directory
            if self.programs_dir.exists():
                shutil.rmtree(self.programs_dir, ignore_errors=True)
                removed_items.append("program files")

            if removed_items:
                print(f"✓ Removed: {', '.join(removed_items)}")
                print("PaprWall has been uninstalled successfully!")
                return True
            else:
                print("No PaprWall installation found.")
                return False

        except Exception as e:
            print(f"Uninstallation failed: {e}")
            return False

    def _copy_icon_from_assets(self, icon_path: Path) -> None:
        """Copy the real icon from assets directory."""
        try:
            import shutil

            # Find the icon in assets directory
            # When running as PyInstaller bundle, assets are bundled
            if getattr(sys, "frozen", False):
                # Running as PyInstaller bundle
                bundle_dir = Path(sys._MEIPASS)
                assets_icon = bundle_dir / "assets" / "paprwall-icon.png"
            else:
                # Running as script - look for assets relative to this file
                installer_dir = Path(__file__).parent
                project_root = installer_dir.parent.parent
                assets_icon = project_root / "assets" / "paprwall-icon.png"

            # Ensure target directory exists
            icon_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy the icon if it exists
            if assets_icon.exists():
                shutil.copy2(assets_icon, icon_path)
                print(f"✓ Copied icon from {assets_icon}")
            else:
                # Fallback: create a simple icon using PIL
                self._create_fallback_icon(icon_path)

        except Exception as e:
            print(f"⚠️  Could not copy icon: {e}")
            # Try to create a fallback icon
            self._create_fallback_icon(icon_path)

    def _create_fallback_icon(self, icon_path: Path) -> None:
        """Create a simple fallback PNG icon if real icon is not available."""
        try:
            from PIL import Image, ImageDraw, ImageFont

            # Create a simple 256x256 icon
            size = 256
            image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            # Draw a gradient background
            for i in range(size):
                alpha = int(255 * (1 - i / size))
                color = (60, 130, 246, alpha)  # Blue gradient
                draw.line([(0, i), (size, i)], fill=color)

            # Draw text
            try:
                font = ImageFont.truetype("arial.ttf", 48)
            except:
                font = ImageFont.load_default()

            text = "PW"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (size - text_width) // 2
            text_y = (size - text_height) // 2

            draw.text((text_x, text_y), text, fill="white", font=font)

            # Save icon
            icon_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(icon_path, "PNG")

        except Exception:
            # If PIL fails, create a simple text file as placeholder
            icon_path.parent.mkdir(parents=True, exist_ok=True)
            with open(icon_path.with_suffix(".txt"), "w") as f:
                f.write("PaprWall Icon Placeholder")


def install_system() -> int:
    """Install PaprWall to the system."""
    installer = SystemInstaller()

    try:
        if installer.system == "linux":
            success = installer.install_linux()
        elif installer.system == "windows":
            success = installer.install_windows()
        else:
            print(f"Installation not supported on {installer.system}")
            return 1

        return 0 if success else 1

    except Exception as e:
        print(f"Installation error: {e}")
        return 1


def uninstall_system() -> int:
    """Uninstall PaprWall from the system."""
    installer = SystemInstaller()

    try:
        if installer.system == "linux":
            success = installer.uninstall_linux()
        elif installer.system == "windows":
            success = installer.uninstall_windows()
        else:
            print(f"Uninstallation not supported on {installer.system}")
            return 1

        return 0 if success else 1

    except Exception as e:
        print(f"Uninstallation error: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        sys.exit(uninstall_system())
    else:
        sys.exit(install_system())
