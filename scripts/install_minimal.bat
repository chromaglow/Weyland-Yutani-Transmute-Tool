@echo off
echo.
echo ========================================
echo  WEYLAND-YUTANI TRANSMUTE TOOL
echo  Complete Installation
echo ========================================
echo.

echo Installing trimesh and scipy for complete mesh repair...
python -m pip install trimesh scipy

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  SUCCESS!
    echo ========================================
    echo.
    echo Complete installation finished!
    echo All mesh repair features are available.
    echo.
    echo Next: Double-click run_app.bat
    echo.
) else (
    echo.
    echo Trying with py launcher...
    py -m pip install trimesh
    
    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo  SUCCESS!
        echo ========================================
        echo.
        echo Minimal installation complete!
        echo.
    ) else (
        echo.
        echo ========================================
        echo  Installation Failed
        echo ========================================
        echo.
        echo Please see PYTHON_314_NOTES.txt
        echo for alternative solutions.
        echo.
    )
)

pause
