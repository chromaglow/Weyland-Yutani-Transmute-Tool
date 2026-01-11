@echo off
REM ============================================================================
REM  WEYLAND-YUTANI TRANSMUTE TOOL - ROOT FOLDER ORGANIZER
REM  Automatically organizes and cleans up the root directory
REM ============================================================================

echo.
echo ============================================================================
echo   WEYLAND-YUTANI TRANSMUTE TOOL - ROOT FOLDER ORGANIZER
echo ============================================================================
echo.
echo This script will organize your project files into proper directories:
echo   - docs/user/        - User documentation
echo   - docs/development/ - Developer documentation
echo   - docs/git/         - Git workflow documentation
echo   - scripts/          - Utility scripts
echo   - tests/            - Test files
echo.
echo Root will contain only essential files (LICENSE, README.md, etc.)
echo.
pause
echo.

REM ============================================================================
REM  CREATE DIRECTORY STRUCTURE
REM ============================================================================

echo Creating directory structure...
echo.

if not exist "docs\user" mkdir "docs\user"
if not exist "docs\development" mkdir "docs\development"
if not exist "docs\git" mkdir "docs\git"
if not exist "scripts" mkdir "scripts"

echo   [OK] docs\user\
echo   [OK] docs\development\
echo   [OK] docs\git\
echo   [OK] scripts\
echo.

REM ============================================================================
REM  MOVE USER DOCUMENTATION
REM ============================================================================

echo Moving user documentation...
echo.

if exist "INSTALLATION_GUIDE.txt" (
    move "INSTALLATION_GUIDE.txt" "docs\user\INSTALLATION.md" >nul 2>&1
    echo   [MOVED] INSTALLATION_GUIDE.txt -^> docs\user\INSTALLATION.md
) else (
    echo   [SKIP] INSTALLATION_GUIDE.txt not found
)

if exist "QUICK_START.txt" (
    move "QUICK_START.txt" "docs\user\QUICK_START.md" >nul 2>&1
    echo   [MOVED] QUICK_START.txt -^> docs\user\QUICK_START.md
) else (
    echo   [SKIP] QUICK_START.txt not found
)

if exist "START_HERE.txt" (
    move "START_HERE.txt" "docs\user\START_HERE.md" >nul 2>&1
    echo   [MOVED] START_HERE.txt -^> docs\user\START_HERE.md
) else (
    echo   [SKIP] START_HERE.txt not found
)

echo.

REM ============================================================================
REM  MOVE DEVELOPMENT DOCUMENTATION
REM ============================================================================

echo Moving development documentation...
echo.

if exist "DEBUG_WINDOW_INTEGRATION.md" (
    move "DEBUG_WINDOW_INTEGRATION.md" "docs\development\" >nul 2>&1
    echo   [MOVED] DEBUG_WINDOW_INTEGRATION.md -^> docs\development\
) else (
    echo   [SKIP] DEBUG_WINDOW_INTEGRATION.md not found
)

if exist "DEBUG_QUICK_REFERENCE.md" (
    move "DEBUG_QUICK_REFERENCE.md" "docs\development\" >nul 2>&1
    echo   [MOVED] DEBUG_QUICK_REFERENCE.md -^> docs\development\
) else (
    echo   [SKIP] DEBUG_QUICK_REFERENCE.md not found
)

if exist "INTEGRATION_COMPLETE.md" (
    move "INTEGRATION_COMPLETE.md" "docs\development\" >nul 2>&1
    echo   [MOVED] INTEGRATION_COMPLETE.md -^> docs\development\
) else (
    echo   [SKIP] INTEGRATION_COMPLETE.md not found
)

if exist "DOS_THEME.txt" (
    move "DOS_THEME.txt" "docs\development\DOS_THEME.md" >nul 2>&1
    echo   [MOVED] DOS_THEME.txt -^> docs\development\DOS_THEME.md
) else (
    echo   [SKIP] DOS_THEME.txt not found
)

if exist "PROGRESS_BAR_FEATURE.txt" (
    move "PROGRESS_BAR_FEATURE.txt" "docs\development\PROGRESS_BAR_FEATURE.md" >nul 2>&1
    echo   [MOVED] PROGRESS_BAR_FEATURE.txt -^> docs\development\PROGRESS_BAR_FEATURE.md
) else (
    echo   [SKIP] PROGRESS_BAR_FEATURE.txt not found
)

if exist "BUGFIX_NOTES.txt" (
    move "BUGFIX_NOTES.txt" "docs\development\BUGFIX_NOTES.md" >nul 2>&1
    echo   [MOVED] BUGFIX_NOTES.txt -^> docs\development\BUGFIX_NOTES.md
) else (
    echo   [SKIP] BUGFIX_NOTES.txt not found
)

