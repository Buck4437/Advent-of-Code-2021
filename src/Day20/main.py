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


img = {}
everything_else_dark = False

minx, maxx = 0, len(imgstr) - 1
miny, maxy = 0, len(imgstr[0]) - 1

for i in range(len(imgstr)):
    row = imgstr[i]
    for j in range(len(row)):
        c = row[j]
        img[str((i, j))] = c

for i in range(50):
    print(i)
    new_img = {}
    for x in range(minx - 1, maxx + 2):
        for y in range(miny - 1, maxy + 2):
            coord = (x, y)
            b = ""
            for n in near(coord):
                key = str(n)
                if everything_else_dark:
                    if key in img:
                        b += "1" if img[key] == "#" else "0"
                    else:
                        b += "1"
                else:
                    if key in img:
                        b += "1" if img[key] == "#" else "0"
                    else:
                        b += "0"
            new_img[str((x, y))] = rules[int(b, 2)]
    minx -= 1
    miny -= 1
    maxx += 1
    maxy += 1
    if rules[0] == "#":
        everything_else_dark = not everything_else_dark
    img = new_img
    if i == 1:
        print("Part 1:", len(list(filter(lambda x: x == "#", img.values()))))
print("Part 2:", len(list(filter(lambda x: x == "#", img.values()))))