import pytest, io, os

import advent.twelve as twelve

def test_parse():
    sl = twelve.SpringLine("???.### 1,1,3")
    assert sl.row == "???.###"
    assert sl.codes == [1,1,3]

@pytest.fixture
def example1():
    return twelve.SpringLine("???.### 1,1,3")

def test_canplace(example1):
    assert example1.can_place(2, 4)
    for x in range(5, 20):
        assert not example1.can_place(2, x)
    assert not example1.can_place(2, 3)
    assert not example1.can_place(2, 2)
    assert not example1.can_place(2, 1)
    assert example1.can_place(2, 0)

def test_canplace_last(example1):
    assert example1.can_place_last(4)
    assert not example1.can_place_last(0)

def test_dp(example1):
    assert twelve.build_dynamic_programme(example1) == 1

@pytest.fixture
def example2():
    return twelve.SpringLine(".??..??...?##. 1,1,3")

def test_dp2(example2):
    assert twelve.build_dynamic_programme(example2) == 4

@pytest.fixture
def example3():
    return twelve.SpringLine("?###???????? 3,2,1")

def test_dp3(example3):
    assert not example3.can_place(0, 0)
    assert example3.can_place(0, 1)
    assert not example3.can_place(0, 2)
    assert twelve.build_dynamic_programme(example3) == 10

# I think we miss some global checks...
# Can solve by checking no "#" appears in a "gap"
def test_corner_case():
    sl = twelve.SpringLine("?#???#???#? 2,1")
    for x in range(11):
        if sl.can_place_last(x):
            assert x==9

    assert twelve.build_dynamic_programme(sl) == 0

def test_example_with_dp():
    with open(os.path.join("tests", "test_12.txt")) as f:
        for row, expected in zip(f, [1,4,1,1,4,10]):
            sl = twelve.SpringLine(row)
            assert twelve.build_dynamic_programme(sl) == expected

def test_example_with_dp_unfolded():
    with open(os.path.join("tests", "test_12.txt")) as f:
        for row, expected in zip(f, [1,16384,1,16,2500,506250]):
            sl = twelve.SpringLine(row, True)
            assert twelve.build_dynamic_programme(sl) == expected
