class SpringLine:
    def __init__(self, input, unfold=False):
        row, code = input.strip().split()
        self._row = row
        self._code = [int(x) for x in code.split(",")]
        if unfold:
            c = list(self._code)
            for _ in range(4):
                self._code.extend(c)
            self._row = "?".join(self._row for _ in range(5))

    @property
    def row(self):
        return self._row
    
    @property
    def codes(self):
        return self._code

    def split(self):
        return [x for x in self._row.split(".") if len(x)>0]

    def __repr__(self):
        return f"SpringLine({self.row, self.codes})"


class PartialSolution:
    def __init__(self, parent_springline, initial_guess):
        self._sl = parent_springline
        self._row = initial_guess

    @property
    def guess(self):
        return self._row

    def greedy_find(self):
        """But this is not a greedy-algorithm problem sadly"""
        partial = ""
        index = 0
        for codenum, length in enumerate(self._sl.codes):
            if index == len(self._row):
                return None
            while self._row[index] == ".":
                partial = partial + "."
                index += 1
                if index == len(self._row):
                    return None
            if self._row[index] == "#":
                count = 0
                while index < len(self._row) and self._row[index] == "#":
                    count += 1
                    partial = partial + "#"
                    index += 1
                if count != length:
                    return None
                continue
            count = 0
            while index < len(self._row) and (self._row[index] == "?" or self._row[index] == "#") and count < length:
                partial = partial + "#"
                index += 1
                count += 1
            if count < length:
                return None
            if codenum < len(self._sl.codes)-1:
                if index == len(self._row)-1:
                    return None
                if self._row[index] == "#":
                    return None
                partial = partial + "."
                index += 1
        while index < len(self._row):
            if self._row[index] == "#":
                return None
            partial = partial + "."
            index += 1
        return partial

    @property
    def is_valid(self):
        """Only works if there are no guesses"""
        if not self.is_complete:
            raise AssertionError()
        runs = [len(x) for x in self._row.split(".") if len(x)>0]
        return runs == self._sl.codes
    
    @property
    def is_complete(self):
        return all(c!="?" for c in self._row)

    def branch(self):
        if self.is_complete:
            raise AssertionError()
        index = self._row.find("?")
        one = self._row[:index] + "." + self._row[index+1:]
        two = self._row[:index] + "#" + self._row[index+1:]
        return PartialSolution(self._sl, one), PartialSolution(self._sl, two)

def search(springline):
    guesses = [PartialSolution(springline, springline.row)]
    solutions = []
    while len(guesses) > 0:
        guess = guesses.pop()
        if guess.is_complete:
            if guess.is_valid:
                solutions.append( guess.guess )
            continue
        guesses.extend( guess.branch() )
    return solutions

def count_all_solutions(file):
    count = 0
    for row in file:
        sl = SpringLine(row)
        count += len(search(sl))
    return count

def possible_length(segment):
    """`segment` should consist of ? or #. Returns number of possible lengths.
    ?#? -> {{1},{2},{3}}
    ??? -> {{1},{2},{3},{1,1}    
    """

# ????#???#????####?#. 1,1,3,3,4,1
# How to do this quickly??
# #.#.###.#???.####.#
    
# #..??????#??#?#?#? 1,1,11
# #..???.###########
# #..??.###########.

# ?.??#?.????#????????.??#?.????#????????.??#?.????#????????.??#?.????#????????.??#?.????#?????? [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

def reduce_end(prefix, codeprefix):
    """-> list of (prefix, codeprefix)"""
    while prefix[-1] == ".":
        prefix = prefix[:-1]
        if len(prefix) == 0:
            if len(codeprefix) == 0:
                return [("", [])]
            return None
    if prefix[-1] == "#":
        if len(prefix) < codeprefix[-1]:
            return None
        for index in range(len(prefix)-codeprefix[-1], len(prefix)):
            if prefix[index] == ".":
                return None
        if codeprefix[-1] == len(prefix):
            if len(codeprefix) == 1:
                return [("",[])]
            return None
        if prefix[len(prefix)-codeprefix[-1]-1] == "#":
            return None
        if codeprefix[-1]+1 == len(prefix):
            if len(codeprefix) == 1:
                return [("",[])]
            return None
        return [(prefix[:len(prefix)-codeprefix[-1]-1], codeprefix[:-1])]
    if len(prefix) == 1:
        if len(codeprefix) == 0:
            return [("", [])]
        return [("#", codeprefix)]
    return [ (prefix[:-1], codeprefix), (prefix[:-1] + "#", codeprefix) ]

def count_solutions_new(springline):
    count = 0
    pool = [(springline.row, springline.codes)]
    while len(pool) > 0:
        pr, codepr = pool.pop()
        if len(codepr) == 0:
            if all(x!="#" for x in pr):
                count += 1
            continue
        choices = reduce_end(pr, codepr)
        if choices is not None:
            pool.extend(choices)
    return count

def count_all_solutions_new(file, unfold=False):
    count = 0
    for row in file:
        sl = SpringLine(row, unfold)
        nc = count_solutions_new(sl)
        print(sl, "-->", nc)
        count += nc
    return count

def main(second_flag):
    with open("input_12.txt") as f:
        if not second_flag:
            # 7047
            return count_all_solutions_new(f)
        return count_all_solutions_new(f, True)
