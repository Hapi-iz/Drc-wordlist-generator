@echo off
setlocal enabledelayedexpansion

echo ===========================================
echo     DRCWL Setup - Python & Rich Installer
echo ===========================================
echo.

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed.
    echo Do you want to install Python automatically? (Y/N)
    set /p installPython=
    if /I "%installPython%"=="Y" (
        echo Downloading Python Installer...
        powershell -Command "& {Start-BitsTransfer -Source 'https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe' -Destination 'python_installer.exe'}"
        
        echo Installing Python...
        start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
        del python_installer.exe
        
        echo Python installed successfully!
    ) else (
        echo Please install Python manually from https://www.python.org and re-run this script.
        exit /b
    )
)

:: Refresh environment variables
set PATH=%PATH%;C:\Python310\Scripts;C:\Python310\

:: Check if pip is installed
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo Pip is not installed.
    echo Do you want to install pip? (Y/N)
    set /p installPip=
    if /I "%installPip%"=="Y" (
        echo Installing pip...
        python -m ensurepip --default-pip
        python -m pip install --upgrade pip
        echo Pip installed successfully!
    ) else (
        echo Pip is required to install dependencies. Please install pip manually.
        exit /b
    )
)

:: Install Rich package
echo Installing Rich...
python -m pip install rich
if %errorlevel% neq 0 (
    echo Failed to install Rich. Please check your internet connection.
    exit /b
)
echo Rich installed successfully!

:: Create an alias for drcwl
echo Creating alias 'drcwl'...
(
    echo @echo off
    echo python3 drcwl %%*
) > "%USERPROFILE%\drcwl.bat"

:: Add alias to PATH
setx PATH "%USERPROFILE%" /M
if %errorlevel% neq 0 (
    echo Failed to create alias. Try manually adding '%USERPROFILE%' to your system PATH.
) else (
    echo Alias 'drcwl' created successfully!
)

echo ===========================================
echo         Setup Completed Successfully!
echo     You can now use 'drcwl' instead of 'python3 drcwl'
echo ===========================================
pause
