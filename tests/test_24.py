import pytest, os

import advent.twentyfour as twentyfour

def test_parse():
    with open(os.path.join("tests", "test_24.txt")) as f:
        h = twentyfour.HailStones(f)
    assert h.entries == 5
    assert h.position(2) == (20,25,34)
    assert h.velocity(2) == (-2,-2,-4)

@pytest.fixture
def eg():
    with open(os.path.join("tests", "test_24.txt")) as f:
        h = twentyfour.HailStones(f)
    return h

def test_collisions(eg):
    assert eg.intersect(0,1,(7,27))
    assert eg.intersect(0,2,(7,27))
    assert not eg.intersect(0,3,(7,27))
    assert not eg.intersect(0,4,(7,27))
    assert not eg.intersect(1,2,(7,27))
    assert not eg.intersect(1,3,(7,27))
    assert not eg.intersect(1,4,(7,27))
    assert not eg.intersect(2,3,(7,27))
    assert not eg.intersect(2,4,(7,27))
    assert not eg.intersect(3,4,(7,27))

def test_count(eg):
    assert eg.count_intersections((7,27)) == 2

@pytest.fixture
def ch(eg):
    return twentyfour.Solve(eg)

def test_Solve(ch):
    for v, d in ch.pos_vel_pairs():
        assert v == twentyfour.Vector(19, 13, 30)
        assert d == twentyfour.Vector(-2,  1, -2)
        break

def test_brute_force(ch):
    pairs = list(ch.pos_vel_pairs())
    (u1,d1), (u2,d2), (u3,d3) = pairs[:3]
    a,b,c,d = ch.compute_direction_matrix(u1,d1,u2,d2,u3,d3)
    assert (a,b,c,d) == (-5,1,0,0)
    t1 = 5
    t2 = 3
    assert a + b*t1 +c*t2 + d*t1*t2== 0

    u3,d3 = pairs[3]
    aa,bb,cc,dd = ch.compute_direction_matrix(u1,d1,u2,d2,u3,d3)
    assert (aa,bb,cc,dd) == (-264, 60, -37, 5)
    assert aa + bb*t1 + cc*t2 + dd*t1*t2 == 0
    # Check the collision times from the question
    assert u1 + t1*d1 == twentyfour.Vector(9,18,20)
    assert u2 + t2*d2 == twentyfour.Vector(15,16,16)

    alpha = b*dd - bb*d
    beta = a*dd + b*cc - aa*d - bb*c
    gamma = a*cc - aa*c
    #print(alpha, beta, gamma)
    assert alpha*t1*t1 + beta*t1 + gamma == 0
    # This needs fixing!!!
    assert twentyfour.util.integer_quadratic(alpha,beta,gamma) == [5]

def test_find_t1(ch):
    assert ch.find_t1() == 5

def test_fine_t1t2(ch):
    assert ch.find_t1t2() == (5, 3)

def test_find_line(ch):
    u, d = ch.find_line()
    assert u == twentyfour.Vector(9, 18, 20)
    assert d == twentyfour.Vector(3, -1, -2)

def test_find_intersection(ch):
    ch.find_line()
    pairs = list(ch.pos_vel_pairs())
    t,s = ch.find_intersection(*pairs[0])
    assert t == 5
    assert s == 5-t
    t,s = ch.find_intersection(*pairs[1])
    assert t == 3
    assert s == 5-t
    for p in pairs:
        t,s = ch.find_intersection(*p)
        assert s == 5-t

def test_find_starting_point(ch):
    ch.find_line()
    start, direction = ch.find_starting_point()
    assert start == twentyfour.Vector(24, 13, 10)
    assert direction == twentyfour.Vector(-3,1,2)

    ch.check(start, direction)
