@echo off
REM PaprWall Uninstall Script for Windows

echo ==========================================
echo   PaprWall Uninstaller
echo ==========================================
echo.

REM Check if paprwall is installed
set "INSTALL_DIR=%LOCALAPPDATA%\Programs\PaprWall"
set "DATA_DIR=%APPDATA%\PaprWall"

if not exist "%INSTALL_DIR%\paprwall-gui.exe" (
    echo WARNING: PaprWall doesn't appear to be installed at:
    echo   %INSTALL_DIR%
    echo.
    set /p REMOVE_DATA="Remove data files anyway? (Y/N): "
    if /i not "%REMOVE_DATA%"=="Y" (
        echo Cancelled.
        pause
        exit /b 0
    )
) else (
    echo Found PaprWall installation
    echo.
    echo This will remove:
    echo   * Application files (%INSTALL_DIR%^)
    echo   * Start Menu shortcut
    echo   * Desktop shortcut (if exists^)
    echo   * Configuration and data files
    echo.
    set /p CONTINUE="Continue with uninstall? (Y/N): "
    if /i not "%CONTINUE%"=="Y" (
        echo Cancelled.
        pause
        exit /b 0
    )
)

echo.
echo Uninstalling PaprWall...
echo.

REM Remove installation directory
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
    echo [OK] Removed application files
)

REM Remove Start Menu shortcut
set "SHORTCUT_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if exist "%SHORTCUT_DIR%\PaprWall.lnk" (
    del "%SHORTCUT_DIR%\PaprWall.lnk"
    echo [OK] Removed Start Menu shortcut
)

REM Remove Desktop shortcut (if exists)
if exist "%USERPROFILE%\Desktop\PaprWall.lnk" (
    del "%USERPROFILE%\Desktop\PaprWall.lnk"
    echo [OK] Removed Desktop shortcut
)

REM Ask about data files
echo.
set /p REMOVE_DATA="Remove configuration and wallpaper data? (Y/N): "
if /i "%REMOVE_DATA%"=="Y" (
    if exist "%DATA_DIR%" (
        echo.
        echo Data to be removed:
        dir "%DATA_DIR%" /s 2>nul | find "File(s)"
        echo Location: %DATA_DIR%
        echo.
        set /p CONFIRM="Confirm deletion? (Y/N): "
        if /i "%CONFIRM%"=="Y" (
            rmdir /s /q "%DATA_DIR%"
            echo [OK] Removed data directory
        ) else (
            echo [SKIP] Kept data directory
        )
    )
) else (
    echo [SKIP] Kept data files (wallpapers and history^)
    echo   Location: %DATA_DIR%
)

echo.
echo ==========================================
echo   Uninstall Complete
echo ==========================================
echo.
echo PaprWall has been removed from your system.
echo.
echo If you installed via pip, also run:
echo   pip uninstall paprwall
echo.
pause
