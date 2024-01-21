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
        self._visited = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self._visited[0][self.start_column] = 1
        while len(routes) > 0:
            startrow,startcol, dr,dc = routes.pop()
            prevrow, prevcol = startrow, startcol
            length = 0
            while True:
                length += 1
                row, col = prevrow+dr, prevcol+dc
                self._visited[row][col] = 1
                choices = {(ddr,ddc) for ddr,ddc in self.possible_directions(row,col) if (ddr!=-dr or ddc!=-dc)}
                if len(choices) == 0:
                    assert row == self.height - 1
                    assert col == self.finish_column
                elif len(choices) > 1 and (row, col) not in vertices:
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
        
    def debug_output(self):
        walked = []
        for row, usedrow in zip(self._grid, self._visited):
            out = []
            for entry, used in zip(row, usedrow):
                if used == 1:
                    assert entry!="#"
                    out.append("O")
                else:
                    assert entry=="#"
                    out.append(entry)
            walked.append("".join(out))
        return "\n".join(walked)

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


class Forest2(Forest):
    def __init__(self, rows):
        super().__init__(rows)

    def possible_directions(self, row, col):
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            e = self.at(row+dr, col+dc)
            if e is not None and e!="#":
                yield dr,dc

    class Path:
        def __init__(self, current_vertex, used_vertices, length):
            self._vertex = current_vertex
            self._used = set(used_vertices)
            self._length = length

        @staticmethod
        def initial():
            return Forest2.Path(0, [0], 0)
        
        @property
        def at(self):
            return self._vertex
        
        @property
        def length(self):
            return self._length

        def using(self, v):
            return v in self._used
        
        def new_path_adding(self, new_vertex, weight):
            s = set(self._used)
            s.add(new_vertex)
            return Forest2.Path(new_vertex, s, self.length + weight)

    def build_undirected_graph(self):
        dgraph = self.construct_weighted_graph()
        num_vertices = len(dgraph.vertices)
        adjacency = [[None for _ in range(num_vertices)] for _ in range(num_vertices)]
        for v in dgraph.vertices:
            for u,l in dgraph.weighted_neighbours_of(v):
                adjacency[u][v] = l
                adjacency[v][u] = l
        graph = util.WeightedGraph()
        for v in dgraph.vertices:
            graph.add_vertex(v)
        for v, row in enumerate(adjacency):
                for u, length in enumerate(row):
                    if length is not None:
                        graph.add_directed_edge(v,u,length)
        return graph

    def longest_path(self):
        graph = self.build_undirected_graph()
        end_vertex = len(graph.vertices) - 1
        max_length = 0
        queue = [Forest2.Path.initial()]
        while len(queue) > 0:
            current = queue.pop()
            if current.at == end_vertex:
                max_length = max(max_length, current.length)
                continue
            for v,d in graph.weighted_neighbours_of(current.at):
                if not current.using(v):
                    queue.append(current.new_path_adding(v,d))
        return max_length


def main(second_flag):
    if not second_flag:
        with open("input_23.txt") as f:
            forest = Forest(f)
        return forest.longest_path()

    with open("input_23.txt") as f:
        forest = Forest2(f)
    return forest.longest_path()
