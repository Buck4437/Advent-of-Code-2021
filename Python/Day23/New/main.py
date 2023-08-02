import time
import main_astar
import main_dijkstra


def test(func):
    t0 = time.time()
    func()
    print("Runtime:", time.time() - t0, "s")


print("Dijkstra:")
print("Part 1:")
test(lambda: main_dijkstra.main("part1.txt", log_all=False))
print("\nPart 2:")
test(lambda: main_dijkstra.main("part2.txt", log_all=False))

print()
print("A*:")
print("Part 1:")
test(lambda: main_astar.main("part1.txt", log_all=False))
print("\nPart 2:")
test(lambda: main_astar.main("part2.txt", log_all=False))
