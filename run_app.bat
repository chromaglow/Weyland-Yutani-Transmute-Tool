@echo off
echo.
echo ========================================
echo  WEYLAND-YUTANI TRANSMUTE TOOL
echo  Launching Application...
echo ========================================
echo.
echo "Building Better Worlds... One Mesh at a Time"
echo.

REM Try different methods to run
echo Starting the transmutation sequence...
echo.

REM Method 1: python
python src/main.py
if %errorlevel% equ 0 goto :success

REM Method 2: py launcher
py src/main.py
if %errorlevel% equ 0 goto :success

REM Method 3: python3
python3 src/main.py
if %errorlevel% equ 0 goto :success

echo.
echo ========================================
echo  LAUNCH ERROR
echo ========================================
echo.
echo Could not start the application automatically.
echo.
echo Please try one of these manually:
echo   python src/main.py
echo   py src/main.py
echo   python3 src/main.py
echo.
echo Make sure Python is installed and in your PATH.
echo.
pause
exit /b 1

:success
echo.
echo ========================================
echo  APPLICATION CLOSED
echo ========================================
echo.
echo Thanks for using Weyland-Yutani Transmute Tool!
echo.
pause