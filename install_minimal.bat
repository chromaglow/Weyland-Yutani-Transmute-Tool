@echo off
echo.
echo ========================================
echo  WEYLAND-YUTANI TRANSMUTE TOOL
echo  Easy Installation for Everyone!
echo ========================================
echo.
echo Don't worry if you're not technical!
echo This will install everything you need.
echo.
echo Just sit back and watch the magic happen...
echo.

REM Check if Python is installed
echo [1/6] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo ========================================
        echo  PYTHON NOT FOUND!
        echo ========================================
        echo.
        echo Python is required but not installed.
        echo.
        echo Please visit: https://python.org/downloads/
        echo Download and install Python 3.8 or newer.
        echo.
        echo Then run this installer again.
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
        echo ✓ Found Python via 'py' launcher
    )
) else (
    set PYTHON_CMD=python
    echo ✓ Found Python via 'python' command
)

echo.
echo [2/6] Upgrading pip (package installer)...
%PYTHON_CMD% -m pip install --upgrade pip --quiet

echo.
echo [3/6] Installing core mesh processing libraries...
echo        (This handles STL files and 3D geometry)
%PYTHON_CMD% -m pip install trimesh scipy networkx --quiet

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Core installation had issues, trying one at a time...
    %PYTHON_CMD% -m pip install trimesh --quiet
    %PYTHON_CMD% -m pip install scipy --quiet
    %PYTHON_CMD% -m pip install networkx --quiet
)

echo.
echo [4/6] Installing fast mesh simplification...
echo        (Makes complex models simpler and faster)
%PYTHON_CMD% -m pip install fast-simplification --quiet

echo.
echo [5/6] Installing audio system...
echo        (Adds background music and sound effects)
%PYTHON_CMD% -m pip install pygame --quiet

echo.
echo [6/6] Installing testing framework...
echo        (For quality assurance - optional but recommended)
%PYTHON_CMD% -m pip install pytest pytest-cov --quiet

echo.
echo ========================================
echo  INSTALLATION COMPLETE!
echo ========================================
echo.
echo 🎉 Everything is ready to go!
echo.
echo Next steps:
echo 1. Double-click: run_app.bat
echo 2. Enjoy your Weyland-Yutani experience!
echo.
echo If you see any errors above, don't worry!
echo The app will still work with basic features.
echo.
echo ========================================
echo  TECHNICAL SUMMARY
echo ========================================
echo.
echo Installed packages:
echo • trimesh      - 3D mesh processing
echo • scipy        - Scientific computing
echo • networkx     - Graph algorithms
echo • fast-simplification - Mesh optimization
echo • pygame       - Audio system
echo • pytest       - Testing framework
echo.
echo Your mesh repair tool is now fully equipped!
echo.

REM Test the installation
echo Testing installation...
%PYTHON_CMD% -c "import trimesh; print('✓ Mesh processing ready')" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Core functionality verified
) else (
    echo ⚠️  Some features may be limited
)

%PYTHON_CMD% -c "import pygame; print('✓ Audio system ready')" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Audio features available
) else (
    echo ⚠️  Audio features disabled
)

echo.
echo ========================================
echo  READY TO LAUNCH!
echo ========================================
echo.
pause
