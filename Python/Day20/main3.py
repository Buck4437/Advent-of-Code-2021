with open("rules.txt") as f:
    rules = f.readline().strip()

with open("input.txt") as f:
    imgstr = [s.strip() for s in f.readlines()]


def near(coord):
    x, y = coord
    neighs = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighs.append((i + x, j + y))
    return neighs


pixels = set()
dark_mode = False

for i in range(len(imgstr)):
    row = imgstr[i]
    for j in range(len(row)):
        c = row[j]
        if c == "#":
            pixels.add((i, j))

from time import time

def step():
    global dark_mode, pixels
    new_pixels = set()
    calculated = set()

    if rules[0] == "#":
        dark_mode = not dark_mode

    tsum, iter = 0, 0
    for base_px in pixels:
        for ngh in near(base_px):
            if ngh in calculated:
                continue
            calculated.add(ngh)
            b = ""
            t0 = time()
            for n in near(ngh):
                # Prev light mode
                if dark_mode:
                    b += "1" if n in pixels else "0"
                else:
                    b += "0" if n in pixels else "1"
            tsum += time() - t0
            iter += 1
            char = rules[int(b, 2)]
            if dark_mode and char == "." or not dark_mode and char == "#":
                new_pixels.add(ngh)
    pixels = new_pixels


t0 = time()
for i in range(50):
    step()
    print(i)
    if i == 1:
        print("Part 1:", len(pixels))
print("Part 2:", len(pixels))
print(time() - t0, "s")