ACTIVE = 17
HALT = 3
FIXED = 0
INFINITY = 9999999999


def nearby(coord):
    x, y = coord
    return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)


def create_map(rds, bugs):
    nw_map = {ky: "." for ky in rds}
    for ltr in bugs:
        for pair in bugs[ltr]:
            pos = pair[0]
            nw_map[pos] = ltr
    return nw_map


def min_dst(st, end, roadmap):
    visited = set()
    unvisited = set(st)
    step = 0
    while len(unvisited) != 0:
        new = set()
        for cur in unvisited:
            print(cur)
            if cur == end:
                return step
            visited.add(cur)
            for near in nearby(cur):
                if near in visited or near not in roadmap or roadmap[near] != ".":
                    continue
                new.add(near)
        unvisited = new
        step += 1
    return INFINITY


def find_min_energy(rds, cur_pos):
    min_en = INFINITY
    for ltr in "ABCD":
        for pair in cur_pos[ltr]:
            pos, state = pair
            print(pair)
    return min_en


test = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".strip().split("\n")

roads = set()
start_pos = {x: [] for x in "ABCD"}

for y in range(len(test)):
    row = test[y]
    for x in range(len(row)):
        char = row[x]
        if char in ".ABCD":
            roads.add((x, y))
        if char in "ABCD":
            start_pos[char].append(((x, y), ACTIVE))

# print(find_min_energy(roads, start_pos))
mp = create_map(roads, start_pos)
print(min_dst((1, 1), (1, 11), mp))
