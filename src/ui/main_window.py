"""
Main GUI Window for Weyland-Yutani Transmute Tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import MeshAnalyzer, MeshRepairer, StepConverter, MeshValidator, MeshSimplifier
from ui.debug_window import DebugWindow, DebugExceptionHandler

# Try to import pygame for audio (optional)
try:
    import pygame
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: pygame not available - audio features disabled")


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
        self.root.geometry("1200x950")  # Increased width to ensure audio controls fit
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
        
        # Audio state
        self.audio_enabled = AUDIO_AVAILABLE
        self.audio_muted = False
        self.audio_volume = 0.5  # 50% volume
        self.audio_playing = False
        self.audio_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Spybreak!Short One Propellerheads.mp3")
        
        # Initialize audio if available
        if self.audio_enabled:
            self._init_audio()
        
        self._create_ui()
        self.root.update()  # Force UI update to ensure all widgets are displayed
        self._redirect_console()
        self._setup_keyboard_shortcuts()
        
        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Log startup
        self.debug_window.log_info("Application initialized successfully")
    
    def _init_audio(self):
        """Initialize pygame audio system"""
        try:
            pygame.mixer.init()
            if os.path.exists(self.audio_file):
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.set_volume(self.audio_volume)
                self.debug_window.log_info("Audio system initialized")
            else:
                self.debug_window.log_warning(f"Audio file not found: {self.audio_file}")
                self.audio_enabled = False
        except Exception as e:
            self.debug_window.log_error(f"Failed to initialize audio: {e}")
            self.audio_enabled = False
    
    def _create_ui(self):
        """Create the user interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.DOS_BG, padx=10, pady=10)
        header_frame.pack(fill=tk.X)
        
        # Title section (left side)
        title_frame = tk.Frame(header_frame, bg=self.DOS_BG)
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(
            title_frame,
            text="WEYLAND-YUTANI TRANSMUTE TOOL",
            font=self.DOS_FONT_TITLE,
            bg=self.DOS_BG,
            fg=self.DOS_FG
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text='"Building Better Worlds... One Mesh at a Time"',
            font=self.DOS_FONT,
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM
        )
        subtitle_label.pack()
        
        # Audio controls (right side)
        if self.audio_enabled:
            audio_frame = tk.Frame(header_frame, bg=self.DOS_BG)
            audio_frame.pack(side=tk.RIGHT, padx=(20,0))
            
            # Mute button
            self.mute_button = tk.Button(
                audio_frame,
                text="[🔊 MUTE]",
                command=self.toggle_mute,
                bg=self.DOS_BG,
                fg=self.DOS_FG,
                font=self.DOS_FONT,
                activebackground=self.DOS_FG,
                activeforeground=self.DOS_BG,
                relief=tk.RAISED,
                bd=2,
                highlightthickness=1,
                highlightbackground=self.DOS_FG
            )
            self.mute_button.pack(side=tk.LEFT, padx=(0,5))
            
            # Volume slider
            volume_label = tk.Label(
                audio_frame,
                text="VOL:",
                bg=self.DOS_BG,
                fg=self.DOS_FG_DIM,
                font=self.DOS_FONT
            )
            volume_label.pack(side=tk.LEFT)
            
            self.volume_var = tk.DoubleVar(value=self.audio_volume * 100)
            self.volume_slider = tk.Scale(
                audio_frame,
                from_=0,
                to=100,
                resolution=5,
                orient=tk.HORIZONTAL,
                variable=self.volume_var,
                command=self._on_volume_change,
                bg=self.DOS_BG,
                fg=self.DOS_FG,
                troughcolor=self.DOS_BG,
                activebackground=self.DOS_FG,
                highlightthickness=0,
                font=self.DOS_FONT,
                length=100
            )
            self.volume_slider.pack(side=tk.LEFT)
        
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
            command=self._load_file_with_audio,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.RAISED,
            bd=3,
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
            command=self._analyze_mesh_with_audio,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.RAISED,
            bd=3,
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
            command=self._repair_mesh_with_audio,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.RAISED,
            bd=3,
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
            command=self._auto_simplify_mesh_with_audio,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.RAISED,
            bd=3,
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
            resolution=1,
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
            command=self._apply_slider_simplification_with_audio,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.RAISED,
            bd=2,
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
                command=lambda f=faces: self._simplify_by_face_count_with_audio(f),
                bg=self.DOS_BG,
                fg=self.DOS_FG,
                font=self.DOS_FONT,
                activebackground=self.DOS_FG,
                activeforeground=self.DOS_BG,
                relief=tk.RAISED,
                bd=2,
                highlightthickness=1,
                highlightbackground=self.DOS_FG,
                width=8
            ).pack(side=tk.LEFT, padx=1)
        
        # Reset button
        tk.Button(
            simplify_frame,
            text="[ RESET MESH ]",
            command=self._reset_mesh_with_audio,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.RAISED,
            bd=3,
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
            command=self._export_files_with_audio,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            font=self.DOS_FONT_BOLD,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.RAISED,
            bd=3,
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
            command=self._clear_console_with_audio,
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
                self._show_dos_message("NO FILE", "Please load an STL file first", "warning")
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
                self._show_dos_message("ERROR", "Failed to analyze mesh", "error")
            
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
                self._show_dos_message("NO FILE", "Please load an STL file first", "warning")
                return
            
            if not self.analysis_results:
                self.debug_window.log_warning("Repair attempted without analysis")
                self._show_dos_message("ANALYZE FIRST", "Please analyze the mesh first", "warning")
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
                    self._show_dos_message("SUCCESS", "Mesh repaired successfully!", "success")
                    
                    # Update slider labels with repaired mesh info
                    if self.simplify_slider_var:
                        self.simplify_slider_var.set(0.0)
                        self._on_slider_change("0")
                else:
                    self._update_status("Repair complete\nWarnings present")
                    warning_count = len(validation.get("warnings", []))
                    self.debug_window.log_warning(f"Mesh repaired but has {warning_count} validation warnings")
                    self._show_dos_message("PARTIAL SUCCESS", "Mesh repaired but validation warnings present", "warning")
            else:
                self._update_status("Repair failed")
                self.debug_window.log_error("No mesh available for repair")
                self._show_dos_message("ERROR", "Failed to repair mesh", "error")
            
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
                self._show_dos_message("NO MESH", "Please repair the mesh first", "warning")
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
                    self._show_dos_message("AUTO-SIMPLIFIED", message, "success")
                else:
                    self._update_status("Mesh complexity OK - no simplification needed")
                    self.debug_window.log_info("Auto-simplification: No changes needed")
                    self._show_dos_message("NO CHANGES", "Mesh complexity is acceptable for STEP conversion", "info")
            else:
                self._update_status("Auto-simplification failed")
                self.debug_window.log_error(f"Auto-simplification failed: {message}")
                self._show_dos_message("ERROR", f"Auto-simplification failed: {message}", "error")
            
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
                self._show_dos_message("NO MESH", "Please repair the mesh first", "warning")
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
                self._show_dos_message("SIMPLIFIED", message, "success")
            else:
                self._update_status("Simplification failed")
                self.debug_window.log_error(f"Percentage simplification failed: {message}")
                self._show_dos_message("ERROR", f"Simplification failed: {message}", "error")
            
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
                self._show_dos_message("NO MESH", "Please repair the mesh first", "warning")
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
                self._show_dos_message("SIMPLIFIED", message, "success")
            else:
                self._update_status("Simplification failed")
                self.debug_window.log_error(f"Face count simplification failed: {message}")
                self._show_dos_message("ERROR", f"Simplification failed: {message}", "error")
            
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
                self._show_dos_message("NO MESH", "Please repair the mesh first", "warning")
                return
            
            self.debug_window.start_operation("reset_mesh")
            self.debug_window.log_info("Resetting mesh to post-repair state...")
            
            # Reset simplifier to original repaired mesh
            self.simplifier.reset()
            self.repaired_mesh = self.simplifier.get_current_mesh()
            
            original_stats = self.simplifier.get_original_stats()
            self._update_status(f"Mesh reset to {original_stats.get('faces', 0)} faces")
            self.debug_window.log_info(f"Mesh reset to {original_stats.get('faces', 0)} faces")
            self._show_dos_message("RESET", f"Mesh reset to {original_stats.get('faces', 0)} faces", "info")
            
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
                self._show_dos_message("NO MESH", "Please repair the mesh first", "warning")
                return
            
            reduction_percent = self.simplify_slider_var.get()
            if reduction_percent <= 0:
                self._show_dos_message("NO CHANGE", "Please set a reduction percentage greater than 0%", "info")
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
                self._show_dos_message("SIMPLIFIED", message, "success")
                
                # Update slider labels with new current face count
                self._on_slider_change(str(reduction_percent))
                
            else:
                self._update_status("Simplification failed")
                self.debug_window.log_error(f"Slider simplification failed: {message}")
                self._show_dos_message("ERROR", f"Simplification failed: {message}", "error")
            
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
                self._show_dos_message("NO REPAIR", "Please repair the mesh first", "warning")
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
                        self._show_dos_message("STEP EXPORT FAILED", f"STEP export failed:\n{error_msg}\n\nSTL export succeeded.", "error")
                else:
                    self.debug_window.log_warning("FreeCAD not available for STEP export")
                    self._show_dos_message("STEP UNAVAILABLE", "FreeCAD not installed. STEP export unavailable.", "warning")
            
            if success_count > 0:
                self._update_status(f"Export complete!\n{success_count} file(s) saved")
                self.debug_window.log_info(f"Export completed successfully - {success_count} file(s) saved")
                self._show_dos_message("SUCCESS", f"Exported {success_count} file(s)", "success")
            else:
                self._update_status("Export failed")
                self.debug_window.log_error("All export operations failed")
                self._show_dos_message("ERROR", "Export failed", "error")
            
            self.debug_window.end_operation("export_files")
        except Exception as e:
            self.debug_window.log_error(f"Error during export: {str(e)}")
            self.debug_window.end_operation("export_files")
            raise
    
    def toggle_mute(self):
        """Toggle audio mute state"""
        if not self.audio_enabled:
            return
        
        self.audio_muted = not self.audio_muted
        
        if self.audio_muted:
            pygame.mixer.music.set_volume(0.0)
            self.mute_button.config(text="[🔇 UNMUTE]")
            self.debug_window.log_info("Audio muted")
        else:
            pygame.mixer.music.set_volume(self.audio_volume)
            self.mute_button.config(text="[🔊 MUTE]")
            self.debug_window.log_info("Audio unmuted")
    
    def _on_volume_change(self, value):
        """Handle volume slider changes"""
        if not self.audio_enabled:
            return
        
        self.audio_volume = float(value) / 100.0
        
        if not self.audio_muted:
            pygame.mixer.music.set_volume(self.audio_volume)
        
        self.debug_window.log_info(f"Volume set to {int(float(value))}%")
    
    def _play_audio_on_interaction(self):
        """Play audio when user interacts with the application"""
        if not self.audio_enabled or self.audio_muted:
            return
        
        try:
            if not self.audio_playing:
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                self.audio_playing = True
                self.debug_window.log_info("Audio playback started")
        except Exception as e:
            self.debug_window.log_error(f"Failed to play audio: {e}")
            self.audio_enabled = False
    
    # Audio-enabled wrapper functions for buttons
    def _load_file_with_audio(self):
        self._play_audio_on_interaction()
        self._show_progress_dialog("Loading File")
        self.load_file()
    
    def _analyze_mesh_with_audio(self):
        self._play_audio_on_interaction()
        self._show_progress_dialog("Analyzing Mesh")
        self.analyze_mesh()
    
    def _repair_mesh_with_audio(self):
        self._play_audio_on_interaction()
        self._show_progress_dialog("Repairing Mesh")
        self.repair_mesh()
    
    def _auto_simplify_mesh_with_audio(self):
        self._play_audio_on_interaction()
        self._show_progress_dialog("Auto Simplifying")
        self.auto_simplify_mesh()
    
    def _apply_slider_simplification_with_audio(self):
        self._play_audio_on_interaction()
        self._show_progress_dialog("Applying Simplification")
        self.apply_slider_simplification()
    
    def _simplify_by_face_count_with_audio(self, faces):
        self._play_audio_on_interaction()
        self._show_progress_dialog(f"Reducing to {faces} Faces")
        self.simplify_by_face_count(faces)
    
    def _reset_mesh_with_audio(self):
        self._play_audio_on_interaction()
        self._show_progress_dialog("Resetting Mesh")
        self.reset_mesh()
    
    def _export_files_with_audio(self):
        self._play_audio_on_interaction()
        self._show_progress_dialog("Exporting Files")
        self.export_files()
    
    def _clear_console_with_audio(self):
        self._play_audio_on_interaction()
        self._show_progress_dialog("Clearing Console")
        self.clear_console()
    
    def _on_window_close(self):
        """Handle window close event"""
        try:
            # Stop audio if playing
            if self.audio_enabled and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            
            # Clean up debug window
            if self.debug_window:
                self.debug_window.monitoring = False
            
            # Destroy the window and quit
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            # Force quit if cleanup fails
            self.root.quit()
            self.root.destroy()
    
    def _show_progress_dialog(self, operation_name, duration=3.5):
        """Show a DOS-style progress dialog with spinning animation"""
        import threading
        import time
        
        # Create progress dialog
        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title("PROCESSING...")
        progress_dialog.geometry("400x150")
        progress_dialog.configure(bg=self.DOS_BG)
        progress_dialog.resizable(False, False)
        progress_dialog.transient(self.root)
        progress_dialog.grab_set()
        
        # Center the dialog
        progress_dialog.geometry("+{}+{}".format(
            self.root.winfo_x() + (self.root.winfo_width() // 2) - 200,
            self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        ))
        
        # Title
        title_label = tk.Label(
            progress_dialog,
            text=f"⚙️  {operation_name.upper()}",
            font=self.DOS_FONT_BOLD,
            bg=self.DOS_BG,
            fg=self.DOS_FG
        )
        title_label.pack(pady=(20, 10))
        
        # Progress bar frame
        progress_frame = tk.Frame(progress_dialog, bg=self.DOS_BG)
        progress_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        progress_bar = tk.Canvas(
            progress_frame,
            height=20,
            bg=self.DOS_BG,
            highlightthickness=1,
            highlightbackground=self.DOS_FG
        )
        progress_bar.pack(fill=tk.X)
        
        # Status text
        status_label = tk.Label(
            progress_dialog,
            text="INITIALIZING...",
            font=self.DOS_FONT,
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM
        )
        status_label.pack(pady=(0, 20))
        
        # Spinning animation characters
        spin_chars = ["|", "/", "-", "\\"]
        spin_index = 0
        
        def update_progress():
            """Update progress bar and spinning animation"""
            nonlocal spin_index
            start_time = time.time()
            
            while time.time() - start_time < duration:
                elapsed = time.time() - start_time
                progress = min(elapsed / duration, 1.0)
                
                # Update progress bar
                self.progress_var.set(progress * 100)
                progress_bar.delete("all")
                progress_bar.create_rectangle(
                    2, 2, 
                    2 + (progress_bar.winfo_width() - 4) * progress, 
                    18,
                    fill=self.DOS_FG,
                    outline=self.DOS_FG
                )
                
                # Update spinning animation
                spin_char = spin_chars[spin_index % len(spin_chars)]
                status_label.config(text=f"PROCESSING {spin_char}")
                spin_index += 1
                
                # Update dialog
                progress_dialog.update()
                time.sleep(0.1)
            
            # Final update
            self.progress_var.set(100)
            progress_bar.delete("all")
            progress_bar.create_rectangle(
                2, 2, progress_bar.winfo_width() - 2, 18,
                fill=self.DOS_FG,
                outline=self.DOS_FG
            )
            status_label.config(text="COMPLETE ✓")
            progress_dialog.update()
            time.sleep(0.3)  # Brief pause to show completion
            
            # Close dialog
            progress_dialog.destroy()
        
        # Start progress animation in separate thread
        progress_thread = threading.Thread(target=update_progress, daemon=True)
        progress_thread.start()
        
        # Wait for completion (but allow dialog to be modal)
        self.root.wait_window(progress_dialog)
    
    def _show_dos_message(self, title, message, message_type="info"):
        """Show a DOS-themed message dialog"""
        # Create message dialog
        message_dialog = tk.Toplevel(self.root)
        message_dialog.title(f"[{title.upper()}]")
        message_dialog.geometry("450x200")
        message_dialog.configure(bg=self.DOS_BG)
        message_dialog.resizable(False, False)
        message_dialog.transient(self.root)
        message_dialog.grab_set()
        
        # Center the dialog
        message_dialog.geometry("+{}+{}".format(
            self.root.winfo_x() + (self.root.winfo_width() // 2) - 225,
            self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
        ))
        
        # Icon based on message type
        icon_map = {
            "info": "ℹ️",
            "success": "✅", 
            "warning": "⚠️",
            "error": "❌"
        }
        icon = icon_map.get(message_type, "ℹ️")
        
        # Title with icon
        title_frame = tk.Frame(message_dialog, bg=self.DOS_BG)
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            title_frame,
            text=f"{icon} {title.upper()}",
            font=self.DOS_FONT_BOLD,
            bg=self.DOS_BG,
            fg=self.DOS_FG
        )
        title_label.pack()
        
        # Message text
        message_frame = tk.Frame(message_dialog, bg=self.DOS_BG)
        message_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        message_label = tk.Label(
            message_frame,
            text=message,
            font=self.DOS_FONT,
            bg=self.DOS_BG,
            fg=self.DOS_FG_DIM,
            wraplength=380,
            justify=tk.LEFT
        )
        message_label.pack()
        
        # OK button
        button_frame = tk.Frame(message_dialog, bg=self.DOS_BG)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        ok_button = tk.Button(
            button_frame,
            text="[ OK ]",
            command=message_dialog.destroy,
            font=self.DOS_FONT_BOLD,
            bg=self.DOS_BG,
            fg=self.DOS_FG,
            activebackground=self.DOS_FG,
            activeforeground=self.DOS_BG,
            relief=tk.RAISED,
            bd=3,
            highlightthickness=1,
            highlightbackground=self.DOS_FG,
            width=10
        )
        ok_button.pack()
        
        # Handle Enter key
        message_dialog.bind('<Return>', lambda e: message_dialog.destroy())
        message_dialog.bind('<Escape>', lambda e: message_dialog.destroy())
        
        # Focus on OK button
        ok_button.focus_set()
        
        # Wait for dialog to close
        self.root.wait_window(message_dialog)
