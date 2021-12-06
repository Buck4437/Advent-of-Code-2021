with open("input.txt", "rt") as f:
    lines = [[[int(i) for i in pt.split(",")] for pt in n.strip().split(" -> ")] for n in f.readlines()]


def part1(p2=False):
    grid = {}
    for line in lines:
        c0, c1 = line
        dsts = [c1[i] - c0[i] for i in range(2)]
        if dsts[0] != 0 and dsts[1] != 0 and not p2:
            continue
        mag = max([abs(x) for x in dsts])
        step = [n // mag for n in dsts]
        for i in range(mag+1):
            key = str([c0[j] + step[j] * i for j in range(2)])
            grid[key] = 1 if key not in grid.keys() else grid[key] + 1
    return sum(1 if n >= 2 else 0 for n in grid.values())


def part2():
    return part1(p2=True)


# Part 1
print(part1())
# Part 2
print(part2())
