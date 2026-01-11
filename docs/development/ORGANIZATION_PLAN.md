# Root Folder Organization Plan

## Current Structure Analysis

The root folder currently contains a mix of documentation, configuration, and utility files. Here's the recommended organization:

## Recommended Structure

```
Weyland-Yutani-Transmute-Tool/
├── docs/                           # All documentation
│   ├── user/                       # User-facing documentation
│   │   ├── README.md              # Main user guide
│   │   ├── INSTALLATION.md        # Installation instructions
│   │   ├── USER_GUIDE.md          # Detailed user guide
│   │   ├── QUICK_START.md         # Quick start guide
│   │   └── START_HERE.md          # Getting started
│   ├── development/               # Developer documentation
│   │   ├── ARCHITECTURE.md        # System architecture
│   │   ├── DEBUG_WINDOW_INTEGRATION.md
│   │   ├── DEBUG_QUICK_REFERENCE.md
│   │   ├── DOS_THEME.md           # Theme documentation
│   │   ├── PROGRESS_BAR_FEATURE.md
│   │   ├── BUGFIX_NOTES.md        # Bug fix history
│   │   └── INTEGRATION_COMPLETE.md
│   └── git/                       # Git workflow docs
│       ├── GIT_WORKFLOW.md        # Git workflow guide
│       └── GITHUB_SETUP.md        # GitHub setup guide
├── scripts/                       # Utility scripts
│   ├── install_minimal.bat        # Installation script
│   ├── run_app.bat                # Run application
│   ├── check_one_file.py          # File checker
│   └── test_syntax.py             # Syntax tester
├── tests/                         # Test files
│   ├── fixtures/                  # Test fixtures
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_analyzer.py
│   ├── test_converter.py
│   ├── test_repairer.py
│   └── test_debug_integration.py  # Debug integration tests
├── src/                           # Source code
│   ├── core/                      # Core functionality
│   ├── ui/                        # User interface
│   └── utils/                     # Utilities
├── examples/                      # Example files
│   └── sample_stl_files/
├── .github/                       # GitHub configuration
│   └── workflows/
├── LICENSE                        # License file
├── README.md                      # Main README
├── requirements.txt               # Python dependencies
├── setup.py                       # Setup configuration
├── pytest.ini                     # Pytest configuration
└── COMMIT_MESSAGE.txt             # Latest commit message
```

## File Reorganization

### Move to docs/user/
- INSTALLATION_GUIDE.txt → docs/user/INSTALLATION.md
- QUICK_START.txt → docs/user/QUICK_START.md
- START_HERE.txt → docs/user/START_HERE.md

### Move to docs/development/
- DEBUG_WINDOW_INTEGRATION.md → docs/development/
- DEBUG_QUICK_REFERENCE.md → docs/development/
- INTEGRATION_COMPLETE.md → docs/development/
- DOS_THEME.txt → docs/development/DOS_THEME.md
- PROGRESS_BAR_FEATURE.txt → docs/development/PROGRESS_BAR_FEATURE.md
- BUGFIX_NOTES.txt → docs/development/BUGFIX_NOTES.md

### Move to docs/git/
- GIT_WORKFLOW.txt → docs/git/GIT_WORKFLOW.md
- GITHUB_SETUP.txt → docs/git/GITHUB_SETUP.md

### Move to scripts/
- install_minimal.bat → scripts/
- run_app.bat → scripts/
- check_one_file.py → scripts/
- test_syntax.py → scripts/

### Move to tests/
- test_debug_integration.py → tests/

### Keep in Root
- LICENSE
- README.md
- requirements.txt
- setup.py
- pytest.ini
- COMMIT_MESSAGE.txt (temporary, for next commit)

### Remove from Root
- python (appears to be a stray file/symlink)

## Benefits of This Organization

1. **Clear Separation**: User docs vs developer docs vs configuration
2. **Easy Navigation**: Related files grouped together
3. **Professional Structure**: Follows Python project conventions
4. **Scalability**: Easy to add new documentation or scripts
5. **Clean Root**: Only essential files in root directory

## Implementation Steps

1. Create new directories:
   - docs/user/
   - docs/development/
   - docs/git/
   - scripts/

2. Move files to appropriate directories (see above)

3. Update references in documentation:
   - Update paths in README.md
   - Update paths in INSTALLATION.md
   - Update paths in other docs that reference moved files

4. Update scripts:
   - Update paths in run_app.bat
   - Update paths in install_minimal.bat

5. Test:
   - Verify all scripts still work
   - Verify documentation links are correct
   - Run tests to ensure imports still work

## Automated Organization Script

Create a script to automate this organization:

```python
# organize_project.py
import os
import shutil
from pathlib import Path

def organize_project():
    base = Path(".")
    
    # Create directories
    (base / "docs" / "user").mkdir(parents=True, exist_ok=True)
    (base / "docs" / "development").mkdir(parents=True, exist_ok=True)
    (base / "docs" / "git").mkdir(parents=True, exist_ok=True)
    (base / "scripts").mkdir(exist_ok=True)
    
    # Move files
    moves = {
        "INSTALLATION_GUIDE.txt": "docs/user/INSTALLATION.md",
        "QUICK_START.txt": "docs/user/QUICK_START.md",
        "START_HERE.txt": "docs/user/START_HERE.md",
        "DEBUG_WINDOW_INTEGRATION.md": "docs/development/",
        "DEBUG_QUICK_REFERENCE.md": "docs/development/",
        "INTEGRATION_COMPLETE.md": "docs/development/",
        "DOS_THEME.txt": "docs/development/DOS_THEME.md",
        "PROGRESS_BAR_FEATURE.txt": "docs/development/PROGRESS_BAR_FEATURE.md",
        "BUGFIX_NOTES.txt": "docs/development/BUGFIX_NOTES.md",
        "GIT_WORKFLOW.txt": "docs/git/GIT_WORKFLOW.md",
        "GITHUB_SETUP.txt": "docs/git/GITHUB_SETUP.md",
        "install_minimal.bat": "scripts/",
        "run_app.bat": "scripts/",
        "check_one_file.py": "scripts/",
        "test_syntax.py": "scripts/",
        "test_debug_integration.py": "tests/",
    }
    
    for src, dst in moves.items():
        src_path = base / src
        dst_path = base / dst
        if src_path.exists():
            shutil.move(str(src_path), str(dst_path))
            print(f"Moved: {src} → {dst}")
    
    print("\nOrganization complete!")

if __name__ == "__main__":
    organize_project()
```

## Post-Organization Tasks

1. Update README.md with new structure
2. Update documentation index
3. Create docs/README.md with navigation
4. Update .gitignore if needed
5. Commit changes with descriptive message

## Notes

- Keep COMMIT_MESSAGE.txt in root temporarily for the next commit
- After committing, can move to docs/development/ or delete
- Consider adding a CHANGELOG.md in root for version history
- Consider adding CONTRIBUTING.md for contribution guidelines
