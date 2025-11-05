# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/paprwall/gui/wallpaper_manager_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('README.md', '.'), ('LICENSE', '.')],
    hiddenimports=['PIL', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont', 'PIL.ImageTk', 'requests', 'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'paprwall', 'paprwall.core', 'paprwall.gui', 'paprwall.gui.wallpaper_manager_gui', 'paprwall.cli', 'paprwall.installer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'scipy', 'pandas', 'jupyter', 'IPython', 'pytest', 'unittest', 'setuptools', 'distutils'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='paprwall',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
