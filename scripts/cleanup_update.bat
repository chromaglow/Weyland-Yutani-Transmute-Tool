@echo off
REM ============================================================================
REM  WEYLAND-YUTANI TRANSMUTE TOOL - CLEANUP & UPDATE SCRIPT
REM  Comprehensive cleanup and update of all files in root folder
REM ============================================================================

echo.
echo ============================================================================
echo   WEYLAND-YUTANI TRANSMUTE TOOL - CLEANUP & UPDATE
echo ============================================================================
echo.
echo This script will:
echo   1. Clean up temporary and cache files
echo   2. Update Python dependencies
echo   3. Organize project files
echo   4. Remove unnecessary files
echo.
echo WARNING: This will modify your project structure!
echo Make sure to commit any important changes first.
echo.
pause
echo.

REM ============================================================================
REM  STEP 1: CLEAN UP TEMPORARY AND CACHE FILES
REM ============================================================================

echo.
echo ============================================================================
echo STEP 1: Cleaning up temporary and cache files...
echo ============================================================================
echo.

echo Removing Python cache files...
if exist "__pycache__" (
    rmdir /s /q "__pycache__" 2>nul
    echo   [OK] Removed __pycache__
)

if exist "src\__pycache__" (
    rmdir /s /q "src\__pycache__" 2>nul
    echo   [OK] Removed src\__pycache__
)

if exist "src\core\__pycache__" (
    rmdir /s /q "src\core\__pycache__" 2>nul
    echo   [OK] Removed src\core\__pycache__
)

if exist "src\ui\__pycache__" (
    rmdir /s /q "src\ui\__pycache__" 2>nul
    echo   [OK] Removed src\ui\__pycache__
)

if exist "src\utils\__pycache__" (
    rmdir /s /q "src\utils\__pycache__" 2>nul
    echo   [OK] Removed src\utils\__pycache__
)

if exist "tests\__pycache__" (
    rmdir /s /q "tests\__pycache__" 2>nul
    echo   [OK] Removed tests\__pycache__
)

echo Removing .pyc files...
del /s /q *.pyc 2>nul
if %errorlevel% equ 0 echo   [OK] Removed .pyc files

echo Removing .pyo files...
del /s /q *.pyo 2>nul
if %errorlevel% equ 0 echo   [OK] Removed .pyo files

echo Removing temporary files...
del /s /q *.tmp 2>nul
del /s /q *.temp 2>nul
del /s /q *.bak 2>nul
if %errorlevel% equ 0 echo   [OK] Removed temporary files

echo Removing OS generated files...
del /q Thumbs.db 2>nul
del /q desktop.ini 2>nul
del /q .DS_Store 2>nul
if %errorlevel% equ 0 echo   [OK] Removed OS files

echo.

REM ============================================================================
REM  STEP 2: UPDATE PYTHON DEPENDENCIES
REM ============================================================================

echo.
echo ============================================================================
echo STEP 2: Updating Python dependencies...
echo ============================================================================
echo.

echo Updating pip...
python -m pip install --upgrade pip
echo.

echo Installing/updating core dependencies...
python -m pip install --upgrade trimesh scipy numpy networkx
echo.

echo Installing/updating development dependencies...
python -m pip install --upgrade pytest pytest-cov
echo.

REM ============================================================================
REM  STEP 3: ORGANIZE PROJECT FILES
REM ============================================================================

echo.
echo ============================================================================
echo STEP 3: Organizing project files...
echo ============================================================================
echo.

echo Running Python organization script...
python scripts\organize_project.py
echo.

REM ============================================================================
REM  STEP 4: CLEAN UP REDUNDANT FILES
REM ============================================================================

echo.
echo ============================================================================
echo STEP 4: Cleaning up redundant files...
echo ============================================================================
echo.

echo Removing old batch files that are no longer needed...
if exist "install_simple.bat" (
    del "install_simple.bat"
    echo   [OK] Removed install_simple.bat
)

if exist "install_dependencies.bat" (
    del "install_dependencies.bat"
    echo   [OK] Removed install_dependencies.bat
)

echo Removing duplicate documentation files...
if exist "docs\INSTALLATION.md" (
    if exist "docs\user\INSTALLATION.md" (
        del "docs\INSTALLATION.md"
        echo   [OK] Removed duplicate docs\INSTALLATION.md
    )
)

if exist "docs\README.md" (
    if exist "docs\user\README.md" (
        del "docs\README.md"
        echo   [OK] Removed duplicate docs\README.md
    )
)

echo Removing old documentation files...
if exist "PYTHON_314_NOTES.txt" (
    del "PYTHON_314_NOTES.txt"
    echo   [OK] Removed PYTHON_314_NOTES.txt
)

if exist "COMMIT_MESSAGE.txt" (
    del "COMMIT_MESSAGE.txt"
    echo   [OK] Removed COMMIT_MESSAGE.txt
)

echo.

REM ============================================================================
REM  STEP 5: VERIFY PROJECT STRUCTURE
REM ============================================================================

echo.
echo ============================================================================
echo STEP 5: Verifying project structure...
echo ============================================================================
echo.

echo Checking for required directories...
if not exist "src" (
    echo   [ERROR] src\ directory missing!
) else (
    echo   [OK] src\ directory exists
)

if not exist "src\core" (
    echo   [ERROR] src\core\ directory missing!
) else (
    echo   [OK] src\core\ directory exists
)

if not exist "src\ui" (
    echo   [ERROR] src\ui\ directory missing!
) else (
    echo   [OK] src\ui\ directory exists
)

if not exist "docs" (
    echo   [ERROR] docs\ directory missing!
) else (
    echo   [OK] docs\ directory exists
)

if not exist "tests" (
    echo   [ERROR] tests\ directory missing!
) else (
    echo   [OK] tests\ directory exists
)

echo.
echo Checking for required files...
if not exist "README.md" (
    echo   [ERROR] README.md missing!
) else (
    echo   [OK] README.md exists
)

if not exist "requirements.txt" (
    echo   [ERROR] requirements.txt missing!
) else (
    echo   [OK] requirements.txt exists
)

if not exist "src\main.py" (
    echo   [ERROR] src\main.py missing!
) else (
    echo   [OK] src\main.py exists
)

echo.

REM ============================================================================
REM  STEP 6: FINAL CLEANUP
REM ============================================================================

echo.
echo ============================================================================
echo STEP 6: Final cleanup...
echo ============================================================================
echo.

echo Removing any empty directories...
for /f "delims=" %%d in ('dir /ad /b /s ^| sort /r') do (
    rmdir "%%d" 2>nul
)
echo   [OK] Cleaned up empty directories

echo.

REM ============================================================================
REM  COMPLETION
REM ============================================================================

echo.
echo ============================================================================
echo   CLEANUP & UPDATE COMPLETE!
echo ============================================================================
echo.
echo Summary of actions performed:
echo   ✓ Cleaned up cache and temporary files
echo   ✓ Updated Python dependencies
echo   ✓ Organized project files
echo   ✓ Removed redundant files
echo   ✓ Verified project structure
echo.
echo Your project is now clean and up-to-date!
echo.
echo Next steps:
echo   - Run tests: python -m pytest tests/
echo   - Run application: python src/main.py
echo   - Or double-click: run_app.bat
echo.
pause