"""
Setup script for riturajprofile-wallpaper package.
"""
from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Enable auto-start after installation
        try:
            subprocess.run([sys.executable, "-m", "riturajprofile_wallpaper.service.autostart", "--enable"], check=True)
            print("\n✅ Auto-start service enabled successfully!")
            print("Paprwall will now start automatically on system boot.")
        except Exception as e:
            print(f"\n⚠️  Could not enable auto-start: {e}")
            print("You can enable it manually with: paprwall --enable-service")

setup(
    name="paprwall",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.28.0",
        "Pillow>=10.0.0",
        "APScheduler>=3.10.0",
        "PyGObject>=3.42.0",
    ],
    entry_points={
        "console_scripts": [
            "paprwall=riturajprofile_wallpaper.cli:main",
        ],
        "gui_scripts": [
            "paprwall-gui=riturajprofile_wallpaper.gui.main_window:main",
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)
