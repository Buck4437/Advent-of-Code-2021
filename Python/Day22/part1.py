import time
t0 = time.time()

with open("input.txt") as f:
    procedures = [str.strip().split(" ") for str in f.readlines()]


class Region:
    def __init__(self, c1, c2):
        self.min = []
        self.max = []
        for i in range(3):
            mn, mx = min(c1[i], c2[i]), max(c1[i], c2[i])
            self.min.append(mn)
            self.max.append(mx)

    def has_pt(self, pt):
        for i in range(3):
            if self.min[i] > pt[i] or self.max[i] < pt[i]:
                return False
        return True

    def size(self):
        dim = 1
        for i in range(3):
            dim *= self.max[i] - self.min[i] + 1
        return dim

    def inside(self, num):
        for i in range(3):
            if self.min[i] > num or self.max[i] < -num:
                return False
        return True

    def list_pt(self):
        li = set()
        for i in range(self.min[0], self.max[0] + 1):
            for j in range(self.min[1], self.max[1] + 1):
                for k in range(self.min[2], self.max[2] + 1):
                    li.add((i, j, k))
        return li

    def __str__(self):
        return str(self.min) + " ~ " + str(self.max)


def parse(str_in):
    axis = str_in.split(",")
    c1, c2 = [], []
    for a in axis:
        cd = a[2:].split("..")
        c1.append(int(cd[0]))
        c2.append(int(cd[1]))
    return Region(c1, c2)


def run(part1=False):
    on = set()
    for pro in procedures:
        reg = parse(pro[1])
        if part1 and not reg.inside(50):
            continue
        print(reg)
        if pro[0] == 'on':
            for coor in reg.list_pt():
                on.add(coor)
        else:
            for coor in reg.list_pt():
                on.discard(coor)
    return len(on)
print(run(part1=True))
print(time.time() - t0, "s")
