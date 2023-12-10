def number_list_to_numbers(parts):
    return [int(x) for x in parts.split(" ") if x!=""]

def parse_line(line):
    pre, post = [x.strip() for x in line.split("|")]
    pre1, pre2 = [x.strip() for x in pre.split(":")]
    assert pre1[:5] == "Card "
    card_number = int(pre1[5:].strip())
    winning_numbers = number_list_to_numbers(pre2)
    have_numbers = number_list_to_numbers(post)

    return card_number, winning_numbers, have_numbers

def line_matches(winning_numbers, have_numbers):
    winners = set(have_numbers).intersection( set(winning_numbers) )
    return len(winners)

def line_value(winning_numbers, have_numbers):
    num_winners = line_matches(winning_numbers, have_numbers)
    if num_winners==0:
        return 0
    return 1 << (num_winners-1)

def multiplying_counts(line_matches):
    card_counts = dict()
    for n, value in enumerate(line_matches):
        if n not in card_counts:
            card_counts[n] = 0
        card_counts[n] = card_counts[n] + 1
        for i in range(1, value+1):
            if n+i not in card_counts:
                card_counts[n+i] = 0
            card_counts[n+i] += card_counts[n]
    return sum(card_counts[n] for n in range(len(line_matches)))

def main(second_flag):
    if not second_flag:
        total = 0
        with open("input_4.txt") as f:
            for line in f:
                n, winners, have = parse_line(line)
                total += line_value(winners, have)
        return total

    with open("input_4.txt") as f:
        matches = []
        for line in f:
            n, winners, have = parse_line(line)
            matches.append( line_matches(winners, have) )
        return multiplying_counts( matches )    