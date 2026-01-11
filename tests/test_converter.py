"""
Tests for STEP converter
"""

import pytest
from src.core.step_converter import StepConverter


def test_converter_initialization():
    """Test converter can be initialized"""
    converter = StepConverter()
    assert converter is not None


def test_converter_freecad_check():
    """Test FreeCAD availability check"""
    converter = StepConverter()
    # Result depends on whether FreeCAD is installed
    assert isinstance(converter.freecad_available, bool)


# More tests would go here