if exist "BUGFIX_DEBUG_WINDOW.md" (
    move "BUGFIX_DEBUG_WINDOW.md" "docs\development\" >nul 2>&1
    echo   [MOVED] BUGFIX_DEBUG_WINDOW.md -^> docs\development\
) else (
    echo   [SKIP] BUGFIX_DEBUG_WINDOW.md not found
)

if exist "PROJECT_SUMMARY.md" (
    move "PROJECT_SUMMARY.md" "docs\development\" >nul 2>&1
    echo   [MOVED] PROJECT_SUMMARY.md -^> docs\development\
) else (
    echo   [SKIP] PROJECT_SUMMARY.md not found
)

if exist "ORGANIZATION_PLAN.md" (
    move "ORGANIZATION_PLAN.md" "docs\development\" >nul 2>&1
    echo   [MOVED] ORGANIZATION_PLAN.md -^> docs\development\
) else (
    echo   [SKIP] ORGANIZATION_PLAN.md not found
)

echo.

REM ============================================================================
REM  MOVE GIT DOCUMENTATION
REM ============================================================================

echo Moving Git documentation...
echo.

if exist "GIT_WORKFLOW.txt" (
    move "GIT_WORKFLOW.txt" "docs\git\GIT_WORKFLOW.md" >nul 2>&1
    echo   [MOVED] GIT_WORKFLOW.txt -^> docs\git\GIT_WORKFLOW.md
) else (
    echo   [SKIP] GIT_WORKFLOW.txt not found
)

if exist "GITHUB_SETUP.txt" (
    move "GITHUB_SETUP.txt" "docs\git\GITHUB_SETUP.md" >nul 2>&1
    echo   [MOVED] GITHUB_SETUP.txt -^> docs\git\GITHUB_SETUP.md
) else (
    echo   [SKIP] GITHUB_SETUP.txt not found
)

echo.

REM ============================================================================
REM  MOVE SCRIPTS
REM ============================================================================

echo Moving scripts...
echo.

if exist "install_minimal.bat" (
    move "install_minimal.bat" "scripts\" >nul 2>&1
    echo   [MOVED] install_minimal.bat -^> scripts\
) else (
    echo   [SKIP] install_minimal.bat not found
)

if exist "run_app.bat" (
    move "run_app.bat" "scripts\" >nul 2>&1
    echo   [MOVED] run_app.bat -^> scripts\
) else (
    echo   [SKIP] run_app.bat not found
)

if exist "check_one_file.py" (
    move "check_one_file.py" "scripts\" >nul 2>&1
    echo   [MOVED] check_one_file.py -^> scripts\
) else (
    echo   [SKIP] check_one_file.py not found
)

if exist "test_syntax.py" (
    move "test_syntax.py" "scripts\" >nul 2>&1
    echo   [MOVED] test_syntax.py -^> scripts\
) else (
    echo   [SKIP] test_syntax.py not found
)

if exist "organize_project.py" (
    move "organize_project.py" "scripts\" >nul 2>&1
    echo   [MOVED] organize_project.py -^> scripts\
) else (
    echo   [SKIP] organize_project.py not found
)

echo.

REM ============================================================================
REM  MOVE TESTS
REM ============================================================================

echo Moving test files...
echo.

if exist "test_debug_integration.py" (
    move "test_debug_integration.py" "tests\" >nul 2>&1
    echo   [MOVED] test_debug_integration.py -^> tests\
) else (
    echo   [SKIP] test_debug_integration.py not found
)

if exist "test_quick.py" (
    move "test_quick.py" "tests\" >nul 2>&1
    echo   [MOVED] test_quick.py -^> tests\
) else (
    echo   [SKIP] test_quick.py not found
)

echo.

REM ============================================================================
REM  CLEAN UP TEMPORARY FILES
REM ============================================================================

echo Cleaning up temporary files...
echo.

if exist "ROOT_README.txt" (
    del "ROOT_README.txt" >nul 2>&1
    echo   [DELETED] ROOT_README.txt
)

if exist "python" (
    del "python" >nul 2>&1
    echo   [DELETED] python (stray file)
)

REM Keep COMMIT_MESSAGE.txt for now (needed for commit)
if exist "COMMIT_MESSAGE.txt" (
    echo   [KEPT] COMMIT_MESSAGE.txt (needed for commit)
)

echo.

REM ============================================================================
REM  CREATE DOCUMENTATION INDEX
REM ============================================================================

echo Creating documentation index...
echo.

