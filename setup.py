"""
Weyland-Yutani Transmute Tool Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="weyland-yutani-transmute-tool",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="STL mesh repair and STEP conversion tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Weyland-Yutani-Transmute-Tool",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Topic :: Scientific/Engineering :: CAD",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "trimesh>=3.15.0",
        "numpy-stl>=2.16.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "repair": [
            "pymeshfix>=0.16.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "transmute=main:main",
        ],
    },
)
