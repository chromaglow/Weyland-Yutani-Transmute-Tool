"""
Mesh Simplification Module for Weyland-Yutani Transmute Tool

Provides both automatic and manual mesh simplification with quality preservation.
"""

import trimesh
import numpy as np
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class MeshSimplifier:
    """
    Handles mesh simplification while preserving shape integrity
    """

    def __init__(self):
        self.original_mesh = None
        self.simplified_mesh = None

    def load_mesh(self, mesh: trimesh.Trimesh) -> None:
        """
        Load a mesh for simplification

        Args:
            mesh: Trimesh object to simplify
        """
        self.original_mesh = mesh
        self.simplified_mesh = mesh.copy()
        logger.info(f"Loaded mesh with {len(mesh.faces)} faces for simplification")

    def simplify_by_percentage(self, percentage: float, preserve_boundaries: bool = True) -> Tuple[bool, str]:
        """
        Simplify mesh by reducing to a percentage of original faces

        Args:
            percentage: Target percentage (0.1 to 1.0)
            preserve_boundaries: Whether to preserve mesh boundaries

        Returns:
            Tuple of (success: bool, message: str)
        """
        if self.original_mesh is None:
            return False, "No mesh loaded for simplification"

        if not 0.01 <= percentage <= 1.0:
            return False, "Percentage must be between 0.01 and 1.0"

        try:
            original_faces = len(self.original_mesh.faces)
            target_faces = max(4, int(original_faces * percentage))  # Minimum 4 faces

            logger.info(f"Simplifying mesh from {original_faces} to ~{target_faces} faces ({percentage*100:.1f}%)")

            # Use trimesh's simplification with quality preservation
            self.simplified_mesh = self.original_mesh.simplify_quadric_decimation(
                percent=percentage  # percentage is the fraction to keep (0.5 = keep 50%)
            )

            # Validate the result
            if len(self.simplified_mesh.faces) == 0:
                return False, "Simplification resulted in invalid mesh (no faces)"

            if not self.simplified_mesh.is_watertight and self.original_mesh.is_watertight:
                logger.warning("Simplification broke watertightness - attempting repair")
                # Try to fix with a slightly higher percentage (reduce simplification)
                repair_percentage = min(1.0, percentage + 0.1)  # Increase by 10%
                self.simplified_mesh = self.original_mesh.simplify_quadric_decimation(
                    percent=repair_percentage
                )

            final_faces = len(self.simplified_mesh.faces)
            actual_percentage = final_faces / original_faces

            message = f"Simplified from {original_faces} to {final_faces} faces ({actual_percentage*100:.1f}%)"
            logger.info(message)
            return True, message

        except Exception as e:
            error_msg = f"Simplification failed: {e}"
            logger.error(error_msg)
            return False, error_msg

    def simplify_by_face_count(self, target_faces: int, preserve_boundaries: bool = True) -> Tuple[bool, str]:
        """
        Simplify mesh to a specific number of faces

        Args:
            target_faces: Target number of faces
            preserve_boundaries: Whether to preserve mesh boundaries

        Returns:
            Tuple of (success: bool, message: str)
        """
        if self.original_mesh is None:
            return False, "No mesh loaded for simplification"

        original_faces = len(self.original_mesh.faces)
        if target_faces >= original_faces:
            return False, f"Target face count ({target_faces}) must be less than original ({original_faces})"

        if target_faces < 4:
            return False, "Target face count must be at least 4"

        try:
            logger.info(f"Simplifying mesh from {original_faces} to {target_faces} faces")

            # Use trimesh's simplification
            self.simplified_mesh = self.original_mesh.simplify_quadric_decimation(
                face_count=target_faces
            )

            # Validate the result
            if len(self.simplified_mesh.faces) == 0:
                return False, "Simplification resulted in invalid mesh (no faces)"

            final_faces = len(self.simplified_mesh.faces)
            message = f"Simplified from {original_faces} to {final_faces} faces"
            logger.info(message)
            return True, message

        except Exception as e:
            error_msg = f"Simplification failed: {e}"
            logger.error(error_msg)
            return False, error_msg

    def auto_simplify_for_step(self) -> Tuple[bool, str, bool]:
        """
        Automatically simplify mesh if needed for STEP conversion

        Returns:
            Tuple of (success: bool, message: str, was_simplified: bool)
        """
        if self.original_mesh is None:
            return False, "No mesh loaded", False

        original_faces = len(self.original_mesh.faces)

        # Thresholds for automatic simplification
        if original_faces <= 25000:
            # No simplification needed
            return True, f"Mesh complexity OK ({original_faces} faces)", False
        elif original_faces <= 75000:
            # Moderate simplification
            target_percentage = 0.6  # Reduce to 60%
            success, message = self.simplify_by_percentage(target_percentage)
            return success, message, success
        else:
            # Aggressive simplification for very complex meshes
            target_percentage = 0.3  # Reduce to 30%
            success, message = self.simplify_by_percentage(target_percentage)
            return success, message, success

    def get_mesh_stats(self) -> dict:
        """
        Get statistics about the current mesh

        Returns:
            Dictionary with mesh statistics
        """
        if self.simplified_mesh is None:
            return {}

        return {
            'faces': len(self.simplified_mesh.faces),
            'vertices': len(self.simplified_mesh.vertices),
            'is_watertight': self.simplified_mesh.is_watertight,
            'bounding_box': self.simplified_mesh.bounds.tolist() if self.simplified_mesh.bounds is not None else None
        }

    def get_original_stats(self) -> dict:
        """
        Get statistics about the original mesh

        Returns:
            Dictionary with original mesh statistics
        """
        if self.original_mesh is None:
            return {}

        return {
            'faces': len(self.original_mesh.faces),
            'vertices': len(self.original_mesh.vertices),
            'is_watertight': self.original_mesh.is_watertight,
            'bounding_box': self.original_mesh.bounds.tolist() if self.original_mesh.bounds is not None else None
        }

    def reset(self) -> None:
        """
        Reset to original mesh
        """
        if self.original_mesh is not None:
            self.simplified_mesh = self.original_mesh.copy()
            logger.info("Reset to original mesh")

    def get_current_mesh(self) -> Optional[trimesh.Trimesh]:
        """
        Get the current (possibly simplified) mesh

        Returns:
            Current mesh object
        """
        return self.simplified_mesh