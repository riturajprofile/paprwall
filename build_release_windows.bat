@echo off
REM PaprWall v1.0.2 Windows Release Build Script

echo ==========================================
echo   PaprWall v1.0.2 Windows Builder
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ from python.org
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv-build" (
    echo Creating build virtual environment...
    python -m venv .venv-build
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv-build\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip wheel setuptools

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec
if exist "src\paprwall.egg-info" rmdir /s /q src\paprwall.egg-info

REM Create version file
echo Creating version info...
(
echo """Version information for PaprWall."""
echo __version__ = "1.0.2"
echo __author__ = "riturajprofile"
echo __description__ = "Modern Desktop Wallpaper Manager"
) > src\paprwall\__version__.py

REM Build GUI application with PyInstaller
echo Building GUI application for Windows...
pyinstaller --name=paprwall-gui ^
    --onefile ^
    --windowed ^
    --icon=assets\icon.ico ^
    --add-data="src\paprwall;paprwall" ^
    --hidden-import=PIL._tkinter_finder ^
    src\paprwall\gui\wallpaper_manager_gui.py

REM Create release directory
set RELEASE_DIR=release-v1.0.2-windows
if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"

REM Copy binary
echo Copying binary to release directory...
copy dist\paprwall-gui.exe "%RELEASE_DIR%\"

REM Copy documentation
echo Copying documentation...
copy README.md "%RELEASE_DIR%\"
copy LICENSE "%RELEASE_DIR%\"
copy CHANGELOG.md "%RELEASE_DIR%\"

REM Copy icon file
echo Copying application icon...
if exist "assets\paprwall-icon.svg" (
    copy assets\paprwall-icon.svg "%RELEASE_DIR%\paprwall.svg"
    echo Icon copied
) else (
    echo Warning: Icon file not found
)

REM Copy uninstall script
echo Copying uninstall script...
if exist "uninstall_windows.bat" (
    copy uninstall_windows.bat "%RELEASE_DIR%\UNINSTALL.bat"
    echo Uninstall script copied
) else (
    echo Warning: Uninstall script not found
)
) else (
    echo Warning: Icon file not found
)

REM Create installation script
echo Creating installation script...
(
echo @echo off
echo echo ==========================================
echo echo   Installing PaprWall v1.0.2
echo echo ==========================================
echo echo.
echo.
echo REM Check if running with admin rights
echo net session ^>nul 2^>^&1
echo if %%errorlevel%% == 0 (
echo     echo WARNING: Running as administrator
echo     echo It's recommended to install for current user only
echo     echo.
echo ^)
echo.
echo REM Get installation directory
echo set "INSTALL_DIR=%%LOCALAPPDATA%%\Programs\PaprWall"
echo.
echo REM Create installation directory
echo if not exist "%%INSTALL_DIR%%" mkdir "%%INSTALL_DIR%%"
echo.
echo REM Copy executable
echo echo Installing PaprWall...
echo copy paprwall-gui.exe "%%INSTALL_DIR%%\"
echo.
echo REM Create data directory and copy resources
echo set "DATA_DIR=%%APPDATA%%\PaprWall"
echo if not exist "%%DATA_DIR%%" mkdir "%%DATA_DIR%%"
echo if exist "UNINSTALL.bat" copy UNINSTALL.bat "%%DATA_DIR%%\"
echo if exist "paprwall.svg" copy paprwall.svg "%%DATA_DIR%%\"
echo.
echo REM Create Start Menu shortcut
echo set "SHORTCUT_DIR=%%APPDATA%%\Microsoft\Windows\Start Menu\Programs"
echo powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%%SHORTCUT_DIR%%\PaprWall.lnk'^); $Shortcut.TargetPath = '%%INSTALL_DIR%%\paprwall-gui.exe'; $Shortcut.Description = 'Modern Desktop Wallpaper Manager'; $Shortcut.Save(^)"
echo.
echo REM Create Desktop shortcut (optional^)
echo set /p CREATE_DESKTOP="Create desktop shortcut? (Y/N): "
echo if /i "%%CREATE_DESKTOP%%"=="Y" (
echo     powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%%USERPROFILE%%\Desktop\PaprWall.lnk'^); $Shortcut.TargetPath = '%%INSTALL_DIR%%\paprwall-gui.exe'; $Shortcut.Description = 'Modern Desktop Wallpaper Manager'; $Shortcut.Save(^)"
echo     echo Desktop shortcut created!
echo ^)
echo.
echo echo.
echo echo ==========================================
echo echo   Installation Complete!
echo echo ==========================================
echo echo.
echo echo PaprWall has been installed to:
echo echo   %%INSTALL_DIR%%
echo echo.
echo echo You can now:
echo echo   1. Find "PaprWall" in Start Menu
echo echo   2. Run: %%INSTALL_DIR%%\paprwall-gui.exe
echo echo.
echo echo To uninstall later, run:
echo echo   %%APPDATA%%\PaprWall\UNINSTALL.bat
echo echo.
echo pause
) > "%RELEASE_DIR%\INSTALL.bat"

REM Create a ZIP file
echo Creating release archive...
powershell -Command "Compress-Archive -Path '%RELEASE_DIR%' -DestinationPath 'paprwall-v1.0.2-windows-x64.zip' -Force"

REM Generate checksum
echo Generating checksum...
powershell -Command "Get-FileHash 'paprwall-v1.0.2-windows-x64.zip' -Algorithm SHA256 | Select-Object -ExpandProperty Hash > paprwall-v1.0.2-windows-x64.zip.sha256"

REM Summary
echo.
echo ==========================================
echo   Build Complete! ✓
echo ==========================================
echo.
echo Release package: paprwall-v1.0.2-windows-x64.zip
echo Release directory: %RELEASE_DIR%\
echo.
echo Contents:
dir "%RELEASE_DIR%" /b
echo.
echo To test the build:
echo   cd %RELEASE_DIR%
echo   INSTALL.bat
echo.

pause
