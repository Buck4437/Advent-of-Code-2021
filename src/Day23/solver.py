import heapq

ACTIVE = 17
HALT = 3
FIXED = 0
FULL = 1002
INFINITY = 9999999999
HALLWAY_POS = [(x, 1) for x in [1, 2, 4, 6, 8, 10, 11]]

BUG_STR = "ABCD"
ENERGY = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


def nearby(coord):
    x, y = coord
    return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)


def create_grid(spaces, bugs):
    nw_map = {ky: "." for ky in spaces}
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


def next_room_pos(grid, ltr, room_size):
    x_ord = 3 + 2 * (ord(ltr) - ord("A"))
    for y in range(1 + room_size, 1, -1):
        coord = x_ord, y
        if grid[coord] == ".":
            return coord
        elif grid[coord] != ltr:
            return None
    return FULL


def replace(old_bug_position, ltr, idx, new_pair):
    new = {}
    for ltr2 in BUG_STR:
        new[ltr2] = []
        for idx2 in range(len(old_bug_position[ltr2])):
            if ltr == ltr2 and idx == idx2:
                new[ltr2].append(new_pair)
            else:
                new[ltr2].append(old_bug_position[ltr2][idx2])
    return new


def hasher(bug_pos):
    hsh = ""
    for ltr in BUG_STR:
        hsh += ltr + ": " + str(sorted(bug_pos[ltr])) + " "
    return hsh


def bug_sorted(grid, room_size):
    for ltr in BUG_STR:
        if next_room_pos(grid, ltr, room_size) != FULL:
            return False
    return True


class Node:
    def __init__(self, info, dst):
        self.info = info
        self.dst = dst
        self.visited = False

    def mark_as_visited(self):
        self.visited = True

    def __str__(self):
        return hasher(self.info)

    def __lt__(self, other):
        return self.dst < other.dst

    def __lte__(self, other):
        return self.dst <= other.dst


def find_min_energy(base_bug_pos, paths):
    base_node = Node(base_bug_pos, 0)
    nodes = {str(base_node): base_node}
    heap = [(0, base_node)]
    heapq.heapify(heap)
    bug_count = len(base_bug_pos["A"])

    while len(heap) != 0:
        dst, cur_node = heapq.heappop(heap)

        # A better node have been created
        if not nodes[str(cur_node)] is cur_node:
            continue

        cur_node.mark_as_visited()

        # if len(heap) % 10000 == 0:
        #     print(len(heap), dst)

        cur_grid = create_grid(paths, cur_node.info)
        if bug_sorted(cur_grid, bug_count):
            return dst

        cur_bug_pos = cur_node.info
        cur_dst = cur_node.dst

        for ltr in BUG_STR:
            for idx in range(bug_count):
                pos, state = cur_bug_pos[ltr][idx]
                if state == FIXED:
                    continue
                if state == ACTIVE:
                    # Try to find all possible paths to hallway
                    for target in HALLWAY_POS:
                        dst = min_dst(pos, target, cur_grid) * ENERGY[ltr]
                        # Can reach this position
                        if dst < INFINITY:
                            new_bug_pos = replace(cur_bug_pos, ltr, idx, (target, HALT))
                            new_node = Node(new_bug_pos, cur_dst + dst)
                            hsh = str(new_node)
                            if hsh in nodes:
                                if nodes[hsh].visited or nodes[hsh].dst <= new_node.dst:
                                    continue
                            nodes[hsh] = new_node
                            heapq.heappush(heap, (new_node.dst, new_node))
                elif state == HALT:
                    target = next_room_pos(cur_grid, ltr, bug_count)
                    if target is None or target == FULL:
                        continue
                    dst = min_dst(pos, target, cur_grid) * ENERGY[ltr]
                    if dst < INFINITY:
                        new_bug_pos = replace(cur_bug_pos, ltr, idx, (target, FIXED))
                        new_node = Node(new_bug_pos, cur_dst + dst)
                        hsh = str(new_node)
                        if hsh in nodes:
                            if nodes[hsh].visited or nodes[hsh].dst < new_node.dst:
                                continue
                        nodes[hsh] = new_node
                        heapq.heappush(heap, (new_node.dst, new_node))
    return INFINITY


def solve(raw):
    raw = raw.strip().split("\n")
    paths = set()
    start_pos = {x: [] for x in BUG_STR}

    for y in range(len(raw)):
        row = raw[y]
        for x in range(len(row)):
            char = row[x]
            if char in ("." + BUG_STR):
                paths.add((x, y))
            if char in BUG_STR:
                start_pos[char].append(((x, y), ACTIVE))
    return find_min_energy(start_pos, paths)