with open("input.txt", "rt") as f:
    height_map = [[int(n) for n in string.strip()] for string in f.readlines()]

rows = len(height_map)
columns = len(height_map[0])
height_table = {}
for i in range(rows):
    for j in range(columns):
        height_table[str((i, j))] = height_map[i][j]


def list_neighbours(coord):
    neighbours = (1, 0), (-1, 0), (0, 1), (0, -1)
    return [(coord[0] + n[0], coord[1] + n[1]) for n in neighbours]


def find_lp():
    lp = set()
    for r in range(rows):
        for c in range(columns):
            coord = (r, c)
            key = str(coord)
            height = height_table[key]
            for n in list_neighbours(coord):
                # If the neighbour exists and it's height is lower or equal to the tile
                if str(n) in height_table.keys() and height_table[str(n)] <= height:
                    break
            else:
                lp.add(coord)
    return lp


def part1():
    return sum([1 + height_table[str(lp)] for lp in find_lp()])


def part2():
    lps = find_lp()
    # This stores all points searched and which low point it is connected to
    basin = {str(lp): str(lp) for lp in lps}
    # This counts how many points are connected to this low point
    tally = {str(lp): 1 for lp in lps}
    points_to_search = lps
    while len(points_to_search) != 0:
        new_points = set()
        for point in points_to_search:
            key_pt = str(point)
            for nb in list_neighbours(point):
                key_nb = str(nb)
                # The neighbour does not exist or has a height of 9
                if key_nb not in height_table.keys() or height_table[key_nb] == 9:
                    continue
                if key_nb not in basin.keys():
                    new_points.add(nb)
                if key_nb in basin.keys() and key_pt not in basin.keys():
                    lp = basin[key_nb]
                    basin[key_pt] = lp
                    tally[lp] += 1
        points_to_search = new_points
    rank = sorted(tally.values(), reverse=True)
    return rank[0] * rank[1] * rank[2]


# Part 1
print(part1())
# Part 2
print(part2())
