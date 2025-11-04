# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for PaprWall - Modern Desktop Wallpaper Manager
This builds a standalone executable for Windows distribution.
"""

import os
import sys
from pathlib import Path

# Get the project root directory in a robust way.
# In some PyInstaller versions, __file__ may not be defined for spec execution.
try:
    _spec_path = Path(__file__).resolve()
    project_root = _spec_path.parent.parent
except NameError:
    # Fall back to current working directory (CI/build scripts call from repo root)
    project_root = Path.cwd()
    # If called from the scripts directory, move one level up
    if project_root.name == "scripts" and (project_root.parent / "src").exists():
        project_root = project_root.parent

src_dir = project_root / "src"
assets_dir = project_root / "assets"

# Add src to Python path
sys.path.insert(0, str(src_dir))

# Import version info
try:
    from paprwall import __version__
    version = __version__
except ImportError:
    version = "1.0.2"

block_cipher = None

# Data files to include
datas = []

# Include assets if they exist (icons, images, etc.)
if assets_dir.exists():
    datas.append((str(assets_dir), 'assets'))
    print(f"Including assets from: {assets_dir}")

# Include any additional data files
additional_data = [
    (str(project_root / "README.md"), '.'),
    (str(project_root / "LICENSE"), '.'),
]

for src, dst in additional_data:
    if os.path.exists(src):
        datas.append((src, dst))

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'PIL.ImageTk',
    'requests',
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'json',
    'threading',
    'subprocess',
    'platform',
    'ctypes',
    'ctypes.wintypes',
    'paprwall',
    'paprwall.core',
    'paprwall.gui',
    'paprwall.gui.wallpaper_manager_gui',
    'paprwall.cli',
    'paprwall.installer',
]

# Excluded modules to reduce size
excludes = [
    'matplotlib',
    'numpy',
    'scipy',
    'pandas',
    'jupyter',
    'IPython',
    'pytest',
    'unittest',
    'test',
    'tests',
    'setuptools',
    'distutils',
    'wheel',
    'pip',
]

# Main analysis
a = Analysis(
    [str(src_dir / 'paprwall' / 'gui' / 'wallpaper_manager_gui.py')],
    pathex=[str(src_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate files
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='paprwall-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windows GUI app (no console window)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=f'VERSION_INFO_{version.replace(".", "_")}',
    icon=str(assets_dir / 'paprwall-icon.ico') if (assets_dir / 'paprwall-icon.ico').exists() else None,
)

# Optional: Create a directory distribution instead of single file
# Uncomment the following lines if you want a directory build:
#
# exe = EXE(
#     pyz,
#     a.scripts,
#     [],
#     exclude_binaries=True,
#     name='paprwall-gui',
#     debug=False,
#     bootloader_ignore_signals=False,
#     strip=False,
#     upx=True,
#     console=False,
#     disable_windowed_traceback=False,
#     target_arch=None,
#     codesign_identity=None,
#     entitlements_file=None,
#     icon=str(assets_dir / 'paprwall-icon.ico') if (assets_dir / 'paprwall-icon.ico').exists() else None,
# )
#
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='paprwall'
# )
