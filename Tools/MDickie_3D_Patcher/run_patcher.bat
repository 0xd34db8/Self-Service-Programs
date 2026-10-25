@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ================================================================
echo           MDickie 3D Universe Universal 1-Click Patcher
echo ================================================================
echo.

:: Scan directory for an input .apks file (skipping previous outputs)
set "INPUT_APKS="
for %%f in (*.apks) do (
    set "FNAME=%%~nf"
    if /i not "!FNAME:~-9!"=="-unlocked" (
        if /i not "!FNAME:~-7!"=="-modded" (
            set "INPUT_APKS=%%~ff"
            set "BASE_NAME=%%~nf"
            goto :found
        )
    )
)

:found
if "%INPUT_APKS%"=="" (
    echo [!] No input .apks file was found in this folder!
    echo.
    echo Instructions:
    echo   1. Copy your original .apks file into this folder.
    echo   2. Double-click run_patcher.bat again.
    echo.
    pause
    exit /b 1
)

set "OUTPUT_APKS=%~dp0!BASE_NAME!-unlocked.apks"

echo [*] Detected input:  %INPUT_APKS%
echo [*] Target output:   !OUTPUT_APKS!
echo.
echo [*] Starting patcher pipeline...
echo.

python "%~dp0patcher.py" "!INPUT_APKS!" -o "!OUTPUT_APKS!"

if errorlevel 1 (
    echo.
    echo [-] An error occurred during patching! See above output.
) else (
    echo.
    echo ================================================================
    echo [✓] SUCCESS!
    echo Unlocked package ready at:
    echo   !OUTPUT_APKS!
    echo.
    echo You can now install it on your device alongside the original.
    echo ================================================================
)

echo.
pause
