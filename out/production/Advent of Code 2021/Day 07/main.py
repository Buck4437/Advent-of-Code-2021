with open("input.txt", "rt") as f:
    crabs = [int(n) for n in f.readline().split(",")]


def compute(formula):
    minimum = None
    for align in range(min(crabs), max(crabs) + 1):
        fuels = sum([formula(abs(pos - align)) for pos in crabs])
        if minimum is None or fuels < minimum:
            minimum = fuels
    return minimum


def part1():
    return compute(lambda x: x)


def part2():
    return compute(lambda x: int(x*(x+1)/2))


# Part 1
print(part1())
# Part 2
print(part2())
