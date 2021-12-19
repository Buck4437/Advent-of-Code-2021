with open("input.txt", "rt") as f:
    lines = [[[int(i) for i in pt.split(",")] for pt in n.strip().split(" -> ")] for n in f.readlines()]


def part1():
    grid = {}
    for line in lines:
        c0, c1 = line
        if c0[0] == c1[0]:
            mn = min(c0[1], c1[1])
            mx = max(c0[1], c1[1])
            for i in range(mn, mx + 1):
                key = " ".join([str(c0[0]), str(i)])
                grid[key] = 1 if key not in grid.keys() else grid[key] + 1

        elif c0[1] == c1[1]:
            mn = min(c0[0], c1[0])
            mx = max(c0[0], c1[0])
            for i in range(mn, mx + 1):
                key = " ".join([str(i), str(c0[1])])
                grid[key] = 1 if key not in grid.keys() else grid[key] + 1
    count = 0
    for v in grid.values():
        if v >= 2:
            count += 1
    return count


def part2():
    grid = {}
    for line in lines:
        c0, c1 = line
        if c0[0] == c1[0]:
            mn = min(c0[1], c1[1])
            mx = max(c0[1], c1[1])
            for i in range(mn, mx + 1):
                key = " ".join([str(c0[0]), str(i)])
                grid[key] = 1 if key not in grid.keys() else grid[key] + 1

        elif c0[1] == c1[1]:
            mn = min(c0[0], c1[0])
            mx = max(c0[0], c1[0])
            for i in range(mn, mx + 1):
                key = " ".join([str(i), str(c0[1])])
                grid[key] = 1 if key not in grid.keys() else grid[key] + 1
        else:
            # l to r
            if c0[0] > c1[0]:
                mx = c0[0]
                mn = c1[0]
                init = c1[1]
                incre = -1 if c1[1] > c0[1] else 1
            else:
                mx = c1[0]
                mn = c0[0]
                init = c0[1]
                incre = -1 if c1[1] < c0[1] else 1
            for i in range(0, mx + 1 - mn):
                key = " ".join([str(mn + i), str(init + i * incre)])
                grid[key] = 1 if key not in grid.keys() else grid[key] + 1
    count = 0
    for v in grid.values():
        if v >= 2:
            count += 1
    return count


# Part 1
print(part1())
# Part 2
print(part2())
