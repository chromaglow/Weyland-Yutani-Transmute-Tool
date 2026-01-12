@echo off
echo ========================================
echo  Weyland-Yutani Transmute Tool
echo  Project Cleanup & Organization
echo ========================================
echo.

cd /d "%~dp0"

echo Cleaning up temporary and development files...
echo.

REM Remove temporary files
if exist "test_audio.py" del "test_audio.py"
if exist "*.pyc" del "*.pyc"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.log" del "*.log"
if exist "*.tmp" del "*.tmp"

REM Clean up src directory
if exist "src\__pycache__" rmdir /s /q "src\__pycache__"
if exist "src\ui\__pycache__" rmdir /s /q "src\ui\__pycache__"
if exist "src\core\__pycache__" rmdir /s /q "src\core\__pycache__"
if exist "src\utils\__pycache__" rmdir /s /q "src\utils\__pycache__"

REM Clean up tests directory
if exist "tests\__pycache__" rmdir /s /q "tests\__pycache__"

REM Remove development artifacts that shouldn't be in final project
if exist "COMMIT_MESSAGE.txt" del "COMMIT_MESSAGE.txt"
if exist "FINAL_SUMMARY.md" del "FINAL_SUMMARY.md"
if exist "ORGANIZE_INSTRUCTIONS.txt" del "ORGANIZE_INSTRUCTIONS.txt"
if exist "organize_root.bat" del "organize_root.bat"

REM Ensure proper Python project structure
echo.
echo Ensuring proper project structure...
echo.

REM Create .gitignore if it doesn't exist
if not exist ".gitignore" (
    echo # Python
    echo __pycache__/
    echo *.pyc
    echo *.pyo
    echo *.pyd
    echo .Python
    echo env/
    echo venv/
    echo .env
    echo .venv
    echo pip-log.txt
    echo pip-delete-this-directory.txt
    echo .tox/
    echo .coverage
    echo .coverage.*
    echo .cache
    echo nosetests.xml
    echo coverage.xml
    echo *.cover
    echo .hypothesis/
    echo .pytest_cache/
    echo.
    echo # Virtual environments
    echo env/
    echo venv/
    echo ENV/
    echo env.bak/
    echo venv.bak/
    echo.
    echo # IDEs
    echo .vscode/
    echo .idea/
    echo *.swp
    echo *.swo
    echo *~
    echo.
    echo # OS
    echo .DS_Store
    echo .DS_Store?
    echo ._*
    echo .Spotlight-V100
    echo .Trashes
    echo ehthumbs.db
    echo Thumbs.db
    echo.
    echo # Project specific
    echo *.log
    echo *.tmp
    echo Spybreak!Short One Propellerheads.mp3
) > .gitignore

echo.
echo ========================================
echo  Cleanup Complete!
echo ========================================
echo.
echo Your Weyland-Yutani Transmute Tool is now
echo professionally organized and ready to impress!
echo.
echo Project structure:
echo ├── src/           (Source code)
echo ├── tests/         (Unit tests)
echo ├── docs/          (Documentation)
echo ├── examples/      (Sample files)
echo ├── scripts/       (Utility scripts)
echo ├── README.md      (Project info)
echo ├── LICENSE        (License)
echo ├── setup.py       (Installation)
echo └── requirements.txt (Dependencies)
echo.
pause