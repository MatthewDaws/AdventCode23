import pytest
import os.path
import io

import advent.six as six

def test_winning_ways():
    assert six.winning_ways(7, 9) == 4
    assert six.winning_ways(15, 40) == 8
    assert six.winning_ways(30, 200) == 9

def test_parse():
    f = io.StringIO("Time:      7  15   30\nDistance:  9  40  200\n")
    t,d = six.parse(f)
    assert t == [7, 15, 30]
    assert d == [9, 40, 200]

def test_parse_second():
    f = io.StringIO("Time:      7  15   30\nDistance:  9  40  200\n")
    t,d = six.parse_second(f)
    assert t == 71530
    assert d == 940200
