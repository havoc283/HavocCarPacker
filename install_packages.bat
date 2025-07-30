@echo off
setlocal

echo Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.4 or newer and ensure 'python' is in your PATH.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%a in ('python --version') do set PYVER=%%a
echo Detected Python version %PYVER%

for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set PYMAJOR=%%a
    set PYMINOR=%%b
)

if %PYMAJOR% LSS 3 (
    echo ERROR: Python 3.4 or newer is required.
    pause
    exit /b 1
) else if %PYMAJOR%==3 if %PYMINOR% LSS 4 (
    echo ERROR: Python 3.4 or newer is required.
    pause
    exit /b 1
)

echo Python version OK.

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing ttkbootstrap...
pip install ttkbootstrap

echo.
echo All done!
pause
endlocal