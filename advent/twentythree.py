# We notice that there are rather few "choices" of direction, so we pre-process into a much smaller graph
from . import util

class Forest:
    def __init__(self, rows):
        self._grid = []
        for row in rows:
            row = row.strip()
            if len(row) == 0:
                break
            self._grid.append(row)
        
        self._start = self._grid[0].find(".")
        self._end = self._grid[-1].find(".")
        self._build_graph()

    @property
    def start_column(self):
        return self._start
    
    @property
    def finish_column(self):
        return self._end
    
    @property
    def width(self):
        return len(self._grid[0])
    
    @property
    def height(self):
        return len(self._grid)

    def at(self, row, col):
        if row<0 or row>=self.height or col<0 or col>=self.width:
            return None
        return self._grid[row][col]

    def possible_directions(self, row, col):
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            e = self.at(row+dr, col+dc)
            if e==".":
                yield dr,dc
            if e=="<" and dc==-1:
                yield dr,dc
            if e==">" and dc==1:
                yield dr,dc
            if e=="^" and dr==-1:
                yield dr,dc
            if e=="v" and dr==1:
                yield dr,dc

    def _build_graph(self):
        vertices = set()
        edges = []
        vertices.add((0,self.start_column))
        routes = [(0,self.start_column,1,0)]
        while len(routes) > 0:
            startrow,startcol, dr,dc = routes.pop()
            prevrow, prevcol = startrow, startcol
            length = 0
            while True:
                length += 1
                row, col = prevrow+dr, prevcol+dc
                choices = {(ddr,ddc) for ddr,ddc in self.possible_directions(row,col) if ddr!=-dr or ddc!=-dc}
                if len(choices) == 0:
                    assert row == self.height - 1
                    assert col == self.finish_column
                elif len(choices) > 1:
                    for ddr,ddc in choices:
                        routes.append( (row,col, ddr,ddc) )
                if len(choices) != 1:
                    vertices.add((row,col))
                    edges.append((startrow, startcol, row, col, length))
                    break
                dr, dc = choices.pop()
                prevrow, prevcol = row, col
        
        self._vertices = [(0,self.start_column)]
        for r,c in vertices:
            if r==0 or r==self.height-1:
                continue
            self._vertices.append((r,c))
        self._vertices.append((self.height-1, self.finish_column))
        lookup = {v:i for i,v in enumerate(self._vertices)}
        self._neighbourhoods = dict()
        for sr,sc, er,ec, l in edges:
            start, end = (sr,sc), (er,ec)
            si = lookup[start]            
            if si not in self._neighbourhoods:
                self._neighbourhoods[si] = []
            ei = lookup[end]
            self._neighbourhoods[si].append((ei, l))
        self._neighbourhoods[len(self._vertices)-1] = []
        
    @property
    def vertices(self):
        return self._vertices
    
    def neighbours(self, vertex_index):
        return self._neighbourhoods[vertex_index]

    def construct_weighted_graph(self, invert_weights = False):
        class Graph(util.BaseGraph):
            def __init__(self, parent, invert_weights):
                self._p = parent
                self._vertices = list(range(len(parent.vertices)))
                self._invert_weights = invert_weights
            
            @property
            def vertices(self):
                return self._vertices
            
            def neighbours_of(self, v):
                return [u for u,_ in self._p.neighbours(v)]
            
            def weighted_neighbours_of(self, v):
                if not invert_weights:
                    return self._p.neighbours(v)
                return [(u,-d) for u,d in self._p.neighbours(v)]
            
        return Graph(self, invert_weights)

    def find_dag(self, graph=None):
        if graph is None:
            graph = self.construct_weighted_graph()
        return util.topological_sort(graph)
    
    def longest_path(self):
        graph = self.construct_weighted_graph(True)
        #ordered_vertices = self.find_dag(graph)
        dists, preds = util.shortest_path_dag(graph, 0)
        return -dists[-1]


def main(second_flag):
    with open("input_23.txt") as f:
        forest = Forest(f)
    return forest.longest_path()
