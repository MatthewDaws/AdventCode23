import re, math, itertools
import util

class LeftRight():
    def __init__(self, string):
        self._string = string

    def __iter__(self):
        index = 0
        while True:
            if index == len(self._string):
                index = 0
            yield self._string[index]
            index += 1

    @property
    def period(self):
        return len(self._string)

    @property
    def once(self):
        return self._string

def parse(file):
    lr_line = next(file).strip()
    
    l = next(file)
    assert l.strip() == ""

    matcher = re.compile("(.+?)\s+=\s+\((.+?)\,\s+(.+?)\)")
    lookup = dict()
    for row in file:
        m = matcher.match(row)
        key, left, right = m.group(1), m.group(2), m.group(3)
        if key in lookup:
            raise KeyError("Already have {}".format(key))
        lookup[key] = (left, right)

    return LeftRight(lr_line), lookup
        
def _move(lookup, direction, cur):
    if direction == "L":
        return lookup[cur][0]
    elif direction == "R":
        return lookup[cur][1]
    raise ValueError()

def time_to_ZZZ(lr, lookup):
    cur = "AAA"
    count = 0
    for direction in lr:
        count += 1
        cur = _move(lookup, direction, cur)
        if cur == "ZZZ":
            return count

def multiple_paths(lr, lookup):
    current_keys = [key for key in lookup if key[-1]=="A"]
    count = 0
    for direction in lr:
        count += 1
        for index in range(len(current_keys)):
            current_keys[index] = _move(lookup, direction, current_keys[index])
        if all(key[-1]=="Z" for key in current_keys):
            return count

def _one_loop(lr, lookup, cur):
    segment = []
    for direction in lr.once:
        cur = _move(lookup, direction, cur)
        segment.append(cur)
    return segment

def find_repeat(lr, lookup, start):
    # Returns segment and period
    segment = [start]
    while True:
        segment.extend(_one_loop(lr, lookup, segment[-1]))
        back_index = lr.period
        while back_index < len(segment):
            if segment[-1] == segment[-1-back_index]:
                return segment, back_index
            back_index += lr.period

def _reduce_periods(numbers, period):
    nums = list(numbers)
    removed = True
    while removed:
        removed = False
        i = len(nums) - 1
        while i>0:
            z = nums[i]
            if z - period in nums:
                nums.remove(z)
                removed = True
                i=0
            i -= 1
    return nums

def z_end(lr, lookup, start):
    segment, period = find_repeat(lr, lookup, start)
    z_indexes = [i for i, key in enumerate(segment) if key[-1]=="Z"]
    if len(z_indexes) == 0:
        raise Exception("Never gets to Z")
    return _reduce_periods(z_indexes, lr.period), period

def fast_multiple_paths(lr, lookup):
    keyperiods = {key : z_end(lr, lookup, key) for key in lookup if key[-1]=="A"}
    periods = [x[1] for x in keyperiods.values()]
    gcd = math.gcd(*periods)
    starts = [_reduce_periods(x[0], gcd) for x in keyperiods.values()]
    # Find smallest N with for each i, there is some s in starts[i] with (N-s) % periods[i] == 0
    candidates = []
    for ss in itertools.product(*starts):
        try:
            N, lcm = util.chinese_remainder(zip(ss, periods))
            if N == 0:
                N += lcm
            candidates.append(N)
        except ValueError:
            pass
    return min(candidates)

def main(second_flag):
    if not second_flag:
        with open("input_8.txt") as f:
            return time_to_ZZZ(*parse(f))

    with open("input_8.txt") as f:
        return fast_multiple_paths(*parse(f))
