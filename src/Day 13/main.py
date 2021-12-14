from util import display

with open("input.txt", "rt") as f:
    str_pt = [x.strip().split(",") for x in f.readlines()]

with open("fold.txt", "rt") as f:
    str_f = [x.strip()[11:].split("=") for x in f.readlines()]

paper = set()

for pt in str_pt:
    x, y = pt
    paper.add((int(x), int(y)))

part1 = 0
count = 0
for f in str_f:
    count += 1
    axis = f[0]
    val = int(f[1])
    n_paper = set()
    for pt in paper:
        x, y = pt
        if axis == "x":
            n_paper.add((x if x < val else 2 * val - x, y))
        else:
            n_paper.add((x, y if y < val else 2 * val - y))
    if count == 1:
        part1 = len(n_paper)
    paper = n_paper

print(part1)
display(paper)