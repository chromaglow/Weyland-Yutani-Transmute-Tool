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

### Installation

**Python 3.14 Users** (you!): Use minimal installation

```bash
# Easiest method - just install trimesh
python -m pip install trimesh

# OR double-click:
install_minimal.bat
```

**Python 3.12 or earlier**: Full installation

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
# Double-click:
run_app.bat

# OR run manually:
python src/main.py
```

---

## 🖥️ Usage

1. **Load STL File** - Click "📁 Load STL" and select your file
2. **Analyze Mesh** - Click "🔍 Analyze" to detect issues
3. **Repair Mesh** - Click "🔧 Repair" to fix defects automatically
4. **Export Files** - Click "💾 Export" to save repaired STL and/or STEP

---

## 📋 Requirements

### Minimum (Works with just this!)
- Python 3.8+
- trimesh (includes numpy)

### Recommended
- scipy (better algorithms)
- networkx (graph operations)

### Optional
- FreeCAD (for STEP export to SolidWorks)
- pytest (for testing)

---

## ⚠️ Python 3.14 Note

You're using Python 3.14 (very new!). Some packages don't have pre-built wheels yet.

**Solution**: Install just trimesh
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

## 🐛 Troubleshooting

### "No module named 'trimesh'"
**Fix**: Run `python -m pip install trimesh`

### "numpy compilation failed"
**Fix**: Use Python 3.12 or install just trimesh (includes numpy)

### GUI won't open
**Fix**: tkinter should be included with Python on Windows

### STEP export not working
**Fix**: Install FreeCAD from https://www.freecadweb.org/

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
