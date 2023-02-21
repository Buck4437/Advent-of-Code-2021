with open("input.txt") as f:
    cums = [[c for c in s.strip()] for s in f]

est = set()
sth = set()
ys = len(cums)
xs = len(cums[0])
for i in range(ys):
    for j in range(xs):
        c = cums[i][j]
        if c == ">":
            est.add((j, i))
        elif c == "v":
            sth.add((j, i))

counter = 0
while True:
    nest, nsth = set(), set()
    counter += 1
    for e in est:
        x, y = e
        crd = (x + 1) % xs, y
        if crd in est or crd in sth:
            nest.add(e)
        else:
            nest.add(crd)

    for s in sth:
        x, y = s
        crd = x, (y + 1) % ys
        if crd in nest or crd in sth:
            nsth.add(s)
        else:
            nsth.add(crd)

    if nest == est and nsth == sth:
        break
    est, sth = nest, nsth
print(counter)
