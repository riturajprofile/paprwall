@echo off
REM PaprWall Windows Build Script
REM Builds standalone executable using PyInstaller

echo ========================================
echo PaprWall Windows Build Script
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "src\paprwall" (
    echo Error: Please run this script from the project root directory
    echo Expected to find: src\paprwall\
    pause
    exit /b 1
)

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist ".venv" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

REM Upgrade pip and install build dependencies
echo Installing/upgrading build dependencies...
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel
python -m pip install pyinstaller>=5.0

REM Install project dependencies
echo Installing project dependencies...
python -m pip install -r requirements.txt

REM Install project in development mode
echo Installing project in development mode...
python -m pip install -e .

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

REM Create build directory
mkdir build 2>nul

REM Build executable using PyInstaller
echo Building Windows executable...
pyinstaller scripts\paprwall.spec --clean --noconfirm

REM Check if build was successful
if not exist "dist\paprwall-gui.exe" (
    echo.
    echo ❌ Build failed: Executable not found
    echo Check the output above for errors
    pause
    exit /b 1
)

REM Get version information
for /f "tokens=*" %%a in ('python -c "from paprwall import __version__; print(__version__)"') do set VERSION=%%a

REM Create release directory
set RELEASE_DIR=release-v%VERSION%
echo Creating release package: %RELEASE_DIR%
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"

REM Copy executable and required files
copy "dist\paprwall-gui.exe" "%RELEASE_DIR%\"
if exist "README.md" copy "README.md" "%RELEASE_DIR%\"
if exist "LICENSE" copy "LICENSE" "%RELEASE_DIR%\" 

REM Create installation scripts
echo Creating installation scripts...

REM Create installer batch script
(
echo @echo off
echo REM PaprWall Windows Installer
echo.
echo echo ================================================================
echo echo   PaprWall Installation
echo echo ================================================================
echo echo.
echo echo This will install PaprWall to your system and create:
echo echo   - Start Menu shortcut
echo echo   - Desktop shortcut
echo echo   - Uninstaller
echo echo.
echo pause
echo.
echo "%%~dp0paprwall-gui.exe" --install
echo if %%ERRORLEVEL%% equ 0 ^(
echo     echo.
echo     echo Installation completed! You can now close this window.
echo     pause
echo ^) else ^(
echo     echo.
echo     echo ❌ Installation failed. Check the messages above.
echo     pause
echo     exit /b 1
echo ^)
) > "%RELEASE_DIR%\INSTALL.bat"

REM Create uninstaller batch script
(
echo @echo off
echo REM PaprWall Windows Uninstaller
echo.
echo echo Uninstalling PaprWall...
echo "%%~dp0paprwall-gui.exe" --uninstall
echo if %%ERRORLEVEL%% equ 0 ^(
echo     echo.
echo     echo ✓ PaprWall uninstalled successfully!
echo ^) else ^(
echo     echo.
echo     echo ❌ Uninstallation failed or PaprWall was not installed.
echo ^)
echo.
echo pause
) > "%RELEASE_DIR%\UNINSTALL.bat"

REM Create simple run script
(
echo @echo off
echo REM Run PaprWall
echo "%%~dp0paprwall-gui.exe"
) > "%RELEASE_DIR%\run.bat"

