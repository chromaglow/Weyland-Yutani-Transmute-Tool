"""
Main GUI Window for Weyland-Yutani Transmute Tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.mesh_analyzer import MeshAnalyzer
from core.mesh_repairer import MeshRepairer
from core.step_converter import StepConverter
from core.validator import MeshValidator


class TransmuteApp:
    """
    Main application window for STL repair and STEP conversion
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Weyland-Yutani Transmute Tool")
        self.root.geometry("900x700")
        
        # Initialize processors
        self.analyzer = MeshAnalyzer()
        self.repairer = MeshRepairer()
        self.converter = StepConverter()
        self.validator = MeshValidator()
        
        # State
        self.current_file = None
        self.analysis_results = None
        self.repaired_mesh = None
        
        self._create_ui()
        self._redirect_console()
    
    def _create_ui(self):
        """Create the user interface"""
        
        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="🏢 Weyland-Yutani Transmute Tool",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text='"Building Better Worlds... One Mesh at a Time"',
            font=("Arial", 10, "italic")
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_frame, padding="5")
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # File selection
        file_frame = ttk.LabelFrame(left_panel, text="Input File", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="No file selected", wraplength=200)
        self.file_label.pack()
        
        ttk.Button(
            file_frame,
            text="📁 Load STL File",
            command=self.load_file
        ).pack(pady=5)
        
        # Analysis section
        analysis_frame = ttk.LabelFrame(left_panel, text="Analysis", padding="10")
        analysis_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            analysis_frame,
            text="🔍 Analyze Mesh",
            command=self.analyze_mesh
        ).pack(fill=tk.X, pady=2)
        
        # Repair section
        repair_frame = ttk.LabelFrame(left_panel, text="Repair", padding="10")
        repair_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            repair_frame,
            text="🔧 Repair Mesh",
            command=self.repair_mesh
        ).pack(fill=tk.X, pady=2)
        
        # Export section
        export_frame = ttk.LabelFrame(left_panel, text="Export", padding="10")
        export_frame.pack(fill=tk.X, pady=5)
        
        self.export_stl_var = tk.BooleanVar(value=True)
        self.export_step_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(
            export_frame,
            text="Export STL",
            variable=self.export_stl_var
        ).pack(anchor=tk.W)
        
        ttk.Checkbutton(
            export_frame,
            text="Export STEP",
            variable=self.export_step_var
        ).pack(anchor=tk.W)
        
        ttk.Button(
            export_frame,
            text="💾 Export Files",
            command=self.export_files
        ).pack(fill=tk.X, pady=5)
        
        # Status section
        status_frame = ttk.LabelFrame(left_panel, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.status_text = tk.Text(status_frame, height=10, width=30, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        self._update_status("Ready for transmutation...")
        
        # Right panel - Console output
        right_panel = ttk.Frame(main_frame, padding="5")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        console_frame = ttk.LabelFrame(right_panel, text="Console Output", padding="10")
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        self.console_text = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        # Clear console button
        ttk.Button(
            console_frame,
            text="Clear Console",
            command=self.clear_console
        ).pack(pady=5)
    
    def _redirect_console(self):
        """Redirect print statements to console widget"""
        class ConsoleRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget
            
            def write(self, text):
                self.text_widget.insert(tk.END, text)
                self.text_widget.see(tk.END)
                self.text_widget.update()
            
            def flush(self):
                pass
        
        sys.stdout = ConsoleRedirector(self.console_text)
    
    def _update_status(self, message):
        """Update status text"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, message)
    
    def clear_console(self):
        """Clear console output"""
        self.console_text.delete(1.0, tk.END)
    
    def load_file(self):
        """Load an STL file"""
        file_path = filedialog.askopenfilename(
            title="Select STL File",
            filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.current_file = file_path
            file_name = Path(file_path).name
            self.file_label.config(text=file_name)
            self._update_status(f"Loaded: {file_name}")
            print(f"
✓ File selected: {file_name}")
    
    def analyze_mesh(self):
        """Analyze the loaded mesh"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please load an STL file first")
            return
        
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
        else:
            self._update_status("Analysis failed")
            messagebox.showerror("Error", "Failed to analyze mesh")
    
    def repair_mesh(self):
        """Repair the loaded mesh"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please load an STL file first")
            return
        
        if not self.analysis_results:
            messagebox.showinfo("Analyze First", "Please analyze the mesh first")
            return
        
        self._update_status("Repairing mesh...")
        
        # Load mesh into repairer
        if self.analyzer.mesh:
            self.repairer.load_mesh(self.analyzer.mesh)
            self.repaired_mesh = self.repairer.repair()
            
            # Validate repaired mesh
            validation = self.validator.validate_mesh(self.repaired_mesh)
            
            if validation["is_valid"]:
                self._update_status("Repair successful!\nMesh is valid")
                messagebox.showinfo("Success", "Mesh repaired successfully!")
            else:
                self._update_status("Repair complete\nWarnings present")
                messagebox.showwarning(
                    "Partial Success",
                    "Mesh repaired but validation warnings present"
                )
        else:
            self._update_status("Repair failed")
            messagebox.showerror("Error", "Failed to repair mesh")
    
    def export_files(self):
        """Export repaired mesh and/or STEP file"""
        if not self.repaired_mesh:
            messagebox.showwarning("No Repair", "Please repair the mesh first")
            return
        
        # Get output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
        
        output_path = Path(output_dir)
        base_name = Path(self.current_file).stem + "_repaired"
        
        success_count = 0
        
        # Export STL
        if self.export_stl_var.get():
            stl_path = output_path / f"{base_name}.stl"
            if self.repairer.save_repaired_mesh(str(stl_path)):
                success_count += 1
        
        # Export STEP
        if self.export_step_var.get():
            if self.converter.is_available():
                step_path = output_path / f"{base_name}.step"
                self.converter.load_mesh(self.repaired_mesh)
                if self.converter.convert_to_step(str(step_path)):
                    success_count += 1
            else:
                messagebox.showwarning(
                    "STEP Unavailable",
                    "FreeCAD not installed. STEP export unavailable."
                )
        
        if success_count > 0:
            self._update_status(f"Export complete!\n{success_count} file(s) saved")
            messagebox.showinfo("Success", f"Exported {success_count} file(s)")
        else:
            self._update_status("Export failed")
            messagebox.showerror("Error", "Export failed")
