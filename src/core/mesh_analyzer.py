"""
Mesh Analyzer - Scanning for lifeforms... I mean defects
Detects issues in STL mesh files
"""

import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import trimesh


class MeshAnalyzer:
    """
    Analyzes STL mesh files for defects and structural issues
    """
    
    def __init__(self):
        self.mesh: Optional[trimesh.Trimesh] = None
        self.analysis_results: Dict = {}
    
    def load_mesh(self, file_path: str) -> bool:
        """
        Load an STL file for analysis
        
        Args:
            file_path: Path to STL file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.mesh = trimesh.load(file_path)
            print(f"✓ Mesh loaded: {Path(file_path).name}")
            print(f"  Vertices: {len(self.mesh.vertices)}")
            print(f"  Faces: {len(self.mesh.faces)}")
            return True
        except Exception as e:
            print(f"❌ Error loading mesh: {e}")
            return False
    
    def analyze(self) -> Dict:
        """
        Perform comprehensive mesh analysis
        
        Returns:
            Dictionary containing analysis results
        """
        if self.mesh is None:
            return {"error": "No mesh loaded"}
        
        print("\n🔍 Initiating mesh analysis...")
        
        results = {
            "is_watertight": self.mesh.is_watertight,
            "is_winding_consistent": self.mesh.is_winding_consistent,
            "volume": float(self.mesh.volume) if self.mesh.is_watertight else None,
            "surface_area": float(self.mesh.area),
            "bounds": self.mesh.bounds.tolist(),
            "vertex_count": len(self.mesh.vertices),
            "face_count": len(self.mesh.faces),
        }
        
        # Check for specific issues
        results["issues"] = self._detect_issues()
        results["severity"] = self._calculate_severity(results["issues"])
        
        self.analysis_results = results
        
        self._print_analysis_report(results)
        
        return results
    
    def _detect_issues(self) -> List[str]:
        """
        Detect specific mesh issues
        
        Returns:
            List of detected issues
        """
        issues = []
        
        if not self.mesh.is_watertight:
            issues.append("Non-watertight mesh (has holes or gaps)")
        
        if not self.mesh.is_winding_consistent:
            issues.append("Inconsistent face winding (inverted normals)")
        
        # Check for degenerate faces
        face_areas = self.mesh.area_faces
        if np.any(face_areas < 1e-10):
            degenerate_count = np.sum(face_areas < 1e-10)
            issues.append(f"Degenerate faces detected ({degenerate_count})")
        
        # Check for duplicate vertices
        if len(self.mesh.vertices) != len(np.unique(self.mesh.vertices, axis=0)):
            issues.append("Duplicate vertices detected")
        
        return issues
    
    def _calculate_severity(self, issues: List[str]) -> str:
        """
        Calculate overall severity of issues
        
        Args:
            issues: List of detected issues
            
        Returns:
            Severity level: "none", "low", "medium", "high"
        """
        if not issues:
            return "none"
        elif len(issues) == 1:
            return "low"
        elif len(issues) <= 3:
            return "medium"
        else:
            return "high"
    
    def _print_analysis_report(self, results: Dict):
        """
        Print formatted analysis report
        
        Args:
            results: Analysis results dictionary
        """
        print("\n" + "=" * 60)
        print("📊 MESH ANALYSIS REPORT")
        print("=" * 60)
        
        print(f"\n✓ Watertight: {results['is_watertight']}")
        print(f"✓ Winding Consistent: {results['is_winding_consistent']}")
        print(f"✓ Vertices: {results['vertex_count']:,}")
        print(f"✓ Faces: {results['face_count']:,}")
        print(f"✓ Surface Area: {results['surface_area']:.2f} mm²")
        
        if results['volume']:
            print(f"✓ Volume: {results['volume']:.2f} mm³")
        
        print(f"\n⚠️  Issues Detected: {len(results['issues'])}")
        print(f"⚠️  Severity: {results['severity'].upper()}")
        
        if results['issues']:
            print("\nDetailed Issues:")
            for i, issue in enumerate(results['issues'], 1):
                print(f"  {i}. {issue}")
        else:
            print("\n✓ No issues detected - mesh is clean!")
        
        print("=" * 60)
    
    def get_mesh_info(self) -> Dict:
        """
        Get basic mesh information
        
        Returns:
            Dictionary with mesh info
        """
        if self.mesh is None:
            return {}
        
        return {
            "vertices": len(self.mesh.vertices),
            "faces": len(self.mesh.faces),
            "bounds": self.mesh.bounds.tolist(),
            "is_watertight": self.mesh.is_watertight,
        }
