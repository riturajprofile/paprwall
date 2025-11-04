"""
Setup script for paprwall package.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="paprwall",
    version="1.0.0",
    author="riturajprofile",
    author_email="riturajprofile@example.com",
    description="Modern Desktop Wallpaper Manager with Motivational Quotes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/riturajprofile/paprwall",
    project_urls={
        "Bug Reports": "https://github.com/riturajprofile/paprwall/issues",
        "Source": "https://github.com/riturajprofile/paprwall",
        "Documentation": "https://github.com/riturajprofile/paprwall#readme",
        "Changelog": "https://github.com/riturajprofile/paprwall/blob/main/CHANGELOG.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications",
        "Natural Language :: English",
    ],
    keywords="wallpaper desktop background quotes motivation linux gnome kde xfce",
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "Pillow>=10.0.0",
    ],
    extras_require={
        "build": ["pyinstaller>=5.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "gui_scripts": [
            "paprwall-gui=paprwall.gui.wallpaper_manager_gui:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
