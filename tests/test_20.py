import pytest, io, os

import advent.twenty as twenty
from advent.twenty import Pulse

def test_FlipFlop():
    f = twenty.FlipFlop()
    assert f.handle(Pulse.HIGH) is None
    assert f.handle(Pulse.LOW) == Pulse.HIGH
    assert f.state == 1
    assert f.handle(Pulse.LOW) == Pulse.LOW
    assert f.state == 0
    assert f.handle(Pulse.LOW) == Pulse.HIGH
    assert f.handle(Pulse.LOW) == Pulse.LOW

def test_Conjunction_single_input():
    c = twenty.Conjunction(["a"])
    assert c.handle(Pulse.LOW, "a") == Pulse.HIGH
    assert c.state == [Pulse.LOW]
    assert c.handle(Pulse.LOW, "a") == Pulse.HIGH
    assert c.handle(Pulse.HIGH, "a") == Pulse.LOW
    assert c.handle(Pulse.HIGH, "a") == Pulse.LOW
    assert c.handle(Pulse.LOW, "a") == Pulse.HIGH
    assert c.handle(Pulse.HIGH, "a") == Pulse.LOW

def test_Conjunction_many_inputs():
    c = twenty.Conjunction(["a", "b", "c"])
    assert c.handle(Pulse.HIGH, "a") == Pulse.HIGH
    assert c.state == [Pulse.HIGH, Pulse.LOW, Pulse.LOW]
    assert c.handle(Pulse.HIGH, "b") == Pulse.HIGH
    assert c.state == [Pulse.HIGH, Pulse.HIGH, Pulse.LOW]
    assert c.handle(Pulse.HIGH, "c") == Pulse.LOW
    assert c.state == [Pulse.HIGH, Pulse.HIGH, Pulse.HIGH]
    assert c.handle(Pulse.LOW, "b") == Pulse.HIGH
    assert c.state == [Pulse.HIGH, Pulse.LOW, Pulse.HIGH]

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test_20a.txt")) as f:
        yield f

def test_Parse1(eg1):
    w = twenty.Wiring(eg1)
    assert w["broadcaster"] == ["a", "b", "c"]
    assert w["inv"][1] == ["a"]
    assert w.state() == [0,0,0,[Pulse.LOW]]
    assert w["inv"][0].handle(Pulse.HIGH, "c") == Pulse.LOW
    assert w.state() == [0,0,0,[Pulse.HIGH]]

def test_button1(eg1):
    w = twenty.Wiring(eg1)
    w.button()
    assert w.pulses_sent == (8, 4)

def test_watch_flipflop(eg1):
    w = twenty.Wiring(eg1)
    w.set_watch("a")
    assert not w.seen_watched
    w.button()
    assert w.seen_watched

@pytest.fixture
def eg2():
    with open(os.path.join("tests", "test_20b.txt")) as f:
        yield f

def test_button2(eg2):
    w = twenty.Wiring(eg2)
    w.button(1000)
    assert w.pulses_sent == (4250, 2750)

def test_maps_to(eg2):
    w = twenty.Wiring(eg2)
    assert set(w.maps_to("con")) == {"a", "b"}

def test_reset(eg2):
    w = twenty.Wiring(eg2)
    w.button(1)
    assert w["con"][0].state == [Pulse.HIGH, Pulse.HIGH]
    w.reset()
    assert w["con"][0].state == [Pulse.LOW, Pulse.LOW]
