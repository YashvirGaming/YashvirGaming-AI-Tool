@echo off
title GPT Desktop by Yashvir Gaming
set "SCRIPT=main.py"

if not exist %SCRIPT% (
    echo [!] %SCRIPT% not found in current directory.
    pause
    exit /b
)

python %SCRIPT%
pause
