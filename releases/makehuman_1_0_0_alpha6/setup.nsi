Name Makehuman
OutFile setup.exe
LicenseData license.txt

InstallDir $PROGRAMFILES\Makehuman

Page license
Page directory
Page instfiles

Section "Copy files"

  # Copy root files
  SetOutPath $INSTDIR
  File makehuman.exe
  # File mh.pyd
  File *.dll
  File main.py
  File license.txt
  File proxy.cfg

  # Copy data files
  SetOutPath $INSTDIR\data
  File /r /x .svn data\*.*  

  # Copy importers
  SetOutPath $INSTDIR\importers
  File /r /x .svn /x .pyc importers\*.*
  
  # Copy docs
  SetOutPath $INSTDIR\docs
  File /r /x .svn docs\*.pdf

  # Copy python files
  SetOutPath $INSTDIR\core
  File /r /x .svn /x .pyc core\*.py
  SetOutPath $INSTDIR\pythonmodules
  File /r /x .svn pythonmodules\*.pyc
  SetOutPath $INSTDIR\plugins
  File /r /x .svn /x .pyc plugins\*.py
  SetOutPath $INSTDIR\shared
  File /r /x .svn /x .pyc shared\*.*
   SetOutPath $INSTDIR\apps
  File /r /x .svn /x .pyc apps\*.py
  
  CreateDirectory $INSTDIR\models
  CreateDirectory $INSTDIR\exports
  CreateDirectory $INSTDIR\backgrounds
  
SectionEnd

Section "Create uninstaller"
  
  WriteUninstaller $INSTDIR\Uninst.exe
  
SectionEnd

Section "Create shortcuts"

  CreateDirectory "$SMPROGRAMS\Makehuman"
  SetOutPath $INSTDIR
  CreateShortCut "$SMPROGRAMS\Makehuman\Makehuman.lnk" "$INSTDIR\makehuman.exe" \
    "" "$INSTDIR\makehuman.exe" 0 SW_SHOWNORMAL ""  "Makehuman"
  CreateShortCut "$SMPROGRAMS\Makehuman\Uninstall.lnk" "$INSTDIR\Uninst.exe" \
    "" "$INSTDIR\Uninst.exe" 0 SW_SHOWNORMAL ""  "Uninstall Makehuman"
    
SectionEnd

Section "Uninstall"

  # Remove Makehuman files
  Delete $INSTDIR\makehuman.exe
  Delete $INSTDIR\mh.pyd
  Delete $INSTDIR\*.dll
  Delete $INSTDIR\main.py
  Delete $INSTDIR\license.txt
  
  # Remove Makehuman data folders
  RMDir /r $INSTDIR\apps
  RMDir /r $INSTDIR\data
  RMDir /r $INSTDIR\docs
  RMDir /r $INSTDIR\core
  RMDir /r $INSTDIR\plugins
  RMDir /r $INSTDIR\shared
  RMDir /r $INSTDIR\pythonmodules
  RMDir /r $INSTDIR\importers
  
  # Remove uninstaller
  Delete $INSTDIR\Uninst.exe
  
  # Remove remaining Makehuman folders if empty
  RMDir $INSTDIR\models
  RMDir $INSTDIR\exports
  RMDir $INSTDIR\backgrounds  
  RMDir $INSTDIR
  
  # Remove shortcuts
  Delete $SMPROGRAMS\Makehuman\Makehuman.lnk
  Delete $SMPROGRAMS\Makehuman\Uninstall.lnk
  RMDir $SMPROGRAMS\Makehuman
  
SectionEnd