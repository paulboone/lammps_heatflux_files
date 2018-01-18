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


def test_extend_triangular_1x1x2():
    atoms, int_bonds, ext_bonds, box_bounds, extend_xyz = pc.mofs.triangular_def((1,2,1))
    all_atoms, all_bonds = pc.extend(atoms, int_bonds, ext_bonds, box_bounds, extend_xyz)
    print(map(tuple, all_bonds))
    assert(set(map(set, all_bonds)) == map(set,set([
    (0, 1), (0, 2), (0, 3), (3, 4), (0, 5), (5, 6), (0, 7), (7, 8), (0, 9), (9, 10), (10, 11), \
     (11, 12), (12, 13), (0, 14), (14, 15), (11, 16), (16, 17), \
    (18, 19), (18, 20), (18, 21), (21, 22), (18, 23), (23, 24), (18, 25), (25, 26), (18, 27), \
     (27, 28), (28, 29), (29, 30), (30, 31), (18, 32), (32, 33), (29, 34), (34, 35), \
    (11,22), (11,8), (11,13), (11,24), (11,17), (29,4), (29,26), (29,31), (29,6), (29,35), \
    (1,2), (19,20), (0,14), (18,32)])))

@pytest.mark.skip
def test_extend_hexagonal_1x1x2():
    atoms, int_bonds, ext_bonds, box_bounds, extend_xyz = pc.mofs.triangular_def((1,1,2))
    all_atoms, all_bonds = pc.extend(atoms, int_bonds, ext_bonds, box_bounds, extend_xyz)
    pass
    assert(set(map(tuple,all_bonds)) == set([(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6), (2, 0), (4, 0),
        (6, 7), (7, 8), (8, 9), (7, 10), (10, 11), (7, 12), (12, 13), (9, 7), (11, 7), (13, 0)]))
