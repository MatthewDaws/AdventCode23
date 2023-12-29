import enum

class Grid:
    def __init__(self, rows):
        self._grid = []
        for row in rows:
            r = row.strip()
            if len(r) == 0:
                break
            self._grid.append(r)
        self._numrows = len(self._grid)
        self._numcols = len(self._grid[0])
        
    @property
    def numrows(self):
        return self._numrows
    
    @property
    def numcols(self):
        return self._numcols
    
    def cost(self, row, col):
        return int(self._grid[row][col])
    
    def in_grid(self, row, col):
        return row>=0 and row<self._numrows and col>=0 and col<self.numcols
    
    def construct_graph(self):
        """Construct a (directed) graph from the problem.  From the start square you can move east
        or south, up to 3 squares.  We make copies of each square to record which direct we entered it.
        Then one has to leave it at right angles."""
        graph = Graph()
        for row in range(self.numrows):
            for col in range(self.numcols):
                for d in ["n", "s", "e", "w"]:
                    vertex = (row, col, d)
                    for tr, tc, td in self.possible_destinations(row, col, d):
                        graph.add_edge(vertex, (tr,tc,td), self.moving_cost((row,col), (tr,tc)) )
        return graph

    def construct_smaller_graph(self, minmove=1, maxmove=3):
        """Only need to keep track of ns (0) or ew (1)"""
        graph = Graph()
        for row in range(self.numrows):
            for col in range(self.numcols):
                for d in [0,1]:
                    vertex = (row, col, d)
                    for label in self.possible_destinations_smaller(row, col, d, minmove, maxmove):
                        graph.add_edge(vertex, label, self.moving_cost((row,col), label[:2]) )
        return graph

    def possible_destinations_smaller(self, row, col, nsew, minmove, maxmove):
        if nsew == 0:
            choices = [1]
        elif nsew == 1:
            choices = [0]
        else:
            choices = [0, 1]

        def add(row, col, rd, cd, d):
            for mult in range(minmove, maxmove+1):
                r, c = row + rd*mult, col + cd*mult
                if r>=0 and r<self.numrows and c>=0 and c<self.numcols:
                    yield r,c,d

        if 0 in choices:
            yield from add(row, col, -1, 0, 0)
            yield from add(row, col, 1, 0, 0)
        if 1 in choices:
            yield from add(row, col, 0, -1, 1)
            yield from add(row, col, 0, 1, 1)

    def add_start(self, graph, startrow, startcol):
        """Adds special vertices to the graph from the starting point: movement in any direction
        initially allowed.  Returns the vertex added."""
        vertex = (startrow, startcol, None)
        # for tr, tc, td in self.possible_destinations(startrow, startcol, None):
        #     graph.add_edge(vertex, (tr,tc,td), self.moving_cost((startrow,startcol), (tr,tc)) )
        sources = [label for label in graph.vertices() if label[:2]==(startrow, startcol)]
        targets = set(label for v in sources for label, _ in list(graph.neighbours(v)))
        for label in targets:
            graph.add_edge(vertex, label, self.moving_cost((startrow,startcol), label[:2]) )
        return vertex

    @staticmethod
    def inc_range_skip_start(a, b):
        """yield all the numbers between a and b, with b inclusive, not a, in any order.
        E.g. (5,7) -> [6,7] and (4,1) -> (3,2,1)"""
        a, b = int(a), int(b)
        if a==b:
            return
        if a < b:
            delta = 1
        else:
            delta = -1
        n = a + delta
        while n!= b:
            yield n
            n += delta
        yield n

    def moving_cost(self, source, dest):
        if source[0] == dest[0]:
            return sum(self.cost(source[0], col) for col in self.inc_range_skip_start(source[1], dest[1]))
        if source[1] == dest[1]:
            start, end = source[0]+1, dest[0]
            if end < start:
                start, end = end, start
            return sum(self.cost(row, source[1]) for row in self.inc_range_skip_start(source[0], dest[0]))
        raise ValueError()

    def possible_destinations(self, row, col, entering_direction):
        if entering_direction == "s" or entering_direction == "n":
            choices = ["e", "w"]
        elif entering_direction == "e" or entering_direction == "w":
            choices = ["n", "s"]
        else:
            choices = ["n", "s", "e", "w"]
        dir_dict = { "n":(-1,0), "s":(1,0), "e":(0,1), "w":(0,-1) }
        for d in choices:
            rd, cd = dir_dict[d]
            for mult in [1,2,3]:
                r, c = row + rd*mult, col + cd*mult
                if r>=0 and r<self.numrows and c>=0 and c<self.numcols:
                    yield r,c,d


