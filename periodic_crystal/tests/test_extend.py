import numpy as np
import pytest

import periodic_crystal as pc
import periodic_crystal.mofs


## IMPORTANT EXT_BONDS DEFINITION
# ext_bonds are defined tuple of:
# 1) (atom in this box, atom in +x direction)
# 2) (atom in this box, atom in +y direction)
# 3) (atom in this box, atom in +z direction)
# ATOM IN THIS BOX MUST BE FIRST!


def test_extend_cubic_1x1x2():
    atoms, int_bonds, ext_bonds, box_bounds, extend_xyz = pc.mofs.cubic_def((1,1,2))
    all_atoms, all_bonds = pc.extend(atoms, int_bonds, ext_bonds, box_bounds, extend_xyz)
    print(all_bonds)
    assert(set(map(tuple,all_bonds)) == set([(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6), (2, 0), (4, 0),
        (6, 7), (7, 8), (8, 9), (7, 10), (10, 11), (7, 12), (12, 13), (9, 7), (11, 7), (13, 0)]))

@pytest.mark.skip
def test_extend_cubic_45_degrees_1x1x2():
    atoms, int_bonds, ext_bonds, box_bounds, extend_xyz = pc.mofs.cubic_45_degrees_def((1,1,2))
    all_atoms, all_bonds = pc.extend(atoms, int_bonds, ext_bonds, box_bounds, extend_xyz)
    pass
    assert(set(map(tuple,all_bonds)) == set([(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6), (2, 0), (4, 0),
        (6, 7), (7, 8), (8, 9), (7, 10), (10, 11), (7, 12), (12, 13), (9, 7), (11, 7), (13, 0)]))

@pytest.mark.skip
def test_extend_triangular_1x1x2():
    atoms, int_bonds, ext_bonds, box_bounds, extend_xyz = pc.mofs.triangular_def((1,1,2))
    all_atoms, all_bonds = pc.extend(atoms, int_bonds, ext_bonds, box_bounds, extend_xyz)
    pass
    assert(set(map(tuple,all_bonds)) == set([(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6), (2, 0), (4, 0),
        (6, 7), (7, 8), (8, 9), (7, 10), (10, 11), (7, 12), (12, 13), (9, 7), (11, 7), (13, 0)]))

@pytest.mark.skip
def test_extend_hexagonal_1x1x2():
    atoms, int_bonds, ext_bonds, box_bounds, extend_xyz = pc.mofs.triangular_def((1,1,2))
    all_atoms, all_bonds = pc.extend(atoms, int_bonds, ext_bonds, box_bounds, extend_xyz)
    pass
    assert(set(map(tuple,all_bonds)) == set([(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6), (2, 0), (4, 0),
        (6, 7), (7, 8), (8, 9), (7, 10), (10, 11), (7, 12), (12, 13), (9, 7), (11, 7), (13, 0)]))
