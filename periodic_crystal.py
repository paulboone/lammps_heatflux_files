import numpy as np

# from mof_screen import generate_lammps_data_file



def generate_lammps_data_file(masses, atoms, bonds, angles, xb, yb, zb):
    atom_lines = []
    bond_lines = []
    angle_lines = []
    mass_lines = [" ".join([str(i + 1),str(t)]) for i, t in enumerate(masses)]

    for i, atom in enumerate(atoms):
        x, y, z = atom
        atom_tuple = (i, 1, 1, 0, x, y, z)
        atom_lines += [" ".join(map(str,atom_tuple))]

    for i, bond in enumerate(bonds):
        bond_tuple = (i, 1, *bond)
        bond_lines += [" ".join(map(str,bond_tuple))]

    # for i, angle in enumerate(angles):
    #     # abs_angle = [str(starting_atom_num + i - 1) for i in angle]
    #     angle_tuple = (str(angle_num), str(angle_type), *abs_angle)
    #     angles += [" ".join(angle_tuple)]


    s = ""
    s += "# lammps data file generated from mof_screen/packmol_to_lammps.py\n"
    s += "%s atoms\n" % len(atoms)
    s += "%s bonds\n" % len(bonds)
    s += "%s angles" % len(angles)
    s += """
0 dihedrals
0 impropers
%d atom types
1 bond types
1 angle types
0 dihedral types
0 improper types
""" % len(masses)

    s += "%.5f %10.5f xlo xhi\n" % xb
    s += "%.5f %10.5f ylo yhi\n" % yb
    s += "%.5f %10.5f zlo zhi\n" % zb

    s += "\n\n Masses\n\n" + "\n".join(mass_lines)
    s += "\n\n Atoms\n\n" + "\n".join(atom_lines)
    s += "\n\n Bonds\n\n" + "\n".join(bond_lines)
    s += "\n\n Angles\n\n" + "\n".join(angle_lines)

    return s



def extend(atoms, int_bonds, ext_bonds, box_size, extend):

    return atoms, int_bonds



linker_length = 10 # angstroms
bl = linker_length / 4
atoms = [(0,0,0), (bl, 0, 0), (2*bl, 0, 0),
         (0, bl, 0), (0, 2*bl, 0),
         (0, 0, bl), (0, 0, 2*bl)]
int_bonds = np.array([(0,1), (1,2), (0,3), (3,4), (0,5), (0,6)])


ext_bonds = np.array([((0,2)), ((0,4)), ((0,6))])

box_bounds = np.array([linker_length, linker_length, linker_length])
extend_xyz = np.array([2,2,2])
allatoms, allbonds = extend(atoms, int_bonds, ext_bonds, box_bounds, extend_xyz)
allbox_bounds = [np.array([0,d]) for d in extend_xyz * box_bounds]
print(*allbox_bounds)
# need to automatically generate angles

lammps_data_file = generate_lammps_data_file([1], allatoms, allbonds, [], (0,1), (0,1), (0,1))
print(lammps_data_file)
