"""
Main GUI Window for Weyland-Yutani Transmute Tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import MeshAnalyzer, MeshRepairer, StepConverter, MeshValidator, MeshSimplifier
from ui.debug_window import DebugWindow, DebugExceptionHandler


class TransmuteApp:
    """
    Main application window for STL repair and STEP conversion
    """
    
    # DOS Theme Colors
    DOS_BG = "#000000"  # Black background
    DOS_FG = "#00FF00"  # Bright green text
    DOS_FG_DIM = "#00AA00"  # Dim green
    DOS_HIGHLIGHT = "#00FF00"  # Bright green highlight
    DOS_FONT = ("Courier New", 10)
    DOS_FONT_BOLD = ("Courier New", 10, "bold")
    DOS_FONT_TITLE = ("Courier New", 14, "bold")
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Weyland-Yutani Transmute Tool")
        self.root.geometry("900x700")
        self.root.configure(bg=self.DOS_BG)
        
        # Initialize debug window
        self.debug_window = DebugWindow(root)
        
        # Install exception handler
        self.exception_handler = DebugExceptionHandler(self.debug_window)
        self.exception_handler.install()
        
        # Initialize processors
        self.analyzer = MeshAnalyzer()
        self.repairer = MeshRepairer()
        self.converter = StepConverter()
        self.validator = MeshValidator()
        self.simplifier = MeshSimplifier()
        
        # State
        self.current_file = None
        self.analysis_results = None
        self.repaired_mesh = None
        
        # Slider state
        self.current_faces_label = None
        self.target_faces_label = None
        self.reduction_percent_label = None
        self.simplify_slider = None
        self.simplify_slider_var = None
        
        self._create_ui()
        self._redirect_console()
        self._setup_keyboard_shortcuts()
        
        # Log startup
        self.debug_window.log_info("Application initialized successfully")
    
    def _create_ui(self):
        """Create the user interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.DOS_BG, padx=10, pady=10)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="WEYLAND-YUTANI TRANSMUTE TOOL",
            font=self.DOS_FONT_TITLE,
            bg=self.DOS_BG,
            fg=self.DOS_FG
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text='"Building Better Worlds... One Mesh at a Time"',
            font=self.DOS_FONT,
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.DOS_BG, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_frame, bg=self.DOS_BG, padx=5, pady=5)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # File selection
        file_frame = tk.LabelFrame(
            left_panel, 
            text="INPUT FILE", 
            bg=self.DOS_BG, 
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            padx=10, 
            pady=10
        )
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_label = tk.Label(
            file_frame, 
            text="No file selected", 
            wraplength=200,
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM,
            font=self.DOS_FONT,
            justify=tk.LEFT
        )
        self.file_label.pack()
        
        tk.Button(
            file_frame,
            text="[ LOAD STL FILE ]",
            command=self.load_file,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        ).pack(pady=5)
        
        # Analysis section
        analysis_frame = tk.LabelFrame(
            left_panel, 
            text="ANALYSIS", 
            bg=self.DOS_BG, 
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            padx=10, 
            pady=10
        )
        analysis_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            analysis_frame,
            text="[ ANALYZE MESH ]",
            command=self.analyze_mesh,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        ).pack(fill=tk.X, pady=2)
        
        # Repair section
        repair_frame = tk.LabelFrame(
            left_panel, 
            text="REPAIR", 
            bg=self.DOS_BG, 
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            padx=10, 
            pady=10
        )
        repair_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            repair_frame,
            text="[ REPAIR MESH ]",
            command=self.repair_mesh,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        ).pack(fill=tk.X, pady=2)
        
        # Simplification section
        simplify_frame = tk.LabelFrame(
            left_panel, 
            text="SIMPLIFY", 
            bg=self.DOS_BG, 
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            padx=10, 
            pady=10
        )
        simplify_frame.pack(fill=tk.X, pady=5)
        
        # Auto-simplify button
        tk.Button(
            simplify_frame,
            text="[ AUTO SIMPLIFY ]",
            command=self.auto_simplify_mesh,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        ).pack(fill=tk.X, pady=2)
        
        # Manual simplification controls
        manual_frame = tk.Frame(simplify_frame, bg=self.DOS_BG)
        manual_frame.pack(fill=tk.X, pady=5)
        
        # Current mesh info
        info_frame = tk.Frame(manual_frame, bg=self.DOS_BG)
        info_frame.pack(fill=tk.X, pady=(0,5))
        
        self.current_faces_label = tk.Label(
            info_frame,
            text="Current: -- faces",
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT
        )
        self.current_faces_label.pack(side=tk.LEFT)
        
        self.target_faces_label = tk.Label(
            info_frame,
            text="Target: -- faces",
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM,
            font=self.DOS_FONT
        )
        self.target_faces_label.pack(side=tk.LEFT, padx=(10,0))
        
        self.reduction_percent_label = tk.Label(
            info_frame,
            text="Reduction: --%",
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM,
            font=self.DOS_FONT
        )
        self.reduction_percent_label.pack(side=tk.RIGHT)
        
        # Slider for percentage reduction
        slider_frame = tk.Frame(manual_frame, bg=self.DOS_BG)
        slider_frame.pack(fill=tk.X, pady=2)
        
        slider_label = tk.Label(
            slider_frame,
            text="Simplify:",
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM,
            font=self.DOS_FONT
        )
        slider_label.pack(side=tk.LEFT)
        
        # Create slider variable
        self.simplify_slider_var = tk.DoubleVar(value=0.0)
        
        self.simplify_slider = tk.Scale(
            slider_frame,
            from_=0,
            to=95,
            resolution=5,
            orient=tk.HORIZONTAL,
            variable=self.simplify_slider_var,
            command=self._on_slider_change,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            troughcolor=self.DOS_BG,
            activebackground=self.DOS_FG,
            highlightthickness=0,
            font=self.DOS_FONT
        )
        self.simplify_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0))
        
        # Apply button for slider
        tk.Button(
            slider_frame,
            text="[APPLY]",
            command=self.apply_slider_simplification,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.DOS_FG,
            width=8
        ).pack(side=tk.RIGHT, padx=(5,0))
        
        # Face count reduction buttons
        faces_label = tk.Label(
            manual_frame,
            text="Reduce to faces:",
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM,
            font=self.DOS_FONT
        )
        faces_label.pack(anchor=tk.W, pady=(5,0))
        
        faces_buttons_frame = tk.Frame(manual_frame, bg=self.DOS_BG)
        faces_buttons_frame.pack(fill=tk.X, pady=2)
        
        for faces in [10000, 5000, 1000, 500]:
            tk.Button(
                faces_buttons_frame,
                text=f"[{faces}]",
                command=lambda f=faces: self.simplify_by_face_count(f),
                bg=self.DOS_BG,
                fg=self.DOS_FG,
                font=self.DOS_FONT,
                activebackground=self.DOS_FG,
                activeforeground=self.DOS_BG,
                relief=tk.FLAT,
                bd=1,
                highlightthickness=1,
                highlightbackground=self.DOS_FG,
                width=8
            ).pack(side=tk.LEFT, padx=1)
        
        # Reset button
        tk.Button(
            simplify_frame,
            text="[ RESET MESH ]",
            command=self.reset_mesh,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        ).pack(fill=tk.X, pady=5)
        
        # Export section
        export_frame = tk.LabelFrame(
            left_panel, 
            text="EXPORT", 
            bg=self.DOS_BG, 
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            padx=10, 
            pady=10
        )
        export_frame.pack(fill=tk.X, pady=5)
        
        self.export_stl_var = tk.BooleanVar(value=True)
        self.export_step_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            export_frame,
            text="Export STL",
            variable=self.export_stl_var,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT,
            selectcolor=self.DOS_BG,
            activebackground=self.DOS_BG,
            activeforeground=self.DOS_FG
        ).pack(anchor=tk.W)
        
        tk.Checkbutton(
            export_frame,
            text="Export STEP",
            variable=self.export_step_var,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT,
            selectcolor=self.DOS_BG,
            activebackground=self.DOS_BG,
            activeforeground=self.DOS_FG
        ).pack(anchor=tk.W)
        
        tk.Button(
            export_frame,
            text="[ EXPORT FILES ]",
            command=self.export_files,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        ).pack(fill=tk.X, pady=5)
        
        # Status section
        status_frame = tk.LabelFrame(
            left_panel, 
            text="STATUS", 
            bg=self.DOS_BG, 
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            padx=10, 
            pady=10
        )
        status_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.status_text = tk.Text(
            status_frame, 
            height=8, 
            width=30, 
            wrap=tk.WORD,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT,
            insertbackground=self.DOS_FG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)
        self._update_status("READY FOR TRANSMUTATION...")
        
        # Progress bar (custom DOS style)
        progress_container = tk.Frame(status_frame, bg=self.DOS_BG)
        progress_container.pack(fill=tk.X, pady=(5, 0))
        
        self.progress_var = tk.DoubleVar()
        self.progress_canvas = tk.Canvas(
            progress_container,
            height=20,
            width=400,  # Set minimum width
            bg=self.DOS_BG,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        )
        self.progress_canvas.pack(fill=tk.X)
        
        # Progress label
        self.progress_label = tk.Label(
            status_frame, 
            text="", 
            font=self.DOS_FONT,
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM
        )
        self.progress_label.pack(pady=(2, 0))
        
        # Right panel - Console output
        right_panel = tk.Frame(main_frame, bg=self.DOS_BG, padx=5, pady=5)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        console_frame = tk.LabelFrame(
            right_panel, 
            text="CONSOLE OUTPUT", 
            bg=self.DOS_BG, 
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            padx=10, 
            pady=10
        )
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        self.console_text = scrolledtext.ScrolledText(
            console_frame,
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
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        # Clear console button
        tk.Button(
            console_frame,
            text="[ CLEAR CONSOLE ]",
            command=self.clear_console,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        ).pack(pady=5)
    
    def _redirect_console(self):
        """Redirect print statements to console widget"""
        class ConsoleRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget
            
            def write(self, text):
                try:
                    self.text_widget.insert(tk.END, text)
                    self.text_widget.see(tk.END)
                    self.text_widget.update()
                except tk.TclError:
                    # Widget has been destroyed
                    pass
            
            def flush(self):
                pass
        
        sys.stdout = ConsoleRedirector(self.console_text)
    
    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Ctrl+D to toggle debug window
        self.root.bind('<Control-d>', lambda e: self.debug_window.toggle())
        self.root.bind('<Control-D>', lambda e: self.debug_window.toggle())
    
    def _update_status(self, message):
        """Update status text"""
        try:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(1.0, message)
        except tk.TclError:
            # Widget has been destroyed
            pass
    
    def _update_progress(self, percent, label=""):
        """Update progress bar and label (DOS style)"""
        try:
            self.progress_var.set(percent)
            self.progress_label.config(text=label)
            
            # Draw custom DOS-style progress bar
            width = max(self.progress_canvas.winfo_width(), 400)  # Use at least 400px width
            height = 20
            
            self.progress_canvas.delete("all")
            
            # Calculate filled width
            filled_width = int((width - 4) * (percent / 100))
            
            # Draw filled portion (green)
            if filled_width > 0:
                self.progress_canvas.create_rectangle(
                    2, 2, filled_width + 2, height - 2,
                    fill=self.DOS_FG,
                    outline=""
                )
            
            # Draw percentage text
            percent_text = f"{int(percent)}%"
            self.progress_canvas.create_text(
                width // 2, height // 2,
                text=percent_text,
                fill=self.DOS_BG if percent > 50 else self.DOS_FG,
                font=self.DOS_FONT_BOLD
            )
            
            # Force UI update
            self.root.update_idletasks()
        except tk.TclError:
            # Widget has been destroyed
            pass
        
        self.root.update_idletasks()
    
    def _reset_progress(self):
        """Reset progress bar"""
        try:
            self.progress_var.set(0)
            self.progress_label.config(text="")
            self.progress_canvas.delete("all")
        except tk.TclError:
            # Widget has been destroyed
            pass
    
    def clear_console(self):
        """Clear console output"""
        try:
            self.console_text.delete(1.0, tk.END)
        except tk.TclError:
            # Widget has been destroyed
            pass
    
    def load_file(self):
        """Load an STL file"""
        try:
            self.debug_window.start_operation("load_file")
            self.debug_window.log_info("Opening file dialog...")
            
            file_path = filedialog.askopenfilename(
                title="Select STL File",
                filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
            )
            
            if file_path:
                self.current_file = file_path
                file_name = Path(file_path).name
                self.file_label.config(text=file_name)
                self._update_status(f"Loaded: {file_name}")
                print(f"\n✓ File selected: {file_name}")
                self.debug_window.log_info(f"File loaded successfully: {file_name}")
                
                # Reset slider to 0 and update labels
                if self.simplify_slider_var:
                    self.simplify_slider_var.set(0.0)
                    self._on_slider_change("0")
            else:
                self.debug_window.log_info("File selection cancelled")
            
            self.debug_window.end_operation("load_file")
        except Exception as e:
            self.debug_window.log_error(f"Error loading file: {str(e)}")
            self.debug_window.end_operation("load_file")
            raise
    
    def analyze_mesh(self):
        """Analyze the loaded mesh"""
        try:
            if not self.current_file:
                self.debug_window.log_warning("Analyze attempted without file loaded")
                messagebox.showwarning("No File", "Please load an STL file first")
                return
            
            self.debug_window.start_operation("analyze_mesh")
            self.debug_window.log_info(f"Starting mesh analysis: {Path(self.current_file).name}")
            self._update_status("Analyzing mesh...")
            
            if self.analyzer.load_mesh(self.current_file):
                self.analysis_results = self.analyzer.analyze()
                
                # Update status with results
                severity = self.analysis_results.get("severity", "unknown")
                issue_count = len(self.analysis_results.get("issues", []))
                
                status_msg = f"Analysis complete\n"
                status_msg += f"Severity: {severity.upper()}\n"
                status_msg += f"Issues: {issue_count}"
                
                self._update_status(status_msg)
                self.debug_window.log_info(f"Analysis complete - Severity: {severity}, Issues: {issue_count}")
                
                if severity in ["critical", "high"]:
                    self.debug_window.log_warning(f"Mesh has {severity} severity issues")
            else:
                self._update_status("Analysis failed")
                self.debug_window.log_error("Failed to load mesh for analysis")
                messagebox.showerror("Error", "Failed to analyze mesh")
            
            self.debug_window.end_operation("analyze_mesh")
        except Exception as e:
            self.debug_window.log_error(f"Error during mesh analysis: {str(e)}")
            self.debug_window.end_operation("analyze_mesh")
            raise
    
    def repair_mesh(self):
        """Repair the loaded mesh"""
        try:
            if not self.current_file:
                self.debug_window.log_warning("Repair attempted without file loaded")
                messagebox.showwarning("No File", "Please load an STL file first")
                return
            
            if not self.analysis_results:
                self.debug_window.log_warning("Repair attempted without analysis")
                messagebox.showinfo("Analyze First", "Please analyze the mesh first")
                return
            
            self.debug_window.start_operation("repair_mesh")
            self.debug_window.log_info("Starting mesh repair...")
            self._update_status("Repairing mesh...")
            self._reset_progress()
            
            # Load mesh into repairer
            if self.analyzer.mesh:
                # Set up progress callback
                def progress_callback(step, total, message):
                    percent = (step / total) * 100
                    self._update_progress(percent, message)
                    self.debug_window.log_info(f"Repair progress: {int(percent)}% - {message}")
                
                self.repairer.load_mesh(self.analyzer.mesh)
                self.repaired_mesh = self.repairer.repair(progress_callback=progress_callback)
                
                # Validate repaired mesh
                self._update_progress(100, "Validating...")
                self.debug_window.log_info("Validating repaired mesh...")
                validation = self.validator.validate_mesh(self.repaired_mesh)
                
                self._reset_progress()
                
                if validation["is_valid"]:
                    self._update_status("Repair successful!\nMesh is valid")
                    self.debug_window.log_info("Mesh repair completed successfully - validation passed")
                    messagebox.showinfo("Success", "Mesh repaired successfully!")
                    
                    # Update slider labels with repaired mesh info
                    if self.simplify_slider_var:
                        self.simplify_slider_var.set(0.0)
                        self._on_slider_change("0")
                else:
                    self._update_status("Repair complete\nWarnings present")
                    warning_count = len(validation.get("warnings", []))
                    self.debug_window.log_warning(f"Mesh repaired but has {warning_count} validation warnings")
                    messagebox.showwarning(
                        "Partial Success",
                        "Mesh repaired but validation warnings present"
                    )
            else:
                self._update_status("Repair failed")
                self.debug_window.log_error("No mesh available for repair")
                messagebox.showerror("Error", "Failed to repair mesh")
            
            self.debug_window.end_operation("repair_mesh")
        except Exception as e:
            self.debug_window.log_error(f"Error during mesh repair: {str(e)}")
            self.debug_window.end_operation("repair_mesh")
            raise
    
    def auto_simplify_mesh(self):
        """Automatically simplify mesh for STEP conversion"""
        try:
            if not self.repaired_mesh:
                self.debug_window.log_warning("Auto-simplify attempted without repaired mesh")
                messagebox.showwarning("No Mesh", "Please repair the mesh first")
                return
            
            self.debug_window.start_operation("auto_simplify")
            self.debug_window.log_info("Starting automatic mesh simplification...")
            self._update_status("Auto-simplifying mesh...")
            self._reset_progress()
            
            # Load mesh into simplifier
            self.simplifier.load_mesh(self.repaired_mesh)
            
            # Perform auto-simplification
            success, message, was_simplified = self.simplifier.auto_simplify_for_step()
            
            if success:
                if was_simplified:
                    self.repaired_mesh = self.simplifier.get_current_mesh()
                    self._update_status(f"Auto-simplified: {message}")
                    self.debug_window.log_info(f"Auto-simplification successful: {message}")
                    messagebox.showinfo("Auto-Simplified", message)
                else:
                    self._update_status("Mesh complexity OK - no simplification needed")
                    self.debug_window.log_info("Auto-simplification: No changes needed")
                    messagebox.showinfo("No Changes", "Mesh complexity is acceptable for STEP conversion")
            else:
                self._update_status("Auto-simplification failed")
                self.debug_window.log_error(f"Auto-simplification failed: {message}")
                messagebox.showerror("Error", f"Auto-simplification failed: {message}")
            
            self.debug_window.end_operation("auto_simplify")
        except Exception as e:
            self.debug_window.log_error(f"Error during auto-simplification: {str(e)}")
            self.debug_window.end_operation("auto_simplify")
            raise
    
    def simplify_by_percentage(self, percentage):
        """Simplify mesh by percentage reduction"""
        try:
            if not self.repaired_mesh:
                self.debug_window.log_warning("Simplify attempted without repaired mesh")
                messagebox.showwarning("No Mesh", "Please repair the mesh first")
                return
            
            self.debug_window.start_operation("simplify_percentage")
            self.debug_window.log_info(f"Starting {percentage*100:.0f}% mesh simplification...")
            self._update_status(f"Simplifying to {percentage*100:.0f}%...")
            self._reset_progress()
            
            # Load mesh into simplifier
            self.simplifier.load_mesh(self.repaired_mesh)
            
            # Perform simplification
            success, message = self.simplifier.simplify_by_percentage(percentage)
            
            if success:
                self.repaired_mesh = self.simplifier.get_current_mesh()
                self._update_status(f"Simplified: {message}")
                self.debug_window.log_info(f"Percentage simplification successful: {message}")
                messagebox.showinfo("Simplified", message)
            else:
                self._update_status("Simplification failed")
                self.debug_window.log_error(f"Percentage simplification failed: {message}")
                messagebox.showerror("Error", f"Simplification failed: {message}")
            
            self.debug_window.end_operation("simplify_percentage")
        except Exception as e:
            self.debug_window.log_error(f"Error during percentage simplification: {str(e)}")
            self.debug_window.end_operation("simplify_percentage")
            raise
    
    def simplify_by_face_count(self, target_faces):
        """Simplify mesh to specific face count"""
        try:
            if not self.repaired_mesh:
                self.debug_window.log_warning("Simplify attempted without repaired mesh")
                messagebox.showwarning("No Mesh", "Please repair the mesh first")
                return
            
            self.debug_window.start_operation("simplify_faces")
            self.debug_window.log_info(f"Starting simplification to {target_faces} faces...")
            self._update_status(f"Simplifying to {target_faces} faces...")
            self._reset_progress()
            
            # Load mesh into simplifier
            self.simplifier.load_mesh(self.repaired_mesh)
            
            # Perform simplification
            success, message = self.simplifier.simplify_by_face_count(target_faces)
            
            if success:
                self.repaired_mesh = self.simplifier.get_current_mesh()
                self._update_status(f"Simplified: {message}")
                self.debug_window.log_info(f"Face count simplification successful: {message}")
                messagebox.showinfo("Simplified", message)
            else:
                self._update_status("Simplification failed")
                self.debug_window.log_error(f"Face count simplification failed: {message}")
                messagebox.showerror("Error", f"Simplification failed: {message}")
            
            self.debug_window.end_operation("simplify_faces")
        except Exception as e:
            self.debug_window.log_error(f"Error during face count simplification: {str(e)}")
            self.debug_window.end_operation("simplify_faces")
            raise
    
    def reset_mesh(self):
        """Reset mesh to post-repair state"""
        try:
            if not self.repaired_mesh:
                self.debug_window.log_warning("Reset attempted without repaired mesh")
                messagebox.showwarning("No Mesh", "Please repair the mesh first")
                return
            
            self.debug_window.start_operation("reset_mesh")
            self.debug_window.log_info("Resetting mesh to post-repair state...")
            
            # Reset simplifier to original repaired mesh
            self.simplifier.reset()
            self.repaired_mesh = self.simplifier.get_current_mesh()
            
            original_stats = self.simplifier.get_original_stats()
            self._update_status(f"Mesh reset to {original_stats.get('faces', 0)} faces")
            self.debug_window.log_info(f"Mesh reset to {original_stats.get('faces', 0)} faces")
            messagebox.showinfo("Reset", f"Mesh reset to {original_stats.get('faces', 0)} faces")
            
            self.debug_window.end_operation("reset_mesh")
        except Exception as e:
            self.debug_window.log_error(f"Error during mesh reset: {str(e)}")
            self.debug_window.end_operation("reset_mesh")
            raise
    
    def _on_slider_change(self, value):
        """Update labels when slider value changes"""
        try:
            if not self.repaired_mesh:
                return
            
            reduction_percent = float(value)
            current_faces = len(self.repaired_mesh.faces)
            target_faces = max(4, int(current_faces * (1.0 - reduction_percent / 100.0)))
            
            # Update labels
            self.current_faces_label.config(text=f"Current: {current_faces:,} faces")
            self.target_faces_label.config(text=f"Target: {target_faces:,} faces")
            self.reduction_percent_label.config(text=f"Reduction: {reduction_percent:.0f}%")
            
        except Exception as e:
            # Silently handle errors during slider updates
            pass
    
    def apply_slider_simplification(self):
        """Apply simplification based on current slider value"""
        try:
            if not self.repaired_mesh:
                self.debug_window.log_warning("Slider simplify attempted without repaired mesh")
                messagebox.showwarning("No Mesh", "Please repair the mesh first")
                return
            
            reduction_percent = self.simplify_slider_var.get()
            if reduction_percent <= 0:
                messagebox.showinfo("No Change", "Please set a reduction percentage greater than 0%")
                return
            
            percentage = 1.0 - (reduction_percent / 100.0)
            
            self.debug_window.start_operation("slider_simplify")
            self.debug_window.log_info(f"Starting {reduction_percent:.0f}% slider simplification...")
            self._update_status(f"Simplifying to {reduction_percent:.0f}% reduction...")
            self._reset_progress()
            
            # Load mesh into simplifier
            self.simplifier.load_mesh(self.repaired_mesh)
            
            # Perform simplification
            success, message = self.simplifier.simplify_by_percentage(percentage)
            
            if success:
                self.repaired_mesh = self.simplifier.get_current_mesh()
                self._update_status(f"Simplified: {message}")
                self.debug_window.log_info(f"Slider simplification successful: {message}")
                messagebox.showinfo("Simplified", message)
                
                # Update slider labels with new current face count
                self._on_slider_change(str(reduction_percent))
                
            else:
                self._update_status("Simplification failed")
                self.debug_window.log_error(f"Slider simplification failed: {message}")
                messagebox.showerror("Error", f"Simplification failed: {message}")
            
            self.debug_window.end_operation("slider_simplify")
        except Exception as e:
            self.debug_window.log_error(f"Error during slider simplification: {str(e)}")
            self.debug_window.end_operation("slider_simplify")
            raise
    
    def export_files(self):
        """Export repaired mesh and/or STEP file"""
        try:
            if not self.repaired_mesh:
                self.debug_window.log_warning("Export attempted without repaired mesh")
                messagebox.showwarning("No Repair", "Please repair the mesh first")
                return
            
            self.debug_window.start_operation("export_files")
            self.debug_window.log_info("Opening output directory dialog...")
            
            # Get output directory
            output_dir = filedialog.askdirectory(title="Select Output Directory")
            if not output_dir:
                self.debug_window.log_info("Export cancelled by user")
                self.debug_window.end_operation("export_files")
                return
            
            output_path = Path(output_dir)
            base_name = Path(self.current_file).stem + "_repaired"
            self.debug_window.log_info(f"Exporting to: {output_dir}")
            
            success_count = 0
            
            # Export STL
            if self.export_stl_var.get():
                stl_path = output_path / f"{base_name}.stl"
                self.debug_window.log_info(f"Exporting STL: {stl_path.name}")
                if self.repairer.save_repaired_mesh(str(stl_path)):
                    success_count += 1
                    self.debug_window.log_info("STL export successful")
                else:
                    self.debug_window.log_error("STL export failed")
            
            # Export STEP
            if self.export_step_var.get():
                if self.converter.is_available():
                    step_path = output_path / f"{base_name}.step"
                    self.debug_window.log_info(f"Exporting STEP: {step_path.name}")
                    self.converter.load_mesh(self.repaired_mesh)
                    success, error_msg = self.converter.convert_to_step(str(step_path))
                    if success:
                        success_count += 1
                        self.debug_window.log_info("STEP export successful")
                    else:
                        self.debug_window.log_error(f"STEP export failed: {error_msg}")
                        # Show detailed error to user
                        messagebox.showerror(
                            "STEP Export Failed",
                            f"STEP export failed:\n{error_msg}\n\nSTL export succeeded."
                        )
                else:
                    self.debug_window.log_warning("FreeCAD not available for STEP export")
                    messagebox.showwarning(
                        "STEP Unavailable",
                        "FreeCAD not installed. STEP export unavailable."
                    )
            
            if success_count > 0:
                self._update_status(f"Export complete!\n{success_count} file(s) saved")
                self.debug_window.log_info(f"Export completed successfully - {success_count} file(s) saved")
                messagebox.showinfo("Success", f"Exported {success_count} file(s)")
            else:
                self._update_status("Export failed")
                self.debug_window.log_error("All export operations failed")
                messagebox.showerror("Error", "Export failed")
            
            self.debug_window.end_operation("export_files")
        except Exception as e:
            self.debug_window.log_error(f"Error during export: {str(e)}")
            self.debug_window.end_operation("export_files")
            raise
