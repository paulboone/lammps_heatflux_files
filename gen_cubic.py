import numpy as np

import periodic_crystal as pc


extend_xyz = np.array([1,1,2])
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
all_atoms, all_bonds = pc.extend(atoms, int_bonds, ext_bonds, box_bounds, extend_xyz)
allbox_bounds = [np.array([0,d]) for d in extend_xyz * box_bounds]

# print('all_atoms')
# for a in all_atoms:
#     print(a)

print(all_bonds)

allowable_angles = [0,180]
allangles = pc.get_angles(all_bonds)
angles_to_use = []
for a in allangles:
    # print(a)
    # print(all_atoms[a[0]][1:], all_atoms[a[1]][1:], all_atoms[a[2]][1:])

    corrected_points = pc.correct_angle(all_atoms[a[0]][1:], all_atoms[a[1]][1:], all_atoms[a[2]][1:], extend_xyz, box_bounds)
    angle_degrees = pc.calculate_angle(*corrected_points)
    print('angle: ', a, angle_degrees)
    # print()
    if angle_degrees in allowable_angles:
        angles_to_use.append(a)


lammps_data_file = pc.generate_lammps_data_file([39.948], all_atoms, all_bonds, allangles,
                    (0,extend_xyz[0]*linker_length),
                    (0,extend_xyz[1]*linker_length),
                    (0,extend_xyz[2]*linker_length))
