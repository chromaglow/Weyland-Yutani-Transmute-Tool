"""
Weyland-Yutani Transmute Tool - Main Entry Point
Initiates the transmutation sequence...
"""

import sys
import tkinter as tk
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import TransmuteApp


def main():
    """
    Main entry point for the Weyland-Yutani Transmute Tool
    """
    print("=" * 60)
    print("🏢 Weyland-Yutani Transmute Tool")
    print("   'Building Better Worlds... One Mesh at a Time'")
    print("=" * 60)
    print()
    print("⏳ Initiating transmutation sequence...")
    print()
    
    # Create and run the application
    root = tk.Tk()
    app = TransmuteApp(root)
    
    print("✓ System online")
    print("✓ GUI initialized")
    print("✓ Ready for mesh transmutation")
    print()
    
    root.mainloop()


if __name__ == "__main__":
    main()
