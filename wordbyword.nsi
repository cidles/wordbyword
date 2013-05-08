; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "WordByWord"

; The file to write
OutFile "setup-wordbyword.exe"

; The default installation directory
InstallDir $PROGRAMFILES\WordByWord

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\PB_WordByWord" "Install_Dir"

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "WordByWord (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /r "dist_win\*"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\PB_WordByWord "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WordByWord" "DisplayName" "WordByWord"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WordByWord" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WordByWord" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WordByWord" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\WordByWord"
  CreateShortCut "$SMPROGRAMS\WordByWord\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\WordByWord\WordByWord.lnk" "$INSTDIR\wordbyword.exe" "" "$INSTDIR\wordbyword.exe" 0
  CreateShortCut "$SMPROGRAMS\WordByWord\WordByWord - Aprendar Minderico.lnk" "$INSTDIR\wordbyword.exe" "courses\pt-mind.yml" "$INSTDIR\wordbyword.exe" 0
  CreateShortCut "$SMPROGRAMS\WordByWord\WordByWord - Portugiesisch lernen.lnk" "$INSTDIR\wordbyword.exe" "courses\de-pt.yml" "$INSTDIR\wordbyword.exe" 0
  CreateShortCut "$SMPROGRAMS\WordByWord\WordByWord - Russisch lernen.lnk" "$INSTDIR\wordbyword.exe" "courses\de-ru.yml" "$INSTDIR\wordbyword.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WordByWord"
  DeleteRegKey HKLM SOFTWARE\PB_WordByWord

  ; Remove files and uninstaller
  Delete $INSTDIR\*
  ;Delete $INSTDIR\uninstall.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\WordByWord\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\WordByWord"
  RMDir "$INSTDIR"

SectionEnd
