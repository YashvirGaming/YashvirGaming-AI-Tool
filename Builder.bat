@echo off
title Yashvir Gaming Premium AI Tool
set "SCRIPT=main.py"
set "ICON=icon.ico"

if not exist %SCRIPT% (
    echo [!] %SCRIPT% not found in current directory.
    pause
    exit /b
)

python -m nuitka ^
--standalone ^
--onefile ^
--windows-disable-console ^
--enable-plugin=tk-inter ^
--windows-icon-from-ico=%ICON% ^
--output-filename=YashvirGaming_AI_Tool.exe ^
--jobs=14 ^
%SCRIPT%

echo.
echo [+] Build complete: YashvirGaming_AI_Tool.exe
pause
