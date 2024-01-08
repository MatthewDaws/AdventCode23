import enum, math

class Pulse(enum.Enum):
    LOW = 0
    HIGH = 1


class FlipFlop:
    """Flips between HIGH and LOW when sent a LOW signal; ignores HIGH."""
    def __init__(self):
        self.reset()

    def reset(self):
        self._status = 0

    def handle(self, pulse, source=None):
        if pulse == Pulse.HIGH:
            return None
        if self._status == 0:
            self._status = 1
            return Pulse.HIGH
        self._status = 0
        return Pulse.LOW

    @property
    def state(self):
        return self._status

    def __str__(self):
        return str(self._status)
    

class Conjunction:
    """Like Not(And(...))"""
    def __init__(self, connections):
        self._memory = {c : Pulse.LOW for c in connections}
        self._keys = list(self._memory)
        self._keys.sort()

    def reset(self):
        for c in self._memory:
            self._memory[c] = Pulse.LOW

    def handle(self, pulse, source):
        if source not in self._memory:
            raise KeyError()
        self._memory[source] = pulse
        if all(v==Pulse.HIGH for v in self._memory.values()):
            return Pulse.LOW
        return Pulse.HIGH
    
    @property
    def state(self):
        return [self._memory[k] for k in self._keys]

    def __str__(self):
        s = []
        for key in self._memory:
            if self._memory[key] == Pulse.LOW:
                s.append(f"{key}:0")
            else:
                s.append(f"{key}:1")
        return " ".join(s)


class Output:
    def __init__(self):
        self.reset()

    def reset(self):
        self._state = None

    def handle(self, pulse, source):
        self._state = pulse
        return None
    
    @property
    def state(self):
        return self._state


class Wiring:
    def __init__(self, rows):
        self._modules = dict()
        all_dests = set()
        for row in rows:
            row = row.strip()
            if len(row) == 0:
                break
            source, dest = row.split(" -> ")
            dests = [x.strip() for x in dest.split(",")]
            if source == "broadcaster":
                self._modules[source] = dests
            elif source[0] == "%":
                self._modules[source[1:]] = (FlipFlop(), dests)
            elif source[0] == "&":
                self._modules[source[1:]] = ("CONJ", dests)
            else:
                raise ValueError()
            all_dests.update(dests)
        conjunctions = [key for key,pair in self._modules.items() if key!="broadcaster" and pair[0]=="CONJ"]
        sources = {c:[] for c in conjunctions}
        for key, value in self._modules.items():
            if key!="broadcaster":
                for d in value[1]:
                    if d in sources:
                        sources[d].append(key)
        for name in sources:
            self._modules[name] = (Conjunction(sources[name]), self._modules[name][1])
        self._outputs = []
        for d in all_dests:
            if d not in self._modules:
                self._modules[d] = (Output(), [])
                self._outputs.append(d)
        self.reset()
            
    def reset(self):
        self._watch = None
        self._lows, self._highs = 0, 0
        for key, value in self._modules.items():
            if key == "broadcaster":
                continue
            value[0].reset()

    def maps_to(self, key):
        return [name for name in self._modules
                if name!="broadcaster" and key in self._modules[name][1] ]

    @property
    def outputs(self):
        out = dict()
        for name in self._outputs:
            out[name]=self._modules[name][0].state
        return out

    def is_flipflop(self, name):
        return type(self._modules[name][0]) == FlipFlop

    def __getitem__(self, key):
        return self._modules[key]

    @property
    def keys(self):
        return [k for k in self._modules if k!="broadcaster"]

    def button(self, times=1):
        for _ in range(times):
            self.button_once()

    def button_once(self):
        self._lows += 1
        tasks = [ (dest, Pulse.LOW, None) for dest in self._modules["broadcaster"] ]
        self._run_tasks(tasks)

    def inject_low(self, key):
        if key not in self._modules:
            raise KeyError()
        tasks = [(key, Pulse.LOW, None)]
        self._run_tasks(tasks)

    def _run_tasks(self, tasks):
        while len(tasks) > 0:
            dest, pulse, source = tasks[0]
            tasks = tasks[1:]
            #print(f"{source} -{pulse}- -> {dest}", end=" ")
            if pulse == Pulse.LOW:
                self._lows += 1
            else:
                self._highs += 1
            module, destinations = self._modules[dest]
            output = module.handle(pulse, source)
            if self._watch == dest and output == Pulse.HIGH:
                self._seen = True
            #print("{"+str(module)+"}")
            if output is None:
                continue
            for d in destinations:
                tasks.append((d, output, dest))

    @property
    def pulses_sent(self):
        return self._lows, self._highs

    def state(self):
        keys = list(self._modules)
        keys.sort()
        return [self._modules[k][0].state for k in keys if k!="broadcaster"]

    def set_watch(self, key):
        self._watch = key
        self._seen = False

    @property
    def seen_watched(self):
        return self._seen

def main(second_flag):
    with open("input_20.txt") as f:
        w = Wiring(f)
    if not second_flag:
        w.button(1000)
        low, high = w.pulses_sent
        return low*high
    
    # I don't see how to do the 2nd part purely programmatically.
    # So we analyse the input a little by eye.
    # &tj -> rx   so rx=LOW when all inputs to tj are HIGH
    # &kk, &xc, &sk, &vt -> tj  and all of these are NOTs
    # So total effect is  LOW -> (all kk etc.) -> HIGH to tj so LOW -> rx
    #   and if any HIGH -> kk (say) then some LOW -> tj so HIGH -> rx
    # Each kk is fed by a complicated conjunction
    # But each of these 4 parts splits into a self-contained part which I guess
    # we could study.
    
    def find_periods(w, flipflops_to_watch, watch, start):
        def all_low(wiring, flipflops):
            return all(wiring[key][0].state == 0 for key in flipflops)
        w.reset()
        w.set_watch(watch)
        count = 0
        while not w.seen_watched:
            count += 1
            w.inject_low(start)
        extras = 0
        while not all_low(w, flipflops_to_watch):
            extras += 1
            w.inject_low("gh")
        return count, count+extras

    def search_back(key):
        found = set()
        searched = set()
        to_search = [key]
        while len(to_search) > 0:
            key = to_search.pop()
            searched.add(key)
            for k in w.maps_to(key):
                found.add(k)
                if k not in searched:
                    to_search.append(k)
        return found

    periods = []
    for output_key in w.maps_to("tj"):
        inplay = [k for k in search_back(output_key) if type(w[k][0]) == FlipFlop]
        start = set(w["broadcaster"]).intersection(inplay)
        assert len(start) == 1
        start = start.pop()
        hit, period = find_periods(w, inplay, output_key, start)
        assert hit==period
        periods.append(period)

    a, b = periods[0], periods[1]
    lcm = a * b // math.gcd(a, b)
    for c in periods[2:]:
        lcm = lcm * c // math.gcd(c, lcm)
    return lcm
