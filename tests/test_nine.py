import pytest, io

import advent.nine as nine

def test_RepeatedDifferences_init():
    rd = nine.RepeatedDifferences([5,5,5,5,5])
    assert  repr(rd) == "5 5 5 5 5\n- 0 0 0 0"

    rd = nine.RepeatedDifferences([1,2,3,4,5])
    assert  repr(rd) == "1 2 3 4 5\n- 1 1 1 1\n- - 0 0 0"

    rd = nine.RepeatedDifferences([1,2,4,7,10])
    assert  repr(rd) == "1 2 4 7 10\n- 1 2 3 3\n- - 1 1 0\n- - - 0 -1\n- - - - -1"

def test_RepeatedDifferences_interpolate():
    rd = nine.RepeatedDifferences([5,5,5,5,5])
    assert rd.interpolate() == 5

    rd = nine.RepeatedDifferences([1,2,3,4,5])
    assert rd.interpolate() == 6

    rd = nine.RepeatedDifferences([0,3,6,9,12,15])
    assert rd.interpolate() == 18

    rd = nine.RepeatedDifferences([1,3,6,10,15,21])
    assert rd.interpolate() == 28

    rd = nine.RepeatedDifferences([10,13,16,21,30,45])
    assert rd.interpolate() == 68

def test_RepeatedDifferences_extrapolate():
    rd = nine.RepeatedDifferences([5,5,5,5,5])
    assert rd.extrapolate() == 5

    rd = nine.RepeatedDifferences([0,3,6,9,12,15])
    assert rd.extrapolate() == -3

def test_sums():
    f = io.StringIO("0 3 6 9 12 15\n1 3 6 10 15 21\n10 13 16 21 30 45")
    assert nine.sum_interpolants(f) == 114

def test_ex_sums():
    f = io.StringIO("0 3 6 9 12 15\n1 3 6 10 15 21\n10 13 16 21 30 45")
    assert nine.sum_extrapolants(f) == 2
