import pytest, io, os

import advent.sixteen as sixteen

def test_Grid():
    with open(os.path.join("tests", "test_16.txt")) as f:
        grid = sixteen.Grid(f)
    assert grid.get(0,1) == "|"
    assert grid.move((0,-1), (0,1)) == [((0,0), (0,1))]
    assert grid.move((0,0), (0,1)) == [((0,1), (1,0)), ((0,1), (-1,0))]
    assert grid.move((0,1), (-1,0)) == []
    assert grid.move((0,1), (1,0)) == [((1,1), (1,0))]

def test_RayTrace():
    with open(os.path.join("tests", "test_16.txt")) as f:
        grid = sixteen.Grid(f)
    rt = sixteen.RayTrace(grid)
    rt.trace()
    assert rt.count() == 46

def test_maximise():
    with open(os.path.join("tests", "test_16.txt")) as f:
        grid = sixteen.Grid(f)
    assert sixteen.maximise(grid) == ((-1,3), 51)
