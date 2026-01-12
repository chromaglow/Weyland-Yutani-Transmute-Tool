"""
Tests for mesh simplification functionality
"""

import pytest
import trimesh
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.mesh_simplifier import MeshSimplifier


class TestMeshSimplifier:
    """Test cases for mesh simplification"""

    def test_initialization(self):
        """Test simplifier initialization"""
        simplifier = MeshSimplifier()
        assert simplifier.original_mesh is None
        assert simplifier.simplified_mesh is None

    def test_load_mesh(self):
        """Test loading a mesh"""
        simplifier = MeshSimplifier()
        mesh = trimesh.creation.box()

        simplifier.load_mesh(mesh)

        assert simplifier.original_mesh is not None
        assert simplifier.simplified_mesh is not None
        assert len(simplifier.original_mesh.faces) == len(simplifier.simplified_mesh.faces)

    def test_simplify_by_percentage(self):
        """Test percentage-based simplification"""
        simplifier = MeshSimplifier()

        # Create a more complex mesh for testing
        mesh = trimesh.creation.box()
        # Subdivide to create more faces
        for _ in range(2):
            mesh = mesh.subdivide()

        simplifier.load_mesh(mesh)
        original_faces = len(mesh.faces)

        # Test 50% reduction
        success, message = simplifier.simplify_by_percentage(0.5)

        assert success
        assert len(simplifier.simplified_mesh.faces) < original_faces
        assert "50.0%" in message

    def test_simplify_by_face_count(self):
        """Test face count-based simplification"""
        simplifier = MeshSimplifier()

        # Create a complex mesh
        mesh = trimesh.creation.box()
        for _ in range(2):
            mesh = mesh.subdivide()

        simplifier.load_mesh(mesh)
        original_faces = len(mesh.faces)

        # Test reducing to 100 faces
        target_faces = 100
        success, message = simplifier.simplify_by_face_count(target_faces)

        assert success
        assert len(simplifier.simplified_mesh.faces) <= target_faces
        assert str(target_faces) in message

    def test_auto_simplify_simple_mesh(self):
        """Test auto-simplify on simple mesh (should not change)"""
        simplifier = MeshSimplifier()
        mesh = trimesh.creation.box()  # Simple mesh with few faces

        simplifier.load_mesh(mesh)

        success, message, was_simplified = simplifier.auto_simplify_for_step()

        assert success
        assert not was_simplified
        assert "OK" in message

    def test_auto_simplify_complex_mesh(self):
        """Test auto-simplify on complex mesh (should simplify)"""
        simplifier = MeshSimplifier()

        # Create very complex mesh
        mesh = trimesh.creation.box()
        for _ in range(4):  # Create many faces
            mesh = mesh.subdivide()

        simplifier.load_mesh(mesh)
        original_faces = len(mesh.faces)

        success, message, was_simplified = simplifier.auto_simplify_for_step()

        assert success
        assert was_simplified
        assert len(simplifier.simplified_mesh.faces) < original_faces

    def test_reset_mesh(self):
        """Test mesh reset functionality"""
        simplifier = MeshSimplifier()
        mesh = trimesh.creation.box()
        for _ in range(2):
            mesh = mesh.subdivide()

        simplifier.load_mesh(mesh)
        original_faces = len(simplifier.simplified_mesh.faces)

        # Simplify
        simplifier.simplify_by_percentage(0.5)
        simplified_faces = len(simplifier.simplified_mesh.faces)
        assert simplified_faces < original_faces

        # Reset
        simplifier.reset()
        reset_faces = len(simplifier.simplified_mesh.faces)
        assert reset_faces == original_faces

    def test_get_stats(self):
        """Test statistics retrieval"""
        simplifier = MeshSimplifier()
        mesh = trimesh.creation.box()

        simplifier.load_mesh(mesh)

        stats = simplifier.get_mesh_stats()
        assert 'faces' in stats
        assert 'vertices' in stats
        assert stats['faces'] == len(mesh.faces)

    def test_error_handling(self):
        """Test error handling for invalid operations"""
        simplifier = MeshSimplifier()

        # Test without loading mesh
        success, message = simplifier.simplify_by_percentage(0.5)
        assert not success
        assert "No mesh loaded" in message

        # Test invalid percentage
        mesh = trimesh.creation.box()
        simplifier.load_mesh(mesh)

        success, message = simplifier.simplify_by_percentage(2.0)  # Invalid percentage
        assert not success
        assert "between 0.01 and 1.0" in message

        # Test invalid face count
        success, message = simplifier.simplify_by_face_count(1000000)  # Too many faces
        assert not success
        assert "must be less than" in message