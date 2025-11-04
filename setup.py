"""
Setup script for paprwall package.
"""
from setuptools import setup, find_packages

setup(
    name="paprwall",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.28.0",
        "Pillow>=10.0.0",
    ],
    extras_require={
        "build": ["pyinstaller>=5.0.0"],
    },
    entry_points={
        "gui_scripts": [
            "paprwall-gui=paprwall.gui.wallpaper_manager_gui:main",
        ],
    },
)
