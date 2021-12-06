def run(days):
    fish = [0] * 9
    with open("input.txt", "rt") as f:
        for i in f.readline().split(","):
            fish[int(i)] += 1
    for i in range(days):
        new = fish.pop(0)
        fish.append(new)
        fish[6] += new
    return sum(fish)


def part1():
    return run(80)


def part2():
    return run(256)


# Part 1
print(part1())
# Part 2
print(part2())
