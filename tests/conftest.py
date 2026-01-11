"""
Pytest configuration and fixtures
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_stl_path():
    """
    Fixture providing path to sample STL file
    """
    # This would point to a real test STL file
    return Path("tests/fixtures/sample.stl")


@pytest.fixture
def temp_output_dir(tmp_path):
    """
    Fixture providing temporary output directory
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
