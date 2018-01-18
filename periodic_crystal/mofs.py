import numpy as np

# import periodic_crystal as pc



def cubic_def(extend_xyz, linker_length=10):
    bl = linker_length / 3
    atoms = np.array([(0, 0, 0, 0), (1, bl, 0, 0), (2, 2*bl, 0, 0),
             (3, 0, bl, 0), (4, 0, 2*bl, 0),
             (5, 0, 0, bl), (6, 0, 0, 2*bl)])
    int_bonds = np.array([(0,1), (1,2), (0,3), (3,4), (0,5), (5,6)])
    ext_bonds = np.array([[(2,0),(1,0,0)], [(4,0),(0,1,0)], [(6,0),(0,0,1)]])
    box_bounds = np.array([linker_length, linker_length, linker_length])

    return atoms, int_bonds, ext_bonds, box_bounds, extend_xyz

def cubic_45_degrees_def(extend_xyz, linker_length=10):
    bl = linker_length / 3
    atoms = np.array([(0, 0, 0, 0), (1, bl, 0, 0), (2, 2*bl, 0, 0),
             (3, 0, bl, 0), (4, 0, 2*bl, 0),
             (5, 0, 0, bl), (6, 0, 0, 2*bl)])
    int_bonds = np.array([(0,1), (1,2), (0,3), (3,4), (0,5), (5,6)])
    ext_bonds = np.array([[(2,0)], [(4,0)], [(6,0)]])
    box_bounds = np.array([linker_length, linker_length, linker_length])

    return atoms, int_bonds, ext_bonds, box_bounds, extend_xyz


def triangular_def(extend_xyz, linker_length=10.0):
    bl = linker_length / 3
    sq3 = np.sqrt(3.0)
    atoms = np.array([(0, 0, 0, 0), (1, bl, 0, 0), (2, -bl, 0, 0),
             (3, bl/2, bl*sq3/2, 0), (4, bl, bl*sq3, 0),
             (5, -bl/2, bl*sq3/2, 0), (6, -bl, bl*sq3, 0),
             (7, -bl/2, -bl*sq3/2, 0), (8, -bl, -bl*sq3, 0),
             (9, bl/2, -bl*sq3/2, 0), (10, bl, -bl*sq3, 0),
             (11, 3*bl/2, -3*bl*sq3/2, 0), (12, bl/2, -3*bl*sq3/2, 0), (13, -bl/2, -3*bl*sq3/2, 0),
             (14, 0, 0, bl), (15, 0, 0, 2*bl),
             (16,  3*bl/2, -3*bl*sq3/2, bl), (17,  3*bl/2, -3*bl*sq3/2, 2*bl)]) \
              + (0, 5, 0, 0)
    int_bonds = np.array([(0,1), (0,2), (0,3), (3,4), (0,5), (5,6), (0,7), (7,8), (0,9), (9,10),
                         (10,11), (11,12), (12,13), (0,14), (14,15), (0,14), (14,15), (11,16), (16,17)])
    ext_bonds = np.array([[(1,2),(1,0,0)], [(4, 11), (0,1,0)], [(6,11),(-1,1,0)], [(11,8),(1,0,0)],
                         [(11,13),(1,0,0)], [(15,0),(0,0,1)], [(17,11), (0,0,1)]])
    box_bounds = np.array([linker_length, linker_length, linker_length])

    return atoms, int_bonds, ext_bonds, box_bounds, extend_xyz

def hexagonal_def(extend_xyz, linker_length=10):
    bl = linker_length / 3
    atoms = np.array([(0, 0, 0, 0), (1, bl, 0, 0), (2, 2*bl, 0, 0),
             (3, 0, bl, 0), (4, 0, 2*bl, 0),
             (5, 0, 0, bl), (6, 0, 0, 2*bl)])
    int_bonds = np.array([(0,1), (1,2), (0,3), (3,4), (0,5), (5,6)])
    ext_bonds = np.array([[(2,0)], [(4,0)], [(6,0)]])
    box_bounds = np.array([linker_length, linker_length, linker_length])

    return atoms, int_bonds, ext_bonds, box_bounds, extend_xyz
