"""
File handling utilities
"""

from pathlib import Path
from typing import Optional


class FileHandler:
    """
    Handles file operations for STL and STEP files
    """
    
    @staticmethod
    def validate_stl_path(file_path: str) -> bool:
        """
        Validate STL file path
        
        Args:
            file_path: Path to STL file
            
        Returns:
            True if valid, False otherwise
        """
        path = Path(file_path)
        return path.exists() and path.suffix.lower() == '.stl'
    
    @staticmethod
    def get_output_path(input_path: str, suffix: str = "_repaired", extension: str = ".stl") -> str:
        """
        Generate output file path
        
        Args:
            input_path: Input file path
            suffix: Suffix to add to filename
            extension: Output file extension
            
        Returns:
            Output file path
        """
        path = Path(input_path)
        output_name = f"{path.stem}{suffix}{extension}"
        return str(path.parent / output_name)
    
    @staticmethod
    def ensure_directory(file_path: str) -> bool:
        """
        Ensure directory exists for file path
        
        Args:
            file_path: File path
            
        Returns:
            True if directory exists or was created
        """
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
