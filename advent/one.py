def first_num(string):
    for x in string:
        if x.isdigit():
            return int(x)

def last_num(string):
    return first_num(string[::-1])

def sum_first_last(string):
    return first_num(string)*10 + last_num(string)

def initial_string_match(string, prefix):
    return len(string) >= len(prefix) and string[:len(prefix)] == prefix

numbers_as_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def first_num_2nd(string):
    for i in range(len(string)):
        if string[i].isdigit():
            return int(string[i])
        for n in range(9):
            if initial_string_match(string[i:], numbers_as_words[n]):
                return n+1
    raise Exception()

def last_num_2nd(string):
    for i in range(len(string)-1, -1, -1):
        if string[i].isdigit():
            return int(string[i])
        for n in range(9):
            if initial_string_match(string[i:], numbers_as_words[n]):
                return n+1
    raise Exception()

def sum_first_last_2nd(string):
    return first_num_2nd(string)*10 + last_num_2nd(string)


def main(second):
    if not second:
        with open("input_1.txt") as f:
            return sum(sum_first_last(line) for line in f)
    else:
        with open("input_1.txt") as f:
            return sum(sum_first_last_2nd(line) for line in f)
