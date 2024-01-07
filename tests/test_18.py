import pytest, io, os

import advent.eighteen as eighteen

def test_DigPlan():
    with open(os.path.join("tests", "test_18.txt")) as f:
        dp = eighteen.DigPlan(f)

    assert dp.instructions[0] == ("R", 6, "70c710")

def test_DigPlan_dig():
    with open(os.path.join("tests", "test_18.txt")) as f:
        dp = eighteen.DigPlan(f)
    grid = dp.dig()
    assert len(grid) == 10
    assert len(grid[0]) == 7
    assert grid[1][0] == 1
    assert grid[1][1] == 0
    assert dp.count_dug(grid) == 38

def test_DigPlan_path():
    with open(os.path.join("tests", "test_18.txt")) as f:
        dp = eighteen.DigPlan(f)
    p = dp.path()
    for i, pos in enumerate(p):
        if i == 0:
            assert pos == (0,0)
        elif i == 1:
            assert pos == (0,1)

def test_DigPlan_fillin():
    with open(os.path.join("tests", "test_18.txt")) as f:
        dp = eighteen.DigPlan(f)
    grid = dp.dig()
    dp.fill_in_dig(grid)
    assert dp.count_dug(grid) == 62

def test_DigPlan_offset():
    dp = eighteen.DigPlan(["R 5 (#000000)", "D 5 (#000000)", "L 10 (#000000)", "U 12 (#000000)", "R 5 (#000000)", "D 7 (#000000)"])
    grid = dp.dig()
    assert dp.count_dug(grid) == 5+5+10+12+5+7
    
def test_DigPlan2():
    with open(os.path.join("tests", "test_18.txt")) as f:
        dp = eighteen.DigPlan2(f)
    assert dp.instructions[0] == ("R", 461937)

def test_right_angle_conjecture():
    with open("input_18.txt") as f:
        dp = eighteen.DigPlan2(f)
    current_dir = None
    for direction, length in dp.instructions:
        if current_dir is not None:
            if current_dir in ["U", "D"]:
                assert direction in ["L", "R"]
            else:
                assert direction in ["U", "D"]
        current_dir = direction

def test_Construct():
    with open(os.path.join("tests", "test_18.txt")) as f:
        dp = eighteen.DigPlan(f)
    rows, cols = eighteen.construct_row_plan(dp.instructions_without_colours())
    assert rows[0] == [eighteen.Interval(0,6)]
    assert rows[2] == [eighteen.Interval(0,2)]
    assert rows[5] == [eighteen.Interval(0,2), eighteen.Interval(4,6)]
    assert cols[0] == [(0,"D"), (6,"D")]
    assert cols[5] == [(0,"D"), (2,"U"), (4,"D"), (6,"U")]

def test_compute_all_up_downs():
    with open(os.path.join("tests", "test_18.txt")) as f:
        dp = eighteen.DigPlan(f)
    _, cols = eighteen.construct_row_plan(dp.instructions_without_colours())
    all_ud = eighteen.compute_all_up_downs(cols)
    assert set(all_ud.keys()) == {0,2,5,7,9}
    assert all_ud[0] == [0, 6]
    assert all_ud[2] == [2, 6]
    assert all_ud[5] == [0, 4]
    assert all_ud[7] == [1, 6]
    assert all_ud[9] == []

def test_find_area():
    with open(os.path.join("tests", "test_18.txt")) as f:
        dp = eighteen.DigPlan(f)
    _, cols = eighteen.construct_row_plan(dp.instructions_without_colours())
    all_ud = eighteen.compute_all_up_downs(cols)
    assert eighteen.compute_area(all_ud) == 62

def test_problem1():
    with open("input_18.txt") as f:
        dp = eighteen.DigPlan(f)
    _, cols = eighteen.construct_row_plan(dp.instructions_without_colours())
    all_ud = eighteen.compute_all_up_downs(cols)
    assert eighteen.compute_area(all_ud) == 47139

def test_find_area2():
    with open(os.path.join("tests", "test_18.txt")) as f:
        dp = eighteen.DigPlan2(f)
    assert eighteen.area_from_digplan2(dp) == 952408144115
