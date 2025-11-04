; PaprWall NSIS Installer Script
; Requires NSIS 3.0+ (https://nsis.sourceforge.io/)

;--------------------------------
; Includes
!include "MUI2.nsh"
!include "FileFunc.nsh"

;--------------------------------
; Configuration
!define PRODUCT_NAME "PaprWall"
!define PRODUCT_VERSION "1.0.2"
!define PRODUCT_PUBLISHER "riturajprofile"
!define PRODUCT_WEB_SITE "https://github.com/riturajprofile/paprwall"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "paprwall-setup-1.0.2-win64.exe"
InstallDir "$LOCALAPPDATA\Programs\${PRODUCT_NAME}"
InstallDirRegKey HKCU "Software\${PRODUCT_NAME}" "InstallDir"
RequestExecutionLevel user

;--------------------------------
; Modern UI Configuration
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_WELCOMEPAGE_TITLE "Welcome to ${PRODUCT_NAME} Setup"
!define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of ${PRODUCT_NAME}.$\r$\n$\r$\n${PRODUCT_NAME} is a modern desktop wallpaper manager with motivational quotes.$\r$\n$\r$\nClick Next to continue."
!define MUI_FINISHPAGE_RUN "$INSTDIR\paprwall-gui.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch ${PRODUCT_NAME}"

;--------------------------------
; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

;--------------------------------
; Installer Sections
Section "Main Application" SecMain
    SetOutPath "$INSTDIR"
    
    ; Copy files
    File "dist\paprwall-gui.exe"
    File "assets\paprwall-icon.svg"
    File "LICENSE"
    File "README.md"
    File "CHANGELOG.md"
    
    ; Create data directory
    CreateDirectory "$APPDATA\PaprWall"
    
    ; Create Start Menu shortcut
    CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
    CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\paprwall-gui.exe" "" "$INSTDIR\paprwall-icon.svg"
    CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
    
    ; Optional Desktop shortcut
    MessageBox MB_YESNO "Create Desktop shortcut?" IDYES desktop IDNO +2
    desktop:
        CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\paprwall-gui.exe" "" "$INSTDIR\paprwall-icon.svg"
    
    ; Write uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    ; Write registry keys
    WriteRegStr HKCU "Software\${PRODUCT_NAME}" "InstallDir" "$INSTDIR"
    WriteRegStr HKCU "Software\${PRODUCT_NAME}" "Version" "${PRODUCT_VERSION}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\paprwall-gui.exe"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKCU "${PRODUCT_UNINST_KEY}" "EstimatedSize" "$0"
SectionEnd

;--------------------------------
; Uninstaller Section
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\paprwall-gui.exe"
    Delete "$INSTDIR\paprwall-icon.svg"
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\CHANGELOG.md"
    Delete "$INSTDIR\uninstall.exe"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk"
    Delete "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk"
    RMDir "$SMPROGRAMS\${PRODUCT_NAME}"
    Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
    
    ; Remove installation directory
    RMDir "$INSTDIR"
    
    ; Ask about user data
    MessageBox MB_YESNO "Remove wallpaper data and configuration?$\r$\n$\r$\nLocation: $APPDATA\PaprWall" IDYES removedata IDNO +3
    removedata:
        RMDir /r "$APPDATA\PaprWall"
        Goto +2
    MessageBox MB_OK "User data preserved at:$\r$\n$APPDATA\PaprWall"
    
    ; Remove registry keys
    DeleteRegKey HKCU "${PRODUCT_UNINST_KEY}"
    DeleteRegKey HKCU "Software\${PRODUCT_NAME}"
    
    MessageBox MB_OK "${PRODUCT_NAME} has been uninstalled."
SectionEnd

;--------------------------------
; Section Descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} "Install ${PRODUCT_NAME} application files."
!insertmacro MUI_FUNCTION_DESCRIPTION_END
