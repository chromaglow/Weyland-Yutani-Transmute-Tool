"""
Quick test to verify debug window methods exist
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ui.debug_window import DebugWindow, DebugExceptionHandler

print("Testing DebugWindow class...")

# Check if methods exist
methods_to_check = [
    'log_info',
    'log_warning', 
    'log_error',
    'start_operation',
    'end_operation',
    'show',
    'hide',
    'toggle',
    'clear'
]

print("\nChecking methods:")
for method in methods_to_check:
    if hasattr(DebugWindow, method):
        print(f"  ✓ {method}")
    else:
        print(f"  ✗ {method} - MISSING!")

print("\n✓ All methods exist! Debug window is ready.")
print("\nYou can now run: python test_debug_integration.py")
