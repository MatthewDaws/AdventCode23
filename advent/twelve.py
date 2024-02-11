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

    # Probably not used
    def split(self):
        return [x for x in self._row.split(".") if len(x)>0]

    def __repr__(self):
        return f"SpringLine({self.row, self.codes})"

    def can_place(self, run_num, location):
        length = self._code[run_num]
        if location < 0 or location + length - 1 >= len(self._row):
            return False
        segment = self._row[location:location+length]
        if "." in segment:
            return False
        if location > 0 and self._row[location-1] == "#":
            return False
        if location + length == len(self._row):
            return True
        return self._row[location + length] != "#"

    def can_place_last(self, location):
        if not self.can_place(len(self._code)-1, location):
            return False
        length = self._code[-1]
        return not("#" in self._row[location+length:])

# N(a,b) = number of solutions with run `a` of known lengths starting at exactly location `b` of string,
#   and `a+1`, `a+2`, ... in some valid place beyond `b`.
# If run `a` is length k then b, b+1, ..., b+k-1 are used, b+k must be "."  So
# N(a,b) = N(a+1, b+k+1) + N(a+1, b+k+2) + N(a+1, b+k+3) + ...
# but we should be careful, as we shouldn't skip a "#" which is otherwise not allocated.
# If there are `n` runs, then N(n-1,b) is 1 exactly when we can place this run at location `b` and there are no more "#"s after.
def build_dynamic_programme(springline):
    num_runs = len(springline.codes)
    length_row = len(springline.row)
    counts = [ [None for _ in range(length_row)] for _ in range(num_runs) ]

    final_length = springline.codes[-1]
    for b in range(length_row):
        if springline.can_place_last(b):
            counts[-1][b] = 1
        else:
            counts[-1][b] = 0

    a = num_runs-2
    while a>=0:
        for b in range(length_row):
            if springline.can_place(a, b):
                length = springline.codes[a]
                s = 0
                for c in range(b+length+1, length_row):
                    s += counts[a+1][c]
                    if springline.row[c] == "#":
                        break
                counts[a][b] = s
            else:
                counts[a][b] = 0
        a -= 1

    # Re-factor this: DRY!
    s = 0
    for c in range(length_row):
        s += counts[0][c]
        if springline.row[c] == "#":
            break
    return s

def count_all_solutions_with_dp(file, unfold=False):
    count = 0
    for row in file:
        sl = SpringLine(row, unfold)
        count += build_dynamic_programme(sl)
    return count



# This code is not now used
    
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


#  End


# The numbers are too large to actually generate all the possibilties.  So we need to _count_ them without
# generating them all.
# All I can think of right now is "Bars and Stars"
# .?????????.  2,3    can be solved: we have 10 ?s and 2+3+1=6 known cells (##.###) so 4 further .s to place
#    in 3 possible places (start, middle or end, in this example).  That's the same as k=3 non-negative integers
#    summing to n=4, so k+n+1 choose n, so 8 choose 4, so 70.
#    See https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)

# ????#???#????####?#. 1,1,3,3,4,1
# How to do this quickly??
#   ????#???#???.####.#. 1,1,3,3,   4,1
#   the two #s must be the 3s, and then the 1s can only fit in as
#   #.#.#???#???.####.#. 1,1,  3,3,   4,1
#   #.#.###.###..####.#. 1,1,  3,3,   4,1
# So actually just 1 choice



# ?.??#?.????#????????.??#?.????#????????.??#?.????#????????.??#?.????#????????.??#?.????#?????? [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
# We see this must be
# ?.####.????#????????.####.????#????????.####.????#????????.####.????#????????.####.????#?????? [4, 4, 4, 4, 4,    4, 4, 4, 4, 4]
#     The 5 remaining blocks must be #### of which there are 4 choices for each one, so 4**5 in total
# But this seems terribly ad hoc.

#  ??.???.#?????.???.#?????.???.#?????.???.#?????.???.#??  1,1,2,1,1,2,1,1,2,1,1,2,1,1,2
#  ..................#.#.##.#.#.##.#.#..##.#.#.##.#.#.##.
#  .......#.#.##.#.#.##.#.#.##..#.#.##.#...#..........##


# ?###??????????###??????????###??????????###??????????###????????   3,2,1,3,2,1,3,2,1,3,2,1,3,2,1
# .###.????????.###.????????.###.????????.###.????????.###.???????

# ?#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#?    1,3,1,6,1,3,1,6,1,3,1,6,1,3,1,6,1,3,1,6
#  # ### # ######  # ### # ######  # ### # ######  # ### # ######  # ### # ######






# Not used???

class SharpBlock():
    def __init__(self, block):
        self._runs = []
        l, t = 0, None
        for x in block:
            assert x in "#?"
            if x == t:
                l += 1
                continue
            if t is not None:
                self._runs.append((t,l))
            t = x
            l = 1
        self._runs.append((t,l))

    def __iter__(self):
        yield from self._runs

    def assignments(self, runs):
        assert len(runs) > 0
        assignments = [ (list(),0) ]
        for t,l in self._runs:
            if t == "?":
                assignments = [(a, tail+l) for (a,tail) in assignments]
                continue
            new_assignments = []
            for assigns, tail_usage in assignments:
                if len(assigns) == 0:
                    index = 0
                else:
                    index = assigns[-1]
                    if tail_usage + l <= runs[index]:
                        new_assignments.append((assigns+[index], tail_usage+l))
                    index += 1
                while index < len(runs) and runs[index] < l:
                    index += 1
                if index == len(runs):
                    # Can't extend, so do nothing with this possible assignment
                    continue
                assigns.append(index)                        
                new_assignments.append((assigns, l))
            assignments = new_assignments
        return [a for a,_ in assignments]

class FastSpringLine(SpringLine):
    def __init__(self, input, unfold=False):
        super().__init__(input, unfold)





# The below code is fine for the 1st problem, but impossibly slow for the 2nd part

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
            return count_all_solutions_with_dp(f)
        return count_all_solutions_with_dp(f, True)
