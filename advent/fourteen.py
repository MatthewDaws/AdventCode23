class Rocks:
    def __init__(self, rows):
        self._rocks = []
        for row in rows:
            r = row.strip()
            if len(r)==0:
                break
            self._rocks.append(r)

    @property
    def numrows(self):
        return len(self._rocks)
    
    @property
    def numcols(self):
        return len(self._rocks[0])
    
    @property
    def grid(self):
        return self._rocks

    def get_col(self, colnum):
        return "".join(x[colnum] for x in self._rocks)

    def as_columns(self):
        return [self.get_col(c) for c in range(self.numcols)]

    @staticmethod
    def tilt_col(col):
        tilted = []
        i, count, rocks = 0, 0, 0
        while i < len(col):
            if col[i] == "#":
                tilted.extend(["O"]*rocks)
                tilted.extend(["."]*(count-rocks))
                tilted.append("#")
                count, rocks = 0, 0
            else:
                count += 1
                if col[i] == "O":
                    rocks += 1
            i += 1
        if count > 0:
            tilted.extend(["O"]*rocks)
            tilted.extend(["."]*(count-rocks))
        return "".join(tilted)

    @staticmethod
    def tilt_north(columns):
        """Returns a list of columns, as that seems easier"""
        return [Rocks.tilt_col(columns[c]) for c in range(len(columns))]

    @staticmethod
    def reverse_col(column):
        return column[::-1]

    @staticmethod
    def tilt_south(columns):
        """Returns a list of columns, as that seems easier"""
        return [Rocks.reverse_col(Rocks.tilt_col(Rocks.reverse_col(columns[c]))) for c in range(len(columns))]

    @staticmethod
    def transpose(grid):
        return ["".join(x[n] for x in grid) for n in range(len(grid[0]))]

    @staticmethod
    def cycle(grid):
        grid = Rocks.transpose(grid)
        grid = Rocks.tilt_north(grid)
        grid = Rocks.transpose(grid)
        grid = Rocks.tilt_north(grid)
        grid = Rocks.transpose(grid)
        grid = Rocks.tilt_south(grid)
        grid = Rocks.transpose(grid)
        grid = Rocks.tilt_south(grid)
        return grid

    @staticmethod
    def score_column(col):
        numcols = len(col)
        return sum(numcols-i for i in range(numcols) if col[i]=="O")
            

def score(file):
    return sum(Rocks.score_column(col) for col in Rocks.tilt_north(Rocks(file).as_columns()))

def find_loop(start_grid):
    """Returns start of cycle (counting from 1) and all the grids in the cycle"""
    history = []
    grid = start_grid
    for count in range(1000000):
        grid_new = Rocks.cycle(grid)
        try:
            match = history.index(grid_new)
            return match+1, history[match:]
        except ValueError:
            pass
        history.append(grid_new)
        grid = grid_new
    raise Exception()

def score_after_long_time(start_grid, loops=1000000000):
    start, grids = find_loop(start_grid)
    period = len(grids)
    offset = (1000000000 - start) % period
    return sum(Rocks.score_column(col) for col in Rocks.transpose(grids[offset]))

def main(second_flag):
    with open("input_14.txt") as f:
        if not second_flag:
            return score(f)
        return score_after_long_time(Rocks(f).grid)
