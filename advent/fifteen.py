class Hasher():
    def __init__(self):
        self._hash = 0

    def append(self, c):
        self._hash = ((self._hash + ord(c)) * 17 ) % 256
        return self

    def digest(self, string):
        for c in string:
            self.append(c)
        return self

    @property
    def value(self):
        return self._hash


def sum_comma_sep(line):
    return sum( Hasher().digest(st).value for st in line.strip().split(",") )

class Boxes():
    def __init__(self):
        self._boxes = [[] for _ in range(256)]

    @staticmethod
    def find_location(box, label):
        for i, entry in enumerate(box):
            if entry[0] == label:
                return i
        return None

    @staticmethod
    def split_line(st):
        for i, c in enumerate(st):
            if c=="=" or c=="-":
                return st[:i], c, st[i+1:]

    def process(self, st):
        label, command, remainder = self.split_line(st)
        box_label = Hasher().digest(label).value
        box = self._boxes[box_label]
        if command == "-":
            i = self.find_location(box, label)
            if i is not None:
                if i == len(box)-1:
                    box = box[:i]
                elif i == 0:
                    box = box[1:]
                else:
                    box = box[:i] + box[i+1:]
                self._boxes[box_label] = box
            return
        elif command == "=":
            lens = int(remainder)
            i = self.find_location(box, label)
            if i is None:
                box.append((label, lens))
            else:
                box[i] = (label, lens)
        else:
            raise ValueError()

    def __getitem__(self, loc):
        return self._boxes[loc]
    
    def process_comma_list(self, l):
        for st in l.strip().split(","):
            self.process(st)
        return self

    def score(self):
        count = 0
        for label, box in enumerate(self._boxes):
            for i, lens in enumerate(box):
                count += (label+1) * (i+1) * lens[1]
        return count


def main(second_flag):
    with open("input_15.txt") as f:
        if not second_flag:
            return sum_comma_sep(next(f))
        return Boxes().process_comma_list(next(f)).score()
