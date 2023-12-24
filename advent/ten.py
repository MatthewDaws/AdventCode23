import enum

class Tile(enum.Enum):
    GROUND = "."
    LEFTRIGHT = "-"
    UPDOWN = "|"
    SOUTHEAST = "F"
    SOUTHWEST = "7"
    NORTHEAST = "L"
    NORTHWEST = "J"
    START = "S"

class Ground():
    def __init__(self, rows):
        self._data = []
        self._start = None
        for row in rows:
            parsed_row = []
            for entity in row:
                for t in Tile:
                    if t.value == entity:
                        if t == Tile.START:
                            if self._start is not None:
                                raise ValueError("Two starts!")
                            self._start = (len(self._data), len(parsed_row))
                        parsed_row.append(t)
                        break
            self._data.append(parsed_row)

    def at(self, row, col):
        return self._data[row][col]

    @property
    def start(self):
        return self._start

    @property
    def rows(self):
        return len(self._data)

    @property
    def columns(self):
        return len(self._data[0])

    def accepting_pipe(self, row, col, from_row, from_col):
        if row<0 or col<0 or row>=self.rows or col>=self.columns:
            return False
        tile = self.at(row, col)
        if col == from_col:
            if from_row == row-1:
                return tile == Tile.UPDOWN or tile == Tile.NORTHEAST or tile == Tile.NORTHWEST
            elif from_row == row+1:
                return tile == Tile.UPDOWN or tile == Tile.SOUTHEAST or tile == Tile.SOUTHWEST
            else:
                raise ValueError()
        elif row == from_row:
            if from_col == col-1:
                return tile == Tile.LEFTRIGHT or tile == Tile.NORTHWEST or tile == Tile.SOUTHWEST
            elif from_col == col+1:
                return tile == Tile.LEFTRIGHT or tile == Tile.NORTHEAST or tile == Tile.SOUTHEAST
            else:
                raise ValueError()
        else:
            raise ValueError()

    def starting_candidates(self):
        choices = []
        row, col = self.start
        if self.accepting_pipe(row-1,col, row,col) and self.accepting_pipe(row+1,col, row,col):
            choices.append(Tile.UPDOWN)
        if self.accepting_pipe(row,col-1, row,col) and self.accepting_pipe(row,col+1, row,col):
            choices.append(Tile.LEFTRIGHT)
        if self.accepting_pipe(row-1,col, row,col) and self.accepting_pipe(row,col+1, row,col):
            choices.append(Tile.NORTHEAST)
        if self.accepting_pipe(row-1,col, row,col) and self.accepting_pipe(row,col-1, row,col):
            choices.append(Tile.NORTHWEST)
        if self.accepting_pipe(row+1,col, row,col) and self.accepting_pipe(row,col+1, row,col):
            choices.append(Tile.SOUTHEAST)
        if self.accepting_pipe(row+1,col, row,col) and self.accepting_pipe(row,col-1, row,col):
            choices.append(Tile.SOUTHWEST)
        return choices

    @staticmethod
    def deltas(tiletype):
        if tiletype == Tile.UPDOWN:
            return (-1,0), (1,0)
        if tiletype == Tile.LEFTRIGHT:
            return (0,-1), (0,1)
        if tiletype == Tile.NORTHEAST:
            return (-1,0), (0,1)
        if tiletype == Tile.NORTHWEST:
            return (-1,0), (0,-1)
        if tiletype == Tile.SOUTHEAST:
            return (1,0), (0,1)
        if tiletype == Tile.SOUTHWEST:
            return (1,0), (0,-1)
        raise ValueError()

    def walk(self, row,col, fromrow,fromcol):
        ds = self.deltas(self.at(row,col))
        targets = [ (row+d[0], col+d[1]) for d in ds ]
        if targets[0] == (fromrow,fromcol):
            return targets[1]
        return targets[0]

    def _try_closed_loop(self, candidate_tile):
        steps = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        path1, path2 = [self.start], []
        row, col = self.start
        steps[row][col] = 0
        positions = [(row+rd,col+cd, row,col) for rd,cd in Ground.deltas(candidate_tile)]
        step = 1
        while True:
            r1,c1,*_ = positions[0]
            r2,c2,*_ = positions[1]
            steps[r1][c1] = step
            steps[r2][c2] = step
            path1.append((r1,c1))
            if (r1,c1)==(r2,c2):
                break
            path2.append((r2,c2))
            positions = [(*self.walk(*x),x[0],x[1]) for x in positions]
            step += 1
        path2.reverse()
        path1.extend(path2)
        return step, steps, path1

    def test_closed_loop(self, candidate_tile):
        step, *_ = self._try_closed_loop(candidate_tile)
        return step
    
    def find_path(self):
        for tile in self.starting_candidates():
            step, steps, path = self._try_closed_loop(tile)
            return path


def winding_number(path, row, col):
    def quadrant(pos, path_pos):
        deltarow, deltacol = path_pos[0] - pos[0], path_pos[1] - pos[1]
        if deltacol > 0 and deltarow <=0:
            return 0
        if deltacol <= 0 and deltarow < 0:
            return 1
        if deltacol < 0 and deltarow >= 0:
            return 2
        if deltacol >=0 and deltarow > 0:
            return 3
        raise ValueError()
    def update_crosses(last_quad, new_quad, crosses):
        if last_quad == 0 and new_quad == 3:
            return crosses + 1
        if last_quad == 3 and new_quad == 0:
            return crosses - 1
        return crosses
    start_quad = quadrant((row,col), path[0])
    last_quad = start_quad
    crosses = 0
    for i in range(1, len(path)):
        new_quad = quadrant((row,col), path[i])
        crosses = update_crosses(last_quad, new_quad, crosses)
        last_quad = new_quad
    crosses = update_crosses(last_quad, start_quad, crosses)
    return crosses

def count_containing_tiles(path):
    minrow = min(row for row,col in path)
    maxrow = max(row for row,col in path)
    mincol = min(col for row,col in path)
    maxcol = max(col for row,col in path)
    count = 0
    for row in range(minrow, maxrow+1):
        for col in range(mincol, maxcol+1):
            if (row,col) in path:
                continue
            if winding_number(path, row, col) != 0:
                count += 1
    return count


def parse(file):
    return Ground(file)

def main(second_flag):
    with open("input_10.txt") as file:
        g = parse(file)
    
    if not second_flag:
        for possible_tile in g.starting_candidates():
            return g.test_closed_loop(possible_tile)

    return count_containing_tiles(g.find_path())
