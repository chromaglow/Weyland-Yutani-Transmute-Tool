"""
Automated Project Organization Script
Organizes the Weyland-Yutani Transmute Tool project structure
"""

import os
import shutil
from pathlib import Path


def organize_project():
    """Organize project files into proper directory structure"""
    
    print("="*60)
    print("WEYLAND-YUTANI TRANSMUTE TOOL - PROJECT ORGANIZER")
    print("="*60)
    print()
    
    base = Path(".")
    
    # Create directories
    print("Creating directory structure...")
    directories = [
        base / "docs" / "user",
        base / "docs" / "development",
        base / "docs" / "git",
        base / "scripts",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {directory}")
    
    print()
    print("Moving files to appropriate locations...")
    print()
    
    # Define file moves
    moves = {
        # User documentation
        "INSTALLATION_GUIDE.txt": "docs/user/INSTALLATION.md",
        "QUICK_START.txt": "docs/user/QUICK_START.md",
        "START_HERE.txt": "docs/user/START_HERE.md",
        
        # Development documentation
        "DEBUG_WINDOW_INTEGRATION.md": "docs/development/DEBUG_WINDOW_INTEGRATION.md",
        "DEBUG_QUICK_REFERENCE.md": "docs/development/DEBUG_QUICK_REFERENCE.md",
        "INTEGRATION_COMPLETE.md": "docs/development/INTEGRATION_COMPLETE.md",
        "DOS_THEME.txt": "docs/development/DOS_THEME.md",
        "PROGRESS_BAR_FEATURE.txt": "docs/development/PROGRESS_BAR_FEATURE.md",
        "BUGFIX_NOTES.txt": "docs/development/BUGFIX_NOTES.md",
        
        # Git documentation
        "GIT_WORKFLOW.txt": "docs/git/GIT_WORKFLOW.md",
        "GITHUB_SETUP.txt": "docs/git/GITHUB_SETUP.md",
        
        # Scripts
        "install_minimal.bat": "scripts/install_minimal.bat",
        "run_app.bat": "scripts/run_app.bat",
        "check_one_file.py": "scripts/check_one_file.py",
        "test_syntax.py": "scripts/test_syntax.py",
        
        # Tests
        "test_debug_integration.py": "tests/test_debug_integration.py",
    }
    
    moved_count = 0
    skipped_count = 0
    
    for src, dst in moves.items():
        src_path = base / src
        dst_path = base / dst
        
        if src_path.exists():
            try:
                # Check if destination already exists
                if dst_path.exists():
                    print(f"  ⚠ Skipped: {src} (destination exists)")
                    skipped_count += 1
                else:
                    shutil.move(str(src_path), str(dst_path))
                    print(f"  ✓ Moved: {src} → {dst}")
                    moved_count += 1
            except Exception as e:
                print(f"  ✗ Error moving {src}: {e}")
        else:
            print(f"  ⚠ Not found: {src}")
            skipped_count += 1
    
    print()
    print("="*60)
    print(f"Organization complete!")
    print(f"  Files moved: {moved_count}")
    print(f"  Files skipped: {skipped_count}")
    print("="*60)
    print()
    print("Next steps:")
    print("  1. Review the new structure")
    print("  2. Update README.md with new paths")
    print("  3. Test scripts in scripts/ directory")
    print("  4. Run tests to verify everything works")
    print("  5. Commit changes")
    print()
    print("Root directory now contains only:")
    print("  - LICENSE")
    print("  - README.md")
    print("  - requirements.txt")
    print("  - setup.py")
    print("  - pytest.ini")
    print("  - COMMIT_MESSAGE.txt (for next commit)")
    print("  - ORGANIZATION_PLAN.md (this plan)")
    print("  - organize_project.py (this script)")
    print()


def create_docs_index():
    """Create a documentation index in docs/README.md"""
    
    docs_readme = Path("docs") / "README.md"
    
    content = """# Weyland-Yutani Transmute Tool - Documentation

## 📚 Documentation Index

### User Documentation
- [Installation Guide](user/INSTALLATION.md) - How to install the tool
- [Quick Start Guide](user/QUICK_START.md) - Get started quickly
- [Start Here](user/START_HERE.md) - First steps
- [User Guide](USER_GUIDE.md) - Complete user manual

### Development Documentation
- [Architecture](ARCHITECTURE.md) - System architecture overview
- [Debug Window Integration](development/DEBUG_WINDOW_INTEGRATION.md) - Debug system details
- [Debug Quick Reference](development/DEBUG_QUICK_REFERENCE.md) - Developer quick reference
- [Integration Complete](development/INTEGRATION_COMPLETE.md) - Latest integration summary
- [DOS Theme](development/DOS_THEME.md) - Theme implementation details
- [Progress Bar Feature](development/PROGRESS_BAR_FEATURE.md) - Progress bar documentation
- [Bug Fix Notes](development/BUGFIX_NOTES.md) - Bug fix history

### Git & Workflow
- [Git Workflow](git/GIT_WORKFLOW.md) - Git workflow guide
- [GitHub Setup](git/GITHUB_SETUP.md) - GitHub repository setup

## 🚀 Quick Links

- **Getting Started**: Start with [Start Here](user/START_HERE.md)
- **Installation**: See [Installation Guide](user/INSTALLATION.md)
- **Development**: Check [Architecture](ARCHITECTURE.md)
- **Debugging**: Use [Debug Quick Reference](development/DEBUG_QUICK_REFERENCE.md)

## 📖 Documentation Structure

```
docs/
├── README.md                    # This file
├── user/                        # User-facing documentation
│   ├── INSTALLATION.md
│   ├── QUICK_START.md
│   └── START_HERE.md
├── development/                 # Developer documentation
│   ├── DEBUG_WINDOW_INTEGRATION.md
│   ├── DEBUG_QUICK_REFERENCE.md
│   ├── INTEGRATION_COMPLETE.md
│   ├── DOS_THEME.md
│   ├── PROGRESS_BAR_FEATURE.md
│   └── BUGFIX_NOTES.md
├── git/                         # Git workflow documentation
│   ├── GIT_WORKFLOW.md
│   └── GITHUB_SETUP.md
├── ARCHITECTURE.md              # System architecture
├── INSTALLATION.md              # Installation details
└── USER_GUIDE.md                # Complete user guide
```

## 🏢 About

**Weyland-Yutani Transmute Tool** - STL repair and STEP conversion with a retro DOS aesthetic.

*"Building Better Worlds... One Mesh at a Time"*
"""
    
    with open(docs_readme, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Created: {docs_readme}")


def main():
    """Main function"""
    try:
        organize_project()
        print("Creating documentation index...")
        create_docs_index()
        print()
        print("✓ All done! Project is now organized.")
        print()
    except Exception as e:
        print(f"\n✗ Error during organization: {e}")
        print("Please review and fix any issues manually.")


if __name__ == "__main__":
    main()
