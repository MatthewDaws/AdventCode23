from .util import winding_number, Interval
import enum, itertools

class DigPlan:
    def __init__(self, rows):
        self._instructions = []
        for row in rows:
            parts = row.split()
            direction = parts[0]
            if direction not in ["U", "D", "L", "R"]:
                raise ValueError()
            length = int(parts[1])
            if parts[2][0]!="(" or parts[2][1]!="#" or parts[2][8]!=")":
                raise ValueError()
            colour_code = parts[2][2:8]
            self._instructions.append((direction, length, colour_code))
        self._cached_fast_path = None

    @property
    def instructions(self):
        return self._instructions
    
    def instructions_without_colours(self):
        return [(d,l) for d,l,_ in self._instructions]

    def dig(self):
        rowrange, colrange = self._find_size()
        self._offsetrow = -rowrange[0]
        self._offsetcol = -colrange[0]
        maxrow = rowrange[1] - rowrange[0] + 1
        maxcol = colrange[1] - colrange[0] + 1
        grid = [[0 for _ in range(maxcol)] for _ in range(maxrow)]
        for row, col in self.path():
            grid[row+self._offsetrow][col+self._offsetcol] = 1
        return grid
    
    def path(self):
        row, col = 0,0
        yield row,col
        for direction, length, colour in self.instructions:
            if direction=="R":
                dr, dc = 0, 1
            elif direction=="L":
                dr, dc = 0, -1
            elif direction=="D":
                dr, dc = 1, 0
            else:
                dr, dc = -1, 0
            for i in range(length):
                row += dr
                col += dc
                yield row, col

    def path_fast_offset(self, offsetrow, offsetcol):
        if self._cached_fast_path is not None:
            return self._cached_fast_path
        self._cached_fast_path = []
        row, col = 0,0
        self._cached_fast_path.append((row+offsetrow, col+offsetcol))
        for direction, length, colour in self.instructions:
            if direction=="R":
                dr, dc = 0, 1
            elif direction=="L":
                dr, dc = 0, -1
            elif direction=="D":
                dr, dc = 1, 0
            else:
                dr, dc = -1, 0
            for i in range(length):
                row += dr
                col += dc
            self._cached_fast_path.append((row+offsetrow, col+offsetcol))
        return self._cached_fast_path

    def _find_size(self):
        maxrow, maxcol = 0, 0
        minrow, mincol = 0, 0
        for row, col in self.path():
            maxrow, maxcol = max(maxrow, row), max(maxcol, col)
            minrow, mincol = min(minrow, row), min(mincol, col)
        return (minrow, maxrow), (mincol, maxcol)

    def fill_in_dig(self, grid):
        maxrow, maxcol = len(grid), len(grid[0])
        for row in range(maxrow):
            for col in range(maxcol):
                if grid[row][col] == 0 and winding_number(self.path_fast_offset(self._offsetrow, self._offsetcol),row,col) != 0:
                    grid[row][col] = 1
        return grid
    
    @staticmethod
    def count_dug(grid):
        return sum(sum(x for x in row) for row in grid)
       

class EndDir(enum.Enum):
    UP = 0
    DOWN = 1


class DigPlan2:
    def __init__(self, rows):
        self._instructions = []
        for row in rows:
            parts = row.split()
            if parts[2][0]!="(" or parts[2][1]!="#" or parts[2][8]!=")":
                raise ValueError()
            colour_code = parts[2][2:8]
            length = int(colour_code[:5], 16)
            if colour_code[5] == "0":
                direction = "R"
            elif colour_code[5] == "1":
                direction = "D"
            elif colour_code[5] == "2":
                direction = "L"
            elif colour_code[5] == "3":
                direction = "U"
            else:
                raise ValueError()
            self._instructions.append((direction, length))

    @property
    def instructions(self):
        return self._instructions


def construct_row_plan(instructions):
    row_plans = dict()
    row, col = 0, 0
    for (d, l) in instructions:
        if row not in row_plans:
            row_plans[row] = list()
        if d == "U":
            row -= l
        if d == "D":
            row += l
        if d == "R":
            row_plans[row].append( Interval.from_start_length(col, l) )
            col += l
        if d == "L":
            row_plans[row].append( Interval.from_start_length(col, -l) )
            col -= l
    for key in row_plans:
        row_plans[key].sort()
    assert (row,col) == (0,0)
    up_downs = dict()
    for (d, l) in instructions:
        if row not in up_downs:
            up_downs[row] = list()
        if d == "U":
            up_downs[row].append((col, "U"))
            row -= l
            if row not in up_downs:
                up_downs[row] = list()
            up_downs[row].append((col, "D"))
        if d == "D":
            up_downs[row].append((col, "D"))
            row += l
            if row not in up_downs:
                up_downs[row] = list()
            up_downs[row].append((col, "U"))
        if d == "R":
            col += l
        if d == "L":
            col -= l
    for key in up_downs:
        up_downs[key].sort(key=lambda pair:pair[0])
    return row_plans, up_downs


def compute_all_up_downs(up_downs):
    all_downs = dict()
    rows = list(up_downs)
    rows.sort()
    current_downs = []
    for row in rows:
        downs = set(col for col, direction in up_downs[row] if direction=="D")
        downs.update(current_downs)
        for col, direction in up_downs[row]:
            if direction=="U":
                downs.remove(col)
        all_downs[row] = list(downs)
        all_downs[row].sort()
        current_downs = downs
    return all_downs

def double_counts(new_intervals, previous_intervals):
    area = 0
    for (i,j) in itertools.product(new_intervals, previous_intervals):
        k = i.intersect(j)
        if k is not None:
            area += k.end - k.start + 1
    return area

def find_intervals(downs):
    new_intervals = []
    index = 0
    width = 0
    while index < len(downs):
        width += downs[index+1] - downs[index] + 1
        new_intervals.append( Interval(downs[index], downs[index+1]) )
        index += 2
    return width, new_intervals

def compute_area(up_downs):
    rows = list(up_downs)
    rows.sort()
    area = 0
    previous_intervals = []
    row_index = 0
    while row_index < len(rows)-1:
        row = rows[row_index]
        height = rows[row_index+1] - row + 1
        width, new_intervals = find_intervals(up_downs[row])
        area += width * height
        area -= double_counts(new_intervals, previous_intervals)
        previous_intervals = new_intervals
        row_index += 1
    return area

def area_from_digplan2(dp2):
    _, cols = construct_row_plan(dp2.instructions)
    all_ud = compute_all_up_downs(cols)
    return compute_area(all_ud)

def main(second_flag):
    if not second_flag:
        with open("input_18.txt") as f:
            dp = DigPlan(f)
        grid = dp.dig()
        dp.fill_in_dig(grid)
        return dp.count_dug(grid)

    with open("input_18.txt") as f:
        dp = DigPlan2(f)
    return area_from_digplan2(dp)
