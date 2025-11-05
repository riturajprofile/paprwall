"""
Service/Daemon management for PaprWall.
Supports systemd on Linux and Windows Task Scheduler for background operation.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Optional


def get_executable_path() -> Optional[str]:
    """Get the path to paprwall-gui executable."""
    # Try to find in PATH
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["where", "paprwall-gui"],
                capture_output=True,
                text=True,
                timeout=5
            )
        else:
            result = subprocess.run(
                ["which", "paprwall-gui"],
                capture_output=True,
                text=True,
                timeout=5
            )
        
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except Exception as e:
        print(f"Failed to find executable: {e}")
    
    # Fallback: try common locations
    if platform.system() == "Windows":
        locations = [
            Path(sys.executable).parent / "Scripts" / "paprwall-gui.exe",
            Path(sys.executable).parent / "paprwall-gui.exe",
        ]
    else:
        locations = [
            Path(sys.executable).parent / "paprwall-gui",
            Path.home() / ".local" / "bin" / "paprwall-gui",
            Path("/usr/local/bin/paprwall-gui"),
            Path("/usr/bin/paprwall-gui"),
        ]
    
    for loc in locations:
        if loc.exists():
            return str(loc)
    
    return None


def install_systemd_service() -> bool:
    """Install PaprWall as a systemd user service on Linux."""
    if platform.system() != "Linux":
        print("❌ systemd services are only available on Linux")
        return False
    
    try:
        exec_path = get_executable_path()
        if not exec_path:
            print("❌ Could not find paprwall-gui executable")
            return False
        
        # Create systemd user service directory
        systemd_dir = Path.home() / ".config" / "systemd" / "user"
        systemd_dir.mkdir(parents=True, exist_ok=True)
        
        service_file = systemd_dir / "paprwall.service"
        
        # Read template or create service file
        template_path = Path(__file__).parent.parent.parent / "assets" / "paprwall.service.template"
        
        if template_path.exists():
            with open(template_path, "r") as f:
                service_content = f.read()
            service_content = service_content.replace("{EXEC_PATH}", exec_path)
        else:
            # Create service content if template doesn't exist
            service_content = f"""[Unit]
Description=PaprWall - Desktop Wallpaper Manager
After=graphical-session.target