class Graph:
    def __init__(self):
        self._vertices = dict()

    def add_edge(self, source, target, cost):
        if source not in self._vertices:
            self._vertices[source] = dict()
        if target in self._vertices[source]:
            raise ValueError()
        self._vertices[source][target] = cost

    def neighbours(self, vertex):
        if vertex not in self._vertices:
            raise KeyError()
        nhood = self._vertices[vertex]
        return nhood.items()
    
    def edge_cost(self, source, target):
        return self._vertices[source][target]

    def vertices(self):
        return self._vertices.keys()


def shortest_paths(graph, start_vertex):
    distances = dict() # {v:None for v in graph.vertices()}
    distances[start_vertex] = 0
    visited = set()
    queue = {start_vertex:0}
    while len(queue) > 0:
        current_vertex, current_dist = _pop_queue(queue)
        visited.add(current_vertex)
        for vertex, cost in graph.neighbours(current_vertex):
            if vertex not in distances or distances[vertex] > current_dist + cost:
                distances[vertex] = current_dist + cost
                if vertex not in visited:
                    queue[vertex] = current_dist + cost
    return distances

def _pop_queue(queue):
    min_vertex = None
    for vertex, value in queue.items():
        if min_vertex is None or value < min_value:
            min_value = value
            min_vertex = vertex
    value = queue.pop(min_vertex)
    return min_vertex, value

def find_min_path_top_bottom(grid):
    graph = grid.construct_graph()
    v = grid.add_start(graph, 0, 0)
    distances = shortest_paths(graph, v)
    return min(cost for key, cost in distances.items() if key[:2] == (grid.numrows-1, grid.numcols-1))

def find_min_path_top_bottom_smaller(grid, minmove=1, maxmove=3):
    graph = grid.construct_smaller_graph(minmove, maxmove)
    v = grid.add_start(graph, 0, 0)
    distances = shortest_paths(graph, v)
    return min(cost for key, cost in distances.items() if key[:2] == (grid.numrows-1, grid.numcols-1))

class ShortestPath:
    def __init__(self, grid, start=(0,0)):
        self._grid = grid
        self._shortests = [[[] for c in range(grid.numcols)] for r in range(grid.numrows)]
        self._shortests[0][0] = [(0,"")]
        self._queue = [(start, 0, "")]

    def solve(self):
        while len(self._queue) > 0:
            self.take_step()

    def take_step(self):
        pos, length, state = self._queue.pop()
        row, col = pos
        if row > 0 and state != "nnn" and (len(state)==0 or state[0]!="s"):
            self._set(row-1, col, self._append_to_state(state, "n"), length)
        if row < self._grid.numrows-1 and state != "sss" and (len(state)==0 or state[0]!="n"):
            self._set(row+1, col, self._append_to_state(state, "s"), length)
        if col > 0 and state != "www" and (len(state)==0 or state[0]!="e"):
            self._set(row, col-1, self._append_to_state(state, "w"), length)
        if col < self._grid.numcols-1 and state != "eee" and (len(state)==0 or state[0]!="w"):
            self._set(row, col+1, self._append_to_state(state, "e"), length)

    def _set(self, row, col, state, prev_length):
        old = self._shortests[row][col]
        length = prev_length + self._grid.cost(row, col)
        found = False
        for i in range(len(old)):
            old_length, old_state = old[i]
            if old_state == state:
                if length < old_length:
                    old[i] = (length, state)
                    found = True
                else:
                    return
                break
        if not found:
            old.append((length, state))
        self._queue.append(((row, col), length, state))

    @staticmethod
    def _append_to_state(state, newdir):
        if len(state) == 0:
            return newdir
        if state[-1] == newdir:
            if len(state) == 3:
                raise AssertionError()
            return state+newdir
        return newdir

    def shortest_path_to(self, row, col):
        choices = self._shortests[row][col]
        return min( l for l,_ in choices )



def main(second_flag):
    with open("input_17.txt") as f:
        grid = Grid(f)
    #solver = ShortestPath(grid)
    #solver.solve()
    #return solver.shortest_path_to(grid.numrows-1, grid.numcols-1)
    if not second_flag:
        return find_min_path_top_bottom_smaller(grid)
    return find_min_path_top_bottom_smaller(grid, 4, 10)
