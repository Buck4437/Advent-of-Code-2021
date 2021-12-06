class Card:
    def __init__(self, cd):
        self.card = [[int(n) for n in r.split()] for r in cd.strip().split("\n")]

    def sum(self):
        return sum([sum(r) for r in self.card])

    def mark(self, num):
        for i in range(5):
            for j in range(5):
                if self.card[i][j] == num:
                    self.card[i][j] = 0
                    return True
        return False

    def win(self):
        for i in range(5):
            if sum(self.card[i]) == 0 or sum([self.card[j][i] for j in range(5)]) == 0:
                return True
        return False

    def __str__(self):
        return "\n".join([" ".join(["--" if n == 0 else str(n).zfill(2) for n in r]) for r in self.card])


with open("input.txt", "rt") as f:
    queue = [int(n) for n in f.readlines(2)[0].strip().split(",")]
    cards = [Card(cd) for cd in f.read().split("\n\n")]


def part1():
    for num in queue:
        for c in cards:
            if c.mark(num) and c.win():
                return c.sum() * num
    return -1


def part2():
    cds = cards[:]
    last = 0
    for num in queue:
        tmp = []
        for c in cds:
            if c.mark(num) and c.win():
                last = c.sum() * num
            else:
                tmp.append(c)
        if len(tmp) == 0:
            return last
        cds = tmp
    return -1


# Part 1
print(part1())
# Part 2
print(part2())
