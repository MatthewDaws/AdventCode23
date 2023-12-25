import pytest, io, os

import advent.fourteen as fourteen

def test_tilt_col():
    assert fourteen.Rocks.tilt_col("O.#..OO..#.O") == "O.#OO....#O."

def test_tilt():
    with open(os.path.join("tests", "test_14a.txt")) as f:
        rocks = fourteen.Rocks(f)
    tilted_columns = fourteen.Rocks.tilt_north(rocks.as_columns())

    with open(os.path.join("tests", "test_14b.txt")) as f:
        expected = fourteen.Rocks(f)

    assert expected.as_columns() == tilted_columns

def test_score_column():
    assert fourteen.Rocks.score_column("OOOO..#.#.") == 10+9+8+7

def test_score():
    with open(os.path.join("tests", "test_14a.txt")) as f:
        assert fourteen.score(f) == 136

def test_cycle():
    with open(os.path.join("tests", "test_14a.txt")) as f:
        rocks = fourteen.Rocks(f)
    with open(os.path.join("tests", "test_14c.txt")) as f:
        expected = fourteen.Rocks(f)

    assert fourteen.Rocks.cycle(rocks.grid) == expected.grid

def test_score_after_long_time():
    with open(os.path.join("tests", "test_14a.txt")) as f:
        rocks = fourteen.Rocks(f)
    assert fourteen.score_after_long_time(rocks.grid) == 64
