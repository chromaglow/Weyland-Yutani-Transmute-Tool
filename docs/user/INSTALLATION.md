================================================================================
🏢 WEYLAND-YUTANI TRANSMUTE TOOL - INSTALLATION GUIDE
================================================================================

⚠️  IMPORTANT: You have Python 3.14 (very new!)
Some packages don't have pre-built versions yet for Python 3.14.

================================================================================
🚀 QUICK START - TRY THESE IN ORDER:
================================================================================

METHOD 1: Complete Installation (RECOMMENDED - Try This First!)
---------------------------------------------------------------
Double-click: install_minimal.bat

This installs trimesh and scipy for full mesh repair functionality.
Most reliable and includes all features!


METHOD 2: Simple Installation
------------------------------
Double-click: install_simple.bat

Installs core packages with pre-built wheels only.


METHOD 3: Full Installation
----------------------------
Double-click: install_dependencies.bat

Attempts to install all packages including optional ones.

================================================================================
📋 MANUAL INSTALLATION (If batch files don't work)
================================================================================

Open Command Prompt in this folder and run:

Complete Installation (Recommended):
    python -m pip install trimesh scipy

OR install all requirements:
    python -m pip install --only-binary :all: numpy scipy trimesh networkx

================================================================================
🔧 IF NOTHING WORKS - PYTHON VERSION ISSUE
================================================================================

Python 3.14 is brand new (2026). Most packages don't support it yet.

SOLUTION: Install Python 3.12 alongside 3.14

1. Download Python 3.12 from: https://www.python.org/downloads/
2. Install it (keep 3.14 too)
3. Use these commands:

   py -3.12 -m pip install trimesh
   py -3.12 src/main.py

This uses Python 3.12 which has better package support.

================================================================================
✅ HOW TO VERIFY INSTALLATION
================================================================================

Run this command:
    python -c "import trimesh; print('Success! Trimesh version:', trimesh.__version__)"

If you see a version number, you're good to go!

================================================================================
🎯 WHAT EACH PACKAGE DOES
================================================================================

REQUIRED:
  trimesh  - Core mesh processing (includes numpy)
  scipy    - Advanced mesh repair algorithms
  numpy    - Math operations (installed with trimesh)

OPTIONAL (Nice to have but not required):
  networkx - Graph operations
  pytest   - Testing framework

================================================================================
🚀 AFTER INSTALLATION
================================================================================

Once packages are installed:

1. Double-click: run_app.bat
   OR
   Run: python src/main.py

2. The GUI will open

3. Use the tool:
   - Load STL file
   - Analyze mesh
   - Repair defects
   - Export fixed files

================================================================================
🆘 TROUBLESHOOTING
================================================================================

Error: "No module named 'trimesh'"
Fix: Installation didn't complete. Try install_minimal.bat

Error: "numpy compilation failed"
Fix: Use --only-binary flag or install Python 3.12

Error: "python is not recognized"
Fix: Use full path or py launcher

Error: GUI won't open
Fix: tkinter should be included with Python on Windows

================================================================================
💡 RECOMMENDED APPROACH
================================================================================

For the best experience with this tool:

1. Try install_minimal.bat first
2. If that works, you're done!
3. If not, consider installing Python 3.12
4. Python 3.12 has better package compatibility

You can have both Python 3.14 and 3.12 installed!

================================================================================
📞 NEED MORE HELP?
================================================================================

Check these files:
  - PYTHON_314_NOTES.txt (Python 3.14 specific issues)
  - README_FIRST.txt (General setup)
  - README.md (Full documentation)

================================================================================

Building Better Worlds... 🚀

================================================================================
