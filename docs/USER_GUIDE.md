# User Guide

## Getting Started

### Launching the Application

```bash
python src/main.py
```

## Workflow

### 1. Load STL File

Click "📁 Load STL File" and select your STL file.

### 2. Analyze Mesh

Click "🔍 Analyze Mesh" to detect issues:
- Non-watertight geometry
- Inverted normals
- Degenerate faces
- Duplicate vertices

### 3. Repair Mesh

Click "🔧 Repair Mesh" to automatically fix detected issues.

### 4. Export Files

Choose your export options:
- ✅ Export STL: Save repaired STL file
- ✅ Export STEP: Convert to solid STEP file (requires FreeCAD)

Click "💾 Export Files" and select output directory.

## Tips

- Always analyze before repairing
- Check console output for detailed information
- Validate exported files in your slicer/CAD software
- Keep original files as backup

## Common Issues

### Mesh still hollow after repair
- Try manual repair in Meshmixer or Blender
- Check if original mesh has severe defects

### STEP export fails
- Ensure FreeCAD is installed
- Verify mesh is watertight after repair

### Large file processing is slow
- This is normal for complex meshes
- Consider simplifying mesh in external tool first
