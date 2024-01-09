import pytest, io, os

import advent.twentyone as twentyone

def test_garden():
    with open(os.path.join("tests", "test_21.txt")) as f:
        g = twentyone.Garden(f)
    assert g.rows == 11
    assert g.cols == 11
    assert g.at(2,3) == "#"
    assert g.start == (5,5)
    assert not g.is_garden(-1, 2)
    assert not g.is_garden(2, 124)
    assert g.is_garden(1,2)
    assert not g.is_garden(2,3)

@pytest.fixture
def eg():
    with open(os.path.join("tests", "test_21.txt")) as f:
        return twentyone.Garden(f)


def test_move(eg):
    assert eg.walk() == { (4,5), (5,4) }

def test_move2(eg):
    places = None
    for _ in range(2):
        places = eg.walk(places)
    assert places == { (3,5), (5,3), (5,5), (6,4) }

    places = eg.walk(places)
    assert places == { (3,6), (4,5), (4,3), (5,4), (6,3), (7,4) }

def test_walkable(eg):
    assert twentyone.count_places_walkable(eg, 6) == 16
