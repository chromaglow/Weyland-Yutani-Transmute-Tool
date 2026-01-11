"""
Tests for mesh analyzer
"""

import pytest
from src.core.mesh_analyzer import MeshAnalyzer


def test_analyzer_initialization():
    """Test analyzer can be initialized"""
    analyzer = MeshAnalyzer()
    assert analyzer is not None
    assert analyzer.mesh is None


def test_analyzer_load_invalid_file():
    """Test analyzer handles invalid file gracefully"""
    analyzer = MeshAnalyzer()
    result = analyzer.load_mesh("nonexistent.stl")
    assert result is False


# More tests would go here with actual STL files
