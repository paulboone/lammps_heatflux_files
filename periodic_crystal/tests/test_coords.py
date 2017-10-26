
from periodic_crystal import coord_to_index, index_to_coord
from periodic_crystal import atom_position_to_box_coords

def test_atom_position_to_box_coords_box_10x10x10():
    s = (10,10,10)
    assert(atom_position_to_box_coords(0,0,0,*s) == (0,0,0))
    assert(atom_position_to_box_coords(5,5,5,*s) == (0,0,0))
    assert(atom_position_to_box_coords(10,0,0,*s) == (1,0,0))
    assert(atom_position_to_box_coords(10,10,10,*s) == (1,1,1))
    assert(atom_position_to_box_coords(80,55,301,*s) == (8,5,30))

def test_coord_to_index_box_2x2x2():
    b = (2,2,2)
    assert(coord_to_index(0,0,0, *b) == 0)
    assert(coord_to_index(1,0,0, *b) == 1)
    assert(coord_to_index(0,1,0, *b) == 2)
    assert(coord_to_index(1,1,0, *b) == 3)
    assert(coord_to_index(0,0,1, *b) == 4)
    assert(coord_to_index(1,0,1, *b) == 5)
    assert(coord_to_index(0,1,1, *b) == 6)
    assert(coord_to_index(1,1,1, *b) == 7)

def test_index_to_coord_box_2x2x2():
    b = (2,2,2)
    assert(index_to_coord(0, *b) == (0,0,0))
    assert(index_to_coord(1, *b) == (1,0,0))
    assert(index_to_coord(2, *b) == (0,1,0))
    assert(index_to_coord(3, *b) == (1,1,0))
    assert(index_to_coord(4, *b) == (0,0,1))
    assert(index_to_coord(5, *b) == (1,0,1))
    assert(index_to_coord(6, *b) == (0,1,1))
    assert(index_to_coord(7, *b) == (1,1,1))
