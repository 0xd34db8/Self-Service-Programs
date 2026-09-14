@echo off
echo Stopping SpoofDPI process inside WSL...
wsl -e bash -c "pkill -f spoofdpi" 2>nul

echo Disabling Windows Proxy...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /f 2>nul

echo.
echo SpoofDPI has been stopped and all proxy settings have been reverted.
pause