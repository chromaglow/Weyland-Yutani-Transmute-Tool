"""
Debug Window - Error and Performance Monitoring
Stays hidden until issues occur
"""

import tkinter as tk
from tkinter import scrolledtext
import sys
import traceback
from datetime import datetime
import threading
import time


class DebugWindow:
    """
    Debug window that monitors for errors and performance issues
    Stays blank/hidden until problems occur
    """
    
    # DOS Theme Colors
    DOS_BG = "#000000"
    DOS_FG = "#00FF00"
    DOS_FG_ERROR = "#FF0000"  # Red for errors
    DOS_FG_WARNING = "#FFFF00"  # Yellow for warnings
    DOS_FONT = ("Courier New", 9)
    DOS_FONT_BOLD = ("Courier New", 9, "bold")
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.text_widget = None
        self.error_count = 0
        self.warning_count = 0
        self.is_visible = False
        self.monitoring = True
        
        # Performance tracking
        self.operation_start_times = {}  # Track multiple operations
        self.hang_threshold = 30  # seconds
        
        # Create window but keep it hidden
        self._create_window()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_performance, daemon=True)
        self.monitor_thread.start()
    
    def _create_window(self):
        """Create the debug window (initially hidden)"""
        self.window = tk.Toplevel()
        self.window.title("🐛 Debug Monitor - Weyland-Yutani")
        self.window.geometry("700x400")
        self.window.configure(bg=self.DOS_BG)
        
        # Hide window initially
        self.window.withdraw()
        
        # Header
        header = tk.Frame(self.window, bg=self.DOS_BG, padx=10, pady=5)
        header.pack(fill=tk.X)
        
        title = tk.Label(
            header,
            text="DEBUG MONITOR - ERROR TRACKING",
            font=self.DOS_FONT_BOLD,
            bg=self.DOS_BG,
            fg=self.DOS_FG
        )
        title.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            header,
            text="[NO ERRORS]",
            font=self.DOS_FONT,
            bg=self.DOS_BG,
            fg=self.DOS_FG
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # Main text area
        text_frame = tk.Frame(self.window, bg=self.DOS_BG, padx=10, pady=5)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=self.DOS_FONT,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            insertbackground=self.DOS_FG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colors
        self.text_widget.tag_config("error", foreground=self.DOS_FG_ERROR)
        self.text_widget.tag_config("warning", foreground=self.DOS_FG_WARNING)
        self.text_widget.tag_config("info", foreground=self.DOS_FG)
        
        # Button frame
        button_frame = tk.Frame(self.window, bg=self.DOS_BG, padx=10, pady=5)
        button_frame.pack(fill=tk.X)
        
        tk.Button(
            button_frame,
            text="[ CLEAR ]",
            command=self.clear,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="[ HIDE ]",
            command=self.hide,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        ).pack(side=tk.LEFT, padx=5)
        
        # Initial message
        self._log_info("Debug monitor initialized. Waiting for events...")
        self._log_info("Window will auto-show on errors or warnings.")
        self._log_info("=" * 60)
    
    def _log(self, message, tag="info", show_window=False):
        """Internal logging method"""
        if self.text_widget:
            timestamp = datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {message}\n"
            
            self.text_widget.insert(tk.END, full_message, tag)
            self.text_widget.see(tk.END)
            
            if show_window and not self.is_visible:
                self.show()
    
    def _log_info(self, message):
        """Log info message (green) - internal use"""
        self._log(message, "info", show_window=False)
    
    def log_info(self, message):
        """Log info message (green) - public method"""
        self._log(message, "info", show_window=False)
    
    def log_warning(self, message):
        """Log warning message (yellow) - shows window"""
        self.warning_count += 1
        self._update_status()
        self._log(f"⚠️  WARNING: {message}", "warning", show_window=True)
    
    def log_error(self, message, exception=None):
        """Log error message (red) - shows window"""
        self.error_count += 1
        self._update_status()
        self._log(f"❌ ERROR: {message}", "error", show_window=True)
        
        if exception:
            tb = traceback.format_exception(type(exception), exception, exception.__traceback__)
            for line in tb:
                self._log(line.rstrip(), "error", show_window=False)
    
    def log_exception(self, exc_type, exc_value, exc_traceback):
        """Log unhandled exception - shows window"""
        self.error_count += 1
        self._update_status()
        
        self._log("=" * 60, "error", show_window=True)
        self._log("🚨 UNHANDLED EXCEPTION DETECTED!", "error", show_window=False)
        self._log("=" * 60, "error", show_window=False)
        
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for line in tb_lines:
            self._log(line.rstrip(), "error", show_window=False)
        
        self._log("=" * 60, "error", show_window=False)
    
    def start_operation(self, operation_name):
        """Mark start of an operation (for hang detection)"""
        self.operation_start_times[operation_name] = time.time()
        self._log_info(f"▶️  Started: {operation_name}")
    
    def end_operation(self, operation_name):
        """Mark end of an operation"""
        if operation_name in self.operation_start_times:
            duration = time.time() - self.operation_start_times[operation_name]
            self._log_info(f"✓ Completed: {operation_name} ({duration:.2f}s)")
            del self.operation_start_times[operation_name]
    
    def _monitor_performance(self):
        """Background thread to monitor for hangs"""
        while self.monitoring:
            time.sleep(5)  # Check every 5 seconds
            
            # Check all running operations
            current_time = time.time()
            for op_name, start_time in list(self.operation_start_times.items()):
                elapsed = current_time - start_time
                
                if elapsed > self.hang_threshold:
                    self.log_warning(
                        f"Operation '{op_name}' running for {elapsed:.0f}s - possible hang detected!"
                    )
                    # Don't delete - let end_operation handle it
    
    def _update_status(self):
        """Update status label"""
        if self.error_count > 0 or self.warning_count > 0:
            status = f"[ERRORS: {self.error_count} | WARNINGS: {self.warning_count}]"
            self.status_label.config(text=status, fg=self.DOS_FG_ERROR if self.error_count > 0 else self.DOS_FG_WARNING)
        else:
            self.status_label.config(text="[NO ERRORS]", fg=self.DOS_FG)
    
    def show(self):
        """Show the debug window"""
        if not self.is_visible:
            self.window.deiconify()
            self.window.lift()
            self.is_visible = True
    
    def hide(self):
        """Hide the debug window"""
        if self.is_visible:
            self.window.withdraw()
            self.is_visible = False
    
    def clear(self):
        """Clear the debug log"""
        if self.text_widget:
            self.text_widget.delete(1.0, tk.END)
            self.error_count = 0
            self.warning_count = 0
            self._update_status()
            self._log_info("Debug log cleared.")
    
    def toggle(self):
        """Toggle window visibility"""
        if self.is_visible:
            self.hide()
        else:
            self.show()
    
    def destroy(self):
        """Clean up"""
        self.monitoring = False
        if self.window:
            self.window.destroy()


class DebugExceptionHandler:
    """
    Custom exception handler that logs to debug window
    """
    
    def __init__(self, debug_window):
        self.debug_window = debug_window
        self.original_excepthook = sys.excepthook
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        # Log to debug window
        self.debug_window.log_exception(exc_type, exc_value, exc_traceback)
        
        # Also call original handler
        self.original_excepthook(exc_type, exc_value, exc_traceback)
    
    def install(self):
        """Install this exception handler"""
        sys.excepthook = self.handle_exception
