class BrainfuckException(Exception):
    pass


class Brainfuck:
    EEND = 0
    EINPUT = 1

    def __init__(self, script):
        self.script = script
        self.pairs = self.__gen_pairs()
        self.mem = {}
        self.ip = 0
        self.mp = 0

    def __gen_pairs(self):
        stack = []
        dct = {}
        for i in range(len(self.script)):
            c = self.script[i]
            if c == "[":
                stack.append(i)
            elif c == "]":
                front = stack[-1]
                del stack[-1]
                dct[i] = front
                dct[front] = i
        if len(stack) != 0:
            raise BrainfuckException
        return dct

    def run(self, ins=[]):
        i = ins
        while True:
            if self.ip >= len(self.script):
                return Brainfuck.EEND
            c = self.script[self.ip]
            if c == ">":
                self.mp += 1
            if c == "<":
                self.mp -= 1
            if c == "+":
                self.mem[self.mp] = self.mem[self.mp] + 1 if self.mp in self.mem.keys() else 1
            if c == "-":
                self.mem[self.mp] = self.mem[self.mp] - 1 if self.mp in self.mem.keys() else -1
            if c == ".":
                print(chr(self.mem[self.mp]), end="")
            if c == ",":
                if len(i) == 0:
                    return Brainfuck.EINPUT
                self.mem[self.mp] = i[-1]
                del i[-1]
            if c == "[":
                if self.mem[self.mp] == 0:
                    self.ip = self.pairs[self.ip]
            if c == "]":
                if self.mem[self.mp] != 0:
                    self.ip = self.pairs[self.ip]
            self.ip += 1