(
echo # Weyland-Yutani Transmute Tool - Documentation
echo.
echo ## 📚 Documentation Index
echo.
echo ### User Documentation
echo - [Installation Guide](user/INSTALLATION.md^) - How to install the tool
echo - [Quick Start Guide](user/QUICK_START.md^) - Get started quickly
echo - [Start Here](user/START_HERE.md^) - First steps
echo - [User Guide](USER_GUIDE.md^) - Complete user manual
echo.
echo ### Development Documentation
echo - [Architecture](ARCHITECTURE.md^) - System architecture overview
echo - [Debug Window Integration](development/DEBUG_WINDOW_INTEGRATION.md^) - Debug system details
echo - [Debug Quick Reference](development/DEBUG_QUICK_REFERENCE.md^) - Developer quick reference
echo - [Integration Complete](development/INTEGRATION_COMPLETE.md^) - Latest integration summary
echo - [DOS Theme](development/DOS_THEME.md^) - Theme implementation details
echo - [Progress Bar Feature](development/PROGRESS_BAR_FEATURE.md^) - Progress bar documentation
echo - [Bug Fix Notes](development/BUGFIX_NOTES.md^) - Bug fix history
echo - [Debug Window Bugfix](development/BUGFIX_DEBUG_WINDOW.md^) - Recent bugfix details
echo - [Project Summary](development/PROJECT_SUMMARY.md^) - Complete project summary
echo - [Organization Plan](development/ORGANIZATION_PLAN.md^) - Folder organization plan
echo.
echo ### Git ^& Workflow
echo - [Git Workflow](git/GIT_WORKFLOW.md^) - Git workflow guide
echo - [GitHub Setup](git/GITHUB_SETUP.md^) - GitHub repository setup
echo.
echo ## 🚀 Quick Links
echo.
echo - **Getting Started**: Start with [Start Here](user/START_HERE.md^)
echo - **Installation**: See [Installation Guide](user/INSTALLATION.md^)
echo - **Development**: Check [Architecture](ARCHITECTURE.md^)
echo - **Debugging**: Use [Debug Quick Reference](development/DEBUG_QUICK_REFERENCE.md^)
echo.
echo ## 🏢 About
echo.
echo **Weyland-Yutani Transmute Tool** - STL repair and STEP conversion with a retro DOS aesthetic.
echo.
echo *"Building Better Worlds... One Mesh at a Time"*
) > "docs\README.md"

echo   [CREATED] docs\README.md
echo.

REM ============================================================================
REM  CREATE SCRIPTS README
REM ============================================================================

echo Creating scripts README...
echo.

(
echo # Utility Scripts
echo.
echo This directory contains utility scripts for the Weyland-Yutani Transmute Tool.
echo.
echo ## Available Scripts
echo.
echo ### Installation ^& Running
echo - **install_minimal.bat** - Install minimal dependencies
echo - **run_app.bat** - Run the application
echo.
echo ### Development Tools
echo - **check_one_file.py** - Check a single file
echo - **test_syntax.py** - Test Python syntax
echo - **organize_project.py** - Organize project structure
echo.
echo ## Usage
echo.
echo ### Run the Application
echo ```batch
echo scripts\run_app.bat
echo ```
echo.
echo ### Install Dependencies
echo ```batch
echo scripts\install_minimal.bat
echo ```
echo.
echo ### Organize Project
echo ```batch
echo python scripts\organize_project.py
echo ```
echo.
echo ## Notes
echo.
echo - Run scripts from the project root directory
echo - Some scripts may require Python to be installed
echo - Check individual script headers for specific requirements
) > "scripts\README.md"

echo   [CREATED] scripts\README.md
echo.

REM ============================================================================
REM  SUMMARY
REM ============================================================================

echo ============================================================================
echo   ORGANIZATION COMPLETE!
echo ============================================================================
echo.
echo Root directory now contains only essential files:
echo   - LICENSE
echo   - README.md
echo   - requirements.txt
echo   - setup.py
echo   - pytest.ini
echo   - COMMIT_MESSAGE.txt (for next commit)
echo   - organize_root.bat (this script)
echo.
echo All other files have been organized into:
echo   - docs\user\        - User documentation
echo   - docs\development\ - Developer documentation
echo   - docs\git\         - Git workflow documentation
echo   - scripts\          - Utility scripts
echo   - tests\            - Test files
echo.
echo Documentation indexes created:
echo   - docs\README.md
echo   - scripts\README.md
echo.
echo ============================================================================
echo   NEXT STEPS
echo ============================================================================
echo.
echo 1. Review the organized structure
echo 2. Update main README.md with new paths (if needed)
echo 3. Test that scripts still work:
echo    - python tests\test_quick.py
echo    - python tests\test_debug_integration.py
echo 4. Commit the organization:
echo    - git add .
echo    - git commit -m "chore: Organize project structure"
echo    - git push origin main
echo.
echo ============================================================================
echo.
echo "Building Better Worlds... One Organized Folder at a Time" 🏢
echo.
pause
