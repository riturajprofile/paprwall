#!/usr/bin/env python3
"""
Post-installation script for PaprWall.
This script is automatically run after pip installation to set up desktop integration.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
from typing import Optional


def get_executable_path() -> Optional[str]:
    """Get the path to the paprwall-gui executable."""
    # Check if paprwall-gui is in PATH
    exec_path = shutil.which("paprwall-gui")
    if exec_path:
        return exec_path
    
    # Check in user's local bin
    local_bin = Path.home() / ".local" / "bin" / "paprwall-gui"
    if local_bin.exists():
        return str(local_bin)
    
    # Check in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        venv_bin = Path(sys.prefix) / "bin" / "paprwall-gui"
        if venv_bin.exists():
            return str(venv_bin)
    
    return None


def get_icon_path() -> str:
    """Get the path to the paprwall icon."""
    # Try to find the icon in the package
    try:
        import paprwall
        package_dir = Path(paprwall.__file__).parent
        
        # Check in package assets
        icon_candidates = [
            package_dir / "assets" / "paprwall-icon.png",
            package_dir.parent / "assets" / "paprwall-icon.png",
            package_dir.parent.parent / "assets" / "paprwall-icon.png",
        ]
        
        for icon in icon_candidates:
            if icon.exists():
                return str(icon)
    except ImportError:
        pass
    
    # Fallback to just the name (will use system icon theme)
    return "paprwall"


def install_desktop_entry_linux() -> bool:
    """Install desktop entry on Linux."""
    try:
        # Get paths
        exec_path = get_executable_path()
        if not exec_path:
            print("⚠️  Could not find paprwall-gui executable. Desktop entry not created.")
            print("   You may need to add your Python bin directory to PATH.")
            return False
        
        icon_path = get_icon_path()
        
        # Create directories
        desktop_entries = Path.home() / ".local" / "share" / "applications"
        desktop_entries.mkdir(parents=True, exist_ok=True)
        
        icons_dir = Path.home() / ".local" / "share" / "icons" / "hicolor" / "256x256" / "apps"
        icons_dir.mkdir(parents=True, exist_ok=True)
        
        # Read template
        try:
            import paprwall
            package_dir = Path(paprwall.__file__).parent
            template_candidates = [
                package_dir / "assets" / "paprwall.desktop.template",
                package_dir.parent / "assets" / "paprwall.desktop.template",
                package_dir.parent.parent / "assets" / "paprwall.desktop.template",
            ]
            
            template_content = None
            for template_path in template_candidates:
                if template_path.exists():
                    template_content = template_path.read_text()
                    break
            
            if not template_content:
                # Fallback to inline template
                template_content = """[Desktop Entry]
Version=1.1
Name=PaprWall
Comment=Modern Desktop Wallpaper Manager with Motivational Quotes
GenericName=Wallpaper Manager
Exec={exec_path}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Graphics;Photography;Viewer;Utility;
Keywords=wallpaper;background;desktop;quotes;image;
StartupNotify=true
StartupWMClass=PaprWall
X-GNOME-UsesNotifications=true
"""
        except ImportError:
            # Fallback template
            template_content = """[Desktop Entry]
Version=1.1
Name=PaprWall
Comment=Modern Desktop Wallpaper Manager with Motivational Quotes
GenericName=Wallpaper Manager
Exec={exec_path}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Graphics;Photography;Viewer;Utility;
Keywords=wallpaper;background;desktop;quotes;image;
StartupNotify=true
StartupWMClass=PaprWall
X-GNOME-UsesNotifications=true
"""
        
        # Fill in template
        desktop_content = template_content.format(
            exec_path=exec_path,
            icon_path=icon_path
        )
        
        # Write desktop file
        desktop_file = desktop_entries / "paprwall.desktop"
        desktop_file.write_text(desktop_content)
        desktop_file.chmod(0o644)
        
        # Copy icon if it's a file path
        if icon_path != "paprwall" and Path(icon_path).exists():
            icon_dest = icons_dir / "paprwall.png"
            shutil.copy2(icon_path, icon_dest)
        
        # Update desktop database (optional, don't fail if not available)
        try:
            subprocess.run(
                ["update-desktop-database", str(desktop_entries)],
                capture_output=True,
                timeout=10,
                check=False
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Update icon cache (optional)
        try:
            subprocess.run(
                ["gtk-update-icon-cache", "-t", str(Path.home() / ".local" / "share" / "icons" / "hicolor")],
                capture_output=True,
                timeout=10,
                check=False
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        print("\n✓ PaprWall desktop integration installed successfully!")
        print(f"  Desktop entry: {desktop_file}")
        print(f"  Executable: {exec_path}")
        print("\n  You can now find PaprWall in your application menu.")
        print("  Search for 'PaprWall' or 'Wallpaper' in your launcher.\n")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Desktop integration setup failed: {e}")
        print("   You can still run PaprWall using: paprwall-gui")
        return False


def install_desktop_entry_windows() -> bool:
    """Install Start Menu entry on Windows."""
    try:
        # Get executable path
        exec_path = get_executable_path()
        if not exec_path:
            print("⚠️  Could not find paprwall-gui executable.")
            return False
        
        # Convert to Windows path
        exec_path = Path(exec_path).resolve()
        
        # Create Start Menu folder
        start_menu = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "PaprWall"
        start_menu.mkdir(parents=True, exist_ok=True)
        
        # Create shortcut using PowerShell
        shortcut_path = start_menu / "PaprWall.lnk"
        ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{exec_path}"
$Shortcut.Description = "Modern Desktop Wallpaper Manager with Motivational Quotes"
$Shortcut.WorkingDirectory = "{exec_path.parent}"
$Shortcut.Save()
'''
        
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✓ PaprWall installed to Start Menu successfully!")
            print(f"  Shortcut: {shortcut_path}")
            print("\n  You can now find PaprWall in your Start Menu.\n")
            return True
        else:
            print(f"⚠️  Could not create Start Menu shortcut: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"⚠️  Start Menu setup failed: {e}")
        print("   You can still run PaprWall using: paprwall-gui")
        return False


def main():
    """Main post-installation function."""
    # Skip in certain environments
    if os.environ.get("SKIP_PAPRWALL_DESKTOP_INSTALL") == "1":
        return
    
    # Skip during build/test
    if "bdist" in sys.argv or "sdist" in sys.argv or "test" in sys.argv:
        return
    
    system = platform.system().lower()
    
    print("\n" + "="*70)
    print("  PaprWall - Desktop Integration Setup")
    print("="*70)
    
    if system == "linux":
        install_desktop_entry_linux()
    elif system == "windows":
        install_desktop_entry_windows()
    elif system == "darwin":
        # macOS - could add .app bundle creation here
        print("⚠️  Desktop integration not yet supported on macOS.")
        print("   You can run PaprWall using: paprwall-gui\n")
    else:
        print(f"⚠️  Desktop integration not supported on {system}.")
        print("   You can run PaprWall using: paprwall-gui\n")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
