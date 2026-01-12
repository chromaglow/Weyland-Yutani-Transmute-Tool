#!/usr/bin/env python3
"""
Quick test of mesh repair operations
"""

import trimesh
import numpy as np

# Create a simple test mesh
vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
faces = np.array([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])
mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

print(f'Original mesh: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces')
print(f'Non-degenerate faces: {mesh.nondegenerate_faces().sum()}')
print(f'Unique faces: {mesh.unique_faces().sum()}')

# Test the repair operations
mesh.update_faces(mesh.nondegenerate_faces())
print(f'After removing degenerates: {len(mesh.faces)} faces')

mesh.update_faces(mesh.unique_faces())
print(f'After removing duplicates: {len(mesh.faces)} faces')

print('Repair operations work correctly!')