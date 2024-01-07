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
