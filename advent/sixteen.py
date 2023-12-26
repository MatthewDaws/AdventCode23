class Grid:
    def __init__(self, rows):
        self._grid = []
        for row in rows:
            r = row.strip()
            if len(r) == 0: break
            self._grid.append(r)
        self._numrows = len(self._grid)
        self._numcols = len(self._grid[0])

    @property
    def numrows(self):
        return self._numrows
    
    @property
    def numcols(self):
        return self._numcols

    def valid_pos(self, row, col):
        return not( row < 0 or row >= self._numrows or col < 0 or col >= self._numcols )

    def get(self, row, col):
        if not self.valid_pos(row, col):
            return None
        return self._grid[row][col]
    
    def move(self, pos, delta):
        row, col = pos[0] + delta[0], pos[1] + delta[1]
        cell = self.get(row, col)
        if cell is None:
            return []
        if cell == ".":
            return [((row,col), delta)]
        if cell == "/":
            new_delta = (-delta[1], -delta[0])
            return[((row,col), new_delta)]
        if cell == "\\":
            new_delta = (delta[1], delta[0])
            return[((row,col), new_delta)]
        if cell == "|":
            if delta[1] == 0:
                return [((row,col), delta)]
            return [((row,col), (1,0)), ((row,col), (-1,0))]
        if cell == "-":
            if delta[0] == 0:
                return [((row,col), delta)]
            return [((row,col), (0,1)), ((row,col), (0,-1))]
        raise ValueError()


class RayTrace:
    def __init__(self, grid):
        self._grid = grid
        self._seen = [[set() for _ in range(grid.numcols)] for _ in range(grid.numrows)]

    def _configure(self, start):
        if start[0] == -1:
            return start, (1,0)
        if start[0] == self._grid.numrows:
            return start, (-1,0)
        if start[1] == -1:
            return start, (0,1)
        if start[1] == self._grid.numcols:
            return start, (0,-1)
        raise ValueError()

    def trace(self, start=(0,-1)):
        self._queue = [self._configure(start)]
        while len(self._queue) > 0:
            pos, delta = self._queue.pop()
            if self._grid.valid_pos(*pos):
                if delta in self._seen[pos[0]][pos[1]]:
                    continue
                self._seen[pos[0]][pos[1]].add(delta)
            self._queue.extend( self._grid.move(pos, delta) )
        return self

    def count(self):
        return sum(1 for row in self._seen for passes in row if len(passes)>0)


def maximise(grid):
    best_count = -1
    best_location = None
    def test(start):
        nonlocal best_count, best_location
        count = RayTrace(grid).trace(start).count()
        if count > best_count:
            best_count, best_location = count, start
    for col in range(grid.numcols):
        test((-1,col))
    for row in range(grid.numrows):
        test((row,-1))
    for col in range(grid.numcols):
        test((grid.numrows,col))
    for row in range(grid.numrows):
        test((row,grid.numcols))
    return best_location, best_count

def main(second_flag):
    with open("input_16.txt") as f:
        if not second_flag:
            grid = Grid(f)
            rt = RayTrace(grid)
            rt.trace()
            return rt.count()
        best_location, best_count = maximise(Grid(f))
        return best_count
