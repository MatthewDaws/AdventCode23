import pytest, io, os

import advent.ten as ten

def test_parse():
    file = io.StringIO(".....\n.S-7.\n.|.|.\n.L-J.\n.....\n")
    g = ten.parse(file)
    
    assert g.at(0,0) == ten.Tile.GROUND
    assert g.at(2,1) == ten.Tile.UPDOWN
    assert g.at(3,3) == ten.Tile.NORTHWEST

    assert g.start == (1,1)

def test_accepting():
    file = io.StringIO(".....\n.S-7.\n.|.|.\n.L-J.\n.....\n")
    g = ten.parse(file)

    assert g.accepting_pipe(1,2, 1,1)
    assert g.accepting_pipe(1,2, 1,3)
    assert not g.accepting_pipe(1,2, 2,2)

    assert g.accepting_pipe(3,1, 3,2)
    assert g.accepting_pipe(3,1, 2,1)
    assert not g.accepting_pipe(3,1, 3,0)

def test_starting_candidates():
    file = io.StringIO(".....\n.S-7.\n.|.|.\n.L-J.\n.....\n")
    g = ten.parse(file)
    assert g.starting_candidates() == [ten.Tile.SOUTHEAST]

    file = io.StringIO("-L|F7\n7S-7|\nL|7||\n-L-J|\nL|-JF")
    g = ten.parse(file)
    assert g.starting_candidates() == [ten.Tile.SOUTHEAST]

def test_find_loop():
    file = io.StringIO(".....\n.S-7.\n.|.|.\n.L-J.\n.....\n")
    g = ten.parse(file)
    assert g.test_closed_loop(ten.Tile.SOUTHEAST) == 4

    file = io.StringIO("..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ...")
    g = ten.parse(file)
    assert g.test_closed_loop(ten.Tile.SOUTHEAST) == 8

def test_find_path():
    file = io.StringIO(".....\n.S-7.\n.|.|.\n.L-J.\n.....\n")
    g = ten.parse(file)
    path = g.find_path()
    assert len(path) == 8
    assert path[0] == (1,1)
    assert path[1] == (2,1)
    assert path[-1] == (1,2)

def test_winding_number():
    file = io.StringIO(".....\n.S-7.\n.|.|.\n.L-J.\n.....\n")
    path = ten.parse(file).find_path()

    assert ten.winding_number(path,0,0) == 0
    assert ten.winding_number(path,2,2) != 0

def test_count_containing_tiles():
    file = io.StringIO(".....\n.S-7.\n.|.|.\n.L-J.\n.....\n")
    path = ten.parse(file).find_path()

    assert ten.count_containing_tiles(path) == 1

def test_example_2nd():
    with open(os.path.join("tests", "test_10a.txt")) as f:
        g = ten.parse(f)
    path = g.find_path()
    assert ten.count_containing_tiles(path) == 8
