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
    

def count_places_walkable(garden, steps):
    places = None
    for _ in range(steps):
        places = garden.walk(places)
    return len(places)


def main(second_flag):
    with open("input_21.txt") as f:
        g = Garden(f)
    if not second_flag:
        return count_places_walkable(g, 64)
    raise NotImplementedError()