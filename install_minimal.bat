@echo off
echo.
echo ========================================
echo  MINIMAL Installation
echo  Just the essentials!
echo ========================================
echo.

echo Installing trimesh (includes numpy)...
python -m pip install trimesh

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  SUCCESS!
    echo ========================================
    echo.
    echo Minimal installation complete!
    echo The tool is ready to use.
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
