#!/usr/bin/env python3
"""
Quick verification script for Paprwall installation.
Run after installing to verify everything is set up correctly.
"""
import sys
import subprocess
from pathlib import Path


def check_command(cmd, name):
    """Check if a command exists"""
    try:
        result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {name} command works")
            return True
        else:
            print(f"❌ {name} command failed")
            return False
    except FileNotFoundError:
        print(f"❌ {name} command not found")
        return False


def check_service():
    """Check systemd service status"""
    try:
        result = subprocess.run(
            ['systemctl', '--user', 'is-enabled', 'paprwall'],
            capture_output=True,
            text=True
        )
        if 'enabled' in result.stdout:
            print("✅ Auto-start service is enabled")
            return True
        else:
            print(f"⚠️  Auto-start service not enabled: {result.stdout.strip()}")
            return False
    except Exception as e:
        print(f"⚠️  Could not check service: {e}")
        return False


def check_service_running():
    """Check if service is running"""
    try:
        result = subprocess.run(
            ['systemctl', '--user', 'is-active', 'paprwall'],
            capture_output=True,
            text=True
        )
        if 'active' in result.stdout:
            print("✅ Service is running")
            return True
        else:
            print(f"⚠️  Service not running: {result.stdout.strip()}")
            print("    You can start it with: systemctl --user start paprwall")
            return False
    except Exception as e:
        print(f"⚠️  Could not check service status: {e}")
        return False


def check_directories():
    """Check if required directories exist"""
    dirs = {
        'Config': Path.home() / '.config' / 'riturajprofile-wallpaper',
        'Data': Path.home() / '.local' / 'share' / 'riturajprofile-wallpaper',
        'Cache': Path.home() / '.cache' / 'riturajprofile-wallpaper',
    }
    
    all_exist = True
    for name, path in dirs.items():
        if path.exists():
            print(f"✅ {name} directory exists: {path}")
        else:
            print(f"⚠️  {name} directory missing: {path}")
            all_exist = False
    
    return all_exist


def check_service_file():
    """Check if systemd service file exists"""
    service_file = Path.home() / '.config' / 'systemd' / 'user' / 'paprwall.service'
    
    if service_file.exists():
        print(f"✅ Service file exists: {service_file}")
        return True
    else:
        print(f"❌ Service file missing: {service_file}")
        print("    Run: python -m riturajprofile_wallpaper.service.autostart --enable")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("Paprwall Installation Verification")
    print("=" * 60)
    print()
    
    checks = []
    
    # Check commands
    print("📦 Checking Commands:")
    checks.append(check_command('paprwall', 'paprwall'))
    checks.append(check_command('paprwall-gui', 'paprwall-gui'))
    print()
    
    # Check directories
    print("📁 Checking Directories:")
    checks.append(check_directories())
    print()
    
    # Check service
    print("⚙️  Checking Service:")
    checks.append(check_service_file())
    checks.append(check_service())
    checks.append(check_service_running())
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ All checks passed! ({passed}/{total})")
        print()
        print("🎉 Paprwall is ready to use!")
        print()
        print("Quick Start:")
        print("  1. Set a theme: paprwall --set-theme ocean")
        print("  2. Fetch wallpapers: paprwall --fetch")
        print("  3. Launch GUI: paprwall-gui")
        print()
        return 0
    else:
        print(f"⚠️  Some checks failed: {passed}/{total} passed")
        print()
        print("Troubleshooting:")
        print("  - Make sure you installed with: pip install -e .")
        print("  - Enable service: python -m riturajprofile_wallpaper.service.autostart --enable")
        print("  - Check logs: journalctl --user -u paprwall")
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())
