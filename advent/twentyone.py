class Garden:
    def __init__(self, rows):
        self._rows = []
        for row in rows:
            row = row.strip()
            if len(row)==0:
                break
            self._rows.append(row)
        self._find_start()
        self._numrows = len(self._rows)
        self._numcols = len(self._rows[0])

    def _find_start(self):
        for n, row in enumerate(self._rows):
            i = row.find("S")
            if i != -1:
                self._start = (n, i)
                break

    def at(self, row, col):
        return self._rows[row][col]
    
    def expand(self, times=3):
        times = int(times)
        if times % 2 == 0:
            raise ValueError("Need to expand by an odd number.")
        sr, sc = self._start
        out = []
        for r, row in enumerate(self._rows):
            if r == sr:
                row = row[:sc] + "." + row[sc+1:]
            out.append(row*times)
        for _ in range(1, times):
            for r in range(self._numrows):
                out.append(out[r])
        sr += self._numrows * ((times-1)//2)
        sc += self._numcols * ((times-1)//2)
        row = out[sr]
        row = row[:sc] + "S" + row[sc+1:]
        out[sr] = row
        return Garden(out)

    @property
    def rows(self):
        return self._numrows
    
    @property
    def cols(self):
        return self._numcols

    @property
    def start(self):
        return self._start
    
    def is_garden(self, row, col):
        if row<0 or col<0 or row>=self._numrows or col>=self._numcols:
            return False
        return self._rows[row][col] != "#"

    def walk(self, current_places=None):
        if current_places == None:
            current_places = [self.start]
        new_places = set()
        for (r,c) in current_places:
            for (dr,dc) in [(1,0), (-1,0), (0,1), (0,-1)]:
                if self.is_garden(r+dr, c+dc):
                    new_places.add((r+dr,c+dc))
        return new_places

    def to_string(self, current_places=None, new_places=None):
        out = [str(row) for row in self._rows]
        if current_places is not None:
            for (r,c) in current_places:
                out[r] = out[r][:c] + "O" + out[r][c+1:]
        if new_places is not None:
            for (r,c) in new_places:
                if (r,c) not in current_places:
                    out[r] = out[r][:c] + "X" + out[r][c+1:]
        return "\n".join(out)

    def maximum_expected_walk(self, steps):
        places = set()
        for r in range(self._start[0]-steps, self._start[0]+steps+1):
            left = steps - abs(r - self._start[0])
            for c in range(self._start[1]-left, self._start[1]+left+1, 2):
                if self.is_garden(r, c):
                    places.add((r,c))
        return places
    

def count_places_walkable(garden, steps):
    places = None
    for _ in range(steps):
        places = garden.walk(places)
    return len(places)


class Counter:
    def __init__(self, base_garden, expansion=5):
        self._g = base_garden.expand(expansion)
        self._expansion = expansion
        self._places = None
        self._size = base_garden.rows
        assert self._size == base_garden.cols
        for _ in range(65):
            self._places = self._g.walk(self._places)

    def walk_out(self, block_steps=None):
        if block_steps is None:
            block_steps = (self._expansion-1)//2
        for _ in range(131 * block_steps):
            self._places = self._g.walk(self._places)
        
    @property
    def locations_reachable(self):
        return len(self._places)

    def block_counts(self):
        counts = [[0]*self._expansion for _ in range(self._expansion)]
        for (r,c) in self._places:
            cr, cc = r // self._size, c // self._size
            counts[cr][cc] += 1
        return counts
    
    def compute(self, steps, counts=None):
        if counts is None:
            assert self._expansion == 5
            counts = self.block_counts()

        even_centre = counts[2][2]
        odd_centre = counts[2][1]
        assert odd_centre == counts[2][3] and odd_centre == counts[1][2] and odd_centre == counts[3][2]
        per_block = counts[1][0] + counts[1][1] + counts[1][3] + counts[1][4] + counts[3][0] + counts[3][1] + counts[3][3] + counts[3][4]
        assert counts[1][0] == counts[0][1] and counts[0][3] == counts[1][4] and counts[3][0] == counts[4][1] and counts[3][4] == counts[4][3]
        extra = counts[1][0] + counts[1][4] + counts[3][0] + counts[3][4]
        extra += counts[0][2] + counts[2][0] + counts[2][4] + counts[4][2]

        assert (steps - 65) % 131 == 0
        block_count = ((steps - 65) // 131) - 1
        odd_count = (block_count+1)**2
        even_count = block_count**2
        return extra + per_block * block_count + odd_centre*odd_count + even_centre*even_count


def main(second_flag):
    with open("input_21.txt") as f:
        g = Garden(f)
    if not second_flag:
        return count_places_walkable(g, 64)
    
    # How do we deal with the number of steps being vast?
    # As we can move forwards and backwards, once we know we can get to a square in time n,
    # then we can get to that square exactly in times n, n+2, n+4, ... (Think about the
    # parity of the sum of row and column)
    # So we only really need to know the minimal visit time of each square.
    #
    # From some experiments, and looking at the garden plan, one notices that there are large diamond
    # shaped gaps, and that for 64 steps (perhaps we are meant to notice this from the 1st part) the
    # area reachable is _exactly_ a diamond shape, minus the rocks (and 4 places which are completely
    # inaccessible).
    # Perhaps this pattern repeats, and so one just has to work out the "edge effects" to get the
    # exact answer.
    # 65 is better: you miss just one point (3720 instead of possible 3721).
    # 26501365 = 20 + 65 * 407713 = 202300 * 131 + 65
    # So this is _exact_ which makes it all a bit easier.

    counter = Counter(g, 5)
    counter.walk_out()
    return counter.compute(26501365)


def test_counter(g):
    counter = Counter(g, 5)
    counter.walk_out()
    counts = counter.block_counts()
    assert counter.compute(65 + 131*2, counts) == counter.locations_reachable
    print("5x5 counts:")
    print(counts)

    test_counter = Counter(g, 7)
    assert counter.compute(65, counts) == test_counter.locations_reachable
    test_counter.walk_out(1)
    assert counter.compute(65 + 131, counts) == test_counter.locations_reachable
    test_counter.walk_out(1)
    assert counter.compute(65 + 2*131, counts) == test_counter.locations_reachable
    test_counter.walk_out(1)
    assert counter.compute(65 + 3*131, counts) == test_counter.locations_reachable
