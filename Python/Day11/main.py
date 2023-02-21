with open("input.txt", "rt") as f:
    octo = [[int(n) for n in s.strip()] for s in f.readlines()]

grid = {}
coordinates = set()
for i in range(10):
    for j in range(10):
        key = str((i, j))
        grid[key] = octo[i][j]
        coordinates.add((i, j))


flashes = 0
steps = 0
while True:
    steps += 1
    for key in grid.keys():
        grid[key] += 1
    while True:
        stopped = True
        for coord in coordinates:
            key = str(coord)
            if grid[key] > 9:
                stopped = False
                if steps <= 100:
                    flashes += 1
                for nx in range(-1, 2):
                    for ny in range(-1, 2):
                        neighbour = coord[0] + nx, coord[1] + ny
                        if neighbour in coordinates:
                            grid[str(neighbour)] += 1
                grid[key] = -100000
        if stopped:
            break
    all_flashed = True
    for key in grid.keys():
        if grid[key] < 0:
            grid[key] = 0
        else:
            all_flashed = False
    if all_flashed:
        break

# Part 1
print(flashes)
# Part 2
print(steps)
