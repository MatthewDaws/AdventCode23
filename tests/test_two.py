import pytest

import advent.two as two

def test_parse_single_trial():
    counts = two.parse_single_trial("3 red")
    assert len(counts) == 3
    assert counts[two.Colour.RED] == 3
    assert counts[two.Colour.BLUE] == 0
    assert counts[two.Colour.GREEN] == 0

    counts = two.parse_single_trial("2 red, 4 blue")
    assert len(counts) == 3
    assert counts[two.Colour.RED] == 2
    assert counts[two.Colour.BLUE] == 4
    assert counts[two.Colour.GREEN] == 0

    counts = two.parse_single_trial("2 red, 4 blue, 5 green")
    assert len(counts) == 3
    assert counts[two.Colour.RED] == 2
    assert counts[two.Colour.BLUE] == 4
    assert counts[two.Colour.GREEN] == 5

    with pytest.raises(Exception):
        two.parse_single_trial("5 violet")

def test_parse_game():
    num, counts = two.parse_game("Game 3: 2 red, 4 blue")
    assert num == 3
    assert len(counts) == 1
    assert counts[0][two.Colour.RED] == 2
    assert counts[0][two.Colour.BLUE] == 4
    assert counts[0][two.Colour.GREEN] == 0

    num, counts = two.parse_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert num == 1
    assert len(counts) == 3
    assert counts[2][two.Colour.GREEN] == 2

def test_max_counts():
    num, counts = two.max_count("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert num == 1
    assert counts[two.Colour.GREEN] == 2
    assert counts[two.Colour.BLUE] == 6
    assert counts[two.Colour.RED] == 4

