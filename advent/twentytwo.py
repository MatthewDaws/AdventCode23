class Bricks:
    def __init__(self, rows):
        # Seems to be the case that bricks are always 1x1xn in size, with some orientation
        # But we don't use this
        def _xyz(parts):
            return [int(x) for x in parts.split(",")]
        self._bricks = []
        for row in rows:
            start, end = [_xyz(p) for p in row.strip().split("~")]
            for index in range(3):
                assert start[index] <= end[index]
            self._bricks.append((start, end))
        self._build()

    def _build(self):
        self._skipped = -1
        if len(self._bricks) == 0:
            return
        def minmax(index):
            d = [x[index] for x,_ in self._bricks]
            d.extend(x[index] for _,x in self._bricks)
            return min(d), max(d)
        xmin, xmax = minmax(0)
        ymin, ymax = minmax(1)
        zmin, zmax = minmax(2)
        self._xmax, self._ymax = xmax, ymax
        assert zmin >= 1
        assert xmin >= 0
        assert ymin >= 0
        self._zrows = [ [[-1 for _ in range(ymax+1)] for _ in range(xmax+1)] for _ in range(zmax+1)]
        for index, (start, end) in enumerate(self._bricks):
            for z in range(start[2], end[2]+1):
                for x in range(start[0], end[0]+1):
                    for y in range(start[1], end[1]+1):
                        self._zrows[z][x][y] = index

    @property
    def xrange(self):
        return self._xmax
    
    @property
    def yrange(self):
        return self._ymax

    def set_skipped_index(self, index):
        self._skipped = index

    @property
    def number_bricks(self):
        return len(self._bricks)

    def occupied(self, x,y,z):
        return self._zrows[z][x][y] != -1

    def _xys(self, index):
        start, end = self._bricks[index]
        for x in range(start[0], end[0]+1):
            for y in range(start[1], end[1]+1):
                yield x,y

    def can_drop(self, index):
        start, end = self._bricks[index]
        z = start[2] - 1
        if z==0:
            return False
        return not any(self.occupied(x,y,z) for (x,y) in self._xys(index))
    
    def drop(self, index):
        start, end = self._bricks[index]
        for (x,y) in self._xys(index):
            self._zrows[start[2]-1][x][y] = index
            self._zrows[end[2]][x][y] = -1
        start = [start[0], start[1], start[2]-1]
        end = [end[0], end[1], end[2]-1]
        self._bricks[index] = (start, end)

    def drop_all(self):
        bricks_dropped = set()
        while True:
            dropped = False
            for index in range(len(self._bricks)):
                if index == self._skipped:
                    continue
                if self.can_drop(index):
                    dropped = True
                    self.drop(index)
                    bricks_dropped.add(index)
            if not dropped:
                return bricks_dropped
            
    def supporting(self, index):
        start, end = self._bricks[index]
        below_row = self._zrows[start[2]-1]
        below = set(below_row[x][y] for x in range(start[0], end[0]+1) for y in range(start[1], end[1]+1))
        below.discard(-1)
        return below

    def not_removable_blocks(self):
        supporting = [self.supporting(index) for index in range(self.number_bricks)]
        return { list(sup)[0] for sup in supporting if len(sup)==1 }

    def removable(self):
        """List of removable blocks.  `index` is removable if for every block supported by index,
        there is another block also supporting"""
        solos = self.not_removable_blocks()
        return [index for index in range(self.number_bricks) if index not in solos]
    
    def spawn_with_removal(self, index_to_remove):
        spawn = Bricks([])
        spawn._bricks = list(self._bricks)
        spawn.set_skipped_index(index_to_remove)
        spawn._zrows = []
        for zrow in self._zrows:
            new_xrow = []
            for xrow in zrow:
                new_yrow = []
                for entry in xrow:
                    if entry == index_to_remove:
                        new_yrow.append(-1)
                    else:
                        new_yrow.append(entry)
                new_xrow.append(new_yrow)
            spawn._zrows.append(new_xrow)
        return spawn
    
    def count_all_drops(self):
        count = 0
        for index in self.not_removable_blocks():
            spawn = self.spawn_with_removal(index)
            count += len(spawn.drop_all())
        return count


def main(second_flag):
    with open("input_22.txt") as f:
        bricks = Bricks(f)
    bricks.drop_all()
    if not second_flag:
        return len(bricks.removable())
    return bricks.count_all_drops()
