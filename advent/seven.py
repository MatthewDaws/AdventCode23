import enum
import collections

class Card():
    # Probably should have been an enum
    def __init__(self, c, jokers=False):
        self._string = c
        _parse = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        self._rank = None
        for rank in range(0, len(_parse)):
            if c == _parse[rank]:
                self._rank = rank
                break
        if self._rank is None:
            raise ValueError()
        self._jokers = jokers
        if jokers and c=="J":
            self._rank = 13

    def __eq__(self, other):
        return self._rank == other._rank

    def __lt__(self, other):
        return self._rank < other._rank

    def __le__(self, other):
        return self._rank <= other._rank

    def __hash__(self):
        return self._rank

    def value(self):
        return self._rank

    def __repr__(self):
        return self._string

    @property
    def is_joker(self):
        return self._jokers and self._string == "J"


class HandType(enum.Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


class Hand():
    def __init__(self, hand):
        assert len(hand) == 5
        self._hand = hand
        c = collections.Counter(hand)
        
        joker = Card("J", True)
        if joker in c and len(c.most_common()) > 1:
            joker_count = c[joker]
            c[joker] = 0
            c = (+c)
            most_common_card = c.most_common(1)[0][0]
            c.update([most_common_card]*joker_count)

        if len(c.most_common()) == 1:
            self._type = HandType.FIVE_OF_A_KIND
        elif c.most_common(1)[0][1] == 4:
            self._type = HandType.FOUR_OF_A_KIND
        elif len(c.most_common()) == 2:
            self._type = HandType.FULL_HOUSE
        elif c.most_common()[0][1] == 3:
            self._type = HandType.THREE_OF_A_KIND
        elif len(c.most_common()) == 3:
            self._type = HandType.TWO_PAIR
        elif c.most_common()[0][1] == 2:
            self._type = HandType.ONE_PAIR
        else:
            self._type = HandType.HIGH_CARD

    @classmethod
    def parse(self, string_hand, jokers=False):
        hand = [Card(c, jokers) for c in string_hand.strip()]
        return Hand(hand)

    @property
    def type(self):
        return self._type

    def __eq__(self, other):
        return self._hand == other._hand
    
    def __lt__(self, other):
        if self._type.value > other._type.value:
            return True
        if self._type.value < other._type.value:
            return False
        for a, b in zip(self._hand, other._hand):
            if a > b:
                return True
            if a < b:
                return False
        return False

    def __le__(self, other):
        return self == other or self < other

    def __hash__(self):
        return hash(self._hand)

    def __repr__(self):
        return "Hand("+"".join(str(c) for c in self._hand)+f",{self._type})"


def parse(file, jokers=False):
    data = []
    for row in file:
        hand, bid = row.strip().split()
        data.append( (Hand.parse(hand, jokers), int(bid)) )
    return data

def sort_bids(bids):
    sorted_bids = list(bids)
    sorted_bids.sort(key = (lambda x : x[0]))
    return sorted_bids

def winnings(bids):
    total = 0
    for rank, bid in zip(range(1,len(bids)+1), sort_bids(bids)):
        total += rank * bid[1]
    return total

def main(second_flag):
    with open("input_7.txt") as f:
        bids = parse(f, jokers=second_flag)
        return winnings(bids)

