"""
Auto-start service configuration for Paprwall.
Enables the application to start automatically on system boot.
"""
import os
import sys
import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

SYSTEMD_USER_DIR = Path.home() / '.config' / 'systemd' / 'user'
SERVICE_NAME = 'paprwall.service'


def get_service_content():
    """Generate systemd service file content"""
    python_path = sys.executable
    module_path = 'riturajprofile_wallpaper.service.daemon'
    
    return f"""[Unit]
Description=Paprwall - Auto-rotating Wallpaper Service
After=graphical-session.target

[Service]
Type=simple
ExecStart={python_path} -m {module_path}
Restart=on-failure
RestartSec=10
Environment=DISPLAY=:0
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%U/bus

[Install]
WantedBy=default.target
"""


def enable_autostart():
    """Enable autostart by creating systemd user service"""
    try:
        # Create systemd user directory if it doesn't exist
        SYSTEMD_USER_DIR.mkdir(parents=True, exist_ok=True)
        
        # Write service file
        service_file = SYSTEMD_USER_DIR / SERVICE_NAME
        service_file.write_text(get_service_content())
        
        logger.info(f"✓ Created service file: {service_file}")
        
        # Reload systemd daemon
        subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
        
        # Enable service
        subprocess.run(['systemctl', '--user', 'enable', SERVICE_NAME], check=True)
        
        logger.info(f"✓ Enabled {SERVICE_NAME}")
        logger.info("Paprwall will now start automatically on system boot")
        logger.info(f"\nTo start now: systemctl --user start {SERVICE_NAME}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to enable autostart: {e}")
        return False
    except Exception as e:
        logger.error(f"Error setting up autostart: {e}")
        return False


def disable_autostart():
    """Disable autostart by removing systemd user service"""
    try:
        service_file = SYSTEMD_USER_DIR / SERVICE_NAME
        
        # Stop service if running
        subprocess.run(['systemctl', '--user', 'stop', SERVICE_NAME], 
                      stderr=subprocess.DEVNULL)
        
        # Disable service
        subprocess.run(['systemctl', '--user', 'disable', SERVICE_NAME],
                      stderr=subprocess.DEVNULL)
        
        # Remove service file
        if service_file.exists():
            service_file.unlink()
            logger.info(f"✓ Removed service file: {service_file}")
        
        # Reload daemon
        subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
        
        logger.info(f"✓ Disabled autostart")
        return True
        
    except Exception as e:
        logger.error(f"Error disabling autostart: {e}")
        return False


def is_autostart_enabled():
    """Check if autostart is enabled"""
    try:
        result = subprocess.run(
            ['systemctl', '--user', 'is-enabled', SERVICE_NAME],
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and result.stdout.strip() == 'enabled'
    except:
        return False


def get_service_status():
    """Get the current status of the service"""
    try:
        result = subprocess.run(
            ['systemctl', '--user', 'status', SERVICE_NAME],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error getting status: {e}"


def main():
    """CLI entry point for autostart management"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage Paprwall autostart')
    parser.add_argument('--enable', action='store_true', help='Enable autostart')
    parser.add_argument('--disable', action='store_true', help='Disable autostart')
    parser.add_argument('--status', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    if args.enable:
        enable_autostart()
    elif args.disable:
        disable_autostart()
    elif args.status:
        if is_autostart_enabled():
            print("✓ Autostart is ENABLED")
            print("\nService status:")
            print(get_service_status())
        else:
            print("✗ Autostart is DISABLED")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
