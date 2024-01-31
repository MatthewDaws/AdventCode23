import itertools, math
from .util import Vector
from . import util

class HailStones:
    def __init__(self, rows):
        self._positions = []
        self._velocities = []
        def xyz(s):
            return tuple(int(x.strip()) for x in s.split(","))
        for row in rows:
            p,v = row.strip().split("@")
            self._positions.append( xyz(p) )
            self._velocities.append( xyz(v) )

    @property
    def entries(self):
        return len(self._positions)
    
    def position(self, i):
        return self._positions[i]
    
    def velocity(self, i):
        return self._velocities[i]

    def intersect(self, i, j, interval):
        delta1, delta2 = self.velocity(i), self.velocity(j)
        v1, v2 = self.position(i), self.position(j)
        perp = (delta2[1], -delta2[0])
        dotprod = delta1[0] * perp[0] + delta1[1] * perp[1]
        if dotprod == 0:
            return False
            #raise ValueError("Colinear!")
        t = (v2[0]-v1[0]) * perp[0] + (v2[1]-v1[1]) * perp[1]
        if t * dotprod < 0:
            return False
        s1 = (v1[0]-v2[0])*delta2[0] + (v1[1]-v2[1])*delta2[1]
        s2 = t * (delta1[0]*delta2[0] + delta1[1]*delta2[1])
        # Need s1 + s2/dotprod > 0
        if s1*dotprod*dotprod + s2*dotprod < 0:
            return False
        a1 = v1[0] * dotprod + t * delta1[0]
        a2 = v1[1] * dotprod + t * delta1[1]
        if dotprod < 0:
            limit1 = dotprod * interval[1]
            limit2 = dotprod * interval[0]
        else:
            limit1 = dotprod * interval[0]
            limit2 = dotprod * interval[1]
        return limit1 <= a1 <= limit2 and limit1 <= a2 <= limit2

    def count_intersections(self, interval):
        count = 0
        for i in range(self.entries-1):
            for j in range(i+1, self.entries):
                if self.intersect(i,j,interval):
                    count += 1
        return count
    

class Solve:
    def __init__(self, hailstones):
        self._hs = hailstones
        self._a1 = Vector(1,1,1)

    def pos_vel_pairs(self, maxnum=None):
        count = 0
        for i in range(self._hs.entries):
            yield Vector(*self._hs.position(i)), Vector(*self._hs.velocity(i))
            count += 1
            if maxnum is not None and count >= maxnum:
                return

    @staticmethod
    def compute_direction_matrix(u1,d1,u2,d2,u3,d3):
        a = (u1-u3)*((u2-u1)@d3)
        b = d1*((u2-u1)@d3) - (u1-u3)*(d1@d3)
        c = (u1-u3)*(d2@d3)
        d = d1*(d2@d3)
        g = math.gcd(a,b,c,d)
        return a//g, b//g, c//g, d//g

    def find_t1(self):
        t1, _ = self.find_t1t2()
        return t1

    def find_t1t2(self):
        pairs = list(self.pos_vel_pairs(4))
        (u1,d1), (u2,d2), (u3,d3) = pairs[:3]
        a,b,c,d = self.compute_direction_matrix(u1,d1,u2,d2,u3,d3)
        #print(a,b,c,d)

        aa,bb,cc,dd = self.compute_direction_matrix(u1,d1,u2,d2,*pairs[3])
        #print(aa,bb,cc,dd)

        alpha = b*dd - bb*d
        beta = a*dd + b*cc - aa*d - bb*c
        gamma = a*cc - aa*c
        #print(alpha, beta, gamma)
        t1 = [x for x in util.integer_quadratic(alpha, beta, gamma) if x>0][0]
        #print(t1)
        top = -(a+b*t1)
        bot = c+d*t1
        if bot == 0:
            top = -(aa+bb*t1)
            bot = cc+dd*t1
        assert top % bot == 0
        t2 = top // bot
        return t1, t2
    
    def find_line(self):
        t1, t2 = self.find_t1t2()
        pairs = list(self.pos_vel_pairs(2))
        x = pairs[0][0] + t1 * pairs[0][1]
        y = pairs[1][0] + t2 * pairs[1][1]
        d = y-x
        g = math.gcd(*d)
        self._u, self._e = x, Vector(d.x//g, d.y//g, d.z//g)
        return self._u, self._e
    
    def find_intersection(self, u, d):
        return self.find_int(u,d,self._u,self._e)
    
    @staticmethod
    def find_int(u, d, v, e):
        x11 = -d*d
        x12 = e*d
        x21 = -x12
        x22 = e*e
        y1 = (u-v)*d
        y2 = (u-v)*e
        det = x11*x22 - x12*x21
        tt = x22 * y1 - x12 * y2
        ss = -x21 * y1 + x11 * y2
        if det == 0:
            print(x11,x12,x21,x22)
            raise ValueError()
        assert tt%det == 0
        assert ss%det == 0
        return tt//det, ss//det

    def find_starting_point(self):
        pairs = list(self.pos_vel_pairs(2))
        t1, s1 = self.find_intersection(*pairs[0])
        t2, s2 = self.find_intersection(*pairs[1])
        if t1 > t2:
            t1, t2 = t2, t1
            s1, s2 = s2, s1
        if s1 < s2:
            d = 1
            r = s1 - t1
        else:
            d = -1
            r = s1 + t1
        return self._u + r * self._e, d * self._e
    
    def check(self, start, direction):
        for u,d in self.pos_vel_pairs():
            t,s = self.find_int(u,d,start,direction)
            assert t==s


def main(second_flag):
    with open("input_24.txt") as f:
        h = HailStones(f)
    if not second_flag:
        return h.count_intersections((200000000000000, 400000000000000))

    ch = Solve(h)
    ch.find_line()
    start, direction = ch.find_starting_point()
    ch.check(start,direction)
    return start * Vector(1,1,1)
