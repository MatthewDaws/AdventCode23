class RangeMap:
    """A map interface which uses a sequences of "ranges".
    A range is a tupe (dest, source, length) where source -> dest, source+1 -> dest+1,
    and so on for length."""
    def __init__(self, lines):
        ranges = []
        for line in lines:
            if len(line)==0: continue
            dest, source, length = [int(x) for x in line.split(" ")]
            ranges.append((dest, source, length))
        self._init_from_list(ranges)

    def _init_from_list(self, ranges):
        self._ranges = list(ranges)
        self._ranges.sort(key=(lambda x : x[1]))

    def __getitem__(self, value):
        for dest, source, length in self._ranges:
            if source <= value < source+length:
                return dest + (value-source)
        return value

    def __iter__(self):
        yield from self._ranges

    @classmethod
    def from_list(cls, ranges):
        obj = cls([])
        obj._init_from_list(ranges)
        return obj

    def as_gaplass_range(self):
        current_position = self._ranges[0][1]
        for dest, source, length in self._ranges:
            if current_position < source:
                yield current_position, current_position, source - current_position
            yield dest, source, length
            current_position = source + length

    def map_run(self, start, length):
        """Make a new RangeMap by applying {start, start+1, ..., start+length-1}
        to the mapping represented by this object."""
        output_ranges = []

        our_start = self._ranges[0][1]
        if start < our_start:
            segment_length = min(our_start - start, length)
            output_ranges.append( (start, start, segment_length))
            length -= segment_length
            start = our_start
        
        if length > 0:
            for dest, source, seglen in self.as_gaplass_range():
                if source <= start < source + seglen:
                    segment_length = min(source + seglen - start, length)
                    output_ranges.append( (dest + start - source, start, segment_length))
                    length -= segment_length
                    start += segment_length
                    if length == 0:
                        break

        if length > 0:
            output_ranges.append( (start, start, length))
        
        return self.from_list(output_ranges)

    def map_range(self, dest, start, length):
        out = self.map_run(dest, length)
        def move_back_ranges():
            for d,s,l in out._ranges:
                yield d, s - dest + start, l
        return RangeMap.from_list(move_back_ranges())


def parse_seeds(line):
    assert line[:7] == "seeds: "
    return [int(x) for x in line[7:].strip().split(" ") if len(x)>0]

def parse_map_section(f):
    line = next(f).strip()
    assert line[-5:] == " map:"
    name_bits = line[:-5].split("-")
    assert name_bits[1] == "to"
    name = (name_bits[0], name_bits[2])

    lines = []
    for line in f:
        if line.strip() != "":
            lines.append(line)
        else:
            break

    return name, RangeMap(lines)

def compute_locations(seeds, maps):
    locations = []
    for seed in seeds:
        for mapper in maps:
            seed = mapper[seed]
        locations.append( seed )
    return locations

def load_file(file):
    seeds = parse_seeds(next(file))
    next(file)
    maps = []
    try:
        while True:
            maps.append( parse_map_section(file) )
    except StopIteration:
        pass
    return seeds, maps

def second(file):
    seeds, maps = load_file(file)
    def seed_pairs():
        for i in range(0, len(seeds), 2):
            yield seeds[i], seeds[i+1]
    minimum = None
    for start, length in seed_pairs():
        ranges = [(start, start, length)]
        for _, m in maps:
            new_ranges = []
            for d,s,l in ranges:
                new_ranges.extend( m.map_range(d,s,l).as_gaplass_range() )
            ranges = new_ranges
        new_min = min(d for d,s,l in ranges)
        if minimum is None or new_min < minimum:
            minimum = new_min
    return minimum

def main(second_flag):
    if not second_flag:
        with open("input_5.txt") as f:
            seeds, maps = load_file(f)
        locations = compute_locations(seeds, [m for _,m in maps])
        return min(locations)

    with open("input_5.txt") as f:
        return second(f)