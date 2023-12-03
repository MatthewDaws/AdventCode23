import pytest

import advent.three as three

def test_parse_line():
    #########################01234567890123456
    n, s = three.parse_line("..321*.#.43...\n")
    assert s == [5, 7]
    assert n == [(321,[2,3,4]), (43, [9,10])]

    # Argh: numbers at the end of the line matter!
    #########################01234567890123456
    n, s = three.parse_line("..321*.#....71\n")
    assert s == [5, 7]
    assert n == [(321,[2,3,4]), (71, [12,13])]

def test_parse_line_only_gears():
    #########################01234567890123456
    n, s = three.parse_line("..321*.#.43...\n", only_gears=True)
    assert s == [5]
    assert n == [(321,[2,3,4]), (43, [9,10])]

def test_input_to_locations():
    ##################################0123456789
    n, s = three.input_to_locations(["467..114..",
                                     "...*......",
                                     "..35.#633."])
    assert s == [(1,3), (2,5)]
    assert n == [ (467,[(0,0),(0,1),(0,2)]), (114,[(0,5),(0,6),(0,7)]), (35,[(2,2),(2,3)]), (633,[(2,6),(2,7),(2,8)]) ]

def test_sum_next_to_symbol():
    n, s = three.input_to_locations(["467..114..",
                                     "...*......",
                                     "..35.#633."])
    assert three.sum_next_to_symbol(n,s, count_all=False) == 467+35+633

def test_sum_gear_ratios():
    n, s = three.input_to_locations(["467..114..",
                                     "...*......",
                                     "..35.#633."], only_gears=True)
    assert three.sum_gear_ratios(n,s) == 467*35

def test_sum_next_to_symbol2():
    n, s = three.input_to_locations( [ "467..114..\n", "...*......\n", "..35..633.\n",
        "......#...\n", "617*......\n", ".....+.58.\n", "..592.....\n",
        "......755.\n", "...$.*....\n", ".664.598..\n", " " ] )
    assert three.sum_next_to_symbol(n,s, count_all=False) == 4361

def test_sum_next_to_symbol3():
    n, s = three.input_to_locations( [ "467..114..\n", "...*......\n", "..35..633.\n",
        "......#...\n", "617*......\n", ".....+.664\n", "..592.....\n",
        "......755.\n", "...$.*....\n", ".664.664..\n", " " ] )
    assert three.sum_next_to_symbol(n,s, count_all=True) == 4361-598+664
    assert three.sum_next_to_symbol(n,s, count_all=False) == 4361-598

def test_write_debug():
    n, s = three.input_to_locations(["467..114..",
                                     "...*......",
                                     "..35.#633."])
    out = three.write_debug(n, s, zero_out=True)
    assert out == "000......\n...#.....\n..00.#000"
    out = three.write_debug(n, s)
    assert out == "467......\n...#.....\n..35.#633"
