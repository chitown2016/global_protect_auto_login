@echo off
REM Launcher for the GlobalProtect auto-login script (MSI laptop = arg 2).
REM %~dp0 = the folder this .bat lives in, so it works even if moved with the project.
cd /d "%~dp0"
"%~dp0env\python.exe" main.py 2
if errorlevel 1 (
    echo.
    echo Script exited with an error. Press any key to close...
    pause >nul
)
