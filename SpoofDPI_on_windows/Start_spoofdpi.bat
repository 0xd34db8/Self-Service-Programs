@echo off
echo Fetching WSL IP address...
for /f "tokens=1" %%i in ('wsl hostname -I') do set WSL_IP=%%i
echo Found WSL IP: %WSL_IP%

echo Enabling Windows Proxy for SpoofDPI...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "%WSL_IP%:8080" /f

echo Starting SpoofDPI via WSL...
start "SpoofDPI (WSL)" wsl -e bash -c "/usr/local/bin/spoofdpi --listen-addr 0.0.0.0:8080 --dns-mode https --https-chunk-size 2"

echo Proxy enabled. SpoofDPI is running in a new window.
echo Note: If your browser does not route traffic immediately, restart the browser.
pause