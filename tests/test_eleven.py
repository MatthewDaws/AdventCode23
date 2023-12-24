import pytest, io, os

import advent.eleven as eleven

@pytest.fixture
def test_star_field():
    with open(os.path.join("tests", "test_11.txt")) as f:
        yield f

def test_parse(test_star_field):
    stars = eleven.Stars(test_star_field)
    assert stars.cols == 10
    assert stars.rows == 10
    assert stars.empty_rows == [3,7]
    assert (0,3) in stars.stars
    assert not (1,4) in stars.stars
    assert stars.empty_cols == [2,5,8]

def test_distance(test_star_field):
    stars = eleven.Stars(test_star_field)
    assert stars.distance((5,1),(9,4)) == 9

def test_all_distances(test_star_field):
    stars = eleven.Stars(test_star_field)
    assert stars.all_distances() == 374

def test_all_distances_2nd(test_star_field):
    stars = eleven.Stars(test_star_field)
    assert stars.all_distances(10) == 1030
    assert stars.all_distances(100) == 8410
