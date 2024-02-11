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




def test_PartialSolution_greedyfind(example1):
    ps = twelve.PartialSolution(example1, "???.###")
    assert ps.greedy_find() == "#.#.###"
    ps = twelve.PartialSolution(example1, "?.?.###")
    assert ps.greedy_find() == "#.#.###"
    ps = twelve.PartialSolution(example1, "??..###")
    assert ps.greedy_find() is None

def test_PartialSolution_isvalid(example1):
    ps = twelve.PartialSolution(example1, "???.###")
    with pytest.raises(AssertionError):
        ps.is_valid

    ps = twelve.PartialSolution(example1, "#.#.###")
    assert ps.is_valid

    ps = twelve.PartialSolution(example1, "##..###")
    assert not ps.is_valid


def test_PartialSolution_greedyfind2(example2):
    ps = twelve.PartialSolution(example2, ".??..??...?##")
    assert ps.greedy_find() == ".#...#....###"
    ps = twelve.PartialSolution(example2, ".?...??...?##")
    assert ps.greedy_find() == ".#...#....###"
    ps = twelve.PartialSolution(example2, "..?..??...?##")
    assert ps.greedy_find() == "..#..#....###"
    ps = twelve.PartialSolution(example2, ".??..??....##")
    assert ps.greedy_find() is None

def test_PartialSolution_branch():
    ps = twelve.PartialSolution(None, ".??..##")
    a, b = ps.branch()
    assert a.guess == "..?..##"
    assert b.guess == ".#?..##"

def test_search(example1):
    assert twelve.search(example1) == ["#.#.###"]

def test_search2(example2):
    assert len(twelve.search(example2)) == 4

def test_example():
    with open(os.path.join("tests", "test_12.txt")) as f:
        assert twelve.count_all_solutions(f) == 21
    
def test_SpringLine_unfold():
    sl = twelve.SpringLine(".# 1", True)
    assert sl.codes == [1,1,1,1,1]
    assert sl.row == ".#?.#?.#?.#?.#"

def test_SpringLine_split():
    sl = twelve.SpringLine("???.### 1,2,3")
    assert sl.split() == ["???", "###"]

    sl = twelve.SpringLine(".??..??...?##. 1,1,3")
    assert sl.split() == ["??", "??", "?##"]

def test_reduced_end():
    assert twelve.reduce_end("??#####.", [4,4]) is None
    assert twelve.reduce_end("??####", [2,4]) == [("?", [2])]
    assert twelve.reduce_end("?.####", [2,4]) == [("?", [2])]
    assert twelve.reduce_end("?..###", [2,4]) is None
    assert twelve.reduce_end("?.#??#", [2,4]) == [("?", [2])]
    assert twelve.reduce_end("#?#??#", [1,2,4]) == [("#", [1,2])]
    assert twelve.reduce_end("###??#", [1,2,4]) is None
    assert twelve.reduce_end("####", [4]) == [("",[])]
    assert twelve.reduce_end(".####", [4]) == [("",[])]
    assert twelve.reduce_end("?####", [4]) == [("",[])]
    assert twelve.reduce_end("..", [1,2,4]) is None
    assert twelve.reduce_end("###???", [1,2,4]) == [("###??", [1,2,4]), ("###??#", [1,2,4])]
    assert twelve.reduce_end("??.", [3]) == [("?",[3]), ("?#",[3])]
    assert twelve.reduce_end("?.", []) == [("",[])]
    assert twelve.reduce_end("?.", [3]) == [("#", [3])]
    assert twelve.reduce_end("..", []) == [("",[])]
    assert twelve.reduce_end('.#', [1, 1]) is None
    
    assert twelve.reduce_end("???.###", [1,1,3]) == [("???", [1,1])]
    assert twelve.reduce_end("???", [1,1]) == [("??", [1,1]), ("??#", [1,1])]
    assert twelve.reduce_end("??#", [1,1]) == [("?", [1])]
    assert twelve.reduce_end("??", [1,1]) == [("?", [1,1]), ("?#", [1,1])]
    assert twelve.reduce_end("?", [1]) == [("#",[1])]
    assert twelve.reduce_end("?", [1,1]) == [("#", [1,1])]
    assert twelve.reduce_end("?#", [1,1]) is None

def test_count_solutions_new(example2):
    assert twelve.count_solutions_new(example2) == 4

def test_count_solutions_new2():
    sl = twelve.SpringLine("???.### 1,1,3")
    assert twelve.count_solutions_new(sl) == 1

def test_example_new():
    with open(os.path.join("tests", "test_12.txt")) as f:
        assert twelve.count_all_solutions_new(f) == 21

# ---------------------------------------------------------------

# twelve.SpringLine("??#????.????#??? 4,2,5,1")
# twelve.SpringLine("?.###?#?#??.? 1,7")

def test_split():
    sl = twelve.FastSpringLine("??#...###.??#?. 2,3,2")
    assert sl.split() == ["??#", "###", "??#?"]

def test_SharpBlock():
    sb = twelve.SharpBlock("???######??#?")
    assert list(sb) == [("?",3), ("#",6), ("?",2), ("#",1), ("?",1)]

    with pytest.raises(AssertionError):
        twelve.SharpBlock("???.##")

def test_SharpBlock_assignments():
    sb = twelve.SharpBlock("???######??#?")
    assert list(sb.assignments([1,7,1])) == [[1,2]]
    assert list(sb.assignments([1,6,3])) == [[1,2]]
    assert list(sb.assignments([5,3])) == []
    assert list(sb.assignments([1,6])) == []
    assert list(sb.assignments([9])) == [[0,0]]
    assert list(sb.assignments([9,2])) == [[0,0], [0,1]]
