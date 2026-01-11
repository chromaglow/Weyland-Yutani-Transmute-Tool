# Installation Guide

## Prerequisites

- Python 3.8 or higher
- Windows 10/11
- pip (Python package manager)

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Install FreeCAD (Optional, for STEP export)

Download and install FreeCAD from:
https://www.freecadweb.org/downloads.php

## Step 3: Verify Installation

```bash
python src/main.py
```

If the GUI launches, installation was successful!

## Troubleshooting

### Issue: Module not found errors
**Solution**: Ensure you're in the project directory and have activated your virtual environment

### Issue: FreeCAD not detected
**Solution**: Install FreeCAD and ensure it's in your system PATH

### Issue: GUI doesn't launch
**Solution**: Verify tkinter is installed (comes with Python on Windows)
