import time

t0 = time.time()


def find_intersection(x1min, x1max, x2min, x2max):
    assert x1min <= x1max and x2min <= x2max
    if x2min > x1max or x2max < x1min:
        return None
    return max(x1min, x2min), min(x1max, x2max)


class Cuboid:
    def __init__(self, corners, negative=False):
        for i in range(3):
            assert corners[0][i] <= corners[1][i]
        self.corners = corners
        self.negative = negative

    def __str__(self):
        return str(self.corners) + (" (Negative)" if self.negative else "")

    def intersection(self, cuboid2):
        imin, imax = [0, 0, 0], [0, 0, 0]
        for i in range(3):
            boundary = find_intersection(self.corners[0][i], self.corners[1][i],
                                         cuboid2.corners[0][i], cuboid2.corners[1][i])
            if boundary is None:
                return None
            imin[i], imax[i] = boundary
        return Cuboid((imin, imax), self.negative != cuboid2.negative)

    def flip(self):
        self.negative = not self.negative
        return self

    def volume(self):
        vol = -1 if self.negative else 1
        for i in range(3):
            vol *= self.corners[1][i] - self.corners[0][i] + 1
        return vol


def parse(s):
    op, bound = s.strip().split(" ")
    axis = bound.split(",")
    c1, c2 = [], []
    for a in axis:
        cd = a[2:].split("..")
        c1.append(int(cd[0]))
        c2.append(int(cd[1]))
    return op, (c1, c2)


def outside_range(bound):
    for i in range(3):
        if bound[0][i] > 50 or bound[1][i] < -50:
            return True
    return False


with open("input.txt") as f:
    steps = [parse(s) for s in f.readlines()]


def run(part1=False):
    total = 0
    cuboids = []
    for step in steps:
        op, bound = step
        cuboid = Cuboid(bound, op == "off")
        if part1 and outside_range(bound):
            continue
        new_cuboids = []
        for prev_cuboid in cuboids:
            intersection = prev_cuboid.intersection(cuboid)
            if intersection is not None:
                if op == "on":
                    intersection.flip()
                new_cuboids.append(intersection)
        cuboids += new_cuboids
        if op == "on":
            cuboids.append(cuboid)
    for cuboid in cuboids:
        total += cuboid.volume()
    return total


# Part 1
print(run(part1=True))

# Part 2
print(run())

print(time.time() - t0, "s")
