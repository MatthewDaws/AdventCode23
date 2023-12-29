import pytest, io, os

import advent.seventeen as seventeen

def test_grid():
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    assert grid.cost(0,1) == 4

def test_grid_possible_directions():
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    assert list(grid.possible_destinations(0,0,"s")) == [(0,1,"e"), (0,2,"e"), (0,3,"e")]
    assert list(grid.possible_destinations(4,4,"e")) == [(3,4,"n"), (2,4,"n"), (1,4,"n"), (5,4,"s"), (6,4,"s"), (7,4,"s")]

def test_inc_range_skip_start():
    assert list(seventeen.Grid.inc_range_skip_start(5, 8)) == [6,7,8]
    assert list(seventeen.Grid.inc_range_skip_start(8, 5)) == [7,6,5]
    assert list(seventeen.Grid.inc_range_skip_start(5, 5)) == []
    assert list(seventeen.Grid.inc_range_skip_start(5, 6)) == [6]
    assert list(seventeen.Grid.inc_range_skip_start(6, 5)) == [5]

def test_grid_construct_graph():
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    graph = grid.construct_graph()
    assert graph.edge_cost((0,0,"s"), (0,1,"e")) == 4
    assert graph.edge_cost((0,0,"s"), (0,2,"e")) == 5
    assert graph.edge_cost((0,0,"s"), (0,3,"e")) == 8
    with pytest.raises(KeyError):
        graph.edge_cost((0,0,"s"), (0,4,"e"))
    with pytest.raises(KeyError):
        graph.edge_cost((1,1,"s"), (2,1,"e"))
    assert graph.edge_cost((1,1,"s"), (1,0,"w")) == 3

    v = grid.add_start(graph, 0, 0)
    assert graph.edge_cost(v, (0,2,"e")) == 5
    assert graph.edge_cost(v, (1,0,"s")) == 3
    with pytest.raises(KeyError):
        graph.edge_cost(v, (1,1,"e"))

def test_grid_construct_smaller_graph():
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    graph = grid.construct_smaller_graph()
    assert graph.edge_cost((0,0,0), (0,1,1)) == 4
    assert graph.edge_cost((0,0,0), (0,2,1)) == 5
    assert graph.edge_cost((0,0,0), (0,3,1)) == 8
    with pytest.raises(KeyError):
        graph.edge_cost((0,0,0), (0,4,1))

def test_shortest_paths():
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    graph = grid.construct_graph()
    v = grid.add_start(graph, 0, 0)
    distances = seventeen.shortest_paths(graph, v)
    assert distances[v] == 0
    assert distances[(0,1,"e")] == 4

def test_shortest_paths_new():
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    graph = grid.construct_smaller_graph()
    v = grid.add_start(graph, 0, 0)
    distances = seventeen.shortest_paths(graph, v)
    assert distances[v] == 0
    assert distances[(0,1,1)] == 4

def test_find_min_path_top_bottom():
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    assert seventeen.find_min_path_top_bottom(grid) == 102

def test_find_min_path_top_bottom_new():
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    assert seventeen.find_min_path_top_bottom_smaller(grid) == 102

def test_find_min_path_top_bottom_second():
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    assert seventeen.find_min_path_top_bottom_smaller(grid, 4, 10) == 94

def not_test_path():
    """This is already rather slow on the test input."""
    with open(os.path.join("tests", "test_17.txt")) as f:
        grid = seventeen.Grid(f)
    sp = seventeen.ShortestPath(grid)
    sp.take_step()
    assert len(sp._queue) == 2
    assert sp._shortests[0][0] == [(0,"")]
    assert sp._shortests[1][0] == [(3,"s")]
    assert sp._shortests[0][1] == [(4,"e")]

    sp.solve()
    assert sp.shortest_path_to(grid.numrows-1, grid.numcols-1) == 102

def test_graph():
    g = seventeen.Graph()
    g.add_edge((0,0,"s"), (1,0,"s"), 5)
    g.add_edge((0,0,"s"), (0,1,"e"), 2)
    with pytest.raises(ValueError):
        g.add_edge((0,0,"s"), (1,0,"s"), 7)

    choices = list(g.neighbours((0,0,"s")))
    assert len(choices) == 2
