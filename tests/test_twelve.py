import pytest, io, os

import advent.twelve as twelve

def test_parse():
    sl = twelve.SpringLine("???.### 1,1,3")
    assert sl.row == "???.###"
    assert sl.codes == [1,1,3]

@pytest.fixture
def example1():
    return twelve.SpringLine("???.### 1,1,3")

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

@pytest.fixture
def example2():
    return twelve.SpringLine(".??..??...?##. 1,1,3")

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

def atest_slow():
    sl = twelve.SpringLine("??.???.#?????.???.#?????.???.#?????.???.#?????.???.#?? 1,1,2,1,1,2,1,1,2,1,1,2,1,1,2")

    assert twelve.count_solutions_new(sl) == 645189


def atest_analysis():
    with open("input_12.txt") as f:
        diffs = []
        for row in f:
            sl = twelve.SpringLine(row, True)
            minlength = sum(sl.codes) + len(sl.codes) - 1
            length = len(sl.row)
            diffs.append(length-minlength)
            if diffs[-1]>10:
                print(sl.row, sl.codes)
    #print(diffs)
    raise Exception()