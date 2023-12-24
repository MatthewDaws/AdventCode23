class Stars:
    def __init__(self, rows):
        self._stars = set()
        self._numrows = 0
        self._emptyrows = []
        self._emptycols = None
        for r, row in enumerate(rows):
            row = row.strip()
            if len(row) == 0:
                break
            self._numrows += 1
            self._numcols = len(row)
            seenstar = False
            if self._emptycols is None:
                self._emptycols = set(x for x in range(self._numcols))
            for c, entity in enumerate(row):
                if entity == "#":
                    self._stars.add((r,c))
                    seenstar = True
                    self._emptycols.discard(c)
                elif entity == ".":
                    pass
                else:
                    raise ValueError("Unexpected character")
            if not seenstar:
                self._emptyrows.append(r)

        self._emptycols = list(self._emptycols)
        self._emptycols.sort()
                
    @property
    def stars(self):
        return set(self._stars)
    
    @property
    def rows(self):
        return self._numrows
    
    @property
    def cols(self):
        return self._numcols

    @property
    def empty_rows(self):
        return self._emptyrows
    
    @property
    def empty_cols(self):
        return self._emptycols
    
    def distance(self, start, end, expansion=2):
        row1 = min(start[0], end[0])
        row2 = max(start[0], end[0])
        col1 = min(start[1], end[1])
        col2 = max(start[1], end[1])
        distance = row2-row1 + col2-col1
        rows = set(self.empty_rows)
        for r in range(row1, row2+1):
            if r in rows:
                distance += expansion-1
        cols = set(self.empty_cols)
        for c in range(col1, col2+1):
            if c in cols:
                distance += expansion-1
        return distance

    def pairs_stars(self):
        stars = list(self._stars)
        for i in range(len(stars)-1):
            for j in range(i+1, len(stars)):
                yield stars[i], stars[j]

    def all_distances(self, expansion=2):
        return sum(self.distance(x,y,expansion) for x,y in self.pairs_stars())
    
def main(second_flag):
    with open("input_11.txt") as f:
        stars = Stars(f)
    if not second_flag:
        return stars.all_distances()
    return stars.all_distances(1000000)
