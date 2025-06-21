[Setup]
AppName=Moaz Video Downloader
AppVersion=1.0
DefaultDirName={pf}\MoazVideoDownloader
DefaultGroupName=Moaz Video Downloader
OutputDir=dist
OutputBaseFilename=MoazVideoDownloaderSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "E:\Moaz3\dist\Moaz Downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Moaz Video Downloader"; Filename: "{app}\Moaz Downloader.exe"
Name: "{group}\Uninstall Moaz Video Downloader"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Moaz Video Downloader"; Filename: "{app}\Moaz Downloader.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\Moaz Downloader.exe"; Description: "Launch Moaz Video Downloader"; Flags: nowait postinstall skipifsilent