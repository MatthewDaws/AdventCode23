import enum

class Colour(enum.Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

def parse_single_trial(string):
    """Something like 3 blue, 4 red; 1 red.  Returns a dict lookup"""
    counts = { c:0 for c in Colour }
    for part in string.split(","):
        count, colour = (x.strip() for x in part.strip().split(" "))
        count = int(count)
        cname = None
        for c in Colour:
            if c.value == colour:
                cname = c
                break
        if cname is None:
            raise Exception(f"Unknown colour: {colour}")
        counts[cname] = count
    return counts

def parse_game(string):
    """Like Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"""
    if string[:5] != "Game ":
        raise SyntaxError(string)
    string = string[5:]
    i = string.find(":")
    if i == -1:
        raise SyntaxError(string)
    game_number = int(string[:i])
    return game_number, [parse_single_trial(part.strip()) for part in string[i+1:].split(";")]

def max_count(string):
    num, counts = parse_game(string)
    max_counts = { c : max(x[c] for x in counts) for c in Colour }
    return num, max_counts

def valid_game(max_counts):
    limits = {Colour.RED:12, Colour.GREEN:13, Colour.BLUE:14}
    return all(max_counts[c] <= limits[c] for c in Colour)

def main(second_flag):
    if not second_flag:
        with open("input_2.txt") as f:
            total = 0
            for line in f:
                num, counts = max_count(line)
                if valid_game(counts):
                    total += num
            return total
    
    with open("input_2.txt") as f:
        total = 0
        for line in f:
            _, counts = max_count(line)
            counts = [counts[c] for c in Colour]
            prod = 1
            for n in counts:
                prod *= n
            total += prod
        return total
