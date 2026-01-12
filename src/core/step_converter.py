"""
STEP Converter - Transmutation sequence engaged
Converts repaired STL meshes to solid STEP files
"""

from pathlib import Path
from typing import Optional
import trimesh
import sys
import os


class StepConverter:
    """
    Converts STL mesh files to STEP solid body format
    
    Note: This is a placeholder implementation.
    Full STEP conversion requires FreeCAD or pythonOCC integration.
    """
    
    def __init__(self):
        self.mesh: Optional[trimesh.Trimesh] = None
        self.freecad_available = self._check_freecad()
    
    def _check_freecad(self) -> bool:
        """
        Check if FreeCAD is available for STEP conversion
        
        Returns:
            True if FreeCAD is available, False otherwise
        """
        # Check if FreeCAD executable exists
        freecad_exe = r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"
        freecad_python = r"C:\Program Files\FreeCAD 1.0\bin\python.exe"
        
        if os.path.exists(freecad_exe) and os.path.exists(freecad_python):
            print("✓ FreeCAD 1.0 detected - STEP conversion available via subprocess")
            self.freecad_exe = freecad_exe
            self.freecad_python = freecad_python
            return True
        
        # Fallback: try direct import (won't work with Python 3.13 but let's check)
        try:
            import FreeCAD
            print("✓ FreeCAD detected via direct import - STEP conversion available")
            self.use_subprocess = False
            return True
        except ImportError as e:
            if "python311.dll" in str(e).lower():
                print("⚠️  FreeCAD Python version conflict detected")
                print("   → Will use subprocess calls to FreeCAD's Python for STEP conversion")
                self.use_subprocess = True
            else:
                print(f"   Direct import failed: {e}")
        
        print("⚠️  FreeCAD not found - STEP conversion unavailable")
        print("   Install FreeCAD from: https://www.freecadweb.org/")
        return False
    
    def _find_freecad_paths(self) -> list:
        """
        Find possible FreeCAD installation paths
        
        Returns:
            List of possible FreeCAD Python module paths
        """
        paths = []
        
        # Common FreeCAD installation paths
        common_paths = [
            r"C:\Program Files\FreeCAD\bin",  # Standard Windows installation
            r"C:\Program Files (x86)\FreeCAD\bin",
            r"C:\FreeCAD\bin",
            r"C:\Program Files\FreeCAD 1.0\bin",  # FreeCAD 1.0 installation
            r"C:\Users\{}\AppData\Local\FreeCAD\bin".format(os.environ.get('USERNAME', '')),  # User installation
        ]
        
        # Add paths from environment variables
        if 'FREECAD_ROOT' in os.environ:
            paths.append(os.path.join(os.environ['FREECAD_ROOT'], 'bin'))
        
        # Check PATH environment variable
        path_env = os.environ.get('PATH', '')
        for path_item in path_env.split(os.pathsep):
            if 'freecad' in path_item.lower() and 'bin' in path_item:
                paths.append(path_item)
        
        # Add common paths
        paths.extend(common_paths)
        
        # Remove duplicates and filter existing paths
        unique_paths = []
        seen = set()
        for path in paths:
            if path and path not in seen and os.path.exists(path):
                unique_paths.append(path)
                seen.add(path)
        
        return unique_paths
    
    def set_freecad_path(self, freecad_bin_path: str) -> bool:
        """
        Manually set the FreeCAD bin path for troubleshooting
        
        Args:
            freecad_bin_path: Path to FreeCAD's bin directory
            
        Returns:
            True if FreeCAD was found at the specified path, False otherwise
        """
        if not os.path.exists(freecad_bin_path):
            print(f"❌ Path does not exist: {freecad_bin_path}")
            return False
        
        try:
            sys.path.insert(0, freecad_bin_path)
            import FreeCAD
            self.freecad_available = True
            print(f"✓ FreeCAD manually configured at {freecad_bin_path}")
            return True
        except ImportError:
            print(f"❌ FreeCAD not found at {freecad_bin_path}")
            return False
    
    def load_mesh(self, mesh: trimesh.Trimesh):
        """
        Load a mesh for STEP conversion
        
        Args:
            mesh: Trimesh object to convert
        """
        self.mesh = mesh
        print(f"✓ Mesh loaded for STEP conversion")
    
    def convert_to_step(self, output_path: str) -> tuple[bool, str]:
        """
        Convert mesh to STEP format
        
        Args:
            output_path: Path to save STEP file
            
        Returns:
            Tuple of (success: bool, error_message: str)
        """
        if self.mesh is None:
            error_msg = "No mesh loaded for conversion"
            print(f"❌ {error_msg}")
            return False, error_msg
        
        if not self.freecad_available:
            error_msg = "FreeCAD not available - cannot convert to STEP"
            print(f"❌ {error_msg}")
            print("   Please install FreeCAD from: https://www.freecadweb.org/")
            print("   If FreeCAD is installed, try running the application as Administrator")
            print("   or ensure FreeCAD's bin folder is in your system PATH")
            return False, error_msg
        
        # Check mesh complexity and provide recommendations
        num_faces = len(self.mesh.faces)
        num_vertices = len(self.mesh.vertices)
        
        print(f"\n🔄 Initiating STEP conversion...")
        print(f"   Mesh complexity: {num_vertices} vertices, {num_faces} faces")
        
        # Provide complexity warnings
        if num_faces > 50000:
            print(f"   ⚠️  WARNING: Mesh has {num_faces} faces - this may take several minutes")
            print("   → Consider simplifying the mesh before STEP conversion")
        elif num_faces > 100000:
            print(f"   ⚠️  WARNING: Mesh has {num_faces} faces - conversion may take 5+ minutes")
            print("   → This is a very complex mesh, consider mesh decimation first")
        
        try:
            # This will be implemented with FreeCAD integration
            success, error_msg = self._convert_with_freecad(output_path)
            
            if success:
                print(f"✓ STEP file created: {output_path}")
                return True, ""
            else:
                print(f"❌ STEP conversion failed: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error during STEP conversion: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def _convert_with_freecad(self, output_path: str) -> tuple[bool, str]:
        """
        Perform actual STEP conversion using FreeCAD via subprocess
        
        Args:
            output_path: Path to save STEP file
            
        Returns:
            Tuple of (success: bool, error_message: str)
        """
        import subprocess
        import tempfile
        
        try:
            # Create temporary STL file
            temp_stl = Path(output_path).with_suffix('.temp.stl')
            print(f"  Creating temporary STL file: {temp_stl}")
            self.mesh.export(str(temp_stl))
            
            # Verify the STL file was created
            if not os.path.exists(str(temp_stl)):
                error_msg = "Failed to create temporary STL file"
                print(f"  ❌ ERROR: {error_msg}")
                return False, error_msg
            
            stl_size = os.path.getsize(str(temp_stl))
            print(f"  ✓ Temporary STL created ({stl_size} bytes, {len(self.mesh.vertices)} vertices, {len(self.mesh.faces)} faces)")
            
            # Create a Python script for FreeCAD to execute
            freecad_script = f"""
import sys
import os
sys.path.append(r'C:\\Program Files\\FreeCAD 1.0\\bin')

try:
    import FreeCAD
    import Mesh
    import Part
    
    print("FreeCAD script: Starting conversion...")
    print(f"FreeCAD version: {{FreeCAD.Version()}}")
    
    # Import STL mesh
    temp_stl_path = r'{temp_stl}'
    print(f"FreeCAD script: Importing mesh from: {{temp_stl_path}}")
    
    if not os.path.exists(temp_stl_path):
        print(f"FreeCAD script: ERROR - STL file not found: {{temp_stl_path}}")
        sys.exit(1)
    
    mesh_obj = Mesh.Mesh(temp_stl_path)
    print(f"FreeCAD script: Mesh imported - {{len(mesh_obj.Facets)}} faces, {{len(mesh_obj.Points)}} vertices")
    
    if len(mesh_obj.Facets) == 0:
        print("FreeCAD script: ERROR - Mesh has no faces")
        sys.exit(1)
    
    # Convert mesh to shape
    print("FreeCAD script: Converting mesh to shape...")
    shape = Part.Shape()
    shape.makeShapeFromMesh(mesh_obj.Topology, 0.05)  # Increased tolerance
    
    if not shape.isValid():
        print("FreeCAD script: WARNING - Shape is not valid, attempting to fix...")
        shape.fixTolerance(0.1)
        if not shape.isValid():
            print("FreeCAD script: ERROR - Could not create valid shape")
            sys.exit(1)
    
    print(f"FreeCAD script: Shape created with {{shape.ShapeType}}")
    
    # Create solid from shape
    print("FreeCAD script: Creating solid...")
    solid = Part.makeSolid(shape)
    
    if solid is None:
        print("FreeCAD script: ERROR - Failed to create solid from shape")
        sys.exit(1)
    
    print(f"FreeCAD script: Solid created - Volume: {{solid.Volume}}")
    
    if solid.Volume <= 0:
        print("FreeCAD script: WARNING - Solid has zero or negative volume")
    
    # Export to STEP
    output_path = r'{output_path}'
    print(f"FreeCAD script: Exporting STEP to: {{output_path}}")
    
    solid.exportStep(output_path)
    
    if os.path.exists(output_path):
        step_size = os.path.getsize(output_path)
        print(f"FreeCAD script: SUCCESS - STEP file created ({{step_size}} bytes)")
    else:
        print("FreeCAD script: ERROR - STEP file was not created")
        sys.exit(1)
    
except Exception as e:
    import traceback
    print(f"FreeCAD script error: {{e}}")
    print("Full traceback:")
    traceback.print_exc()
    sys.exit(1)
"""
            
            # Write the script to a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(freecad_script)
                script_path = f.name
            
            print("  ⏳ Running FreeCAD conversion script...")
            
            # Determine timeout based on mesh complexity
            num_faces = len(self.mesh.faces)
            if num_faces > 100000:
                timeout_seconds = 600  # 10 minutes for very complex meshes
                print(f"  ⏱️  Using extended timeout: {timeout_seconds}s for complex mesh ({num_faces} faces)")
            elif num_faces > 50000:
                timeout_seconds = 300  # 5 minutes for moderately complex meshes
                print(f"  ⏱️  Using extended timeout: {timeout_seconds}s for moderately complex mesh")
            else:
                timeout_seconds = 120  # 2 minutes for simple meshes
                print(f"  ⏱️  Using standard timeout: {timeout_seconds}s")
            
            # Run FreeCAD's Python with the script
            result = subprocess.run(
                [self.freecad_python, script_path],
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            
            # Clean up temporary files
            os.unlink(script_path)
            temp_stl.unlink()
            
            print(f"  Subprocess completed with return code: {result.returncode}")
            print(f"  STDOUT: {result.stdout}")
            if result.stderr:
                print(f"  STDERR: {result.stderr}")
            
            if result.returncode == 0:
                print("  ✓ STEP conversion complete")
                return True, ""
            else:
                error_msg = f"FreeCAD conversion failed (exit code: {result.returncode})"
                if result.stderr:
                    error_msg += f" - {result.stderr.strip()}"
                print(f"  ❌ {error_msg}")
                return False, error_msg
            
        except subprocess.TimeoutExpired:
            error_msg = f"FreeCAD conversion timed out after {timeout_seconds} seconds"
            print(f"  ❌ {error_msg}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Subprocess error: {e}"
            print(f"  ❌ {error_msg}")
            return False, error_msg
    
    def is_available(self) -> bool:
        """
        Check if STEP conversion is available
        
        Returns:
            True if conversion is available, False otherwise
        """
        return self.freecad_available
