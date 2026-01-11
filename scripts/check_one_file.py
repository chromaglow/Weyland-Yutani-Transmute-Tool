import py_compile
import sys

try:
    py_compile.compile('src/core/mesh_repairer.py', doraise=True)
    print("✓ File is valid!")
except py_compile.PyCompileError as e:
    print(f"✗ Error: {e}")
    print(f"\nFull error:\n{e.msg}")
    sys.exit(1)
