@echo off
REM Weyland-Yutani Transmute Tool - FreeCAD Compatible Launcher
REM This script runs the application with FreeCAD's Python 3.11 to avoid DLL conflicts

echo ============================================================
echo 🏢 Weyland-Yutani Transmute Tool
echo    'Building Better Worlds... One Mesh at a Time'
echo ============================================================
echo.
echo 🔧 Using FreeCAD's Python 3.11 to avoid version conflicts...
echo.

REM Set the path to FreeCAD's Python
set FREECAD_PYTHON="C:\Program Files\FreeCAD 1.0\bin\python.exe"

REM Check if FreeCAD Python exists
if not exist %FREECAD_PYTHON% (
    echo ❌ ERROR: FreeCAD Python not found at %FREECAD_PYTHON%
    echo    Please verify FreeCAD 1.0 is installed correctly
    pause
    exit /b 1
)

REM Run the application with FreeCAD's Python
echo 🚀 Starting application...
%FREECAD_PYTHON% src/main.py

echo.
echo ✨ Application finished!
pause