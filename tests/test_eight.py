import pytest, io

import advent.eight as eight

def test_LR():
    x = eight.LeftRight("LR")
    assert [a for _,a in zip(range(2), x)] == ["L", "R"]
    assert x.period == 2
    assert "".join(a for _,a in zip(range(5), x)) == "LRLRL"


def test_parse():
    input = io.StringIO("LLR\n\nAAA = (BBB, BBB)\nBBB = (AAA, ZZZ)\nZZZ = (ZZZ, ZZZ)\n")
    lr, lookup = eight.parse(input)
    assert lr.period == 3

    assert "".join(a for _,a in zip(range(5), lr)) == "LLRLL"
    assert lookup["AAA"] == ("BBB", "BBB")
    assert lookup["BBB"] == ("AAA", "ZZZ")

def test_example():
    input = io.StringIO("LLR\n\nAAA = (BBB, BBB)\nBBB = (AAA, ZZZ)\nZZZ = (ZZZ, ZZZ)\n")
    assert eight.time_to_ZZZ(*eight.parse(input)) == 6

def test_2nd_example():
    input = io.StringIO("LR\n\n11A = (11B, XXX)\n11B = (XXX, 11Z)\n11Z = (11B, XXX)\n22A = (22B, XXX)\n22B = (22C, 22C)\n22C = (22Z, 22Z)\n22Z = (22B, 22B)\nXXX = (XXX, XXX)\n")
    data = eight.parse(input)
    assert eight.multiple_paths(*data) == 6
    assert eight.fast_multiple_paths(*data) == 6

def test_find_repeat():
    input = io.StringIO("LR\n\n11A = (11B, XXX)\n11B = (XXX, 11Z)\n11Z = (11B, XXX)\n22A = (22B, XXX)\n22B = (22C, 22C)\n22C = (22Z, 22Z)\n22Z = (22B, 22B)\nXXX = (XXX, XXX)\n")
    lr, lookup = eight.parse(input)
    assert eight.find_repeat(lr, lookup, "11A") == (["11A", "11B", "11Z", "11B", "11Z"], 2)
    assert eight.z_end(lr, lookup, "11A") == ([2], 2)