REM Create README for release
(
echo # PaprWall v%VERSION% - Windows Release
echo.
echo ## Quick Start
echo.
echo ### Option 1: Install to System ^(Recommended^)
echo 1. Double-click `INSTALL.bat`
echo 2. Follow the prompts
echo 3. Launch from Desktop shortcut or Start Menu
echo.
echo ### Option 2: Portable Mode
echo 1. Double-click `paprwall-gui.exe`
echo 2. Use without installation
echo.
echo ## What Gets Installed?
echo.
echo When you run `INSTALL.bat`, PaprWall will create:
echo - ✅ **Desktop Shortcut** - Quick launch from your desktop
echo - ✅ **Start Menu Entry** - Find in Start Menu ^> PaprWall
echo - ✅ **Uninstaller** - Easy removal via Start Menu or Programs folder
echo - ✅ **Program Files** - Copied to `%LOCALAPPDATA%\Programs\PaprWall`
echo.
echo ## Files Included
echo.
echo - `paprwall-gui.exe` - Main application ^(portable^)
echo - `INSTALL.bat` - System installer ^(creates shortcuts^)
echo - `UNINSTALL.bat` - System uninstaller
echo - `run.bat` - Simple launcher
echo - `README.md` - This file
echo - `LICENSE` - License information
echo.
echo ## System Requirements
echo.
echo - Windows 10 ^(1809+^) or Windows 11
echo - Display: 720p or higher recommended
echo - Internet connection for downloading wallpapers
echo.
echo ## Usage After Installation
echo.
echo 1. Launch from Desktop or Start Menu
echo 2. Select a quote category
echo 3. Click "Random" or "Refresh"
echo 4. Click "Set Wallpaper"
echo 5. Enable auto-rotate if desired
echo.
echo ## Uninstallation
echo.
echo - **From Start Menu**: Start ^> PaprWall ^> Uninstall PaprWall
echo - **From Programs Folder**: Run `UNINSTALL.bat` in the installation directory
echo - **Manual**: Run the included `UNINSTALL.bat` script
echo.
echo ## Support
echo.
echo - Issues: https://github.com/riturajprofile/paprwall/issues
echo - Documentation: https://github.com/riturajprofile/paprwall
echo.
echo ---
echo Built on %DATE% %TIME%
) > "%RELEASE_DIR%\README.md"

REM Calculate file sizes and create manifest
echo Creating build manifest...
for %%f in ("%RELEASE_DIR%\*") do echo %%~nxf - %%~zf bytes >> "%RELEASE_DIR%\FILES.txt"

REM Create ZIP archive
echo Creating ZIP archive...
set ZIP_NAME=paprwall-v%VERSION%-windows-x64.zip
if exist "%ZIP_NAME%" del "%ZIP_NAME%"

REM Use PowerShell to create ZIP (available on Windows 10/11)
powershell -Command "Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_NAME%' -CompressionLevel Optimal"

if exist "%ZIP_NAME%" (
    echo ✓ Created: %ZIP_NAME%
) else (
    echo ❌ Failed to create ZIP archive
)

REM Calculate checksums
echo Calculating checksums...
powershell -Command "Get-FileHash '%ZIP_NAME%' -Algorithm SHA256 | Select-Object Hash | ForEach-Object { $_.Hash }" > "%ZIP_NAME%.sha256"
powershell -Command "Get-FileHash 'dist\paprwall-gui.exe' -Algorithm SHA256 | Select-Object Hash | ForEach-Object { $_.Hash }" > "paprwall-gui.exe.sha256"

REM Display build summary
echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Version: %VERSION%
echo.
echo Files created:
echo   📁 %RELEASE_DIR%\               - Release directory
echo   📦 %ZIP_NAME%                   - Distribution package
echo   🔒 %ZIP_NAME%.sha256            - Package checksum
echo   ⚡ dist\paprwall-gui.exe        - Standalone executable
echo   🔒 paprwall-gui.exe.sha256      - Executable checksum
echo.

REM Get file sizes
for %%f in ("dist\paprwall-gui.exe") do echo Executable size: %%~zf bytes
for %%f in ("%ZIP_NAME%") do echo Package size: %%~zf bytes

echo.
echo 🎉 Ready for distribution!
echo.
echo To test the build:
echo   1. Navigate to %RELEASE_DIR%\
echo   2. Run paprwall-gui.exe (portable mode)
echo.
echo To test installation (creates Desktop + Start Menu shortcuts):
echo   1. Run %RELEASE_DIR%\INSTALL.bat
echo   2. Check Desktop for PaprWall shortcut
echo   3. Check Start Menu ^> PaprWall
echo.
echo Distribution package includes:
echo   • Portable executable (no installation needed)
echo   • INSTALL.bat (creates Desktop + Start Menu shortcuts)
echo   • UNINSTALL.bat (removes all shortcuts)
echo.
pause
