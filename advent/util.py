import math

def lcm(n, m):
    return n * m // math.gcd(n, m)

def bezout(n, m):
    """Returns (s,t) with n*s + m*t = gcd(n, m)"""
    aold, a = n, m
    sold, s = 1, 0
    told, t = 0, 1
    while a > 0:
        q = aold // a
        aold, a = a, aold - q*a
        sold, s = s, sold - q*s
        told, t = t, told - q*t
    return sold, told

def chinese_remainder(anpairs):
    """Generalise chinese remainder.

    Finds smallest N with N \equiv a_i \mod n_i.

    Returns (N, lcm) where if N is a solution, so is N + n*lcm for any integer n.

    Theory: N = a \mod n and N = b \mod n implies that N = a+nx = b+my for some integers
    x, y and so g=\gcd(n,m) divides a-b.  If this holds, then by Bezout we find s, t with
    n*s + m*t = g
    so  n*s*x + m*t*x = a-b for some integer x
    so  a + (-s*x)*n = b + (t*x)*m
    so  X = a + (-s*x)*n  has  X = a mod n and X = b mod m.
    If Y also solves these then X=Y mod n and mod m so X=Y mod lcm(n,m)

    If we need to solve 3 equations, we solve the first 2 and then replace these by N = X \mod lcm(n,m)
    """
    anpairs = list(anpairs)
    if len(anpairs) == 1:
        a, n = anpairs[0]
        return a % n, n
    while True:
        b, m = anpairs.pop()
        a, n = anpairs.pop()
        g = math.gcd(n, m)
        if (a-b)%g != 0:
            raise ValueError("No solutions")
        s, t = bezout(n, m)
        x = a - s * ((a-b)//g) * n
        assert (x-a)%n == 0
        assert (x-b)%m == 0
        lc = lcm(n, m)
        x = x % lc
        if len(anpairs) == 0:
            return x, lc
        anpairs.append((x, lc))

def brute_force_chinese_remainder(anpairs):
    ns = [x[1] for x in anpairs]
    while len(ns) > 1:
        n = ns.pop()
        m = ns.pop()
        ns.append(lcm(n, m))
    for x in range(ns[0]):
        if all( (x-a)%n == 0 for (a,n) in anpairs ):
            return x
    raise ValueError()

def winding_number(path, row, col):
    """Computes the winding number of a path around the point (row,col).
    `path` should be list of (row,col) coordinates."""
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
    # start_quad = quadrant((row,col), path[0])
    # last_quad = start_quad
    # crosses = 0
    # for i in range(1, len(path)):
    #     new_quad = quadrant((row,col), path[i])
    #     crosses = update_crosses(last_quad, new_quad, crosses)
    #     last_quad = new_quad
    for i, pos in enumerate(path):
        if i == 0:
            start_quad = quadrant((row,col), pos)
            last_quad = start_quad
            crosses = 0
        else:
            new_quad = quadrant((row,col), pos)
            crosses = update_crosses(last_quad, new_quad, crosses)
            last_quad = new_quad
    crosses = update_crosses(last_quad, start_quad, crosses)
    return crosses


class Interval:
    """Represents an interval including the end-points"""
    def __init__(self, a, b):
        if not a<=b:
            raise ValueError()
        self._range=(a,b)

    @staticmethod
    def from_start_length(start, length):
        if length < 0:
            return Interval(start+length, start)
        return Interval(start, start+length)

    @property
    def start(self):
        return self._range[0]

    @property
    def end(self):
        return self._range[1]

    def contains(self, x):
        return self.start <= x and  x <= self.end

    def __repr__(self):
        return f"Interval({self.start},{self.end})"
    
    def __eq__(self, other):
        return self._range == other._range
    
    def __hash__(self):
        return hash(self._range)
    
    def __lt__(self, other):
        return self.start < other.start
    
    def __le__(self, other):
        return self.start <= other.start

    def intersect(self, other):
        a = max(self.start, other.start)
        b = min(self.end, other.end)
        if a<=b:
            return Interval(a,b)
        return None


class BaseGraph:
    """Just defines an interface for various algorithms"""
    def __init__(self):
        pass

    @property
    def vertices(self):
        pass

    def neighbours_of(self, vertex):
        pass

    def weighted_neighbours_of(self, vertex):
        """Return a list of pairs (neighbour, length_of_edge)"""
        raise NotImplementedError()


class Graph(BaseGraph):
    def __init__(self):
        self._vertices = []
        self._neighbourhoods = dict()

    def add_vertex(self, v):
        if v in self._neighbourhoods:
            raise ValueError(f"Already has vertex '{v}'")
        self._vertices.append(v)
        self._neighbourhoods[v] = []

    def add_directed_edge(self, start, end):
        self._neighbourhoods[start].append(end)

    @property
    def vertices(self):
        return self._vertices
    
    def neighbours_of(self, vertex):
        return self._neighbourhoods[vertex]
    

class WeightedGraph(Graph):
    def __init__(self):
        super().__init__()
        self._weights = dict()

    def add_vertex(self, v):
        super().add_vertex(v)
        self._weights[v] = []

    def add_directed_edge(self, start, end, weight):
        super().add_directed_edge(start, end)
        self._weights[start].append(weight)

    def weighted_neighbours_of(self, vertex):
        return zip(self._neighbourhoods[vertex], self._weights[vertex])

    def __str__(self):
        out = []
        for v in self.vertices:
            line = f"{v}: "
            for u,l in self.weighted_neighbours_of(v):
                line = line + f" ({u},{l})"
            out.append(line)
        return "\n".join(out)


def topological_sort(graph):
    to_visit = set(graph.vertices)
    seen = dict()
    reverse_dag = []
    def visit(vertex):
        if vertex in seen:
            if seen[vertex] == 1:
                return
            raise ValueError("Not a DAG")
        seen[vertex] = 0
        to_visit.discard(vertex)
        for neigh in graph.neighbours_of(vertex):
            visit(neigh)
        seen[vertex] = 1
        reverse_dag.append(vertex)
    while len(to_visit) > 0:
        visit(to_visit.pop())
    reverse_dag.reverse()
    return reverse_dag

def shortest_path_dag(graph, initial_vertex, sorted_vertices=None):
    if sorted_vertices is None:
        sorted_vertices = topological_sort(graph)
    distances = [None for _ in range(len(sorted_vertices))]
    predecessors = [None for _ in range(len(sorted_vertices))]
    distances[initial_vertex] = 0
    index = sorted_vertices.index(initial_vertex)
    while index < len(sorted_vertices):
        vertex = sorted_vertices[index]
        for u, d in graph.weighted_neighbours_of(vertex):
            newlen = distances[vertex] + d
            if distances[u] is None or distances[u] > newlen:
                distances[u] = newlen
                predecessors[u] = vertex
        index += 1
    return distances, predecessors


def integer_sqrt(x):
    """Find the integer sqaure-root of x, rounding down"""
    if x<0:
        raise ValueError()
    if x==0:
        return 0
    low = 1
    high = x
    while high-low > 1:
        # Keep invariant low*low <= x <= high*high
        mid = (low+high)//2
        if mid*mid > x:
            high = mid
        else:
            low = mid
    if high*high == x:
        return high
    return low

def integer_quadratic(a,b,c):
    """Find integer solutions to a*x*x+b*x+c==0"""
    if a == 0:
        if b==0:
            raise ValueError()
        if c%b != 0:
            return []
        return [-c//b]
    dis = b*b - 4*a*c
    if dis < 0:
        return []
    dissqr = integer_sqrt(dis)
    if dissqr * dissqr != dis:
        return []
    out = set()
    def allowed(sign):
        top = -b + sign * dissqr
        bot = 2 * a
        if top % bot == 0:
            out.add(top//bot)
    allowed(+1)
    allowed(-1)
    out = list(out)
    out.sort()
    return out


class Vector:
    """A simple 3D vector class"""
    def __init__(self,x,y,z):
        self._coords = [x,y,z]

    @property
    def x(self):
        return self._coords[0]

    @property
    def y(self):
        return self._coords[1]

    @property
    def z(self):
        return self._coords[2]
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __getitem__(self, i):
        return self._coords[i]

    def __eq__(self, other):
        return self._coords == other._coords

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def __matmul__(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

    def __rmul__(self, scalar):
        return Vector(scalar*self.x, scalar*self.y, scalar*self.z)

    def is_null(self):
        return all(x==0 for x in self._coords)


def extgcd(a, b):
    """Extended Euclidean algorithm.
    
    (a, b) : Integers to find gcd of

    Returns: (d, s, t)
      d : The gcd of (a,b)
      (s,t) : Integers such that s*a + t*b == d

    Raises: ValueError if a==b==0
    """
    a, b = int(a), int(b)
    if a==0 and b==0:
        raise ValueError("gcd(0,0) is undefined")
    nega, negb = 1, 1
    if a < 0:
        nega, a = -1, -a
    if b < 0:
        negb, b = -1, -b
    s, ss, t, tt  = 1, 0, 0, 1
    while b > 0:
        q = a // b
        a, b = b, a % b
        s, ss = ss, s - q*ss
        t, tt = tt, t - q*tt
    return a, s*nega, t*negb

def inverse_modn(x, n):
    """Compute the inverse of `x` modulo `n` or Raises ValueError."""
    d, s, t = extgcd(x, n)
    if d != 1:
        raise ValueError(f"{x} is not invertible modulo {n}")
    return s % n


class DisjointSet:
    def __init__(self, iterable=None):
        self._elements = dict()
        if iterable is not None:
            for x in iterable:
                self.add(x)
        
    @property
    def entries(self):
        """Returns set of elements"""
        return set(self._elements.keys())
    
    def contains(self, element):
        """Does the disjoint set currently contain `element`?"""
        return element in self._elements

    def as_sets(self):
        lookup = dict()
        for key in self._elements.keys():
            root = self._find_entry(key)
            if root not in lookup:
                lookup[root] = set()
            lookup[root].add(key)
        return {frozenset(x) for x in lookup.values()}

    def add(self, element):
        """Add a (possibly) new `element`."""
        if element in self._elements:
            return
        self._elements[element] = DisjointSet.Entry()

    def find(self, element):
        """Find an abstract representative of the partition containing `element`, else raises `KeyError`"""
        return hash(self._find_entry(element))

    def _find_entry(self, element):
        entry = self._elements[element]
        while entry.parent is not None:
            entry = entry.parent
        return entry

    def find_depth(self):
        maxdepth = 0
        for entry in self._elements.values():
            depth = 0
            while entry.parent is not None:
                entry = entry.parent
                depth += 1
            maxdepth = max(maxdepth, depth)
        return maxdepth

    def union(self, a, b):
        """Merge the partitions containing elements `a` and `b`; raises `KeyError` if these elements are not present."""
        aentry = self._find_entry(a)
        bentry = self._find_entry(b)
        if aentry is bentry:
            return
        if aentry.rank < bentry.rank:
            aentry, bentry = bentry, aentry
        bentry.parent = aentry
        if aentry.rank == bentry.rank:
            aentry.rank += 1

    class Entry:
        def __init__(self):
            self.parent = None
            self.rank = 0


def Kruskal(ordered_edges):
    """Apply Kruskal's algorithm to find a minimal weight spanning tree.
    
    input: `ordered_edges` is iterable of pairs (u,v) of vertices, ordered least weight edge first

    output: list of edges (u,v) forming minimal spanning tree
    """
    components = DisjointSet()
    spanning_tree = list()
    for (u,v) in ordered_edges:
        components.add(u)
        components.add(v)
        if components.find(u) != components.find(v):
            spanning_tree.append( (u,v) )
            components.union(u, v)
    return spanning_tree
