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

    def sum_to_sharp(start, counts_row):
        s = 0
        for c in range(start, length_row):
            s += counts_row[c]
            if springline.row[c] == "#":
                break
        return s
    
    a = num_runs-2
    while a>=0:
        for b in range(length_row):
            if springline.can_place(a, b):
                length = springline.codes[a]
                counts[a][b] = sum_to_sharp(b+length+1, counts[a+1])
            else:
                counts[a][b] = 0
        a -= 1

    return sum_to_sharp(0, counts[0])

def count_all_solutions_with_dp(file, unfold=False):
    count = 0
    for row in file:
        sl = SpringLine(row, unfold)
        count += build_dynamic_programme(sl)
    return count

def main(second_flag):
    with open("input_12.txt") as f:
        if not second_flag:
            # 7047
            return count_all_solutions_with_dp(f)
        return count_all_solutions_with_dp(f, True)
