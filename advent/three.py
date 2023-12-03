def parse_line(line, only_gears=False):
    """Returns tuple (nums, symbols):
    nums is a list of (number, [column entries used])
    symbols is a list of [column locations]"""
    nums = []
    symbols = []
    current_number, number_locations = 0, []
    for i, d in enumerate(line.strip()):
        if d.isdigit():
            current_number = 10 * current_number + int(d)
            number_locations.append(i)
        else:
            if current_number != 0:
                nums.append((current_number, number_locations))
                current_number, number_locations = 0, []
            if d != "." and not only_gears:
                symbols.append(i)
            if only_gears and d=="*":
                symbols.append(i)
    if current_number != 0:
        nums.append((current_number, number_locations))
        current_number, number_locations = 0, []
    return nums, symbols

def input_to_locations(lines, only_gears=False):
    """Parse all the input -> (number_locs, symbols) where:
    number_locs is a list [ (number, [(row,col)]) ]
    symbols is a list of (row,col) symbol locations"""
    number_locs, symbols = [], []
    for row, line in enumerate(lines):
        nums, syms = parse_line(line, only_gears)
        for col in syms:
            symbols.append((row,col))
        for num, locs in nums:
            number_locs.append( (num, [(row,c) for c in locs]) )
    return number_locs, symbols

def diagonal_locs(row, col):
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if not (i==0 and j==0):
                yield (row+i, col+j)

def _find_used_numbers(number_locs, symbols):
    loc_to_number = dict()
    for i, (num, locs) in enumerate(number_locs):
        for l in locs:
            loc_to_number[l] = i
    used_numbers = set()
    for loc in symbols:
        for l in diagonal_locs(*loc):
            if l in loc_to_number:
                used_numbers.add(loc_to_number[l])
    return used_numbers

def sum_next_to_symbol(number_locs, symbols, count_all=True):
    if count_all:
        return sum(number_locs[i][0] for i in _find_used_numbers(number_locs, symbols))
    unique_used_numbers = set( number_locs[i][0] for i in _find_used_numbers(number_locs, symbols) )
    return sum(unique_used_numbers)

def sum_gear_ratios(number_locs, symbols):
    loc_to_number = dict()
    for i, (num, locs) in enumerate(number_locs):
        for l in locs:
            loc_to_number[l] = i
    total = 0
    for loc in symbols:
        neighbours = set(loc_to_number[l] for l in diagonal_locs(*loc) if l in loc_to_number)
        if len(neighbours) == 2:
            numbers = [number_locs[nb][0] for nb in neighbours]
            total += numbers[0] * numbers[1]
    return total

def write_debug(number_locs, symbols, zero_out=False, inverse=False):
    maxrow, maxcol = 0, 0
    for row, col in symbols:
        maxrow=max(row, maxrow)
        maxcol=max(col, maxcol)
    for num, locs in number_locs:
        for row, col in locs:
            maxrow=max(row, maxrow)
            maxcol=max(col, maxcol)

    rows = [ ["." for _ in range(maxcol+1)] for _ in range(maxrow+1) ]
    for row, col in symbols:
        rows[row][col] = "#"
    if not inverse:
        for number in _find_used_numbers(number_locs, symbols):
            num, locs = number_locs[number]
            for c, (row, col) in zip(str(num), locs):
                if zero_out:
                    rows[row][col] = "0"
                else:
                    rows[row][col] = c
    else:
        used = _find_used_numbers(number_locs, symbols)
        for i in range(len(number_locs)):
            if i not in used:
                num, locs = number_locs[i]
                for c, (row, col) in zip(str(num), locs):
                    if zero_out:
                        rows[row][col] = "0"
                    else:
                        rows[row][col] = c

    unique_numbers = set()
    for n in _find_used_numbers(number_locs, symbols):
        num, locs = number_locs[n]
        unique_numbers.add(num)
    return "\n".join("".join(row) for row in rows)

def main(second_flag):
    if not second_flag:
        with open("input_3.txt") as f:
            data = input_to_locations(f)
        with open("debug.txt", "w") as f:
            print(write_debug(*data, inverse=True), file=f)
        return sum_next_to_symbol(*data)

    with open("input_3.txt") as f:
        data = input_to_locations(f)
        return sum_gear_ratios(*data)
