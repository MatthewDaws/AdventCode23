class RepeatedDifferences():
    def __init__(self, data):
        self._matrix = [list(data)]
        for depth in range(1, len(self._matrix[0])):
            row = ["-" for _ in range(depth)]
            lastrow = self._matrix[-1]
            for i in range(len(self._matrix[0])-depth):
                row.append( lastrow[i+depth] - lastrow[i+depth-1] )
            self._matrix.append(row)
            if all(x==0 or x=="-" for x in row):
                break

    def __repr__(self):
        return "\n".join(" ".join(str(x) for x in row) for row in self._matrix)

    def interpolate(self):
        col = [None for _ in range(len(self._matrix))]
        col[-1] = self._matrix[-1][-1]
        i = len(col) - 2
        while i>=0:
            col[i] = col[i+1] + self._matrix[i][-1]
            i -= 1
        return col[0]

    def extrapolate(self):
        col = [None for _ in range(len(self._matrix))]
        col[-1] = self._matrix[len(col)-1][len(col)-1]
        i = len(col) - 2
        while i>=0:
            col[i] = self._matrix[i][i] - col[i+1]
            i -= 1
        return col[0]


def parse(file):
    return [ [int(x) for x in row.strip().split()] for row in file ]

def sum_interpolants(file):
    return sum(RepeatedDifferences(row).interpolate() for row in parse(file))

def sum_extrapolants(file):
    return sum(RepeatedDifferences(row).extrapolate() for row in parse(file))

def main(second_flag):
    if not second_flag:
        with open("input_9.txt") as f:
            return sum_interpolants(f)

    with open("input_9.txt") as f:
        return sum_extrapolants(f)
