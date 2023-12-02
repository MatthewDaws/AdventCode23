import pytest

import advent.one as one

def test_first_digit():
    assert one.first_num("1") == 1
    assert one.first_num("4622") == 4
    assert one.first_num("ahjfs267ajf27") == 2

def test_last_digit():
    assert one.last_num("1") == 1
    assert one.last_num("4622") == 2
    assert one.last_num("ahjfs267ajf27") == 7

def test_sum():
    assert one.sum_first_last("1abc2") == 12
    assert one.sum_first_last("pqr3stu8vwx") == 38
    assert one.sum_first_last("a1b2c3d4e5f") == 15
    assert one.sum_first_last("treb7uchet") == 77

def test_initial_string_match():
    assert one.initial_string_match("asdhgf", "asd")
    assert not one.initial_string_match("abc", "ahjfdgj")
    assert not one.initial_string_match("ajkdfgh", "jkd")

def test_first_num_2nd():
    assert one.first_num_2nd("ags1a") == 1
    assert one.first_num_2nd("asgone") == 1
    assert one.first_num_2nd("a4twoas") == 4
    assert one.first_num_2nd("atwoas") == 2

def test_last_num_2nd():
    assert one.last_num_2nd("ahdg32as") == 2
    assert one.last_num_2nd("ahdg32anines") == 9
    assert one.last_num_2nd("a13aseights") == 8

def test_sum_first_last_2nd():
    assert one.sum_first_last_2nd("two1nine") == 29
    assert one.sum_first_last_2nd("eightwothree") == 83
    assert one.sum_first_last_2nd("abcone2threexyz") == 13
    assert one.sum_first_last_2nd("xtwone3four") == 24
    assert one.sum_first_last_2nd("4nineeightseven2") == 42
    assert one.sum_first_last_2nd("zoneight234") == 14
    assert one.sum_first_last_2nd("7pqrstsixteen") == 76
