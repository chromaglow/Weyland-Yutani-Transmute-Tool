@echo off
echo.
echo ========================================
echo  Weyland-Yutani Transmute Tool
echo  "Building Better Worlds..."
echo ========================================
echo.

REM Try different methods to run
echo Launching application...
echo.

REM Method 1: python
python src/main.py
if %errorlevel% equ 0 exit /b 0

REM Method 2: py
py src/main.py
if %errorlevel% equ 0 exit /b 0

REM Method 3: Direct path
C:\Users\ezrashiv\AppData\Local\Python\pythoncore-3.14-64\python.exe src/main.py
if %errorlevel% equ 0 exit /b 0

echo.
echo ========================================
echo  ERROR: Could not launch application
echo ========================================
echo.
echo Please try manually:
echo   python src/main.py
echo.
pause
