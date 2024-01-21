import pytest, os

import advent.twentythree as twentythree

def test_parse():
    with open(os.path.join("tests", "test_23.txt")) as f:
        forest = twentythree.Forest(f)
    assert forest.start_column == 1
    assert forest.finish_column == 21
    assert forest.at(0,0) == "#"
    assert forest.at(-1,0) is None
    assert forest.at(2,-1) is None

@pytest.fixture
def eg():
    with open(os.path.join("tests", "test_23.txt")) as f:
        return twentythree.Forest(f)

def test_directions(eg):
    assert list(eg.possible_directions(0,1)) == [(1,0)]
    assert set(eg.possible_directions(5,3)) == {(1,0), (0,1)}
    assert list(eg.possible_directions(5,11)) == [(1,0)]
    assert set(eg.possible_directions(11,20)) == {(0,-1),(0,1)}
    assert set(eg.possible_directions(1,1)) == {(-1,0), (0,1)}

def test_build_graph(eg):
    assert eg.vertices[0] == (0,1)
    assert eg.vertices[-1] == (eg.height-1, eg.finish_column)
    assert len(eg.neighbours(0)) == 1
    vi, l = eg.neighbours(0)[0]
    assert eg.vertices[vi] == (5,3)
    assert l == 15
    final_index = len(eg.vertices) - 1
    assert eg.neighbours(final_index) == []

def test_top_sort(eg):
    ts = eg.find_dag()

def test_longest_path(eg):
    assert eg.longest_path() == 94

def test_2nd_parse_build_graph():
    with open(os.path.join("tests", "test_23.txt")) as f:
        forest = twentythree.Forest2(f)

@pytest.fixture
def eg2():
    with open(os.path.join("tests", "test_23.txt")) as f:
        return twentythree.Forest2(f)

def test_2nd_graph(eg2):
    g = eg2.build_undirected_graph()
    assert len(list(g.neighbours_of(0))) == 1
    _l, length = list(g.weighted_neighbours_of(0))[0]
    assert length == 15

def test_2nd_longest_path(eg2):
    assert eg2.longest_path() == 154
