import pytest, io, os

import advent.thirteen as thirteen

def test_grid():
    with open(os.path.join("tests", "test_13.txt")) as f:
        g = thirteen.Grid(f)

    assert g.rows == 7
    assert g.cols == 9
    assert g.grid[2][3] == "."
    assert g.get_column(2) == "##..###"

def test_sym_horizontal():
    with open(os.path.join("tests", "test_13.txt")) as f:
        g = thirteen.Grid(f)
    assert g.is_symmetry_horizontal() == 5
    assert g.is_symmetry_vertical() is None

def test_sym_vertical():
    with open(os.path.join("tests", "test_13a.txt")) as f:
        g = thirteen.Grid(f)
    assert g.is_symmetry_horizontal() is None
    assert g.is_symmetry_vertical() == 4

def test_score():
    with open(os.path.join("tests", "test_13b.txt")) as f:
        assert thirteen.score_all(f) == 405

def test_score_2nd():
    with open(os.path.join("tests", "test_13b.txt")) as f:
        assert thirteen.score_all(f, diffs=1) == 400
