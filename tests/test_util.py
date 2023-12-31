import pytest

import advent.util as util

def test_lcm():
    assert util.lcm(1, 5) == 5
    assert util.lcm(5, 7) == 35
    assert util.lcm(4, 6) == 12

def test_bezout():
    s, t = util.bezout(1, 5)
    assert s*1 + t*5 == 1

    s, t = util.bezout(5, 10)
    assert s*5 + t*10 == 5

    s, t = util.bezout(3, 9)
    assert s*3 + t*9 == 3

    s, t = util.bezout(15, 35)
    assert s*15 + t*35 == 5

def test_brute_force_chinese_remainder():
    assert util.brute_force_chinese_remainder([(5,2)]) == 1
    assert util.brute_force_chinese_remainder([[5, 2], [7, 3]]) == 1
    assert util.brute_force_chinese_remainder([(1, 7), (3, 10), (5, 17)]) == 1093
    with pytest.raises(ValueError):
        util.brute_force_chinese_remainder([(5, 8), (102, 7), (162, 6)])

def test_chinese_remainder_single():
    assert util.chinese_remainder([(5, 2)]) == (1, 2)

def test_chinese_remainder():
    assert util.chinese_remainder([[5, 2], [7, 3]]) == (1, 6)
    td = [(1, 7), (3, 10), (5, 17)]
    assert util.chinese_remainder(td) == (util.brute_force_chinese_remainder(td), 7*10*17)
    with pytest.raises(ValueError):
        assert util.chinese_remainder([(5, 8), (102, 7), (162, 6)])

def test_Interval():
    i = util.Interval(10, 15)
    assert i.contains(10)
    assert i.contains(15)
    assert i.contains(12)
    assert not i.contains(8)
    assert repr(i) == "Interval(10,15)"

    with pytest.raises(ValueError):
        util.Interval(10, 8)

    i = util.Interval.from_start_length(10, -3)
    assert repr(i) == "Interval(7,10)"

    j = util.Interval(5, 12)
    assert j < i
    assert j <= i
    assert i > j
    assert i >= j
    assert not i==j
    assert hash(i) != hash(j)
    assert i==i
    assert i<=i
    assert i>=i

    assert i.intersect(j) == util.Interval(7,10)

