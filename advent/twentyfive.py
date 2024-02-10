from . import util
import random

class Components:
    def __init__(self, rows):
        self._wiring = dict()
        for row in rows:
            key, connections = row.strip().split(":")
            if key in self._wiring:
                raise ValueError(f"Two lines for '{key}'")
            self._wiring[key] = set()
            for con in connections.split():
                self._wiring[key].add(con)
        # Remember this is not currently symmetric
        self._pop_edges_verts()
                
    def edges(self):
        return self._edges
    
    def vertices(self):
        return self._vertices

    def _pop_edges_verts(self):
        self._edges = []
        self._vertices = set()
        for key, cons in self._wiring.items():
            self._vertices.add(key)
            for c in cons:
                self._edges.append( (key, c) )
                self._vertices.add(c)

    def random_2_components(self):
        edges = list(self.edges())
        random.shuffle(edges)
        tree = util.Kruskal(edges)
        final_edge = tree[-1]
        ds = util.DisjointSet()
        for (u,v) in tree[:-1]:
            ds.add(u)
            ds.add(v)
            ds.union(u,v)
        for v in final_edge:
            ds.add(v)
        return ds.as_sets()

    def find_cut(self, components=None):
        if components is None:
            components = self.random_2_components()
        components = list(components)
        A, B = components
        cut = set()
        for u,v in self.edges():
            if u in A and v in A:
                continue
            if u in B and v in B:
                continue
            cut.add((u,v))
        return cut
        
    def find_cut_of_size(self, maxsize, maxiters=100000):
        count = 0
        while True:
            components = self.random_2_components()
            cut = self.find_cut(components)
            if len(cut) <= maxsize:
                return components, cut
            count += 1
            if count >= maxiters:
                raise AssertionError()
            

def main(second_flag):
    with open("input_25.txt") as f:
        com = Components(f)
    if not second_flag:
        coms, cut = com.find_cut_of_size(3)
        part1, part2 = list(coms)
        return len(part1) * len(part2)
