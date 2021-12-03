with open("input.txt", "r") as f:
    lst = [[1 if char == "1" else -1 for char in line.strip()] for line in f.readlines()]

flip = {
    "1": "0",
    "0": "1"
}


def part1():
    gamma = epsi = ""
    for i in range(len(lst[0])):
        val = "1" if sum(list(map(lambda x: x[i], lst))) >= 0 else "0"
        gamma += val
        epsi += flip[val]
    return int(gamma, 2) * int(epsi, 2)


def part2():
    def calc(reverse=False):
        tmp = lst[:]
        for i in range(len(tmp[0])):
            val = 1 if sum(list(map(lambda x: x[i], tmp))) >= 0 else -1
            if reverse:
                val = -val
            tmp = list(filter(lambda x: x[i] == val, tmp))
            if len(tmp) == 1:
                num = "".join(map(lambda x: "1" if x == 1 else "0", tmp[0]))
                return int(num, 2)

    return calc() * calc(reverse=True)


print(part1())
print(part2())