[Service]
Type=simple
ExecStart={exec_path} --daemon
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
"""
        
        # Write service file
        with open(service_file, "w") as f:
            f.write(service_content)
        
        print(f"✓ Created systemd service file: {service_file}")
        
        # Reload systemd daemon
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        print("✓ Reloaded systemd daemon")
        
        # Enable service
        subprocess.run(["systemctl", "--user", "enable", "paprwall.service"], check=True)
        print("✓ Enabled paprwall service")
        
        # Start service
        subprocess.run(["systemctl", "--user", "start", "paprwall.service"], check=True)
        print("✓ Started paprwall service")
        
        print("\n✅ PaprWall service installed and running!")
        print("\n🚀 Service is now:")
        print("  • Running in background (daemon mode)")
        print("  • Auto-starts on every login")
        print("  • Auto-restarts on failure")
        print("  • Changing wallpapers automatically")
        
        print("\n📋 Useful commands:")
        print("  • Check status:  systemctl --user status paprwall")
        print("  • Stop service:  systemctl --user stop paprwall")
        print("  • Restart:       systemctl --user restart paprwall")
        print("  • Disable:       systemctl --user disable paprwall")
        print("  • View logs:     journalctl --user -u paprwall -f")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install systemd service: {e}")
        return False
    except Exception as e:
        print(f"❌ Error installing systemd service: {e}")
        return False


def uninstall_systemd_service() -> bool:
    """Uninstall PaprWall systemd service."""
    if platform.system() != "Linux":
        print("❌ systemd services are only available on Linux")
        return False
    
    try:
        # Stop service
        subprocess.run(["systemctl", "--user", "stop", "paprwall.service"], 
                      capture_output=True)
        print("✓ Stopped paprwall service")
        
        # Disable service
        subprocess.run(["systemctl", "--user", "disable", "paprwall.service"],
                      capture_output=True)
        print("✓ Disabled paprwall service")
        
        # Remove service file
        service_file = Path.home() / ".config" / "systemd" / "user" / "paprwall.service"
        if service_file.exists():
            service_file.unlink()
            print(f"✓ Removed service file: {service_file}")
        
        # Reload systemd daemon
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        print("✓ Reloaded systemd daemon")
        
        print("\n✅ PaprWall service uninstalled successfully!")
        return True
        
    except Exception as e:
        print(f"⚠️  Error uninstalling systemd service: {e}")
        return False


def install_windows_startup() -> bool:
    """Install PaprWall to Windows startup."""
    if platform.system() != "Windows":
        print("❌ Windows startup is only available on Windows")
        return False
    
    try:
        exec_path = get_executable_path()
        if not exec_path:
            print("❌ Could not find paprwall-gui executable")
            return False
        
        # Create startup folder shortcut
        startup_folder = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        startup_folder.mkdir(parents=True, exist_ok=True)
        
        shortcut_path = startup_folder / "PaprWall.lnk"
        
        # Create shortcut using PowerShell
        ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{exec_path}"
$Shortcut.Arguments = "--daemon"
$Shortcut.Description = "PaprWall Desktop Wallpaper Manager"
$Shortcut.WorkingDirectory = "{Path(exec_path).parent}"
$Shortcut.Save()
'''
        
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✅ PaprWall added to Windows startup!")
            print(f"   Shortcut: {shortcut_path}")
            
            # Start daemon immediately
            try:
                print("\n🚀 Starting PaprWall in background mode...")
                # Use CREATE_NO_WINDOW flag on Windows to hide console
                creation_flags = 0x08000000 if platform.system() == "Windows" else 0  # CREATE_NO_WINDOW
                subprocess.Popen(
                    [exec_path, "--daemon"],
                    creationflags=creation_flags,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print("✓ PaprWall is now running in the background!")
            except Exception as e:
                print(f"⚠️  Could not auto-start daemon: {e}")
                print("   You can start it manually or it will start on next login")
            
            print("\n   PaprWall will start automatically when you log in.")
            print("   To disable: Delete the shortcut from the Startup folder")
            return True
        else:
            print(f"❌ Failed to create startup shortcut: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error setting up Windows startup: {e}")
        return False


def uninstall_windows_startup() -> bool:
    """Remove PaprWall from Windows startup."""
    if platform.system() != "Windows":
        print("❌ Windows startup is only available on Windows")
        return False
    
    try:
        startup_folder = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        shortcut_path = startup_folder / "PaprWall.lnk"
        
        if shortcut_path.exists():
            shortcut_path.unlink()
            print(f"✓ Removed startup shortcut: {shortcut_path}")
            print("\n✅ PaprWall removed from Windows startup!")
            return True
        else:
            print("⚠️  No startup shortcut found")
            return False
            
    except Exception as e:
        print(f"❌ Error removing Windows startup: {e}")
        return False


def check_service_status() -> None:
    """Check if PaprWall service is running."""
    if platform.system() == "Linux":
        try:
            # Check if systemctl exists
            try:
                subprocess.run(
                    ["which", "systemctl"],
                    capture_output=True,
                    check=True,
                    timeout=2
                )
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                print("❌ systemd not available on this system")
                return
            
            # Check if service file exists
            service_file = Path.home() / ".config" / "systemd" / "user" / "paprwall.service"
            
            if not service_file.exists():
                print("❌ PaprWall service is not installed")
                print(f"   Service file not found: {service_file}")
                print("\n   Install with: paprwall-service install")
                return
            
            # Check if service is active
            result = subprocess.run(
                ["systemctl", "--user", "is-active", "paprwall.service"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip() == "active":
                print("✅ PaprWall service is running")
                print()
                
                # Show detailed status
                subprocess.run(["systemctl", "--user", "status", "paprwall.service"])
            else:
                # Check if enabled
                enabled = subprocess.run(
                    ["systemctl", "--user", "is-enabled", "paprwall.service"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if enabled.returncode == 0:
                    print("⚠️  PaprWall service is installed but not running")
                    print()
                    print("Start it with: systemctl --user start paprwall")
                else:
                    print("⚠️  PaprWall service is installed but disabled")
                    print()
                    print("Enable it with: systemctl --user enable paprwall")
                    print("Start it with: systemctl --user start paprwall")
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout while checking service status")
        except Exception as e:
            print(f"❌ Error checking service status: {e}")
            
    elif platform.system() == "Windows":
        try:
            appdata = os.environ.get("APPDATA", "")
            if not appdata:
                print("❌ Cannot find APPDATA environment variable")
                return
            
            startup_folder = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
            
            if not startup_folder.exists():
                print(f"❌ Startup folder not found: {startup_folder}")
                return
            
            shortcut_path = startup_folder / "PaprWall.lnk"
            
            if shortcut_path.exists():
                print("✅ PaprWall is in Windows startup")
                print(f"   Shortcut: {shortcut_path}")
                print()
                print("PaprWall will start automatically when you log in.")
            else:
                print("❌ PaprWall is not in Windows startup")
                print(f"   Expected shortcut: {shortcut_path}")
                print()
                print("Install with: paprwall-service install")
                
        except Exception as e:
            print(f"❌ Error checking startup status: {e}")
    else:
        print(f"❌ Service status check not supported on {platform.system()}")


def main() -> None:
    """Command-line interface for service management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PaprWall Service Management")
    parser.add_argument("action", choices=["install", "uninstall", "status"],
                       help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "install":
        if platform.system() == "Linux":
            install_systemd_service()
        elif platform.system() == "Windows":
            install_windows_startup()
        else:
            print(f"❌ Unsupported platform: {platform.system()}")
            
    elif args.action == "uninstall":
        if platform.system() == "Linux":
            uninstall_systemd_service()
        elif platform.system() == "Windows":
            uninstall_windows_startup()
        else:
            print(f"❌ Unsupported platform: {platform.system()}")
            
    elif args.action == "status":
        check_service_status()


if __name__ == "__main__":
    main()
