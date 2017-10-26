import numpy as np

import periodic_crystal as pc



def fixture_cubic(extend_xyz):
    linker_length = 10 # angstroms
    bl = linker_length / 3
    atoms = np.array([(0, 0, 0, 0), (1, bl, 0, 0), (2, 2*bl, 0, 0),
             (3, 0, bl, 0), (4, 0, 2*bl, 0),
             (5, 0, 0, bl), (6, 0, 0, 2*bl)])
    int_bonds = np.array([(0,1), (1,2), (0,3), (3,4), (0,5), (5,6)])

    # ext_bonds are defined tuple of:
    # 1) atom in this box, atom in +x direction
    # 2) atom in this box, atom in +y direction
    # 3) atom in this box, atom in +z direction

    ext_bonds = np.array([[(2,0)], [(4,0)], [(6,0)]])
    box_bounds = np.array([linker_length, linker_length, linker_length])

    return atoms, int_bonds, ext_bonds, box_bounds, extend_xyz


def test_extend_1x1x2():
    atoms, int_bonds, ext_bonds, box_bounds, extend_xyz = fixture_cubic((1,1,2))
    all_atoms, all_bonds = pc.extend(atoms, int_bonds, ext_bonds, box_bounds, extend_xyz)

    assert(set(map(tuple,all_bonds)) == set([(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6), (2, 0), (4, 0),
        (6, 7), (7, 8), (8, 9), (7, 10), (10, 11), (7, 12), (12, 13), (9, 7), (11, 7), (13, 0)]))
