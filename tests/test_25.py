import pytest, os

import advent.twentyfive as twentyfive

@pytest.fixture
def eg():
    with open(os.path.join("tests", "test_25.txt")) as f:
        return twentyfive.Components(f)

def test_components(eg):
    coms = eg.random_2_components()
    assert len(coms) == 2
    coms = list(coms)
    verts = set(coms[0]) | set((coms[1]))
    assert verts == eg.vertices()

def test_random_cut(eg):
    coms, cut = eg.find_cut_of_size(3)
    a, b = list(coms)
    assert len(a) * len(b) == 54
    