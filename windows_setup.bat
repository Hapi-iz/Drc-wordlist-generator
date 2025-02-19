@echo off
setlocal enabledelayedexpansion

echo ===========================================
echo     DRCWL Setup - Python & Rich Installer
echo ===========================================
echo.

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Attempting to install...
    powershell -Command "Start-Process msiexec.exe -ArgumentList '/i https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe /quiet InstallAllUsers=1 PrependPath=1' -Wait -NoNewWindow"
    if %errorlevel% neq 0 (
        echo Failed to install Python automatically. Please install it manually from https://www.python.org
        exit /b
    ) else (
        echo Python installed successfully!
    )
)

:: Refresh environment variables
set PATH=%PATH%;C:\Python310\Scripts;C:\Python310\

:: Check if pip is installed
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo Pip is not installed. Attempting to install...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
)

:: Install Rich
echo Installing Rich...
python -m pip install rich

:: Create an alias for drcwl
setx drcwl "python3 drcwl" /M
if %errorlevel% neq 0 (
    echo Failed to create alias. Try manually adding 'drcwl' in your environment variables.
) else (
    echo Alias 'drcwl' created successfully!
)

echo ===========================================
echo         Setup Completed Successfully!
echo     You can now use 'drcwl' instead of 'python3 drcwl'
echo ===========================================
pause
