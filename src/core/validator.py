"""
Mesh Validator - Structural integrity check
Validates mesh quality and solid body properties
"""

from typing import Dict, List
import trimesh


class MeshValidator:
    """
    Validates mesh quality and ensures solid body requirements are met
    """
    
    @staticmethod
    def validate_mesh(mesh: trimesh.Trimesh) -> Dict:
        """
        Perform comprehensive mesh validation
        
        Args:
            mesh: Trimesh object to validate
            
        Returns:
            Dictionary containing validation results
        """
        print("\n✅ Initiating validation sequence...")
        
        results = {
            "is_valid": True,
            "checks": {},
            "warnings": [],
            "errors": [],
        }
        
        # Check 1: Watertight
        is_watertight = mesh.is_watertight
        results["checks"]["watertight"] = is_watertight
        if not is_watertight:
            results["is_valid"] = False
            results["errors"].append("Mesh is not watertight")
        
        # Check 2: Winding consistency
        is_winding_consistent = mesh.is_winding_consistent
        results["checks"]["winding_consistent"] = is_winding_consistent
        if not is_winding_consistent:
            results["warnings"].append("Face winding is inconsistent")
        
        # Check 3: Volume
        if is_watertight:
            volume = mesh.volume
            results["checks"]["has_volume"] = volume > 0
            if volume <= 0:
                results["is_valid"] = False
                results["errors"].append("Mesh has zero or negative volume")
        
        # Check 4: Degenerate faces
        face_areas = mesh.area_faces
        degenerate_count = (face_areas < 1e-10).sum()
        results["checks"]["no_degenerate_faces"] = degenerate_count == 0
        if degenerate_count > 0:
            results["warnings"].append(f"{degenerate_count} degenerate faces detected")
        
        # Check 5: Self-intersections (expensive check)
        # Skipped for performance - can be added as optional deep validation
        
        MeshValidator._print_validation_report(results)
        
        return results
    
    @staticmethod
    def _print_validation_report(results: Dict):
        """
        Print formatted validation report
        
        Args:
            results: Validation results dictionary
        """
        print("\n" + "=" * 60)
        print("✅ VALIDATION REPORT")
        print("=" * 60)
        
        print("\nChecks:")
        for check_name, passed in results["checks"].items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name.replace('_', ' ').title()}")
        
        if results["warnings"]:
            print("\n⚠️  Warnings:")
            for warning in results["warnings"]:
                print(f"  - {warning}")
        
        if results["errors"]:
            print("\n❌ Errors:")
            for error in results["errors"]:
                print(f"  - {error}")
        
        print(f"\n{'✓ VALIDATION PASSED' if results['is_valid'] else '✗ VALIDATION FAILED'}")
        print("=" * 60)
    
    @staticmethod
    def validate_for_printing(mesh: trimesh.Trimesh) -> bool:
        """
        Quick validation for 3D printing readiness
        
        Args:
            mesh: Trimesh object to validate
            
        Returns:
            True if ready for printing, False otherwise
        """
        return mesh.is_watertight and mesh.is_winding_consistent
