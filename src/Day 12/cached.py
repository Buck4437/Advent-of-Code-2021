import time
with open("input.txt", "rt") as f:
    str_paths = [s.strip() for s in f.readlines()]

node = {}
prev = {}
searches = 0


def add_edge(name, neighbour):
    if name in node.keys():
        node[name].add(neighbour)
    else:
        node[name] = set()
        node[name].add(neighbour)


for p in str_paths:
    n1, n2 = p.split("-")
    add_edge(n1, n2)
    add_edge(n2, n1)


def count_paths(cur, visited, has_visited_twice=False):
    if cur == "end":
        return 1
    paths = 0
    hash = cur + str(visited) + str(has_visited_twice)
    if hash in prev:
        return prev[hash]
    for n in node[cur]:
        if n == "start":
            continue
        if n in visited and has_visited_twice:
            continue
        n_v = list(visited)
        n_hvt = has_visited_twice
        if n.islower():
            n_v.append(n)
            if n in visited and not has_visited_twice:
                n_hvt = True
        paths += count_paths(n, n_v, n_hvt)
    prev[hash] = paths
    return paths


t0 = time.time()

# Part 1
print(count_paths("start", ["start"], True))
# Part 2
print(count_paths("start", ["start"], False))

print("Execution time:", (time.time() - t0) * 1000, "ms")
