# Architecture

## Project Structure

```
Weyland-Yutani-Transmute-Tool/
├── src/
│   ├── core/           # Core processing logic
│   ├── ui/             # GUI components
│   └── utils/          # Utility functions
├── tests/              # Test suite
├── docs/               # Documentation
└── examples/           # Sample files
```

## Core Modules

### MeshAnalyzer
Detects defects in STL meshes:
- Watertight check
- Normal consistency
- Degenerate faces
- Duplicate vertices

### MeshRepairer
Fixes detected issues:
- Merge duplicate vertices
- Remove degenerate faces
- Fix normals
- Fill holes

### StepConverter
Converts STL to STEP:
- Uses FreeCAD Python API
- Creates solid bodies
- Exports STEP format

### MeshValidator
Validates mesh quality:
- Structural integrity
- Print readiness
- Volume calculation

## Data Flow

```
STL File → Analyzer → Repairer → Validator → Exporter
                                              ├→ STL
                                              └→ STEP
```

## Technology Stack

- **GUI**: tkinter
- **Mesh Processing**: trimesh
- **STEP Conversion**: FreeCAD
- **Testing**: pytest
