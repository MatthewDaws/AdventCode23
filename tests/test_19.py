import pytest, io, os

import advent.nineteen as nineteen

def test_parse():
    with open(os.path.join("tests", "test_19.txt")) as f:
        p = nineteen.Parse(f)

    assert "px" in p.commands
    assert len(p.commands) == 11
    assert len(p.data) == 5

@pytest.fixture
def parsed():
    with open(os.path.join("tests", "test_19.txt")) as f:
        yield nineteen.Parse(f)

def test_parse_commands(parsed):
    assert parsed.commands["px"][0]({"a":1000}) == "qkq"
    assert parsed.commands["px"][0]({"a":2006}) is None
    assert parsed.commands["px"][1]({"m":2090}) is None
    assert parsed.commands["px"][1]({"m":2091}) == "A"
    assert parsed.commands["px"][2](None) == "rfg"

def test_parse_data(parsed):
    assert parsed.data[0] == {"x":787, "m":2655, "a":1222, "s":2876}

def test_compute_accept_reject(parsed):
    results = parsed.compute_accept_reject()
    assert results == [True, False, True, False, True]

def test_score(parsed):
    assert parsed.score([True, False, True, False, True]) == 19114

def test_Interval():
    a = nineteen.Interval()
    b = nineteen.Interval(100, 1000)
    with pytest.raises(ValueError):
        nineteen.Interval(5, 2)
    c = a.intersect(b)
    assert [c.start, c.end] == [100, 1000]
    d = nineteen.Interval(50, 70)
    assert d.intersect(b) is None

    assert a.complement() == []
    assert b.complement() == [nineteen.Interval(1,99), nineteen.Interval(1001,4000)]
    assert nineteen.Interval(1,2123).complement() == [nineteen.Interval(2124,4000)]

def test_VariableInterval():
    vi = nineteen.VariableInterval()
    assert vi["x"].start == 1
    assert vi["m"].end == 4000
    assert vi.choices() == 4000**4

    vi["a"] = nineteen.Interval(5, 10)
    with pytest.raises(KeyError):
        vi["b"] = 7
    assert vi.choices() == 4000**3 * 6

    vi1 = nineteen.VariableInterval()
    vi1["a"] = nineteen.Interval(6, 15)

    vi2 = vi.intersect(vi1)
    assert vi2["a"].start == 6
    assert vi2["a"].end == 10

    assert vi.complement() == []

def test_DecisionTree(parsed):
    dt = nineteen.DecisionTree(parsed)
    next_level = dt.compute_next_level(None)
    assert len(next_level) == 2
    assert next_level[0][0] == "px"
    assert repr(next_level[0][1]) == "VariableInterval(x=[1,4000], m=[1,4000], a=[1,4000], s=[1,1350])"
    assert next_level[1][0] == "qqz"
    assert repr(next_level[1][1]) == "VariableInterval(x=[1,4000], m=[1,4000], a=[1,4000], s=[1351,4000])"
 
    next_level = dt.compute_next_level(next_level)
    assert len(next_level) == 6
    assert next_level[0][0] == "qkq"
    assert repr(next_level[0][1]) == "VariableInterval(x=[1,4000], m=[1,4000], a=[1,2005], s=[1,1350])"
    assert next_level[1][0] == "A"
    assert repr(next_level[1][1]) == "VariableInterval(x=[1,4000], m=[2091,4000], a=[2006,4000], s=[1,1350])"
    assert next_level[2][0] == "rfg"
    assert repr(next_level[2][1]) == "VariableInterval(x=[1,4000], m=[1,2090], a=[2006,4000], s=[1,1350])"
    assert next_level[3][0] == "qs"
    assert repr(next_level[3][1]) == "VariableInterval(x=[1,4000], m=[1,4000], a=[1,4000], s=[2771,4000])"
    assert next_level[4][0] == "hdj"
    assert repr(next_level[4][1]) == "VariableInterval(x=[1,4000], m=[1,1800], a=[1,4000], s=[1351,2770])"
    assert next_level[5][0] == "R"
    assert repr(next_level[5][1]) == "VariableInterval(x=[1,4000], m=[1801,4000], a=[1,4000], s=[1351,2770])"

def test_DecisionTree_compute_all(parsed):
    dt = nineteen.DecisionTree(parsed)
    results = dt.compute_tree()
    accept_intervals = [vi for name, vi in results if name=="A"]
    import itertools
    for pair in itertools.combinations(accept_intervals, 2):
        vi = pair[0].intersect(pair[1])
        assert vi.choices() == 0

def test_DecisionTree_2nd_example(parsed):
    dt = nineteen.DecisionTree(parsed)
    assert dt.choices() == 167409079868000
    