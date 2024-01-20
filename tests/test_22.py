import pytest, io, os

import advent.twentytwo as twentytwo

def test_parse():
    with open(os.path.join("tests", "test_22.txt")) as f:
        b = twentytwo.Bricks(f)
    assert b.occupied(1,0,1)
    assert b.occupied(1,1,1)
    assert b.occupied(1,2,1)
    assert not b.occupied(0,0,1)
    
@pytest.fixture
def eg():
    with open(os.path.join("tests", "test_22.txt")) as f:
        yield twentytwo.Bricks(f)
    
def test_can_drop(eg):
    assert not eg.can_drop(0)
    assert not eg.can_drop(1)
    assert eg.can_drop(2)

def test_drop(eg):
    assert eg.occupied(0,2,3)
    assert not eg.occupied(0,2,2)
    eg.drop(2)
    assert not eg.occupied(0,2,3)
    assert eg.occupied(0,2,2)

def test_drop_all(eg):
    assert not eg.occupied(1,1,5)
    dropped = eg.drop_all()
    assert eg.occupied(1,1,5)
    assert dropped == {2,3,4,5,6}

def test_supporting(eg):
    assert eg.supporting(0) == set()
    assert eg.supporting(1) == {0}

    eg.drop_all()
    assert eg.supporting(0) == set()
    assert eg.supporting(1) == {0}
    assert eg.supporting(2) == {0}
    assert eg.supporting(3) == {1,2}
    assert eg.supporting(4) == {1,2}
    assert eg.supporting(5) == {3,4}
    assert eg.supporting(6) == {5}

def test_removable(eg):
    eg.drop_all()
    assert eg.not_removable_blocks() == {0,5}
    assert eg.removable() == [1,2,3,4,6]

def test_spawn(eg):
    eg.drop_all()
    s = eg.spawn_with_removal(0)
    assert s.drop_all() == {1,2,3,4,5,6}

def test_count_all_drops(eg):
    eg.drop_all()
    assert eg.count_all_drops() == 7
    