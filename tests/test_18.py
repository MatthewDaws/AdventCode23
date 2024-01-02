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

    