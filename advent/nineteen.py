import re, itertools

class Comparison:
    def __init__(self, variable, comparison, value, cmd):
        assert variable in "xmas"
        self._variable = variable
        assert comparison in "<>"
        self._comparison = comparison
        self._value = value
        self._cmd = cmd
    
    def __call__(self, variables):
        var = variables[self._variable]
        if self._comparison == ">":
            okay = var > self._value
        else:
            okay = var < self._value
        if okay:
            return self._cmd
        return None
    
    @property
    def variable(self):
        return self._variable

    @property
    def outcome(self):
        return self._cmd

    def pass_fail_intervals(self):
        if self._comparison == ">":
            return Interval(start = self._value+1), Interval(end = self._value)
        return Interval(end = self._value-1), Interval(start = self._value)


class Always:
    def __init__(self, cmd):
        self._cmd = cmd

    def __call__(self, variables):
        return self._cmd

    @property
    def variable(self):
        return "x"

    @property
    def outcome(self):
        return self._cmd

    def pass_fail_intervals(self):
        return Interval(), None


class Parse:
    _cmd_re = re.compile("(.*?)\{(.*)\}")
    _cmd2_re = re.compile("()")

    def __init__(self, rows):
        self._commands = dict()
        for row in rows:
            row = row.strip()
            if len(row)==0:
                break
            self._parse_command(row)

        self._data = []
        for row in rows:
            row = row.strip()
            if len(row)==0:
                break
            self._parse_data(row)

    def _parse_command(self, row):
        m = self._cmd_re.match(row)
        if not m:
            raise ValueError()
        name, cmdgroup = m.group(1), m.group(2)
        commands = cmdgroup.split(",")
        ordered_commands = []
        for i in range(len(commands)-1):
            variable = commands[i][0]
            comparison = commands[i][1]
            a, cmd = commands[i].split(":")
            value = int(a[2:])
            ordered_commands.append( Comparison(variable, comparison, value, cmd) )
        ordered_commands.append( Always(commands[-1]) )
        self._commands[name] = ordered_commands

    def _parse_data(self, row):
        data = dict()
        assert row[0] == "{" and row[-1] == "}"
        for value in row[1:-1].split(","):
            variable = value[0]
            assert value[1] == "="
            data[variable] = int(value[2:])
        self._data.append(data)

    @property
    def commands(self):
        return self._commands
    
    @property
    def data(self):
        return self._data

    def compute_accept_reject(self):
        return [ self._run(variables) for variables in self.data ]

    def _run(self, variables):
        current_command = "in"
        while True:
            for cmd in self.commands[current_command]:
                new_command = cmd(variables)
                if new_command is not None:
                    current_command = new_command
                    break
            if current_command == "R":
                return False
            if current_command == "A":
                return True
            
    def score(self, results):
        return sum(sum(vars.values()) for vars, result in zip(self.data, results) if result)


class Interval:
    def __init__(self, start=1, end=4000):
        if not end >= start:
            raise ValueError()
        self._start =start
        self._end = end
    
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    @property
    def count(self):
        return self._end - self._start + 1

    def intersect(self, other):
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start > end:
            return None
        return Interval(start, end)

    def __eq__(self, other):
        return self._start == other._start and self._end == other._end

    def __repr__(self):
        return f"Interval({self._start}, {self._end})"

    def complement(self):
        out = []
        if self.start > 1:
            out.append( Interval(end=self.start-1) )
        if self.end < 4000:
            out.append( Interval(start=self.end+1) )
        return out


class VariableInterval:
    def __init__(self):
        self._vars = {name:Interval() for name in "xmas"}

    @staticmethod
    def from_variable(variable, interval):
        vi = VariableInterval()
        vi[variable] = interval
        return vi

    def __getitem__(self, name):
        return self._vars[name]

    def __setitem__(self, name, interval):
        if name not in self._vars:
            raise KeyError()
        self._vars[name] = interval

    def intersect(self, other):
        vi = VariableInterval()
        for name in "xmas":
            vi[name] = self[name].intersect(other[name])
        return vi

    def complement(self):
        coms = [self[name].complement() for name in "xmas"]
        return list(itertools.product(*coms))
    
    def choices(self):
        count = 1
        for interval in self._vars.values():
            if interval is None:
                count = 0
            else:
                count *= (interval.end - interval.start + 1)
        return count
 
    def __repr__(self):
        s = []
        for n in "xmas":
            if self[n] is None:
                s.append(f"{n}=Empty")
            else:
                s.append( "{}=[{},{}]".format(n, self[n].start, self[n].end) )
        return "VariableInterval("+", ".join(s)+")"
    

class DecisionTree:
    def __init__(self, parsed):
        self._parsed = parsed

    def compute_next_level(self, current):
        if current is None:
            current = [("in", VariableInterval())]
        out = []
        for name, intervals in current:
            if name == "A" or name == "R":
                out.append((name, intervals))
                continue
            current_intervals = [ intervals ]
            for cmd in self._parsed.commands[name]:
                pass_interval, fail_interval = cmd.pass_fail_intervals()
                for vi in current_intervals:
                    out.append((cmd.outcome, vi.intersect( VariableInterval.from_variable(cmd.variable, pass_interval) )))
                if fail_interval is None:
                    current_intervals = []
                else:
                    current_intervals = [ VariableInterval.from_variable(cmd.variable, fail_interval).intersect(i) for i in current_intervals ]
        return out

    def level_complete(self, level):
        return all(name=="A" or name=="R" for name,_ in level)
    
    def compute_tree(self):
        level = self.compute_next_level(None)
        while not self.level_complete(level):
            level = self.compute_next_level(level)
        return level
    
    def choices(self):
        tree = self.compute_tree()
        accept_intervals = [vi for name, vi in tree if name=="A"]
        for pair in itertools.combinations(accept_intervals, 2):
            vi = pair[0].intersect(pair[1])
            assert vi.choices() == 0
        return sum(vi.choices() for vi in accept_intervals)


def main(second_flag):
    with open("input_19.txt") as f:
        parsed = Parse(f)
    if not second_flag:
        results = parsed.compute_accept_reject()
        return parsed.score(results)
    dt = DecisionTree(parsed)
    return dt.choices() 
