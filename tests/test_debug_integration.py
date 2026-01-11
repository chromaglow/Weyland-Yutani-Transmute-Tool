"""
Test script to verify debug window integration
"""

import tkinter as tk
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ui.main_window import TransmuteApp


def main():
    """Run the application"""
    root = tk.Tk()
    app = TransmuteApp(root)
    
    print("\n" + "="*60)
    print("DEBUG WINDOW INTEGRATION TEST")
    print("="*60)
    print("\nThe application has started with debug window integration.")
    print("\nFeatures to test:")
    print("  1. Press Ctrl+D to toggle the debug window")
    print("  2. Try loading a file (debug logs will appear)")
    print("  3. Try operations without files (warnings will appear)")
    print("  4. Debug window auto-shows on errors/warnings")
    print("  5. Performance monitoring tracks long operations")
    print("\nDebug window should be hidden initially.")
    print("It will automatically appear when errors or warnings occur.")
    print("="*60 + "\n")
    
    root.mainloop()


if __name__ == "__main__":
    main()
