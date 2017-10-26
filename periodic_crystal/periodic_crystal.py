import numpy as np

def get_angles(bonds):
    """ Iterate through bonds to get angles.
    Bonds should contain no duplicates.
    """
    angles = []
    for i1, b1 in enumerate(bonds):
        for i2, b2 in enumerate(bonds):
            if i2 > i1:
                shared_atom = list(set(b1) & set(b2))
                if len(shared_atom) > 0:
                    atom1 = [b for b in b1 if b != shared_atom[0]][0]
                    atom2 = [b for b in b2 if b != shared_atom[0]][0]
                    other_atoms = sorted([atom1, atom2])
                    angles.append((other_atoms[0], shared_atom[0], other_atoms[1]))

    return sorted(angles)


def calculate_angle(p1, p2, p3):
    """ Calculate angle for three given points in space
      p2 ->  o
            / \
    p1 ->  o   o  <- p3
    """
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    v21 = p1 - p2
    v23 = p3 - p2
    angle = np.arccos(np.dot(v21, v23) / (np.linalg.norm(v21) * np.linalg.norm(v23)))
    # print(np.degrees(angle))
    return np.degrees(angle)

def correct_angle(p1, p2, p3, box_size, unit_size):
    p1 = np.array(p1); p2 = np.array(p2); p3 = np.array(p3)
    # print(p1, p2, p3, box_size, unit_size)

    coords1 = np.array(atom_position_to_box_coords(*p1, *unit_size))
    coords2 = np.array(atom_position_to_box_coords(*p2, *unit_size))
    coords3 = np.array(atom_position_to_box_coords(*p3, *unit_size))

    corrected_point1 = np.copy(p1)
    if np.sqrt(np.dot(p2 - p1, p2 - p1)) > unit_size[0] / 2:
        offset1 = np.sign(coords2 - coords1) * box_size * unit_size
        corrected_point1 += offset1

    corrected_point3 = np.copy(p3)
    if np.sqrt(np.dot(p2 - p3, p2 - p3)) > unit_size[0] / 2:
        offset3 = np.sign(coords2 - coords3) * box_size * unit_size
        corrected_point3 += offset3

    # print("points_orig", p1, p2, p3)
    # print("coords", coords1, coords2, coords3)
    # # print("offsets", offset1, offset3)
    # print("points_corr", corrected_point1, p2, corrected_point3)
    # print("-----")
    return (corrected_point1, p2, corrected_point3)



def atom_position_to_box_coords(x, y, z, sx, sy, sz):
    # print('atom_position_to_box_coords', x, y, z, sx, sy, sz)
    return (x // sx, y // sy, z // sz)

def coord_to_index(x, y, z, bx, by, bz):
    """
index a set of x, y, z coordinates according to a box size bx, by, bz in order of x, then y, then z.

so with box_size (2, 2, 2):

0 | 1
2 | 3

4 | 5
6 | 7
"""
    return z * bx * by + y * bx + x

def index_to_coord(i, bx, by, bz):
    z = i // (bx * by)
    y = (i % (bx * by)) // bx
    x = (i % (bx * by)) % bx
    return (x,y,z)


def generate_lammps_data_file(masses, atoms, bonds, angles, xb, yb, zb):
    atom_lines = []
    bond_lines = []
    angle_lines = []
    mass_lines = [" ".join([str(i + 1),str(t)]) for i, t in enumerate(masses)]

    for i, atom in enumerate(atoms):
        atom_id, x, y, z = atom
        atom_tuple = (int(atom_id + 1), 1, 1, 0, x, y, z)
        atom_lines += [" ".join(map(str, atom_tuple))]

    for i, bond in enumerate(bonds):
        bond_tuple = (i + 1, 1, bond[0] + 1, bond[1] + 1)
        bond_lines += [" ".join(map(str, bond_tuple))]

    for i, angle in enumerate(angles):
        angle_tuple = (i + 1, 1, angle[0] + 1, angle[1] + 1, angle[2] + 1)
        angle_lines += [" ".join(map(str, angle_tuple))]


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



def extend(atoms, int_bonds, ext_bonds, box_size, extend_dims):
    all_atoms = []
    all_bonds = []
    combinations = []
    atom_ids = list(np.arange(len(atoms)))
    for d2 in np.arange(extend_dims[2]):
        for d1 in np.arange(extend_dims[1]):
            for d0 in np.arange(extend_dims[0]):
                combinations += [(d0,d1,d2)]


    for dmult in combinations:
        cx, cy, cz = dmult
        atom_id_offset = coord_to_index(cx, cy, cz, *extend_dims) * len(atoms)
        atom_offsets = (atom_id_offset, *(dmult * box_size))

        # fill in box with atoms / internal bonds
        all_atoms += (atoms + atom_offsets).tolist()
        all_bonds += (int_bonds + atom_id_offset).tolist()

        # connect in +x, +y, +z directions
        # note that it is ok to do this without the atoms already existing because we
        # know what their future coords will be

        atom_dir_offset = (atom_id_offset, coord_to_index((cx + 1) % extend_dims[0], cy, cz, *extend_dims) * len(atoms))
        all_bonds += (ext_bonds[0] + atom_dir_offset).tolist()

        atom_dir_offset = (atom_id_offset, coord_to_index(cx, (cy + 1) % extend_dims[1], cz, *extend_dims) * len(atoms))
        all_bonds += (ext_bonds[1] + atom_dir_offset).tolist()

        atom_dir_offset = (atom_id_offset, coord_to_index(cx, cy, (cz + 1) % extend_dims[2], *extend_dims) * len(atoms))
        all_bonds += (ext_bonds[2] + atom_dir_offset).tolist()


    return all_atoms, all_bonds




# print(lammps_data_file)
