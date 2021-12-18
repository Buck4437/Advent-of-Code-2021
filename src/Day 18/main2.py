with open("input.txt") as f:
    raw_exps = [s.strip() for s in f.readlines()]


class Tree:
    def __init__(self):
        self.tree = []

    def append(self, value):
        self.tree.append(value)

    def __str__(self):
        return str(self.tree)

    def explode(self):
        stack = []
        for i in range(len(self.tree)):
            cur = self.tree[i]
            if cur is None:
                stack.append(cur)
            elif stack[-1] is None:
                stack[-1] = cur
            else:
                while len(stack) > 0 and stack[-1] is not None:
                    stack.pop()
                if len(stack) > 0:
                    stack[-1] = cur
            if len(stack) > 4:
                self.explode_at(i)
                return True
        return False

    def explode_at(self, i):
        l_num, r_num = self.tree[i+1:i+3]
        # Find L
        for l_pos in range(i-1, -1, -1):
            if self.tree[l_pos] is not None:
                self.tree[l_pos] += l_num
                break
        # Find R
        for r_pos in range(i+3, len(self.tree)):
            if self.tree[r_pos] is not None:
                self.tree[r_pos] += r_num
                break

        del self.tree[i:i+3]
        self.tree.insert(i, 0)

    def split(self):
        for i in range(len(self.tree)):
            value = self.tree[i]
            if value is None:
                continue
            floor = value // 2
            if value >= 10:
                self.tree = self.tree[:i] + [None, floor, value - floor] + self.tree[i+1:]
                return True
        return False

    def reduce(self):
        while True:
            if not self.explode() and not self.split():
                return

    def add(self, t2):
        self.tree = [None] + self.tree + t2.tree
        self.reduce()

    def mag(self):
        stack = []
        for cur in self.tree:
            if cur is None:
                stack.append(cur)
            elif stack[-1] is None:
                stack[-1] = cur
            else:
                mag = cur
                while stack[-1] is not None:
                    mag = mag * 2 + stack.pop() * 3
                    if len(stack) == 0:
                        return mag
                stack[-1] = mag
        return -1


base_tree = None
for raw in raw_exps:
    val = ""
    tree = Tree()
    for c in raw:
        if c == "[":
            tree.append(None)
        elif c == "]" or c == ",":
            if val != "":
                tree.append(int(val))
                val = ""
        else:
            val += c
    if base_tree is None:
        base_tree = tree
    else:
        base_tree.add(tree)

print(base_tree)
print(base_tree.mag())
