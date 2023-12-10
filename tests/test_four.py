import pytest

import advent.four as four

def test_number_list_to_numbers():
    assert four.number_list_to_numbers("12 34 5") == [12, 34, 5]
    assert four.number_list_to_numbers("12  5   8") == [12, 5, 8]

def test_parse_line():
    n, w, h = four.parse_line("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert n==1
    assert w==[41, 48, 83, 86, 17]
    assert h==[83, 86,  6, 31, 17,  9, 48, 53]

def test_line_value():
    assert four.line_value([41, 48, 83, 86, 17], [83, 86,  6, 31, 17,  9, 48, 53]) == 8
    assert four.line_value([87, 83, 26, 28, 32], [88, 30, 70, 12, 93, 22, 82, 36,]) == 0

def test_multiplying_counts():
    i = [4, 2, 2, 1, 0, 0]
    assert four.multiplying_counts(i) == 30
