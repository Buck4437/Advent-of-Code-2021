from collections import Counter

with open("test.txt") as f:
    init = f.readline().strip()

with open("testrules.txt") as f:
    r = dict(map(lambda r: (r[:2], r.strip()[-1]), f.readlines()))

mem = {}


def poly(base, step, layer=1):
    key = base + str(step)
    print("   " * (layer - 1) + " |-" * 1, "Computing", base, "with step", step)
    if key in mem:
        print("   " * layer, "Result found in memory")
        return mem[key]
    if step == 0:
        print("   " * layer, "Step is 0, returning the count")
        count = Counter(base)
    else:
        print("   " * layer, "Step > 0, solving with recursion")
        count = Counter({})
        mid = Counter(base[1:-1])
        for i in range(len(base) - 1):
            pair = base[i:i+2]
            print("   " * layer, "Current pair is", pair)
            count += poly(pair[0] + r[pair] + pair[1], step-1, layer + 1)
            print("   " * layer, "Merging previous results...")
        count -= mid
    print("   " * layer, "The answer is", count)
    mem[key] = count
    return count


def ans(ct):
    s = sorted(ct.values())
    return s[-1] - s[0]


# Part 1
print(ans(poly(init, 10)))

# Part 2
print(ans(poly(init, 40)))
