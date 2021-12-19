from collections import Counter

with open("input.txt") as f:
    init = f.readline().strip()

with open("rules.txt") as f:
    r = dict(map(lambda s: (s[:2], s.strip()[-1]), f.readlines()))

mem = {}


def poly(base, step):
    key = base + str(step)
    if key in mem:
        return mem[key]
    if step == 0:
        count = Counter(base)
    else:
        count = Counter({})
        mid = Counter(base[1:-1])
        for i in range(len(base) - 1):
            pair = base[i:i+2]
            count += poly(pair[0] + r[pair] + pair[1], step-1)
        count -= mid

    mem[key] = count
    return count


def ans(ct):
    s = sorted(ct.values())
    return s[-1] - s[0]


# Part 1
print(ans(poly(init, 10)))

# Part 2
print(ans(poly(init, 40)))
