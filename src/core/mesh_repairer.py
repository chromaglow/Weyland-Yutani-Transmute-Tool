"""
Mesh Repairer - Initiating repair protocols
Fixes defects in STL mesh files
"""

import numpy as np
from typing import Optional
import trimesh


class MeshRepairer:
    """
    Repairs defects in STL mesh files to create watertight, manifold geometry
    """
    
    def __init__(self):
        self.original_mesh: Optional[trimesh.Trimesh] = None
        self.repaired_mesh: Optional[trimesh.Trimesh] = None
    
    def load_mesh(self, mesh: trimesh.Trimesh):
        """
        Load a mesh for repair
        
        Args:
            mesh: Trimesh object to repair
        """
        self.original_mesh = mesh
        print(f"✓ Mesh loaded for repair")
        print(f"  Original vertices: {len(mesh.vertices)}")
        print(f"  Original faces: {len(mesh.faces)}")
    
    def repair(self) -> trimesh.Trimesh:
        """
        Perform comprehensive mesh repair
        
        Returns:
            Repaired Trimesh object
        """
        if self.original_mesh is None:
            raise ValueError("No mesh loaded for repair")
        
        print("
🔧 Initiating repair sequence...")
        
        # Start with a copy
        mesh = self.original_mesh.copy()
        
        # Step 1: Remove duplicate vertices
        print("  ⏳ Removing duplicate vertices...")
        mesh.merge_vertices()
        
        # Step 2: Remove degenerate faces
        print("  ⏳ Removing degenerate faces...")
        mesh.remove_degenerate_faces()
        
        # Step 3: Remove duplicate faces
        print("  ⏳ Removing duplicate faces...")
        mesh.remove_duplicate_faces()
        
        # Step 4: Fix normals
        print("  ⏳ Fixing face normals...")
        mesh.fix_normals()
        
        # Step 5: Fill holes (if not watertight)
        if not mesh.is_watertight:
            print("  ⏳ Attempting to fill holes...")
            mesh.fill_holes()
        
        # Step 6: Remove unreferenced vertices
        print("  ⏳ Cleaning unreferenced vertices...")
        mesh.remove_unreferenced_vertices()
        
        self.repaired_mesh = mesh
        
        self._print_repair_report()
        
        return self.repaired_mesh
    
    def _print_repair_report(self):
        """
        Print formatted repair report
        """
        print("
" + "=" * 60)
        print("🔧 REPAIR REPORT")
        print("=" * 60)
        
        print("
Before Repair:")
        print(f"  Vertices: {len(self.original_mesh.vertices):,}")
        print(f"  Faces: {len(self.original_mesh.faces):,}")
        print(f"  Watertight: {self.original_mesh.is_watertight}")
        
        print("
After Repair:")
        print(f"  Vertices: {len(self.repaired_mesh.vertices):,}")
        print(f"  Faces: {len(self.repaired_mesh.faces):,}")
        print(f"  Watertight: {self.repaired_mesh.is_watertight}")
        
        # Calculate changes
        vertex_diff = len(self.repaired_mesh.vertices) - len(self.original_mesh.vertices)
        face_diff = len(self.repaired_mesh.faces) - len(self.original_mesh.faces)
        
        print("
Changes:")
        print(f"  Vertices: {vertex_diff:+,}")
        print(f"  Faces: {face_diff:+,}")
        
        if self.repaired_mesh.is_watertight:
            print("
✓ Mesh successfully repaired and watertight!")
        else:
            print("
⚠️  Mesh repaired but still not watertight")
            print("   Consider manual repair in external tool")
        
        print("=" * 60)
    
    def save_repaired_mesh(self, output_path: str) -> bool:
        """
        Save the repaired mesh to file
        
        Args:
            output_path: Path to save repaired STL
            
        Returns:
            True if successful, False otherwise
        """
        if self.repaired_mesh is None:
            print("❌ No repaired mesh to save")
            return False
        
        try:
            self.repaired_mesh.export(output_path)
            print(f"✓ Repaired mesh saved: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving mesh: {e}")
            return False
    
    def get_repaired_mesh(self) -> Optional[trimesh.Trimesh]:
        """
        Get the repaired mesh object
        
        Returns:
            Repaired Trimesh object or None
        """
        return self.repaired_mesh
