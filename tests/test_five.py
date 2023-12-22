import pytest
import os.path

import advent.five as five

def test_RangeMap():
    r = five.RangeMap(["50 98 2\n", "52 50 48\n"])
    assert r[2] == 2
    assert r[50] == 52
    assert r[52] == 54
    assert r[97] == 99
    assert r[98] == 50
    assert r[99] == 51
    assert r[100] == 100

def test_RangeMap_iter():
    r = five.RangeMap(["50 98 2\n", "52 50 48\n"])
    assert list(r) == [(52,50,48), (50,98,2)]

def test_from_range():
    r = five.RangeMap.from_list([(50, 98, 2), (52, 50, 48)])
    # 50->52,...,97->99, 98->50, 99->51
    assert r[2] == 2
    assert r[50] == 52
    assert r[52] == 54
    assert r[97] == 99
    assert r[98] == 50
    assert r[99] == 51
    assert r[100] == 100

def test_map_run():
    r = five.RangeMap.from_list([(50, 98, 2), (52, 50, 48)])
    rr = list(r.map_run(50, 10).as_gaplass_range())
    assert rr == [ (52, 50, 10) ]

    rr = list(r.map_run(40, 5).as_gaplass_range())
    assert rr == [ (40, 40, 5) ]

    rr = list(r.map_run(40, 20).as_gaplass_range())
    assert rr == [ (40, 40, 10), (52, 50, 10)]

    rr = list(r.map_run(95, 20).as_gaplass_range())
    assert rr == [ (97, 95, 3), (50, 98, 2), (100, 100, 15) ]

    rr = list(r.map_run(40, 70).as_gaplass_range())
    assert rr == [ (40, 40, 10), (52, 50, 48), (50, 98, 2), (100, 100, 10) ]

def test_map_range():
    r = five.RangeMap.from_list([(50, 98, 2), (52, 50, 48)])
    rr = list(r.map_range(10, 20, 5).as_gaplass_range())
    assert rr == [ (10,20,5) ]

    rr = list(r.map_range(60, 20, 5).as_gaplass_range())
    assert rr == [ (62, 20, 5) ]

    rr = list(r.map_range(90, 200, 20))
    assert rr == [ (92, 200, 8), (50,208,2), (100,210,10)]

def test_gapless_range():
    r = five.RangeMap.from_list([ (20, 35, 5), (10, 42, 3)])
    # 35->20, ..., 39->24,  40->40, 41->41, 42->10, 43->11
    gapless = list(r.as_gaplass_range())
    assert gapless[0] == (20, 35, 5)
    assert gapless[1] == (40, 40, 2)
    assert gapless[2] == (10, 42, 3)
    assert len(gapless) == 3

def test_parse_seeds():
    assert five.parse_seeds("seeds: 5 1031  15432\n") == [5, 1031, 15432]

def test_parse_map_section():
    lines = ["seed-to-soil map:\n", "50 98 2\n", "52 50 48\n", "\n"]
    out = five.parse_map_section(iter(lines))
    assert out[0] == ("seed", "soil")
    assert out[1][98] == 50

def test_compute_locations():
    map1 = {5:7, 10:12, 11:9}
    map2 = {7:15, 12:19, 9:9}
    assert five.compute_locations([5,10], [map1, map2]) == [15, 19]

def test_second_example_data():
    with open(os.path.join("tests", "test_5.txt")) as f:
        assert five.second(f) == 46
