from .util import winding_number

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



def main(second_flag):
    with open("input_18.txt") as f:
        dp = DigPlan(f)
    grid = dp.dig()
    dp.fill_in_dig(grid)
    return dp.count_dug(grid)
