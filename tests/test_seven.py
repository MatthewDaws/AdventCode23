import pytest
import io

import advent.seven as seven

def test_Card():
    c = seven.Card("K")
    c = seven.Card("3")
    assert not c.is_joker
    with pytest.raises(ValueError):
        seven.Card("G")
    c = seven.Card("J")
    assert not c.is_joker
    c = seven.Card("J", True)
    assert c.is_joker
    c = seven.Card("5", True)
    assert not c.is_joker

def test_Card_ordering():
    assert seven.Card("K") == seven.Card("K")
    assert seven.Card("K") <= seven.Card("K")
    assert seven.Card("A") < seven.Card("K")
    assert seven.Card("3") > seven.Card("T")
    assert seven.Card("J") < seven.Card("2")
    assert not seven.Card("J") > seven.Card("2")
    assert seven.Card("J", True) > seven.Card("2")

def test_Hand():
    assert seven.Hand.parse("AAAAA").type == seven.HandType.FIVE_OF_A_KIND
    assert seven.Hand.parse("AA8AA").type == seven.HandType.FOUR_OF_A_KIND
    assert seven.Hand.parse("23332").type == seven.HandType.FULL_HOUSE
    assert seven.Hand.parse("TTT98").type == seven.HandType.THREE_OF_A_KIND
    assert seven.Hand.parse("23432").type == seven.HandType.TWO_PAIR
    assert seven.Hand.parse("A23A4").type == seven.HandType.ONE_PAIR
    assert seven.Hand.parse("23456").type == seven.HandType.HIGH_CARD

    assert seven.Hand.parse("QJJQ2").type == seven.HandType.TWO_PAIR
    assert seven.Hand.parse("QJJQ2", True).type == seven.HandType.FOUR_OF_A_KIND

    seven.Hand.parse("JJJJJ", True)

def test_Hand_ordering():
    assert seven.Hand.parse("AAAAA") == seven.Hand.parse("AAAAA")
    assert seven.Hand.parse("AAAAA") <= seven.Hand.parse("AAAAA")
    assert not seven.Hand.parse("AA8AA") == seven.Hand.parse("8AAAA")

    assert seven.Hand.parse("AAAA8") < seven.Hand.parse("55555")
    assert seven.Hand.parse("AAAA8") <= seven.Hand.parse("55555")
    assert seven.Hand.parse("55555") > seven.Hand.parse("AAAA8")

    assert not seven.Hand.parse("AAAA8") > seven.Hand.parse("55555")
    assert not seven.Hand.parse("AAAA8") >= seven.Hand.parse("55555")
    assert not seven.Hand.parse("55555") < seven.Hand.parse("AAAA8")
    assert not seven.Hand.parse("55555") <= seven.Hand.parse("AAAA8")

    assert seven.Hand.parse("AAAA8") > seven.Hand.parse("A8AAA")
    assert seven.Hand.parse("33332") > seven.Hand.parse("2AAAA")
    assert seven.Hand.parse("33332") >= seven.Hand.parse("2AAAA")
    assert seven.Hand.parse("77888") > seven.Hand.parse("77788")

    assert seven.Hand.parse("JK863") > seven.Hand.parse("69A48")
    assert not seven.Hand.parse("JK863") < seven.Hand.parse("69A48")
    assert seven.Hand.parse("JK863") >= seven.Hand.parse("69A48")
    assert seven.Hand.parse("69A48") < seven.Hand.parse("JK863")
    assert seven.Hand.parse("69A48") <= seven.Hand.parse("JK863")

def test_parse():
    data = io.StringIO("32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483\n")
    bids = seven.parse(data)
    assert len(bids) == 5
    assert bids[2][1] == 28

def test_sort():
    data = io.StringIO("32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483\n")
    bids = seven.sort_bids( seven.parse(data) )
    assert bids[0][1] == 765
    assert bids[-1][1] == 483

def test_sort_in_real_file_problem():
    a = (seven.Hand.parse("JK863"), 10)
    b = (seven.Hand.parse("69A48"), 15)
    data = [a, b]
    data = seven.sort_bids(data)
    assert data[0][1] == 15
    assert data[1][1] == 10

def test_winnings():
    data = io.StringIO("32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483\n")
    assert seven.winnings( seven.parse(data) ) == 6440
    
    data = io.StringIO("32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483\n")
    assert seven.winnings( seven.parse(data, True) ) == 5905
    