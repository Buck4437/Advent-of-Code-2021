with open("input.txt", "rt") as f:
    boards = [s for s in f.readlines()]

seven_seg = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]
seg_table = {str(i): set(seven_seg[i]) for i in range(len(seven_seg))}


def solve(displays):
    t = {}
    for d in displays.split():
        key = len(d)
        t[key] = t[key] & set(d) if key in t.keys() else set(d)
    table = {
        "a": t[3] - t[2],
        "b": t[6] & (t[4] - t[2]),
        "c": t[2] - (t[2] & t[6]),
        "d": t[5] & t[4],
        "e": t[7] - (t[5] | t[4]),
        "f": t[2] & t[6],
        "g": (t[7] - (t[3] | t[4])) & t[5]
    }
    return {"".join(val): key for (key, val) in table.items()}


def decode(table, digits):
    num = ""
    for digit in digits.split():
        actual = set([table[x] for x in digit])
        for val in seg_table.keys():
            if seg_table[val] == set(actual):
                num += val
                break
        else:
            raise Exception("You fucked up")
    return int(num)


def part1():
    count = 0
    for board in boards:
        count += sum([1 if len(digit) in [2, 3, 4, 7] else 0 for digit in board.split(" | ")[1].split()])
    return count


def part2():
    s = 0
    for board in boards:
        parts = board.split(" | ")
        table = solve(parts[0])
        s += decode(table, parts[1])
    return s


# Part 1
print(part1())
# Part 2
print(part2())
