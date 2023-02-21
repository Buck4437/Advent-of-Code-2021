with open("input.txt", "rt") as f:
    lines = [[[int(i) for i in pt.split(",")] for pt in n.strip().split(" -> ")] for n in f.readlines()]


def part1(p2=False):
    grid = {}
    for line in lines:
        c0, c1 = line
        hd, vd = c1[0] - c0[0], c1[1] - c0[1]
        if hd != 0 and vd != 0 and not p2:
            continue
        mag = max(abs(hd), abs(vd))
        hs, vs = hd // mag, vd // mag
        for i in range(mag+1):
            key = str([c0[0] + hs * i, c0[1] + vs * i])
            grid[key] = 1 if key not in grid.keys() else grid[key] + 1
    return sum(1 if n >= 2 else 0 for n in grid.values())


def part2():
    return part1(p2=True)


# Part 1
print(part1())
# Part 2
print(part2())
