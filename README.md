# 🏢 Weyland-Yutani Transmute Tool

**"Building Better Worlds... One Mesh at a Time"**

Professional STL mesh repair and STEP conversion utility for 3D printing.

---

## 🎯 What This Tool Does

Fixes STL files that appear solid but slice as hollow shells:

1. **Analyze** - Detect mesh defects (holes, inverted normals, etc.)
2. **Repair** - Automatically fix issues to create watertight geometry
3. **Validate** - Verify mesh quality and print readiness
4. **Export** - Save as repaired STL and/or solid STEP file

---

## ⚡ Quick Start

### 🚀 Easy Installation (Recommended for Everyone!)

**Just double-click these files in the root folder:**
```
install_minimal.bat    <- Click this first to install everything
run_app.bat           <- Click this to run the app after installation
```

That's it! The installer will:
- ✅ Check if Python is installed
- ✅ Install all required packages automatically
- ✅ Set up audio features and mesh processing
- ✅ Guide you through any issues
- ✅ Tell you when everything is ready

**No technical knowledge required!** Perfect for sharing with friends.

### Alternative: Scripts Folder Installation

If you prefer the original location:
```
scripts/install_minimal.bat
scripts/run_app.bat
```

### Manual Installation (For Advanced Users)

If you prefer manual installation:

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install core packages only
pip install trimesh scipy networkx fast-simplification pygame
```

### Running the Application

```bash
# Double-click:
run_app.bat

# OR run manually:
python src/main.py
```

---

## 🎵 Features

- **DOS-Themed Interface** - Authentic retro green-on-black design
- **Background Music** - Immersive audio experience with volume control
- **Mesh Analysis** - Detect holes, inverted normals, and defects
- **Auto Repair** - Fix watertight geometry automatically
- **Smart Simplification** - Reduce complexity while preserving quality
- **STEP Export** - Convert to solid CAD formats (requires FreeCAD)
- **Progress Feedback** - Visual progress bars and status updates
- **Professional Logging** - Debug window for troubleshooting

---

## 📋 System Requirements

### Required
- **Python 3.8+** (3.13 recommended)
- **Windows 10/11** (Linux/Mac may work but not tested)

### Optional
- **FreeCAD** - For STEP file export to CAD software
- **Audio device** - For background music (auto-disables if unavailable)

---

## 🖥️ How to Use

1. **Install** - Double-click `install_minimal.bat` in the root folder
2. **Launch** - Double-click `run_app.bat` in the root folder
3. **Load** - Click "📁 Load STL" and select your 3D file
4. **Analyze** - Click "🔍 Analyze" to check for issues
5. **Repair** - Click "🔧 Repair" to fix problems automatically
6. **Simplify** - Use sliders or buttons to reduce mesh complexity
7. **Export** - Save as repaired STL and/or STEP file

---

## 🎮 Interface Guide

- **Volume Control** - Top-right slider and mute button
- **Progress Dialogs** - 3.5-second animated feedback for all actions
- **DOS Aesthetics** - Green text on black background throughout
- **Keyboard Shortcuts** - Ctrl+D for debug window
- **Status Updates** - Real-time feedback in bottom console

---

## 🔧 Troubleshooting

**Installation Issues:**
- Run `scripts/install_minimal.bat` as Administrator
- Check that Python is in your PATH
- Restart command prompt after Python installation

**Audio Not Working:**
- Audio features automatically disable if pygame fails
- App works perfectly without sound

**STEP Export Issues:**
- Install FreeCAD from freecad.org
- STL export always works regardless

**Performance:**
- Large meshes may take time to process
- Use simplification features to speed up operations
```bash
python -m pip install trimesh
```

**Alternative**: Install Python 3.12 alongside 3.14 for better compatibility
```bash
py -3.12 -m pip install trimesh
py -3.12 src/main.py
```

---

## 🔧 Installation Options

| Method | Command | Best For |
|--------|---------|----------|
| **Minimal** | `install_minimal.bat` | Python 3.14, quick start |
| **Simple** | `install_simple.bat` | Core packages only |
| **Full** | `install_dependencies.bat` | All features |

---

## 📁 Project Structure

```
Weyland-Yutani-Transmute-Tool/
├── src/
│   ├── core/           # Mesh processing (analyzer, repairer, converter)
│   ├── ui/             # GUI application
│   └── utils/          # File handling, logging
├── tests/              # Test suite
├── docs/               # Detailed documentation
├── examples/           # Sample files
├── install_minimal.bat # Quick installation
├── run_app.bat         # Launch application
└── README.md           # This file
```

---

## 🚀 Features

- ✅ **Mesh Analysis** - Detect non-manifold edges, holes, defects
- ✅ **Automatic Repair** - Fix normals, merge vertices, fill holes
- ✅ **Validation** - Verify watertight geometry
- ✅ **STL Export** - Save repaired mesh for 3D printing
- ✅ **STEP Export** - Convert to solid body for CAD (requires FreeCAD)
- ✅ **GUI Interface** - Easy-to-use graphical interface
- ✅ **Console Output** - Detailed logging and progress

---

## 🧹 Maintenance

### Clean Up & Update Project
For comprehensive cleanup and updates:

```bash
# Double-click:
cleanup_update.bat
```

This script will:
- Clean cache files and temporary files
- Update Python dependencies
- Organize project files
- Remove redundant files
- Verify project structure

---

## 🐛 Troubleshooting

### "No module named 'trimesh'"
**Fix**: Run `python -m pip install trimesh`

### "numpy compilation failed"
**Fix**: Use Python 3.12 or install just trimesh (includes numpy)

### GUI won't open
**Fix**: tkinter should be included with Python on Windows

### STEP export not working
**Issue**: "FreeCAD not available - cannot convert to STEP"

**Solutions**:
1. **Install FreeCAD**: Download from https://www.freecadweb.org/
2. **Run as Administrator**: Right-click the application and "Run as administrator"  
3. **Check PATH**: Ensure FreeCAD's `bin` folder is in your system PATH
4. **Automatic Detection**: The program searches common FreeCAD installation locations

---

## 📚 Documentation

- **Quick Start**: This README
- **Installation Help**: `INSTALLATION_GUIDE.txt`
- **Python 3.14 Issues**: `PYTHON_314_NOTES.txt`
- **Detailed Docs**: See `docs/` folder

---

## 🎨 Technology Stack

- **Language**: Python 3.8+
- **GUI**: tkinter (built-in)
- **Mesh Processing**: trimesh, numpy
- **STEP Conversion**: FreeCAD Python API
- **Testing**: pytest

---

## 📝 License

MIT License - Free to use, modify, and distribute

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 🆘 Support

- Check console output for detailed error messages
- Read `INSTALLATION_GUIDE.txt` for setup help
- See `docs/USER_GUIDE.md` for usage instructions
- Review `PYTHON_314_NOTES.txt` for Python 3.14 specific issues

---

## 🎯 Use Case

**Problem**: Your STL files from certain tools look solid but slice as hollow in Bamboo Studio

**Root Cause**: Non-manifold geometry, holes, inverted normals

**Solution**: This tool repairs mesh defects and ensures watertight geometry for successful 3D printing

---

**Weyland-Yutani Corporation**: Building Better Worlds Since 2093 🚀
