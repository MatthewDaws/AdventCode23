class Grid:
    def __init__(self, rows):
        self._grid = []
        for row in rows:
            r = row.strip()
            if len(r) == 0:
                break
            self._grid.append(r)
        if len(self._grid) == 0:
            raise StopIteration()

    @property
    def grid(self):
        return self._grid
    
    @property
    def rows(self):
        return len(self._grid)
    
    @property
    def cols(self):
        return len(self._grid[0])
    
    def get_column(self, col):
        return "".join(x[col] for x in self._grid)

    def is_symmetry_vertical(self, diffs=0):
        for i in range(1, (self.rows//2)+1):
            if self.compute_diffs(i, lambda row : self.grid[row]) == diffs:
                return i
            if self.compute_diffs(i, lambda row : self.grid[self.rows-1-row]) == diffs:
                return self.rows-i

    def is_symmetry_horizontal(self, diffs=0):
        for i in range(1, (self.cols//2)+1):
            if self.compute_diffs(i, lambda row : self.get_column(row)) == diffs:
                return i
            if self.compute_diffs(i, lambda row : self.get_column(self.cols-1-row)) == diffs:
                return self.cols-i

    @staticmethod
    def compute_diffs(rows_to_compare, get_func):
        count = 0
        for j in range(rows_to_compare):
            a = get_func(j)
            b = get_func(rows_to_compare*2 - j - 1)
            count += sum(1 for x,y in zip(a,b) if x!=y)
        return count


def score_all(file, diffs=0):
    score = 0
    while True:
        try:
            g = Grid(file)
        except StopIteration:
            break
        h = g.is_symmetry_horizontal(diffs)
        if h is not None:
            score += h
            continue
        score += 100 * g.is_symmetry_vertical(diffs)
    return score

def main(second_flag):
    with open("input_13.txt") as f:
        if not second_flag:
            return score_all(f)
        return score_all(f, diffs=1)
    