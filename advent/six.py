import math

def winning_ways(time, distance):
    """Hold the button for x milliseconds, then travels at `x` mm a time unit, for `time-x` time units,
    so `x * (time - x)` total distance.  Could the number of ways this can be larger then `distance`"""
    # x * (time - x) > distance
    # x*x - x*time + distance < 0
    # (x - time/2)**2 + distance - time*time/4 < 0
    # Roots at time/2 +/- sqrt(time*time/4 - distance)
    # = (time +- sqrt(time*time-4*distance)) / 2
    disc = time*time - 4*distance
    if disc < 0:
        raise ValueError()
    disc = math.sqrt(disc)
    rootlow = math.ceil((time - disc) / 2)
    if rootlow * (time-rootlow) == distance:
        rootlow += 1
    roothigh = math.floor((time + disc) / 2)
    if roothigh * (time-roothigh) == distance:
        roothigh -= 1
    return roothigh - rootlow + 1

def parse(file):
    timeline = next(file)
    assert timeline[:5] == "Time:"
    times = [int(x) for x in timeline[5:].split()]
    distanceline = next(file)
    assert distanceline[:9] == "Distance:"
    distances = [int(x) for x in distanceline[9:].split()]
    return times, distances

def parse_second(file):
    timeline = next(file)
    assert timeline[:5] == "Time:"
    time = int( "".join(timeline[5:].split()) )
    distanceline = next(file)
    assert distanceline[:9] == "Distance:"
    distance = int( "".join(distanceline[9:].split()) )
    return time, distance

def main(second_flag):
    if not second_flag:
        with open("input_6.txt") as f:
            t, d = parse(f)
            ways = 1
            for time, dist in zip(t,d):
                ways *= winning_ways(time, dist)
            return ways

    with open("input_6.txt") as f:
        t, d = parse_second(f)
    return winning_ways(t, d)
