with open("input.txt") as f:
    str_g = [list(s.strip()) for s in f.readlines()]
size = len(str_g)
grid = {}
visited = {}
for i in range(size ** 2):
    x, y = i // size, i % size
    key = str((x, y))
    grid[key] = int(str_g[x][y])
    visited[key] = False


def gen_neighbours(coord):
    x, y = coord
    return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)


class Node:
    def __init__(self, coord, prev=None):
        if prev is None:
            prev = set()
        self.coord = coord
        self.prev = prev
        self.key = str(coord)

    def neighbours(self):
        neighbours = set()
        new = set(self.prev)
        new.add(self.coord)
        for n in gen_neighbours(self.coord):
            neigh = Node(n)
            if n not in self.prev and neigh.key in grid:
                neighbours.add(neigh)
        return neighbours

    def __str__(self):
        return self.key


def shortest(start, end):
    queue = [set() for i in range(9)]
    queue[0].add(Node(start))
    steps = 0
    while True:
        next_queue = queue.pop(0)
        queue.append(set())
        for node in next_queue:
            if node.coord == end:
                return steps
            if visited[node.key]:
                continue
            visited[node.key] = True
            for n in node.neighbours():
                key = n.key
                if visited[key]:
                    continue
                dst = grid[key]
                queue[dst - 1].add(n)
        steps += 1


print(shortest((0, 0), (size - 1, size - 1)))
