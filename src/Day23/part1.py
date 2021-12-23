ACTIVE = 17
HALT = 3
FIXED = 0
FULL = 1002
INFINITY = 9999999999
HALLWAY_POS = [(x, 1) for x in range(1, 12)]
BUG_COUNT = 2
BUG_STR = "ABCD"
ENERGY = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

test = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".strip().split("\n")
# HALLWAY_POS = [(x, 1) for x in range(2, 7)]
# BUG_COUNT = 2
# BUG_STR = "AB"
# ENERGY = {
#     "A": 1,
#     "B": 10,
#     "C": 100,
#     "D": 1000
# }
#
# test = """
# #############
# ##.....######
# ###B#A#######
#   #A#B#####
#   #########""".strip().split("\n")


def nearby(coord):
    x, y = coord
    return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)


def create_grid(rds, bugs):
    nw_map = {ky: "." for ky in rds}
    for ltr in bugs:
        for pair in bugs[ltr]:
            pos = pair[0]
            nw_map[pos] = ltr
    return nw_map


def min_dst(st, end, grid):
    visited = set()
    unvisited = {st}
    step = 0
    while len(unvisited) != 0:
        new = set()
        for cur in unvisited:
            if cur == end:
                return step
            visited.add(cur)
            for near in nearby(cur):
                if near in visited or near not in grid or grid[near] != ".":
                    continue
                new.add(near)
        unvisited = new
        step += 1
    return INFINITY


def next_room_pos(grid, ltr):
    x_ord = 3 + 2 * (ord(ltr) - ord("A"))
    for y in range(1 + BUG_COUNT, 1, -1):
        coord = x_ord, y
        if grid[coord] == ".":
            return coord
        elif grid[coord] != ltr:
            return None
    return FULL


def replace(grid, ltr, idx, new_pair):
    new = {}
    for ltr2 in BUG_STR:
        new[ltr2] = []
        for idx2 in range(BUG_COUNT):
            if ltr == ltr2 and idx == idx2:
                new[ltr2].append(new_pair)
            else:
                new[ltr2].append(grid[ltr2][idx2])
    return new


CACHE = {}


def hasher(bug_pos):
    hsh = ""
    for ltr in BUG_STR:
        hsh += ltr + ": " + str(bug_pos[ltr]) + " "
    return hsh


def bug_sorted(grid):
    for ltr in BUG_STR:
        if next_room_pos(grid, ltr) != FULL:
            return False
    return True


def find_min_energy(grid, cur_bug_pos, layer=0):
    hsh = hasher(cur_bug_pos)
    if hsh in CACHE:
        # print(len(CACHE))
        return CACHE[hsh]
    if bug_sorted(grid):
        return 0
    min_en = INFINITY
    for ltr in BUG_STR:
        for idx in range(BUG_COUNT):
            pos, state = cur_bug_pos[ltr][idx]
            if state == FIXED:
                continue
            if state == ACTIVE:
                # Try to find all possible paths to hallway
                for target in HALLWAY_POS:
                    dst = min_dst(pos, target, grid)
                    # Can reach this cell
                    if dst != INFINITY:
                        new_bug_pos = replace(cur_bug_pos, ltr, idx, (target, HALT))
                        new_gd = create_grid(roads, new_bug_pos)
                        min_en = min(min_en, dst +
                                     find_min_energy(new_gd, new_bug_pos, layer + 1))
            elif state == HALT:
                target = next_room_pos(grid, ltr)
                if target is None or target == FULL:
                    continue
                dst = min_dst(pos, target, grid)
                if dst != INFINITY:
                    new_bug_pos = replace(cur_bug_pos, ltr, idx, (target, FIXED))
                    new_gd = create_grid(roads, new_bug_pos)
                    min_en = min(min_en, dst +
                                 find_min_energy(new_gd, new_bug_pos, layer + 1))
    CACHE[hsh] = min_en
    if layer < 6:
        print(layer)
    return min_en


roads = set()
start_pos = {x: [] for x in BUG_STR}

for y in range(len(test)):
    row = test[y]
    for x in range(len(row)):
        char = row[x]
        if char in ("." + BUG_STR):
            roads.add((x, y))
        if char in BUG_STR:
            start_pos[char].append(((x, y), ACTIVE))

# print(find_min_energy(roads, start_pos))
mp = create_grid(roads, start_pos)
# for i in range(100000):
#     min_dst((1, 1), (11, 1), mp)
# print("Done")
# print(replace(start_pos, "A", 0, ((10, 10), HALT)))
# print(start_pos)
print(find_min_energy(mp, start_pos))
# print(hasher(start_pos))
