[Setup]
AppName=AppBlocker
AppVersion=2.1
DefaultDirName={localappdata}\AppBlocker
DefaultGroupName=AppBlocker
OutputDir=installer_output
OutputBaseFilename=AppBlockerSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=MainIcon.ico

[Files]
Source: "dist\AppBlocker.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\AppBlockerWatchdog.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\appBlockerIconImage.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\appBlockerKeyImage.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "MainIcon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AppBlocker"; Filename: "{app}\AppBlocker.exe"
Name: "{commondesktop}\AppBlocker"; Filename: "{app}\AppBlocker.exe"

[Run]
Filename: "{sys}\ie4uinit.exe"; Parameters: "-ClearIconCache"; Flags: runhidden skipifdoesntexist; StatusMsg: "Refreshing icon cache..."
Filename: "{app}\AppBlocker.exe"; Description: "Launch AppBlocker"; Flags: postinstall nowait skipifsilent
