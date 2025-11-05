#!/usr/bin/env python3
"""
Custom setup script for PaprWall with post-installation instructions.
"""

import sys
import atexit
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop


def print_post_install_message():
    """Print post-installation instructions."""
    message = """
╔════════════════════════════════════════════════════════════════════╗
║              PaprWall Installation Complete! 🎨                   ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  To set up desktop integration (recommended):                     ║
║                                                                    ║
║    $ paprwall-setup-desktop                                       ║
║                                                                    ║
║  This will create a desktop entry so you can launch PaprWall      ║
║  from your application menu instead of just the terminal.         ║
║                                                                    ║
║  Or run PaprWall directly:                                        ║
║                                                                    ║
║    $ paprwall-gui                                                 ║
║                                                                    ║
║  For more information:                                            ║
║    https://github.com/riturajprofile/paprwall                    ║
║    https://www.riturajprofile.me                                   ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
"""
    print(message)


class PostInstallCommand(install):
    """Post-installation command to show instructions."""
    
    def run(self):
        """Run the standard installation and show post-install message."""
        install.run(self)
        
        # Register message to print at exit
        atexit.register(print_post_install_message)


class PostDevelopCommand(develop):
    """Post-development installation command for editable installs."""
    
    def run(self):
        """Run the standard development installation and show post-install message."""
        develop.run(self)
        
        # Register message to print at exit
        atexit.register(print_post_install_message)


if __name__ == "__main__":
    # Use setuptools with custom install commands
    setup(
        cmdclass={
            'install': PostInstallCommand,
            'develop': PostDevelopCommand,
        },
    )
