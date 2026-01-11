"""
Quick syntax check for all Python files
"""

import py_compile
import sys
from pathlib import Path

print("=" * 60)
print("🔍 Checking Python Syntax")
print("=" * 60)
print()

# Find all Python files
src_dir = Path("src")
python_files = list(src_dir.rglob("*.py"))

errors = []
success = 0

for py_file in python_files:
    try:
        py_compile.compile(str(py_file), doraise=True)
        print(f"✓ {py_file}")
        success += 1
    except py_compile.PyCompileError as e:
        print(f"✗ {py_file}")
        print(f"  Error: {e}")
        errors.append((py_file, e))

print()
print("=" * 60)
print(f"Results: {success} passed, {len(errors)} failed")
print("=" * 60)

if errors:
    print("\nErrors found:")
    for file, error in errors:
        print(f"  - {file}: {error}")
    sys.exit(1)
else:
    print("\n✅ All files passed syntax check!")
    sys.exit(0)
