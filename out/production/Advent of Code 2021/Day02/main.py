with open("input.txt", "rt") as f:
    instructions = [line.split() for line in f.readlines()]


def part1():
    h = d = 0
    for i in instructions:
        op = i[0]
        num = int(i[1])
        if op == "forward":
            h += num
        elif op == "down":
            d += num
        else:
            d -= num
    return h * d


def part2():
    h = d = aim = 0
    for i in instructions:
        op = i[0]
        num = int(i[1])
        if op == "forward":
            h += num
            d += aim * num
        elif op == "down":
            aim += num
        else:
            aim -= num
    return h * d


# Part 1
print(part1())
# Part 2
print(part2())
