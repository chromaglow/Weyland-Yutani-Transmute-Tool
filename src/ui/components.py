"""
Reusable UI components
"""

import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):
    """
    Status bar widget for displaying application status
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.label = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X, padx=2, pady=2)
    
    def set_status(self, text):
        """Update status text"""
        self.label.config(text=text)


class ProgressDialog:
    """
    Simple progress dialog
    """
    
    def __init__(self, parent, title="Processing"):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x100")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        ttk.Label(self.dialog, text="Processing...").pack(pady=10)
        
        self.progress = ttk.Progressbar(
            self.dialog,
            mode='indeterminate',
            length=250
        )
        self.progress.pack(pady=10)
        self.progress.start()
    
    def close(self):
        """Close the dialog"""
        self.progress.stop()
        self.dialog.destroy()
